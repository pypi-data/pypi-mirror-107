

from typing import Optional, Dict
# import datetime
import os
import traceback
import time
import tarfile

from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np

from ...util.mail_retriever import MailAttachmentRetriever, IMAP_SPType, UID_FILE_NAME
from ...util.wechat_bot import WechatBot
from ...util.calculator import Calculator
from ..wrapper.mysql import RawDatabaseConnector, BasicDatabaseConnector, DerivedDatabaseConnector
from ..api.raw import RawDataApi
from ..api.basic import BasicDataApi
from ..api.derived import DerivedDataApi
from ..view.raw_models import HFIndexPrice, HFFundNav
from ..view.basic_models import FOFInfo
from ..view.derived_models import FOFNavPublic
from ..fund.raw.other_raw_data_downloader import OtherRawDataDownloader
from ..fund.raw.raw_data_helper import RawDataHelper


class ResearchNAVReader:

    def __init__(self, read_dir: str, user_name: str, password: str):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        self._read_dir = read_dir
        assert os.path.isdir(self._read_dir), f'arg dump_dir should be a directory (now){self._read_dir}'

        self._user_name = user_name
        self._password = password
        self._wechat_bot = WechatBot()

    @staticmethod
    def _read_for_NAVData(file_path: str) -> Dict[str, int]:
        update_info: Dict[str, int] = {}
        tar = tarfile.open(file_path, 'r:gz', encoding='gb2312')
        for one in tar:
            if not one.name.endswith('.xls') and not one.name.endswith('.xlsx'):
                continue
            if '业绩走势' in one.name:
                continue
            try:
                # try:
                #     normal_replace_dict = {
                #         '・': '·',
                #     }
                #     p_name = one.name
                #     for k, v in normal_replace_dict.items():
                #         p_name = p_name.replace(k, v)
                #     print(f'[_read_for_NAVData] (name in tar){one.name}')
                # except UnicodeEncodeError:
                #     replace_dict = {
                #         '\udc9bK': '汯',
                #         '\udcacB': '珺',
                #         '\udcd4Z': '訸',
                #         '\udcb6G': '禛',
                #         '\udc95D': '旸',
                #         '\udcf1I': '馡',
                #         '\udca9q': '﹒',
                #     }
                #     p_name = one.name
                #     for k, v in replace_dict.items():
                #         p_name = p_name.replace(k, v)
                #     print(f'[_read_for_NAVData] (name in tar (fixed)){p_name}')
                if one.name.startswith('./'):
                    fund_id = one.name[len('./'):].split('.')[0]
                else:
                    fund_id = one.name.split('.')[0]
                print(f'[_read_for_NAVData] (name in tar){one.name} (fund_id){fund_id}')
                df = pd.read_excel(tar.extractfile(one), na_values=['--'])
                df = df.rename(columns={'日期': 'datetime', '净值(分红再投)': 'nav'})
                df = df[['datetime', 'nav']]
                # hf_fund_info = RawDataApi().get_hf_fund_info()
                # hf_fund_info = hf_fund_info[hf_fund_info.desc_name == p_name]
                # fund_id = hf_fund_info.fund_id.array[0]
                df['fund_id'] = fund_id
                df['datetime'] = pd.to_datetime(df.datetime, infer_datetime_format=True).dt.date
                hf_fund_nav = RawDataApi().get_hf_fund_nav(fund_ids=[fund_id])
                if hf_fund_nav is not None:
                    df_fitted = df.astype(hf_fund_nav.dtypes.to_dict())
                    # merge on all columns
                    df_fitted = df_fitted.merge(hf_fund_nav, how='left', indicator=True, validate='one_to_one')
                    df_fitted = df_fitted[df_fitted._merge == 'left_only'].drop(columns=['_merge'])
                else:
                    df_fitted = df
                print(f'to hf_fund_nav {df_fitted}')
                if not df_fitted.empty:
                    # TODO: 最好原子提交下边两步
                    RawDataApi().delete_hf_fund_nav(fund_id_to_delete=fund_id, datetime_list=df_fitted.datetime.to_list())
                    # 更新到db
                    df_fitted.to_sql(HFFundNav.__table__.name, RawDatabaseConnector().get_engine(), index=False, if_exists='append')

                # 再向 FOFNavPublic 更新一份
                df = df.rename(columns={'fund_id': 'fof_id', 'nav': 'adjusted_nav'})
                df = df[df.adjusted_nav.notna()]
                if df.empty:
                    continue
                df['nav'] = df.adjusted_nav
                df['acc_net_value'] = df.adjusted_nav
                fof_nav_public = DerivedDataApi().get_fof_nav_public(fof_id_list=[fund_id])
                if fof_nav_public is not None:
                    fof_nav_public = fof_nav_public.drop(columns=['volume', 'mv', 'ret', 'create_time', 'update_time', 'is_deleted'])
                    df = df.astype(fof_nav_public.dtypes.to_dict())
                    # merge on all columns
                    df = df.merge(fof_nav_public, how='left', indicator=True, validate='one_to_one')
                    df = df[df._merge == 'left_only'].drop(columns=['_merge'])
                print(f'to fof_nav_public {df}')
                if not df.empty:
                    # TODO: 最好原子提交下边两步
                    DerivedDataApi().delete_fof_nav_public(fof_id_to_delete=fund_id, datetime_list=df.datetime.to_list())
                    # 更新到db
                    df.to_sql(FOFNavPublic.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
                    update_info[fund_id] = df.shape[0]

                fof_nav_public = DerivedDataApi().get_fof_nav_public(fof_id_list=[fund_id])
                if fof_nav_public is not None and not fof_nav_public.empty:
                    fof_nav_public = fof_nav_public.set_index('datetime')['adjusted_nav']
                    res_status = Calculator.get_stat_result(fof_nav_public.index, fof_nav_public.array)
                    Session = sessionmaker(BasicDatabaseConnector().get_engine())
                    db_session = Session()
                    # '1' 表示公有的 FOFInfo
                    fof_info_to_set = db_session.query(FOFInfo).filter(FOFInfo.manager_id == '1', FOFInfo.fof_id == fund_id).one_or_none()
                    fof_info_to_set.net_asset_value = float(res_status.last_unit_nav) if not pd.isnull(res_status.last_unit_nav) else None
                    fof_info_to_set.adjusted_net_value = float(fof_nav_public.array[-1]) if not pd.isnull(fof_nav_public.array[-1]) else None
                    fof_info_to_set.latest_cal_date = res_status.end_date
                    fof_info_to_set.ret_year_to_now = float(res_status.recent_year_ret) if not pd.isnull(res_status.recent_year_ret) else None
                    fof_info_to_set.ret_total = float(res_status.cumu_ret) if not pd.isnull(res_status.cumu_ret) else None
                    fof_info_to_set.ret_ann = float(res_status.annualized_ret) if not pd.isnull(res_status.annualized_ret) else None
                    fof_info_to_set.mdd = float(res_status.mdd) if not pd.isnull(res_status.mdd) else None
                    fof_info_to_set.sharpe = float(res_status.sharpe) if not pd.isnull(res_status.sharpe) else None
                    fof_info_to_set.vol = float(res_status.annualized_vol) if not pd.isnull(res_status.annualized_vol) else None
                    fof_info_to_set.has_nav = True
                    db_session.commit()
                    db_session.close()
            except Exception as e:
                traceback.print_exc()
                print(f'[_read_for_NAVData] failed (err){e}')
        tar.close()
        return update_info

    @staticmethod
    def _read_for_IndexData(file_path: str) -> Dict[str, int]:
        update_info = {}
        tar = tarfile.open(file_path, 'r:gz', encoding='gb2312')
        for one in tar:
            print(f'[_read_for_IndexData] (name in tar){one.name}')
            index_name = one.name.split('/')[-1].split('.')[0]
            if '朝阳永续' in one.name:
                key_name = one.name.split('朝阳永续-')[-1].split('.')[0]
                df = pd.read_excel(tar.extractfile(one), na_values=['--'], thousands=',')
                df = df.rename(columns={'时间': 'index_date', key_name: 'close'})
                df = df[['index_date', 'close']]
                df['calcu_date'] = None
            else:
                if '融智' not in one.name:
                    continue
                    # print(f'[_read_for_IndexData] got special file name {one}')
                key_name = one.name.split('融智-')[-1].split('.')[0]
                df = pd.read_excel(tar.extractfile(one), header=3, na_values=['--'])
                df = df.rename(columns={'指数日期': 'index_date', '指数计算日期': 'calcu_date', key_name: 'close'})
                df = df[['index_date', 'calcu_date', 'close']]
                df['calcu_date'] = pd.to_datetime(df.calcu_date, infer_datetime_format=True).dt.date
            df = df[df.close.notna()]
            asset_info = BasicDataApi().get_asset_info_by_type(['策略指数'])
            asset_info = asset_info[asset_info.real_name == index_name]
            if asset_info.empty:
                assert False, f'[_read_for_IndexData] can not find name of index {index_name}'
            index_id = asset_info.real_id.array[0]
            df['index_id'] = index_id
            df['index_date'] = pd.to_datetime(df.index_date, infer_datetime_format=True).dt.date
            hf_index_price = RawDataApi().get_hf_index_price(index_ids=[index_id])
            if hf_index_price is not None:
                df = df.astype(hf_index_price.dtypes.to_dict())
                # merge on all columns
                df = df.merge(hf_index_price, how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            print(df)
            if not df.empty:
                # TODO: 最好原子提交下边两步
                RawDataApi().delete_hf_index_price(index_id, df.index_date.to_list())
                # 更新到db
                df.to_sql(HFIndexPrice.__table__.name, RawDatabaseConnector().get_engine(), index=False, if_exists='append')
                update_info[key_name] = df.shape[0]
        tar.close()
        return update_info

    def _notify_error_event(self, err_msg: str):
        print(f'[read_navs_and_dump_to_db] {err_msg}')
        # self._wechat_bot.send_hedge_fund_nav_update_failed(err_msg)

    def read_navs_and_dump_to_db(self):
        try:
            with open(os.path.join(self._read_dir, UID_FILE_NAME), 'rb') as f:
                uid_last = f.read()
                if not uid_last:
                    uid_last = None
        except Exception as e:
            self._notify_error_event(f'read uid file failed (e){e}, use None instead(read all emails)')
            uid_last = None

        try:
            mar = MailAttachmentRetriever(self._read_dir, ['tar.gz', ])
            data = mar.get_excels(IMAP_SPType.IMAP_QQ, self._user_name, self._password, uid_last)
        except Exception as e:
            self._notify_error_event(f'FATAL ERROR!! get new data of hedge fund nav failed (e){e}')
            return

        uid_last_succeed: Optional[bytes] = None
        for name, comp_date in data.items():
            uid, file_path = comp_date
            if not name.endswith('.tar.gz'):
                continue

            try:
                if '净值数据' in name:
                    update_info = ResearchNAVReader._read_for_NAVData(file_path)

                    ordd = OtherRawDataDownloader(RawDataHelper())
                    ret = ordd.hf_fund_nav_miss()
                    assert not ret, 'update table of hf fund nav miss failed!!'

                    # self._wechat_bot.send_research_data_update('净值', update_info)
                elif '指数数据' in name:
                    update_info = ResearchNAVReader._read_for_IndexData(file_path)

                    # self._wechat_bot.send_research_data_update('指数', update_info)
                else:
                    raise NotImplementedError('unknown research nav file from attachment')
            except Exception as e:
                traceback.print_exc()
                self._notify_error_event(f'{e} (parse) (name){name} (file_path){file_path}')
                continue

            uid_last_succeed = uid
            time.sleep(1)

        # 记录下成功的最后一个uid
        if uid_last_succeed is not None:
            with open(os.path.join(self._read_dir, UID_FILE_NAME), 'wb') as f:
                f.write(uid_last_succeed)
        return


if __name__ == '__main__':
    try:
        email_data_dir = os.environ['SURFING_EMAIL_DATA_DIR']
        user_name = os.environ['SURFING_EMAIL_USER_NAME']
        password = os.environ['SURFING_EMAIL_PASSWORD']
    except KeyError as e:
        import sys
        sys.exit(f'can not found enough params in env (e){e}')

    r_nav_r = ResearchNAVReader(email_data_dir, user_name, password)
    r_nav_r.read_navs_and_dump_to_db()
