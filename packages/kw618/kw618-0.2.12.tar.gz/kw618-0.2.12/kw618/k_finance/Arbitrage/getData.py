"""
    导入本模块:
    from kw618.k_finance.Arbitrage.getData import *
"""
from kw618.k_finance.utils_quant import *
import multiprocessing
import time


class MarketDataReceiver():

    def __init__(self, assets=[], connect_types=[1, 2, 3, 4], account_setting=LZC_BINANCE_SETTING):
        """
            args:
                - connect_types:
                    1: 代表获取'现货的盘口'数据
                    2: 代表获取'u本位的盘口'数据
                    3: 代表获取'币本位的盘口'数据
                    4: 代表获取'溢价指数'数据
                    [1, 2, 3, 4]: 表示同时订阅以上所有数据的ws推送
            notes:
                - 1. 数据系统
        """
        self.bra_spot = BinanceRestApi(api_type="spot", settings=account_setting)
        self.bra_futures = BinanceRestApi(api_type="futures", settings=account_setting)
        self.bra_dfutures = BinanceRestApi(api_type="dfutures", settings=account_setting)

        self.connect(assets=assets, connect_types=connect_types)


    # 获取四个关键数据源的ws
        # i. 现货的挂单数据ws
    def get_spot_marketData_ws(self, assets=[]):
        """
        todo:
            - 处理时间戳问题 (通过增量接口)
        """
        if assets:
            channels = [f"{asset.lower()}usdt@bookTicker" for asset in assets]
            spot_marketData_ws = self.bra_spot.subscribe_market_data(channels=channels)
        else:
            spot_marketData_ws = self.bra_spot.subscribe_market_data(channels=["!bookTicker"])
        self.spot_marketData_ws = spot_marketData_ws
        return spot_marketData_ws

        # ii. u本位合约的挂单数据ws
    def get_futures_marketData_ws(self, assets=[]):
        if assets:
            channels = [f"{asset.lower()}usdt@bookTicker" for asset in assets]
            futures_marketData_ws = self.bra_futures.subscribe_market_data(channels=channels)
        else:
            futures_marketData_ws = self.bra_futures.subscribe_market_data(channels=["!bookTicker"])
        self.futures_marketData_ws = futures_marketData_ws
        return futures_marketData_ws

        # iii. 币本位合约的挂单数据ws
    def get_dfutures_marketData_ws(self, assets=[]):
        if assets:
            channels = []
            for asset in assets:
                channels.append(f"{asset.lower()}usd_perp@bookTicker")
                if asset in DFUTURES_QUARTER_ASSETS:
                    channels.append(f"{asset.lower()}usd_210625@bookTicker")
                    channels.append(f"{asset.lower()}usd_210924@bookTicker")
            dfutures_marketData_ws = self.bra_dfutures.subscribe_market_data(channels=channels)
        else:
            dfutures_marketData_ws = self.bra_dfutures.subscribe_market_data(channels=["!bookTicker"])
        self.dfutures_marketData_ws = dfutures_marketData_ws
        return dfutures_marketData_ws

        # iv. 溢价指数ws
    def get_premium_index_ws(self, assets=[]):
        """
        notes:
            - 溢价指数只能传入指定的'asset' (不能一次性订阅所有的symbol)
        """
        if assets:
            symbols = []
            for asset in assets:
                # 溢价指数不同于上面3个行情数据的ws, 这里的symbol需要大写 (上面的symbol需要小写)
                symbols.append(f"{asset.upper()}USDT") # U本位
                # symbols.append(f"{asset.upper()}USD") # 币本位 // 币本位的ws在网页上也获取不到..很神奇..暂时放弃...
            premium_index_ws = self.bra_spot.subscribe_premium_index(symbols=symbols)
        self.premium_index_ws = premium_index_ws
        return premium_index_ws


    # 多进程获取最优盘口挂单/溢价指数数据 (4个ws使用多进程获取)
    def get_spot_marketData(self, assets):
        r0 = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
        ws = self.get_spot_marketData_ws(assets=assets)
        while True:
            # time.sleep(1)
            t = ws.recv()
            # print(t)
            receiver_timestamp = time.time()
            d = json.loads(t)
            data = d.get("data")
            symbol = data.get("s")
            # asset = symbol[:-4]
            updateId = data.get("u")
            bid_price = data.get("b")
            bid_volume = data.get("B")
            ask_price = data.get("a")
            ask_volume = data.get("A")
            # print(f"{symbol}: bid_price:{bid_price}; bid_volume:{bid_volume}; ask_price:{ask_price}, ask_volume:{ask_volume}")
            r0.hset(symbol, "bid_price", bid_price)
            r0.hset(symbol, "bid_volume", bid_volume)
            r0.hset(symbol, "ask_price", ask_price)
            r0.hset(symbol, "ask_volume", ask_volume)
            r0.hset(symbol, "receiver_timestamp", receiver_timestamp)

    def get_futures_marketData(self, assets):
        r0 = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
        ws = self.get_futures_marketData_ws(assets=assets)
        while True:
            # time.sleep(1)
            t = ws.recv()
            # print(t)
            receiver_timestamp = time.time()
            d = json.loads(t)
            data = d.get("data")
            symbol = data.get("s")
            if not "_" in symbol:
                # 如果symbol是 BTCUSDT_210625 则不修改, 表示u本位的季度合约
                kw_symbol = symbol + "_PERP" # 用 BTCUSDT_PERP 命名, 来表示u本位永续合约
            # asset = symbol[:-4]
            updateId = data.get("u") # // 1621861778316
            match_time = data.get("T") # 撮合时间 (可能比事件推送时间更早一些) // 1621861778316
            event_time = data.get("E") # 事件推送时间 // 1621861778319
            bid_price = data.get("b") # // "1.48020"
            bid_volume = data.get("B") # // "64"
            ask_price = data.get("a")
            ask_volume = data.get("A")
            # print(
            #     f"{kw_symbol}: bid_price:{bid_price}; bid_volume:{bid_volume}; "\
            #     f"ask_price:{ask_price}; ask_volume:{ask_volume}; "\
            #     f"server_timestamp:{match_time}; receiver_timestamp:{receiver_timestamp}"
            # )
            r0.hset(kw_symbol, "bid_price", bid_price)
            r0.hset(kw_symbol, "bid_volume", bid_volume)
            r0.hset(kw_symbol, "ask_price", ask_price)
            r0.hset(kw_symbol, "ask_volume", ask_volume)
            r0.hset(kw_symbol, "server_timestamp", match_time)
            r0.hset(kw_symbol, "receiver_timestamp", receiver_timestamp)

    def get_dfutures_marketData(self, assets):
        r0 = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
        ws = self.get_dfutures_marketData_ws(assets=assets)
        while True:
            # time.sleep(1)
            t = ws.recv()
            # print(t)
            receiver_timestamp = time.time()
            d = json.loads(t)
            data = d.get("data")
            symbol = data.get("s") # BTCUSD_200626
            pair = data.get("ps") # BTCUSD
            # asset = symbol[:-4]
            updateId = data.get("u") # // 1621861778316
            match_time = data.get("T") # 撮合时间 (可能比事件推送时间更早一些) // 1621861778316
            event_time = data.get("E") # 事件推送时间 // 1621861778319
            bid_price = data.get("b") # // "1.48020"
            bid_volume = data.get("B") # // "64"
            ask_price = data.get("a")
            ask_volume = data.get("A")
            # print(
            #     f"{symbol}: bid_price:{bid_price}; bid_volume:{bid_volume}; "\
            #     f"ask_price:{ask_price}; ask_volume:{ask_volume}; "\
            #     f"server_timestamp:{match_time}; receiver_timestamp:{receiver_timestamp}"
            # )
            r0.hset(symbol, "bid_price", bid_price)
            r0.hset(symbol, "bid_volume", bid_volume)
            r0.hset(symbol, "ask_price", ask_price)
            r0.hset(symbol, "ask_volume", ask_volume)
            r0.hset(symbol, "server_timestamp", match_time)
            r0.hset(symbol, "receiver_timestamp", receiver_timestamp)

    def get_premium_index(self, assets):
        r0 = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
        ws = self.get_premium_index_ws(assets=assets) # 当assets传入为[]时, 该函数是返回None的 (它只能指定symbol订阅)
        if ws:
            while True:
                # time.sleep(1)
                t = ws.recv()
                # print(t)
                receiver_timestamp = time.time()
                d = json.loads(t)
                data = d.get("data")
                symbol = data.get("s") # pBTCUSDT // 币安官方的命名 (p表示premium)
                event_time = data.get("E") # 事件推送时间 // 1621861778319
                k_data = data.get("k") # 下一层的k线数据
                period_start_time = k_data.get("t") # 间隔的开始时间 (如: 23:59:00 整分钟的第0秒)
                period_end_time = k_data.get("T") # 间隔的结束时间
                open_price = k_data.get("o") # // 开盘价
                close_price = k_data.get("c") # // 收盘价
                high_price = k_data.get("h")
                low_price = k_data.get("l")
                # print(
                #     f"{symbol}: open_price:{open_price}; close_price:{close_price}; "\
                #     f"high_price:{high_price}; low_price:{low_price}; "\
                #     f"server_timestamp:{event_time}; receiver_timestamp:{receiver_timestamp}"
                # )
                r0.hset(symbol, "open_price", open_price)
                r0.hset(symbol, "close_price", close_price)
                r0.hset(symbol, "high_price", high_price)
                r0.hset(symbol, "low_price", low_price)
                r0.hset(symbol, "server_timestamp", event_time)
                r0.hset(symbol, "receiver_timestamp", receiver_timestamp)



    def connect(self, assets, connect_types):
        """
            notes:
                - asset一次connect, 最多可以接收6个信息推送: (有些asset没有币本位, 就只有3个数据)
                    1. 现货挂单
                    2. U本位永续合约挂单
                    3. 币本位永续合约挂单
                    4. 币本位当季合约挂单
                    5. 币本位次季合约挂单
                    6. U本位永续合约溢价指数
                    (以上6个数据由4个进程分别运行)
        """

        # 循环获取数据 (利用多进程)
        if 1 in connect_types:
            p1 = multiprocessing.Process(target=self.get_spot_marketData, kwargs=({'assets':assets}))
            p1.start()
        if 2 in connect_types:
            p2 = multiprocessing.Process(target=self.get_futures_marketData, kwargs=({'assets':assets}))
            p2.start()
        if 3 in connect_types:
            p3 = multiprocessing.Process(target=self.get_dfutures_marketData, kwargs=({'assets':assets}))
            p3.start()
        if 4 in connect_types:
            p4 = multiprocessing.Process(target=self.get_premium_index, kwargs=({'assets':assets}))
            p4.start()
        print("....")


    def keep_connect(self):
        """
        notes: 定期延长ws的有效时间
        """
        pass




if __name__ == "__main__":
    # assets = ["BEL", "RSR", "DEFI", "1INCH", "GRT", "ETC"]
    # assets = ["ETC", "1INCH", "ZIL", "GRT", "BEL", "RSR"]
    # assets = ["AXS", "MANA", "STORJ", "RUNE", "ETC", "IOTA"]
    # assets = ["BNB", "hnt", "ankr", "axs", "matic"]
    assets = ["rsr"]
    # assets = KEY_FUTURES_ASSETS
    mdr = MarketDataReceiver(assets=assets, connect_types=[1, 2, 3, 4])

#
