from datetime import datetime, timedelta
from db_cons import sql_write_path_work
import pandas as pd
import numpy as np
from hbshare.cta_factor.factor_func import factor_compute
from hbshare.cta_factor.factor_algo import carry, tsmom, tsrev, xsmom, xsrev, tswr, xswr

start_date = datetime(2010, 1, 1).date()
# end_date = datetime(2021, 4, 9).date()
end_date = datetime.now().date()

PV_window_days_list = [1, 2, 3, 10, 20, 30, 40, 50, 60, 100, 200, 250]
fundamental_window_days_list = [1, 2, 3, 10, 30, 60, 90, 100, 150, 200, 250]
liq_d = 20

sql_path = sql_write_path_work['daily']
table = 'hsjy_fut_com_index'
table_wr = 'hsjy_fut_wr'

data = pd.read_sql_query(
    'select * from ' + table + ' where TDATE<='
    + end_date.strftime('%Y%m%d')
    + ' and TDATE>=' + (start_date - timedelta(days=500)).strftime('%Y%m%d')
    + ' order by TDATE',
    sql_path
)
data_wr0 = pd.read_sql_query(
    'select TDATE, EXCHANGE, PCODE, PNAME, WRQCURRENT from ' + table_wr + ' where TDATE<='
    + end_date.strftime('%Y%m%d')
    + ' and TDATE>=' + (start_date - timedelta(days=500)).strftime('%Y%m%d')
    + ' and FREQ=5 order by TDATE',
    sql_path
)
calendar = data[['TDATE']].sort_values(by='TDATE').drop_duplicates().reset_index(drop=True)
data_wr = pd.DataFrame()
for e in data['EXCHANGE'].drop_duplicates().tolist():
    PCODEs = data[data['EXCHANGE'] == e]['PCODE'].drop_duplicates().tolist()
    for p in PCODEs:
        data_wr_p = data_wr0[np.array(data_wr0['EXCHANGE'] == e) & np.array(data_wr0['PCODE'] == p)]
        data_wr_p = pd.merge(calendar, data_wr_p, on='TDATE', how='left').fillna(method='ffill')
        data_wr_p = data_wr_p[data_wr_p['WRQCURRENT'] >= 0].reset_index(drop=True)
        data_wr = pd.concat([data_wr, data_wr_p])
data_wr = data_wr.reset_index(drop=True)


factor_compute(
    window_days_list=[20, 50], hedge_ratio_list=[50, 60, 70, 80, 90], data=data, factor_func=carry, liq_days=liq_d
)

factor_compute(
    window_days_list=PV_window_days_list, data=data, factor_func=tsmom, liq_days=liq_d
)

factor_compute(
    window_days_list=PV_window_days_list, data=data, factor_func=tsrev, liq_days=liq_d
)


factor_compute(
    window_days_list=PV_window_days_list, hedge_ratio_list=[50, 75], data=data, factor_func=xsmom, liq_days=liq_d
)

factor_compute(
    window_days_list=PV_window_days_list, hedge_ratio_list=[50, 75], data=data, factor_func=xsrev, liq_days=liq_d
)

factor_compute(
    window_days_list=fundamental_window_days_list,
    hedge_ratio_list=[50, 75],
    data=data,
    data_wr=data_wr,
    factor_func=xswr,
    liq_days=liq_d,
    price_field='OPEN',
)

factor_compute(
    window_days_list=fundamental_window_days_list,
    data=data,
    data_wr=data_wr,
    factor_func=tswr,
    liq_days=liq_d,
    price_field='OPEN',
)


