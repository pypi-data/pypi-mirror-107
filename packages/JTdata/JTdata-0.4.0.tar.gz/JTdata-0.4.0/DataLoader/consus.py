import os
import abc

from .config import data_path
from .tools import print_func_time,to_intdate
from .utils import read_mergeh5
from collections.abc import Iterable
defualt_si = 0
defualt_ei = 1e7

ashare_consus_fy0_30d = os.path.join(data_path,r'AShareConsensusData_FY0_30D')
ashare_consus_fy0_90d = os.path.join(data_path,r'AShareConsensusData_FY0_90D')
ashare_consus_fy0_180d = os.path.join(data_path,r'AShareConsensusData_FY0_180D')
ashare_consus_fy0_180l = os.path.join(data_path,r'AShareConsensusData_FY0_180L')
ashare_consus_fy1_30d = os.path.join(data_path,r'AShareConsensusData_FY1_30D')
ashare_consus_fy1_90d = os.path.join(data_path,r'AShareConsensusData_FY1_90D')
ashare_consus_fy1_180d = os.path.join(data_path,r'AShareConsensusData_FY1_180D')
ashare_consus_fy1_180l = os.path.join(data_path,r'AShareConsensusData_FY1_180L')
ashare_consus_fy2_30d = os.path.join(data_path,r'AShareConsensusData_FY2_30D')
ashare_consus_fy2_90d = os.path.join(data_path,r'AShareConsensusData_FY2_90D')
ashare_consus_fy2_180d = os.path.join(data_path,r'AShareConsensusData_FY2_180D')
ashare_consus_fy2_180l = os.path.join(data_path,r'AShareConsensusData_FY2_180L')
ashare_consus_fy3_30d = os.path.join(data_path,r'AShareConsensusData_FY3_30D')
ashare_consus_fy3_90d = os.path.join(data_path,r'AShareConsensusData_FY3_90D')
ashare_consus_fy3_180d = os.path.join(data_path,r'AShareConsensusData_FY3_180D')
ashare_consus_fy3_180l = os.path.join(data_path,r'AShareConsensusData_FY3_180L')

ashare_consus_rolling_cagr = os.path.join(data_path,r"AShareConsensusRollingData_CAGR")
ashare_consus_rolling_fy0 = os.path.join(data_path,r"AShareConsensusRollingData_FY0")
ashare_consus_rolling_fy1 = os.path.join(data_path,r"AShareConsensusRollingData_FY1")
ashare_consus_rolling_fy2 = os.path.join(data_path,r"AShareConsensusRollingData_FY2")
ashare_consus_rolling_fy3 = os.path.join(data_path,r"AShareConsensusRollingData_FY3")
ashare_consus_rolling_yoy = os.path.join(data_path,r"AShareConsensusRollingData_YOY")
ashare_consus_rolling_yoy2 = os.path.join(data_path,r"AShareConsensusRollingData_YOY2")

ashare_sktrating_30d = os.path.join(data_path,r"AShareStockRatingConsus_30D")
ashare_sktrating_90d = os.path.join(data_path,r"AShareStockRatingConsus_90D")
ashare_sktrating_180d = os.path.join(data_path,r"AShareStockRatingConsus_180D")

class BaseConsusDataProvider(abc.ABC):

    @abc.abstractmethod
    def get_repo_data(self,instruments,fields,start_date,end_date):
        raise NotImplementedError

class LoacalConsusProvider(BaseConsusDataProvider):

    def __init__(self, tidx=['est_report_period','est_date']) -> None:
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
                        data = data.loc[(data['rating_date']>=sd)&(data['rating_date']<=ed)] # 部分表用的 ann_dt

            if self.tidx[0] in kws:
                tgt_rp = kws.get(self.tidx[0],None)
                if not isinstance(tgt_rp,Iterable):
                    tgt_rp = [tgt_rp,]
                data = data.loc[data[self.tidx[0]].isin(tgt_rp)]
            return data
        
    @print_func_time
    def consus(self,instruments,fields,foreward_type,window_days,**kws):
        path = eval('_'.join(["ashare_consus",foreward_type,window_days]))
        return self.get_repo_data(path,instruments,fields,**kws)

    @print_func_time
    def consus_rolling(self,instruments,fields,foreward_type,**kws):
        path = eval('_'.join(["ashare_consus_rolling",foreward_type]))
        return self.get_repo_data(path,instruments,fields,**kws)

    @print_func_time
    def stk_rating(self,instruments,fields,window_days,**kws):
        path = eval('_'.join(["ashare_sktrating",window_days]))
        return self.get_repo_data(path,instruments,fields,**kws)