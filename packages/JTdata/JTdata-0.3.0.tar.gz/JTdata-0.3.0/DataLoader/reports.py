import os
import abc

from .config import data_path
from .tools import print_func_time,to_intdate
from .utils import read_mergeh5
from collections.abc import Iterable
defualt_si = 0
defualt_ei = 1e7

ashare_cashflow = os.path.join(data_path,r'AShareCashFlow')
ashare_cashflow_q = os.path.join(data_path,r'AShareCashFlow_quarterly')
ashare_income = os.path.join(data_path,r'AShareIncome')
ashare_income_q = os.path.join(data_path,r'AShareIncome_quarterly')
ashare_balancesheet = os.path.join(data_path,r'AShareBalanceSheet')
ashare_profit_expr = os.path.join(data_path,r'AShareProfitExpress')
ashare_profit_noti = os.path.join(data_path,r'AShareProfitNotice')
ashare_ttmhis = os.path.join(data_path,r'AShareTTMHis')
ashare_holdernumber = os.path.join(data_path,r'AShareHolderNumber')
ashare_issuedate_pre = os.path.join(data_path,r'AShareIssuingDatePredict')
ashare_fanc_indicator = os.path.join(data_path,r'AShareFinancialIndicator')

class BaseFincReportsProvider(abc.ABC):

    @abc.abstractmethod
    def get_repo_data(self,instruments,fields,start_date,end_date):
        raise NotImplementedError

class LoacalFincReportsProvider(BaseFincReportsProvider):

    def __init__(self, tidx=['report_period','ann_date']) -> None:
        self.tidx = tidx
        super().__init__()

    def get_repo_data(self,datapath,instruments,fields,**kws):
        """ report table reader """
        if isinstance(instruments,str):
            instruments = [instruments]
        path = os.path.join(datapath,'merged.h5')
        data = read_mergeh5(path,instruments,fields,defualt_si,defualt_ei,self.tidx)
        if data.empty:
            return data
        if ("start_date" in kws)&("end_date" in kws):
            start_date,end_date = kws.get("start_date"),kws.get("end_date")
            sd,ed = to_intdate(start_date),to_intdate(end_date)
            if kws.get('by',None) == self.tidx[0]:
                data = data.loc[(data[self.tidx[0]] >= sd) & (data[self.tidx[0]] <= ed)]
            else:
                try:
                    data = data.loc[(data[self.tidx[1]]>=sd)&(data[self.tidx[1]]<=ed)]
                except KeyError:
                    data = data.loc[(data['ann_dt']>=sd)&(data['ann_dt']<=ed)] # 部分表用的 ann_dt

        if self.tidx[0] in kws:
            tgt_rp = kws.get(self.tidx[0],None)
            if not isinstance(tgt_rp,Iterable):
                tgt_rp = [tgt_rp,]
            data = data.loc[data[self.tidx[0]].isin(tgt_rp)]
        return data

    @print_func_time
    def repo_cashflow(self,instruments,fields,**kws):
        return self.get_repo_data(ashare_cashflow,instruments,fields,**kws)
    
    @print_func_time
    def repo_cashflow_q(self,instruments,fields,**kws):
        return self.get_repo_data(ashare_cashflow_q,instruments,fields,**kws)  

    @print_func_time
    def repo_income(self,instruments,fields,**kws):
        return self.get_repo_data(ashare_income,instruments,fields,**kws)
    
    @print_func_time
    def repo_income_q(self,instruments,fields,**kws):
        return self.get_repo_data(ashare_income_q,instruments,fields,**kws)  

    @print_func_time
    def repo_balancesheet(self,instruments,fields,**kws):
        return self.get_repo_data(ashare_balancesheet,instruments,fields,**kws)

    @print_func_time
    def repo_profit_expr(self,instruments,fields,**kws):
        return self.get_repo_data(ashare_profit_expr,instruments,fields,**kws)
    
    @print_func_time
    def repo_profit_noti(self,instruments,fields,**kws):
        return self.get_repo_data(ashare_profit_noti,instruments,fields,**kws)  

    @print_func_time
    def repo_ttmhis(self,instruments,fields,**kws):
        return self.get_repo_data(ashare_ttmhis,instruments,fields,**kws) 
    
    @print_func_time
    def repo_holder_number(self,instruments,fields,**kws):
        return self.get_repo_data(ashare_holdernumber,instruments,fields,**kws) 
    
    @print_func_time
    def repo_issuedate_pre(self,instruments,fields,**kws):
        return self.get_repo_data(ashare_issuedate_pre,instruments,fields,**kws) 

    @print_func_time
    def repo_fanc_indicator(self,instruments,fields,**kws):
        return self.get_repo_data(ashare_fanc_indicator,instruments,fields,**kws)
        

