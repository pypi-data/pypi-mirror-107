
#%%
import os
import abc

from .config import data_path
from .tools import print_func_time,to_intdate
from .utils import read_mergeh5
from .calendarpd import Tdcal

defualt_si = 0
defualt_ei = 1e7

ashare_eod_price = os.path.join(data_path,r'AShareEODPrices')
ashare_blocktrade = os.path.join(data_path,r'AShareBlockTrade')
ashare_derivative_indicator = os.path.join(data_path,r'AShareEODDerivativeIndicator')
ashare_dividend_record = os.path.join(data_path,r'AShareEXRightDividendRecord')
ashare_l2_indicator = os.path.join(data_path,r'AShareL2Indicators')
ashare_margin_trade = os.path.join(data_path,r'AShareMarginTrade')
ashare_money_flow = os.path.join(data_path,r'AShareMoneyFlow')
ashare_tech_indicator = os.path.join(data_path,r'AShareTechIndicators')
ashareyield = os.path.join(data_path,r'AShareYield')

aswsindexeod = os.path.join(data_path,r'ASWSIndexEOD')
aindex_eod_price = os.path.join(data_path,r'AIndexEODPrices')
aindex_idueodcitics = os.path.join(data_path,r'AIndexIndustriesEODCITICS')
aindex_freeweight = os.path.join(data_path,r'AIndexFreeWeight')
#%%
class BaseDailyTSInfoProvider(abc.ABC):

    @abc.abstractmethod
    def get_daily_data(self,instruments,fields,start_date,end_date):
        raise NotImplementedError


class TradeDayInfoProvider(BaseDailyTSInfoProvider):
    """ Intensive time sereis data with trade day as index """

    tidx = 'trade_dt'
    def get_daily_data(self,datapath,instruments,fields,start_date,end_date):
        if isinstance(instruments,str):
            instruments = [instruments]
        path = os.path.join(datapath,'merged.h5')
        start_index,end_index = Tdcal.locate_index(start_date,end_date,freq = 'Tdays')
        return read_mergeh5(path,instruments,fields,start_index,end_index,self.tidx)
    
    def get_sparse_daily_data(self,datapath,instruments,**kws):
        if isinstance(instruments,str):
            instruments = [instruments]
        defualt_si,defualt_ei = 0,1e7
        path = os.path.join(datapath,'merged.h5')
        data = read_mergeh5(path,instruments,None,defualt_si,defualt_ei,self.tidx)
        if data.empty:
            return data
        if ("start_date" in kws)&("end_date" in kws):
            start_date,end_date = kws.get("start_date"),kws.get("end_date")
            sd,ed = to_intdate(start_date),to_intdate(end_date)
            data = data.loc[(data[self.tidx]>=sd)&(data[self.tidx]<=ed)]
        if kws.get("fields"):
            data = data[kws.get("fields")]
        return data

    @print_func_time
    def get_daily_share_data(self,instruments,fields,start_date,end_date):
        return self.get_daily_data(ashare_eod_price,instruments,fields,start_date,end_date)

    @print_func_time
    def get_daily_share_deridi(self,instruments,fields,start_date,end_date):
        return self.get_daily_data(ashare_derivative_indicator,instruments,fields,start_date,end_date)

    @print_func_time
    def get_daily_share_l2idi(self,instruments,fields,start_date,end_date):
        return self.get_daily_data(ashare_l2_indicator,instruments,fields,start_date,end_date)

    @print_func_time
    def get_daily_moneyflow(self,instruments,fields,start_date,end_date):
        return self.get_daily_data(ashare_money_flow,instruments,fields,start_date,end_date)

    @print_func_time
    def get_daily_techindi(self,instruments,fields,start_date,end_date):
        return self.get_daily_data(ashare_tech_indicator,instruments,fields,start_date,end_date)

    @print_func_time
    def get_daily_yield(self,instruments,fields,start_date,end_date):
        return self.get_daily_data(ashareyield,instruments,fields,start_date,end_date)

    @print_func_time
    def get_daily_index_data(self,instruments,fields,start_date,end_date):
        return self.get_daily_data(aindex_eod_price,instruments,fields,start_date,end_date)

    @print_func_time
    def get_daily_index_industries(self,instruments,fields,start_date,end_date):
        return self.get_daily_data(aindex_idueodcitics,instruments,fields,start_date,end_date)

    @print_func_time
    def get_daily_aswsindexeod(self,instruments,fields,start_date,end_date):
        return self.get_daily_data(aswsindexeod,instruments,fields,start_date,end_date)

    @print_func_time
    def get_daily_indexweight(self,instruments,**kws):
        df = self.get_sparse_daily_data(aindex_freeweight,instruments,**kws)
        df['stockcode'] = df['stockcode'].apply(lambda x: bytes.decode(x))

        return df
    
    @print_func_time
    def get_daily_share_divdrec(self,instruments,fields,start_date,end_date):
        return self.get_sparse_daily_data(ashare_dividend_record,instruments,fields = fields ,start_date = start_date,end_date = end_date)
    
    @print_func_time
    def get_daily_blocktrade(self,instruments,fields,start_date,end_date):
        return self.get_sparse_daily_data(ashare_blocktrade,instruments,fields = fields ,start_date = start_date,end_date = end_date)

    @print_func_time
    def get_daily_margintrade(self,instruments,fields,start_date,end_date):
        return self.get_sparse_daily_data(ashare_margin_trade,instruments,fields = fields ,start_date = start_date,end_date = end_date)


if __name__ == '__main__':
    TradeDayInfoProvider().get_daily_indexweight()