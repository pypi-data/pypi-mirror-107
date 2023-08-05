"""
经济增长类指标
"""
import pandas as pd
from datetime import datetime
from hbshare.asset_allocation.macro_index.util import create_table, delete_duplicate_records, WriteToDB
from WindPy import w

w.start()


class EconomyIncrease:
    def __init__(self, start_date, end_date, is_increment=1):
        self.start_date = start_date
        self.end_date = end_date
        self.is_increment = is_increment
        self.table_name = 'mac_eco_increase'

    def get_eco_increase_data(self):
        """
        经济增长类数据：GDP不变价当季同比（实际增速）、GDP现价当季同比（名义增速）、制造业PMI、
                    发电量：当月同比、消费者信心指数、70个大中城市新建商品住宅价格指数:环比
        """
        index_list = ['M0039354', 'M6637815', 'M0017126', 'S0027013', 'M0012303', 'S2707412']
        name_dict = {'M0039354': 'GDP_real', 'M6637815': 'GDP_nominal', 'M0017126': 'PMI',
                     'S0027013': 'generating_cap_yoy',
                     'M0012303': 'Consumer_Index', 'S2707412': 'house_price_yoy'}

        res = w.edb(','.join(index_list), self.start_date, self.end_date)
        if res.ErrorCode != 0:
            data = pd.DataFrame()
            print("fetch economy increase data error: start_date = {}, end_date = {}".format(
                self.start_date, self.end_date))
        else:
            if len(res.Data) == 1:
                data = pd.DataFrame(res.Data[0], index=res.Codes, columns=res.Times).T
            else:
                data = pd.DataFrame(res.Data, index=res.Codes, columns=res.Times).T
            data.index.name = 'trade_date'
            data.reset_index(inplace=True)
            data['trade_date'] = data['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
            data.rename(columns=name_dict, inplace=True)

        return data

    def get_construct_result(self):
        if self.is_increment == 1:
            data = self.get_eco_increase_data()
            sql_script = "delete from {} where trade_date in ({})".format(
                self.table_name, ','.join(data['trade_date'].tolist()))
            # delete first
            delete_duplicate_records(sql_script)
            # add new records
            WriteToDB().write_to_db(data, self.table_name)
        else:
            sql_script = """
                    create table mac_eco_increase(
                    id int auto_increment primary key,
                    trade_date date not null unique,
                    GDP_real decimal(6, 1),
                    GDP_nominal decimal(6, 1),
                    PMI decimal(4, 2),
                    generating_cap_yoy decimal(6, 2),
                    Consumer_Index decimal(6, 2),
                    house_price_yoy decimal(4, 2)) 
                """
            create_table(self.table_name, sql_script)
            data = self.get_eco_increase_data()
            WriteToDB().write_to_db(data, self.table_name)


if __name__ == '__main__':
    EconomyIncrease('2005-01-01', '2021-05-17', is_increment=0).get_construct_result()