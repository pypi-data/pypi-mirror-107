"""
货币类指标
"""
import pandas as pd
from datetime import datetime
from hbshare.asset_allocation.macro_index.util import create_table, delete_duplicate_records, WriteToDB
from WindPy import w

w.start()


class Currency:
    def __init__(self, start_date, end_date, is_increment=1):
        self.start_date = start_date
        self.end_date = end_date
        self.is_increment = is_increment
        self.table_name = 'mac_curr'

    def get_currency_data(self):
        """
        货币类数据：M1同比、M2同比、金融机构：短期贷款余额、金融机构：中长期贷款余额、社会融资规模存量同比、
                 7日逆回购利率、贷款市场报价利率(LPR):1年、贷款市场报价利率(LPR):5年
        """
        index_list = ['M0001383', 'M0001385', 'M0043417', 'M0043418', 'M5525763', 'M0041371', 'M0096870', 'M0331299']
        name_dict = {"M0001383": "M1_yoy", "M0001385": "M2_yoy",
                     "M0043417": "short_term_loan_balance", "M0043418": "long_term_loan_balance",
                     "M5525763": "social_finance_yoy",
                     "M0041371": "reverse_repo_7", "M0096870": "LPR_1_year",
                     "M0331299": "LPR_5_year"}

        res = w.edb(','.join(index_list), self.start_date, self.end_date)
        if res.ErrorCode != 0:
            data = pd.DataFrame()
            print("fetch currency data error: start_date = {}, end_date = {}".format(self.start_date, self.end_date))
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
            data = self.get_currency_data()
            sql_script = "delete from {} where trade_date in ({})".format(
                self.table_name, ','.join(data['trade_date'].tolist()))
            # delete first
            delete_duplicate_records(sql_script)
            # add new records
            WriteToDB().write_to_db(data, self.table_name)
        else:
            sql_script = """
                create table mac_curr(
                id int auto_increment primary key,
                trade_date date not null unique,
                M1_yoy decimal(4, 2),
                M2_yoy decimal(4, 2),
                short_term_loan_balance decimal(10, 2),
                long_term_loan_balance decimal(10, 2),
                social_finance_yoy decimal(4, 2),
                reverse_repo_7 decimal(4, 2),
                LPR_1_year decimal(4, 2),
                LPR_5_year decimal(4, 2)) 
            """
            create_table(self.table_name, sql_script)
            data = self.get_currency_data()
            WriteToDB().write_to_db(data, self.table_name)


if __name__ == '__main__':
    Currency('2021-01-01', '2021-04-23', is_increment=0).get_construct_result()
