from time import sleep

from notecoin.huobi.client import GenericClient
from notecoin.huobi.strategy.message import HuoBiMessage
from notetool.tool.log import logger
from notetool.tool.secret import read_secret


class FindNewCoin:
    def __init__(self):
        self.huobi = HuoBiMessage()

        api_key = read_secret(cate1='coin', cate2='huobi', cate3='api_key')
        secret_key = read_secret(cate1='coin', cate2='huobi', cate3='secret_key')

        self.generic = GenericClient(api_key=api_key, secret_key=secret_key)
        self.symbol_df_last = None
        self.symbol_df_now = None
        self.symbol_dict = {}

    def init(self):
        df = self.generic.get_exchange_symbols().data
        self.symbol_df_last = self.symbol_df_now = df
        symbols = df[['symbol', 'state']].values
        for symbol, status in symbols:
            self.symbol_dict[symbol] = status
            if 'lat' in symbol:
                print(symbol)

    def update(self, df):
        self.symbol_df_last = self.symbol_df_now
        self.symbol_df_now = df

        symbols = df[['symbol', 'state']].values
        for symbol, status in symbols:
            if symbol not in self.symbol_dict.keys():
                self.huobi.send_msg(f"new symbol:{symbol}:{status}")
                self.symbol_dict[symbol] = status
            elif status != self.symbol_dict[symbol]:
                self.huobi.send_msg(f"status change:{symbol}:{self.symbol_dict[symbol]}->{status}")
                self.symbol_dict[symbol] = status
            else:
                pass

    def run(self):
        self.init()
        step = 0
        while True:
            try:
                df = self.generic.get_exchange_symbols().data
                self.update(df)
            except Exception as e:
                print(e)
                logger.info(f"error:{e}")

            if step % 8640 == 0:
                self.info()

            sleep(10)
            step += 1

    def info(self):
        status_dict = {}
        for k, v in self.symbol_dict.items():
            ks = status_dict.get(v, [])
            ks.append(k)
            status_dict[v] = ks

        for k, v in status_dict.items():
            self.huobi.send_msg(f"{k}:\t{', '.join(v)}")


find = FindNewCoin()
find.run()

# ps -elf|grep check_new
# nohup /root/anaconda3/bin/python3.8 /root/workspace/notechats/notecoin/notecoin/huobi/strategy/check_new.py >>/root/workspace/tmp/notecoin-check-run-$(date +%Y-%m-%d).log 2>&1 &
