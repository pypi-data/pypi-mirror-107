"""
    导入本模块:
    from kw618.k_finance.Arbitrage.calData import *
"""
from kw618.k_finance.utils_quant import *
import multiprocessing
import time
import signal

# 自定义信号处理函数
def my_handler(signum, frame):
    global Ctrl_C_Kill
    Ctrl_C_Kill = True
    print("进程被终止")
signal.signal(signal.SIGINT, my_handler)
signal.signal(signal.SIGHUP, my_handler)
signal.signal(signal.SIGTERM, my_handler)
Ctrl_C_Kill = False # 通过这个全局变量, 让robot捕捉'Ctrl C 的信号' (做好善后工作)

class CalSpreadRobotManager():
    """
    notes:
    """

    def __init__(self):
        """
            notes:
            todo:
                - 要实现一键检查所有robot是否还alive的函数
        """
        # 1. 初始化
        self.robots = [] # 存储所有'计算robot'
        self.spread_symbols = [] # 所有正在计算的'套利价差symbol'


    def add_robots(self, spread_symbols=["adausd_perp/adausd_210625"], unstoppable_cal=False):
        for spread_symbol in spread_symbols:
            cs_robot = CalSpreadRobot(spread_symbol=spread_symbol, unstoppable_cal=unstoppable_cal)
            self.robots.append(cs_robot)
            self.spread_symbols.append(spread_symbol)
            cs_robot.run()

    def active(self):
        for robot in self.robots:
            robot.active()

    def pause(self):
        for robot in self.robots:
            robot.pause()

class CalSpreadRobot():
    """
    notes:
        - 想要获取任意一个币对的价差率, 都需要实例化一个'计算价差率的机器人'
        - MarketDataReceiver的"数据获取"是24小时不间断运行的, 但是CalSpreadRobot的'价差率计算'是需要开平仓才会启动的
    """

    def __init__(self, spread_symbol="adausd_perp/adausd_210625", unstoppable_cal=False):
        """
            notes:
                - 一个对象只负责一个'币对'的价差率计算 [专一性]
                - spread_symbol: 大小写不敏感;  且有左右腿的概念(价差为:左腿-右腿)
                - 存储在redis中的symbol, 都是大写的
                - redis数据存储方式:
                    - 开/平仓价差率, 时间差, 时间戳, 平均价差率, 都分别存储在不同key里吗? 还是存在同个symbol的key中?

            todo:
                - 要实现一键检查所有robot是否还alive的函数
                - 计算近一段时间的平均价差率 (可以参考vnpy的arrayManager对象)
                - 收集最小挂单量, 小于阈值就不下单!!  (min(leftLeg_volume, rightLeg_volume))
                - 因为我这里计算的价差率会被所有'下单robot'获取, 他们都是依据同一个数据下单, 不免会造成抢单的情况发生!!!
                    解决方案1:
                        使用原来的代码, 每个账户开一个程序来计算价差率
                    解决方案2:
                        提高计算的频次(如0.3s一次), 每个'下单robot'的循环睡眠时间设置成0.5-1.5s的随机数
                            (错开时间下单, 避免多账号同时抢盘口价差)


        """
        # 1. 获取左右腿的symbol
        self.spread_symbol = spread_symbol.upper()
        self.left_leg_symbol = self.spread_symbol.split("/")[0] # 左腿symbol
        self.right_leg_symbol = self.spread_symbol.split("/")[1] # 右腿symbol

        # 2. 初始化必要的参数
        self.alive = False # 表明这个机器人还活着 (活着表示'正在计算中', False表示'没有在计算中', 可以通过active激活继续计算)
        self.unstoppable_cal = unstoppable_cal # 无法阻挡地计算  (极端行情, 需要它义无反顾的计算...)
        self.cal_interval = 1 # 每次计算间隔1s
        self.open_spread_lst = []
        self.r0 = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True) # 0号数据库(用于获取盘口数据)
        self.r1 = redis.StrictRedis(host="localhost", port=6379, db=1, decode_responses=True) # 1号数据库(用于存储价差率数据)
        self.threads = [] # 存储所有线程

    def active(self):
        """
        notes:
            - 功能: 激活被暂停的robot, 让它重新执行任务  (它被激活的前提是已经开始执行run了)
        """
        print("Active中....")
        self.alive = True
        running_count = self.r0.hget("running_calRobot", self.spread_symbol)
        running_count = int(running_count)+1 if running_count != None else 1
        # 在redis上记录'正在跑的calRobot'
        self.r0.hset("running_calRobot", self.spread_symbol, running_count)

    def pause(self):
        """
        notes:
            - 功能: 让robot暂时停止cal... 可以通过active继续执行
        """
        print("Pause中....")
        self.alive = False
        running_count = self.r0.hget("running_calRobot", self.spread_symbol)
        running_count = int(running_count)-1 if running_count != None else 0
        self.r0.hset("running_calRobot", self.spread_symbol, running_count)

    def main_cal(self):
        """
            notes:
                - 主要用于计算'价差率'
        """
        try:
            while self.alive:
                if Ctrl_C_Kill:
                    msg = "[Ctrl C 终止该进程]"
                    print(msg)
                    self.pause()
                # 1. 获取左右腿的实时'挂单信息' (每个腿有6样数据: 买一/卖一价, 买一/卖一量, 服务/接收端时间戳)
                left_leg_dict = self.r0.hgetall(self.left_leg_symbol)
                right_leg_dict = self.r0.hgetall(self.right_leg_symbol)
                if left_leg_dict == {} or right_leg_dict == {}:
                    msg = f"[{self.spread_symbol}]\n"\
                        f"左腿数据: {left_leg_dict};\n"\
                        f"右腿数据: {right_leg_dict};\n"\
                        f"左右腿数据有缺失, 请检查ws数据是否正常推送...\n\n"
                    raise Exception(msg)
                    # i. 左腿数据
                        # 异常处理: 如果获取不到想要的腿数据, float()会自动报错! (所以只要不报错, 每个数据都能正常获取到)
                left_bid_price = float(left_leg_dict.get("bid_price"))
                left_ask_price = float(left_leg_dict.get("ask_price"))
                left_bid_volume = float(left_leg_dict.get("bid_volume"))
                left_ask_volume = float(left_leg_dict.get("ask_volume"))
                left_receiver_timestamp = float(left_leg_dict.get("receiver_timestamp"))
                # left_server_timestamp = float(left_leg_dict.get("server_timestamp"))/1000 # 币安的时间戳单位是毫秒
                # 防止现货没有时间戳报错: 临时替代
                left_server_timestamp = left_receiver_timestamp # 币安的时间戳单位是毫秒
                    # ii. 右腿数据
                right_bid_price = float(right_leg_dict.get("bid_price"))
                right_ask_price = float(right_leg_dict.get("ask_price"))
                right_bid_volume = float(right_leg_dict.get("bid_volume"))
                right_ask_volume = float(right_leg_dict.get("ask_volume"))
                right_receiver_timestamp = float(right_leg_dict.get("receiver_timestamp"))
                # right_server_timestamp = float(right_leg_dict.get("server_timestamp"))/1000 # 币安的时间戳单位是毫秒
                # 防止现货没有时间戳报错: 临时替代
                right_server_timestamp = right_receiver_timestamp # 币安的时间戳单位是毫秒

                # 2. 计算'时间差' (也是很关键的数据, 关系到捕捉价差的准确性!)
                msg = f"[{self.spread_symbol}]\n"
                msg += f"{left_server_timestamp}; {right_server_timestamp}\n"
                msg += f"{left_receiver_timestamp}; {right_receiver_timestamp}\n"
                deltaTime_server = abs(left_server_timestamp - right_server_timestamp) # 左右腿的服务端时间差
                deltaTime_left_server_receiver = abs(left_server_timestamp - left_receiver_timestamp) # 左腿服务端和接受端的时间差
                deltaTime_right_server_receiver = abs(right_server_timestamp - right_receiver_timestamp) # 右腿服务端和接受端的时间差
                deltaTime_receiver = (deltaTime_left_server_receiver + deltaTime_right_server_receiver)/2 # 接收端的平均时间差
                cal_timestamp = get_timestamp(arg="now").timestamp()
                time_bias = abs(((left_receiver_timestamp + right_receiver_timestamp)/2) - cal_timestamp)
                msg += f"cal时间偏移:{time_bias}\n"
                if time_bias > 5:
                    """
                    notes:
                        - 发现网络延迟导致时间差大于5s的情况很常见, 程序一下就被报错停止了...要想想解决办法....
                    """
                    msg = f"[时间偏差: {time_bias}秒]\n"
                    if self.unstoppable_cal:
                        msg += "设置了'无法阻挡cal', 仍然计算中....(适用于极端行情)\n"
                        logger.log(30, msg)
                    else:
                        msg += "'数据获取时间'和'当前计算时间'偏差大于5秒, 暂停计算...\n"
                        # self.alive = False # 将这个机器人的计算任务杀死... (也可机动地选择不杀死, 忽略延迟)
                        self.pause()
                        raise Exception(msg)

                # 3. 计算'价差率'
                    # i. 开仓的价差率
                open_spread_rate = (left_bid_price - right_ask_price) / right_ask_price
                    # ii. 平仓的价差率
                close_spread_rate = (left_ask_price - right_bid_price) / right_bid_price
                # print(f"[{self.spread_symbol}]: --------开仓价差率:{open_spread_rate:.2%}, 左右腿时间差:{deltaTime_server:.3f}, 接收端时间差:{deltaTime_receiver:.3f}")
                # print(f"[{self.spread_symbol}]: --------平仓价差率:{close_spread_rate:.2%}, 左右腿时间差:{deltaTime_server:.3f}, 接收端时间差:{deltaTime_receiver:.3f}\n\n")
                msg += f"开仓价差率:{open_spread_rate:.2%}, 平仓价差率:{close_spread_rate:.2%}, 左右腿时间差:{deltaTime_server:.3f}, 接收端时间差:{deltaTime_receiver:.3f}\n\n"
                print(msg)

                # 4. 存入redis(内存中)
                self.r1.hset(self.spread_symbol, "open_spread_rate", open_spread_rate)
                self.r1.hset(self.spread_symbol, "close_spread_rate", close_spread_rate)
                self.r1.hset(self.spread_symbol, "left_server_timestamp", left_server_timestamp)
                self.r1.hset(self.spread_symbol, "left_receiver_timestamp", left_receiver_timestamp)
                self.r1.hset(self.spread_symbol, "right_server_timestamp", right_server_timestamp)
                self.r1.hset(self.spread_symbol, "right_receiver_timestamp", right_receiver_timestamp)
                self.r1.hset(self.spread_symbol, "deltaTime_server", deltaTime_server)
                self.r1.hset(self.spread_symbol, "deltaTime_receiver", deltaTime_receiver)
                self.r1.hset(self.spread_symbol, "cal_timestamp", cal_timestamp)
                time.sleep(0.3)
        except Exception as e:
            self.pause()
            raise Exception(e)

    def cal_avg_spread(self):
        """
            notes:
                - 每分钟计算平均价差率
        """
        pass

    def run(self):
        """
            functions:
                - 异步执行 [多线程]
        """
        self.active() # 只有激活后, 才可以run...
        # 1. 计算价差的核心函数
        t1 = threading.Thread(target=self.main_cal) # 生成一个子线程去跑, 所以不影响主进程的运行
        t1.start()
        self.threads.append(t1)
        # 2. 计算平均价差率, 价差率增幅等周边辅助函数..
        # t2 = threading.Thread(target=self.main_cal) # 生成一个子线程去跑, 所以不影响主进程的运行
        # t2.start()
        # self.threads.append(t2)



# d1 = r.hgetall("ETCUSDT")
# d2 = r.hgetall("ETCUSDT_PERP")
spread_symbols = ["rsrUSDT/rsrUSDT_PERP"]
csrm = CalSpreadRobotManager()
csrm.add_robots(spread_symbols=spread_symbols, unstoppable_cal=True)


if __name__ == "__main__":
    # spread_symbols = ["ankrUSDT/ankrUSDT_PERP", "zilUSDT/zilUSDT_PERP", "rsrUSDT/rsrUSDT_PERP"]
    # spread_symbols = ["bnbUSD_PERP/bnbUSDT", "axsUSDT/axsUSDT_PERP", "maticUSDT/maticUSDT_PERP"]
    # spread_symbols = ["axsUSDT/axsUSDT_PERP", "bnbUSDT/bnbUSDT_PERP", "maticUSDT/maticUSDT_PERP"]
    # spread_symbols = ["rsrUSDT/rsrUSDT_PERP"]
    # csrm = CalSpreadRobotManager()
    # csrm.add_robots(spread_symbols=spread_symbols, unstoppable_cal=True)
    pass










#
