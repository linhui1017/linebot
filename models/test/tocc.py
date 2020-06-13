import datetime
from sqlalchemy import Column, String, Integer, DateTime, event, Boolean, JSON 

from db.database import pg_Base, pg_engine, pg_session
import uuid
import json
from lib.Checker import isNone
from lib.CountryUnit import country_to_name
from lib.utils import  logger
from lib.utils import  logger
from models.kfsyscc.emp.empdatmv import get_emp
from models.kfsyscc.sys.Sysdept import get_dept_by_code
from db.dbutils import  clzs_to_dicts



import pandas as pd
import io

DEFAULT_TOCC_TITLE ={
1:{'name': '單號', 'filter' : lambda x: x['MASTER_ID']},
2:{'name': '就醫日期', 'filter' :lambda x: x['REG_DATE'] },
3:{'name': '填寫者ID', 'filter' :lambda x: x['APPLY_USER_IDNO'] },
4:{'name': '填寫者姓名', 'filter' :lambda x:  x['APPLY_USER_NAME'] },
5:{'name': '病人ID', 'filter' :lambda x: x['PAT_IDNO'] },
6:{'name': '病人病歷號', 'filter' :lambda x: x['CHART_NO'] },
7:{'name': '病人姓名', 'filter' :lambda x:  x['PAT_NAME'] },
8:{'name': '建檔日期', 'filter' :lambda x: x['CRE_DATE'] },
9:{'name': '建檔時間', 'filter' :lambda x: x['CRE_TIME'] },
10:{'name': '填表原因', 'filter' :lambda x: x['REASON_DESC'] },
11:{'name': '病服協助登入', 'filter' :lambda x: ('N' if(isNone(x['IP_ADDRESS'])) else ('Y' if (x['IP_ADDRESS'][:3] == '172' and not (x['IN_REASON'] in ['EMP', 'EMP2']) )  else 'N')) },
12:{'name': 'TOCC判定結果', 'filter' :lambda x: ('Y' if x['TOOC_PASS'] else 'N') },
13:{'name': '職業別', 'filter' :lambda x:  x['TOOC_JSON2DICT']['occupation_name']},
14:{'name': '您自己是否有以下呼吸道不適或類流感症狀？例如：咳嗽、發燒、流鼻水、肌肉痠痛、頭痛', 'filter' :lambda x: x['TOOC_JSON2DICT']['healthHistory_selfSymptom'] },
15:{'name': '同住家人是否居家隔離', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_familyQuarantineIso'] },
16:{'name': '周遭朋友最近是否有發燒或呼吸道不適症狀', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_friendSymptom'] },
17:{'name': '同住家人最近是否有發燒或呼吸道不適症', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_familySymptom'] },
18:{'name': '同住家人是否居家檢疫', 'filter' :lambda x:  x['TOOC_JSON2DICT']['cluster_familyQuarantineCheck'] },
19:{'name': '到期日', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_dueDate'] },
20:{'name': '工作同事最近是否有發燒或呼吸道不適症狀', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_colleagueSymptom'] },
21:{'name': '身邊親友最近是否有接二連三發燒或呼吸道不適症狀', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_rfFrequentSymptom'] },
22:{'name': '同住家人是否自主健康管理', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_familyHealthManage'] },
23:{'name': '您近期是否與確診者接觸', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_confirmCaseTouch'] },
24:{'name': '接觸史(無)', 'filter' :lambda x: x['TOOC_JSON2DICT']['contactHistory_none'] },
25:{'name': '接觸史(曾參與公眾集會)', 'filter' :lambda x:  x['TOOC_JSON2DICT']['contactHistory_PA'] },
26:{'name': '接觸史(曾出入機場、觀光景點及其他頻繁接觸外國人場所)', 'filter' :lambda x: x['TOOC_JSON2DICT']['contactHistory_ATF'] },
27:{'name': '接觸史(曾參與開學/畢業典禮、婚喪喜慶、運動賽事等聚眾活動)', 'filter' :lambda x: x['TOOC_JSON2DICT']['contactHistory_GMS'] },
28:{'name': '接觸史(野生動物與禽鳥接觸)', 'filter' :lambda x: x['TOOC_JSON2DICT']['contactHistory_WB'] },
29:{'name': '接觸史(曾至醫院、診所就醫)', 'filter' :lambda x: x['TOOC_JSON2DICT']['contactHistory_HC'] },
30:{'name': '接觸史(曾參與宗教/政治/學術/藝文活動)', 'filter' :lambda x:  x['TOOC_JSON2DICT']['contactHistory_RPEC'] },
31:{'name': '接觸史(其他)', 'filter' :lambda x: x['TOOC_JSON2DICT']['contactHistory_others'] },
32:{'name': '過去21日內是否出過國？', 'filter' :lambda x: x['TOOC_JSON2DICT']['travelHistory_isSelfGoAbroad'] },
33:{'name': '1.國家', 'filter' :lambda x: x['TOOC_JSON2DICT']['travelHistory_countrySelf_Name'] },
34:{'name': '同住家屬過去21天是否曾至國外旅遊？', 'filter' :lambda x: x['TOOC_JSON2DICT']['travelHistory_isFamilyGoAbroad'] },
35:{'name': '2.國家', 'filter' :lambda x: x['TOOC_JSON2DICT']['travelHistory_countryFamily_Name'] },
36:{'name': '經常接觸之親友過去21天是否曾至國外旅遊？', 'filter' :lambda x: x['TOOC_JSON2DICT']['travelHistory_isFriendGoAbroad'] },
37:{'name': '3.國家', 'filter' :lambda x: x['TOOC_JSON2DICT']['travelHistory_countryFriend_Name'] },
38:{'name': '陪探病證申請結果', 'filter' :lambda x: x['TOOC_JSON2DICT']['passport']}
}


EMP_TOCC_TITLE ={
1:{'name': '單號', 'filter' : lambda x:x['MASTER_ID'] },
2:{'name': '申請日期', 'filter' : lambda x:x['REG_DATE'] },
3:{'name': '員工編號', 'filter' : lambda x:x['CRE_USER'] },
4:{'name': '員工姓名', 'filter' : lambda x: x['APPLY_USER_NAME']},
5:{'name': '部門代碼', 'filter' : lambda x:get_emp_dept(x['CRE_USER'], 'DEPT_ID') },
6:{'name': '部門名稱', 'filter' : lambda x: get_emp_dept(x['CRE_USER'], 'DEPT_NAME')},
7:{'name': '職稱', 'filter' : lambda x: get_emp_dept(x['CRE_USER'], 'TITLE_NAME')},
8:{'name': '建檔日期', 'filter' : lambda x: x['CRE_DATE'] },
9:{'name': '建檔時間', 'filter' : lambda x:x['CRE_TIME'] },
10:{'name': '填表原因', 'filter' : lambda x: x['REASON_DESC']},
11:{'name': '過去14日內是否出過國？', 'filter' : lambda x: x['TOOC_JSON2DICT']['travelHistory_isSelfGoAbroad']},
12:{'name': '國家', 'filter' : lambda x: x['TOOC_JSON2DICT']['travelHistory_countrySelf_Name']},
13:{'name': '同住家人是否居家隔離', 'filter' : lambda x:x['TOOC_JSON2DICT']['cluster_familyQuarantineIso'] },
14:{'name': '同住家人是否居家檢疫', 'filter' : lambda x: x['TOOC_JSON2DICT']['cluster_familyQuarantineCheck']},
15:{'name': '同住家人是否自主健康管理', 'filter' : lambda x: x['TOOC_JSON2DICT']['cluster_familyHealthManage']},
16:{'name': '您自己是否近期有下列症狀？如：急性咳嗽或發燒', 'filter' : lambda x: x['TOOC_JSON2DICT']['healthHistory_selfSymptom']},
17:{'name': '同住家人最近是否有發燒或呼吸道不適症', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_familySymptom'] },
18:{'name': '周遭朋友最近是否有發燒或呼吸道不適症狀', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_friendSymptom'] },
19:{'name': '工作同事最近是否有發燒或呼吸道不適症狀', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_colleagueSymptom'] },
20:{'name': '身邊親友最近是否有接二連三發燒或呼吸道不適症狀', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_rfFrequentSymptom'] },
}



EMP2_TOCC_TITLE ={
1:{'name': '單號', 'filter' : lambda x:x['MASTER_ID'] },
2:{'name': '申請日期', 'filter' : lambda x:x['REG_DATE'] },
3:{'name': '填寫者ID', 'filter' : lambda x:x['APPLY_USER_IDNO'] },
4:{'name': '填寫者姓名', 'filter' : lambda x: x['APPLY_USER_NAME']},
5:{'name': '部門名稱', 'filter' : lambda x:get_outside_emp(x['APPLY_USER_IDNO'], 'DEPT_NAME') },
6:{'name': '送訓機構', 'filter' : lambda x: get_outside_emp(x['APPLY_USER_IDNO'], 'ORGANIZATION')},
7:{'name': '院內聯絡人', 'filter':lambda x: get_emp_dept(x['CRE_USER'], 'NAME_CH')},
8:{'name': '性質', 'filter' : lambda x: get_outside_emp(x['APPLY_USER_IDNO'], 'TRAN_TYPE')},
9:{'name': '建檔日期', 'filter' : lambda x: x['CRE_DATE'] },
10:{'name': '建檔時間', 'filter' : lambda x:x['CRE_TIME'] },
11:{'name': '填表原因', 'filter' : lambda x: x['REASON_DESC']},
12:{'name': '過去14日內是否出過國？', 'filter' : lambda x: x['TOOC_JSON2DICT']['travelHistory_isSelfGoAbroad']},
13:{'name': '國家', 'filter' : lambda x: x['TOOC_JSON2DICT']['travelHistory_countrySelf_Name']},
14:{'name': '同住家人是否居家隔離', 'filter' : lambda x:x['TOOC_JSON2DICT']['cluster_familyQuarantineIso'] },
15:{'name': '同住家人是否居家檢疫', 'filter' : lambda x: x['TOOC_JSON2DICT']['cluster_familyQuarantineCheck']},
16:{'name': '同住家人是否自主健康管理', 'filter' : lambda x: x['TOOC_JSON2DICT']['cluster_familyHealthManage']},
17:{'name': '您自己是否近期有下列症狀？如：急性咳嗽或發燒', 'filter' : lambda x: x['TOOC_JSON2DICT']['healthHistory_selfSymptom']},
18:{'name': '同住家人最近是否有發燒或呼吸道不適症', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_familySymptom'] },
19:{'name': '周遭朋友最近是否有發燒或呼吸道不適症狀', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_friendSymptom'] },
20:{'name': '工作同事最近是否有發燒或呼吸道不適症狀', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_colleagueSymptom'] },
21:{'name': '身邊親友最近是否有接二連三發燒或呼吸道不適症狀', 'filter' :lambda x: x['TOOC_JSON2DICT']['cluster_rfFrequentSymptom'] },
}

def get_emp_dept(empmo, field):
    emp = get_emp(empmo)
    return ('' if isNone(emp) else emp[field])

def get_deptbycode(deptcode, field):
    dept = get_dept_by_code(deptcode)
    return ('' if isNone(dept) else dept[field])
    
def get_outside_emp(apply_user_idno, field):
    session = pg_session()
    try:
        res = session.query(OutsideEmpEntity).filter(OutsideEmpEntity.ID_NO == apply_user_idno ).first()
        if(not isNone(res)):
            temp = clzs_to_dicts(res)
            return ('' if isNone(temp) else temp[field])
        return ''
    except Exception as e:
        return None
    finally:
        session.close() 



TOCC_IN_REASON= {
    '住院陪病': 
    {
        'name' : 'AI', 
        'filter' :lambda x: x['IN_REASON'] == 'AI',
        'XLS_TITLE': DEFAULT_TOCC_TITLE

    }, 
    '門診化療中心陪病': 
    {
        'name' :'AO', 
        'filter' :  lambda x: x['IN_REASON']  == 'AO',
        'XLS_TITLE': DEFAULT_TOCC_TITLE
    },  
    '急診陪病': 
    {
        'name' :'AE', 
        'filter' :  lambda x: x['IN_REASON']  == 'AE',
        'XLS_TITLE': DEFAULT_TOCC_TITLE 
    }, 
    '住院探病上午時段': 
    {
        'name' :'EI1', 
        'filter' :  lambda x: x['IN_REASON']  == 'EI1',
        'XLS_TITLE': DEFAULT_TOCC_TITLE 
    }, 
    '住院探病下午時段': 
    {
        'name' :'EI2', 
        'filter' :  lambda x: x['IN_REASON']  == 'EI2',
        'XLS_TITLE': DEFAULT_TOCC_TITLE 
    }, 
    '員工每天自評': 
    {
        'name' :'EMP', 
        'filter' :  lambda x: x['IN_REASON'] == 'EMP',
        'XLS_TITLE': EMP_TOCC_TITLE 
    }, 
    '實習人員自評': 
    {
        'name' :'EMP2', 
        'filter' :  lambda x: x['IN_REASON'] == 'EMP2',
        'XLS_TITLE': EMP2_TOCC_TITLE 
    }

}



class DoorPatCheckLogEntity(pg_Base):
    __tablename__ = 'door_pat_check_log'
    RELATIONSHIPS_TO_DICT = False

    CHECK_LOG_ID = Column(String(64), primary_key=True)
    PAT_ID = Column(String(20))
    PAT_NAME = Column(String(80))
    BIRTHDAY = Column(String(10))
    CRE_DATETIME = Column(DateTime, default=datetime.datetime.now())
    IP_ADDRESS = Column(String(64))
    DEL_DATE = Column(String(8))
    DEL_TIME = Column(String(6))
    DEL_USER = Column(String(7))


    def __init__(self):
        pass
    def __repr__(self):
        return '<CHECK_LOG_ID: {0}, PAT_ID:{1}>'.format(self.CHECK_LOG_ID, self.PAT_ID)
    def __str__(self):
        return '<CHECK_LOG_ID: {0}, PAT_ID:{1}>'.format(self.CHECK_LOG_ID, self.PAT_ID)   


@event.listens_for(DoorPatCheckLogEntity, 'before_insert')
def receive_before_insert(mapper, connection, target):
    target.CHECK_LOG_ID = str(uuid.uuid1()).replace('-', '')
    target.CRE_DATETIME = datetime.datetime.now()


class DoorPatCheckRemarkEntity(pg_Base):
    __tablename__ = 'door_pat_check_remark'
    RELATIONSHIPS_TO_DICT = False

    CHECK_REMARK_ID = Column(String(64), primary_key=True)
    PAT_ID = Column(String(20))
    PAT_NAME = Column(String(80))
    BIRTHDAY = Column(String(10))
    CRE_DATETIME = Column(DateTime, default=datetime.datetime.now())
    IP_ADDRESS = Column(String(64))
    DEL_DATE = Column(String(8))
    DEL_TIME = Column(String(6))
    DEL_USER = Column(String(7))
    CHECK_FLAG = Column(String(2))
    CHECK_FLAG2 = Column(String(2))
    CHECK_FLAG3 = Column(String(2))

    @property
    def REASON(self):
        return reason_to_name(self.CHECK_FLAG)

    @property
    def JOB_NAME(self):
        return reason_to_name(self.CHECK_FLAG2)

    @property
    def CRE_DATETIME_STR(self):
        return self.CRE_DATETIME.strftime("%Y-%m-%d %H:%M:%S")


    def __init__(self):
        pass
    def __repr__(self):
        return '<CHECK_REMARK_ID: {0}, PAT_ID:{1}>'.format(self.CHECK_REMARK_ID, self.PAT_ID)
    def __str__(self):
        return '<CHECK_REMARK_ID: {0}, PAT_ID:{1}>'.format(self.CHECK_REMARK_ID, self.PAT_ID)

        

@event.listens_for(DoorPatCheckRemarkEntity, 'before_insert')
def DoorPatCheckLogEntity_before_insert(mapper, connection, target):
    target.CHECK_REMARK_ID = str(uuid.uuid1()).replace('-', '')
    target.CRE_DATETIME = datetime.datetime.now()


def tocc_pass_check_default(data):
    #過去14天是否出國旅遊
    if(data['travelHistory']['isSelfGoAbroad'] == 'Y'):
        return False
            
    #同住家屬過去14天出國旅遊    
    if(data['travelHistory']['isFamilyGoAbroad'] == 'Y'):
        return False
            
    #經常接觸之親屬過去14天出國旅遊
    if(data['travelHistory']['isFriendGoAbroad'] == 'Y'):
        return False

    #同住家人是否居家隔離
    if(data['cluster']['familyQuarantineIso'] == 'Y'):
        return False

    #同住家人是否居家檢疫
    if(data['cluster']['familyQuarantineCheck'] == 'Y'):
        return False

    #同住家人是否自主健康管理
    if(data['cluster']['familyHealthManage'] == 'Y'):
        return False    

    #同住家人最近是否有發燒或呼吸道不適症
    if(data['cluster']['familySymptom'] == 'Y'):
        return False  

    #周遭朋友最近是否有發燒或呼吸道不適症狀
    if(data['cluster']['friendSymptom'] == 'Y'):
        return False   

    #身邊親友最近是否有接二連三發燒或呼吸道不適症狀
    if(data['cluster']['rfFrequentSymptom'] == 'Y'):
        return False 


    #工作同事最近是否有發燒或呼吸道不適症狀
    if(data['cluster']['colleagueSymptom'] == 'Y'):
        return False

    #您近期是否與確診者接觸
    if(('confirmCaseTouch' in data['cluster']) and (data['cluster']['confirmCaseTouch'] == 'Y')):
        return False                                                                                              

    #有呼吸道不適或類流感症狀
    if(data['healthHistory']['selfSymptom'] == 'Y'):
        return False
    
    return True

def tocc_pass_check_emp(data):
    try:
        #過去14天是否出國旅遊
        if(data['travelHistory']['isSelfGoAbroad'] == 'Y'):
            return False

        #同住家人是否居家隔離
        if(data['cluster']['familyQuarantineIso'] == 'Y'):
            return False

        #同住家人是否居家檢疫
        if(data['cluster']['familyQuarantineCheck'] == 'Y'):
            return False

        #同住家人是否自主健康管理
        if(data['cluster']['familyHealthManage'] == 'Y'):
            return False  

        #有呼吸道不適或類流感症狀
        if(data['healthHistory']['selfSymptom'] == 'Y'):
            return False

    except Exception as e: 
        return True 
    return True 

FORMS =  {
    'V09-09-10':{
        '1':{
            'TOOC_PASS_CHECK':lambda x, y: tocc_pass_check_emp(x) if (y in ['EMP', 'EMP2']) else tocc_pass_check_default(x)

        },
        '2':{   
            'TOOC_PASS_CHECK':lambda x, y: tocc_pass_check_emp(x) if (y in ['EMP', 'EMP2']) else tocc_pass_check_default(x)
        }
    },
}

#-----------------------------------------------------------
class DoorAccessCtrlEntity(pg_Base):
    __tablename__ = 'door_access_ctrl'
    RELATIONSHIPS_TO_DICT = False

    ACCESS_ID = Column(String(64), primary_key=True)
    REG_DATE = Column(String(8))
    APPLY_USER_IDNO = Column(String(20))
    APPLY_USER_NAME = Column(String(80))

    TEL_MOBILE =  Column(String(20))
    TEL_HOME =  Column(String(20))
    EMAIL =  Column(String(60))
    IN_REASON =  Column(String(5))
    
    PAT_IDNO =  Column(String(20))
    CHART_NO =  Column(String(8))
    PAT_NAME =  Column(String(80))
    
    CRE_DATE =  Column(String(8))
    CRE_TIME =  Column(String(6))
    CRE_USER =  Column(String(7))
    DEL_DATE =  Column(String(8))
    DEL_TIME =  Column(String(6))
    DEL_USER =  Column(String(7))

    VALID_FLAG =  Column(String(1), default = 'Y') 
    START_DATETIME = Column(DateTime())
    CLOSE_DATETIME = Column(DateTime())
    TOCC_FROM_MASTER_ID = Column(String(64))
    DEL_REASON = Column(String(1000))
    VALIDITY_PERIOD = Column(String(1000))
    INP_NO = Column(String(8))
    IP_ADDRESS = Column(String(64))
    PRN_CNT = Column(Integer() , default = 0 ) 
    PRN_DATETIME = Column(DateTime())     

    def __init__(self):
        pass
    def __repr__(self):
        return '<ACCESS_ID: {0}, APPLY_USER_IDNO:{1}>'.format(self.ACCESS_ID, self.APPLY_USER_IDNO)
    def __str__(self):
        return '<ACCESS_ID: {0}, APPLY_USER_IDNO:{1}>'.format(self.ACCESS_ID, self.APPLY_USER_IDNO)

    def get_tocc(self):
        if(not isNone(self.TOCC_FROM_MASTER_ID)):
            return pg_session.query(ToccFormMasterEntity).filter(ToccFormMasterEntity.MASTER_ID == self.TOCC_FROM_MASTER_ID).first()





class ToccFormMasterEntity(pg_Base):
    __tablename__ = 'tocc_form_master'
    RELATIONSHIPS_TO_DICT = False

    MASTER_ID = Column(String(64), primary_key=True)
    REG_DATE = Column(String(8))
    APPLY_USER_IDNO = Column(String(20))
    APPLY_USER_NAME = Column(String(80))

    PAT_IDNO = Column(String(20))
    CHART_NO = Column(String(8))
    PAT_NAME = Column(String(80))
    
    FORM_ID = Column(String(64))
    FORM_VER = Column(String(5))
    CONTENT = Column(JSON())
    CRE_DATE = Column(String(8))
    CRE_TIME = Column(String(6))
    CRE_USER = Column(String(7))
    DEL_DATE = Column(String(8))
    DEL_TIME = Column(String(6))
    DEL_USER = Column(String(7))
    DEL_REASON = Column(String(1000))
    REASON_DESC = Column(String(1000))
    INP_NO = Column(String(8))
    IP_ADDRESS = Column(String(64))
    PRN_CNT = Column(Integer() , default = 0 ) 
    PRN_DATETIME = Column(DateTime())
    IN_REASON =  Column(String(5))

    def __init__(self):
        pass
    def __repr__(self):
        return '<MASTER_ID: {0}, APPLY_USER_IDNO:{1}>'.format(self.MASTER_ID, self.APPLY_USER_IDNO)
    def __str__(self):
        return '<MASTER_ID: {0}, APPLY_USER_IDNO:{1}>'.format(self.MASTER_ID, self.APPLY_USER_IDNO)


    @property
    def PASSPORT(self):
        #陪探病證申請結果
        return ('N' if(isNone(self.PRN_CNT)) else ('Y' if self.PRN_CNT > 0 else 'N'))


    @property
    def TOOC_PASS(self):
        try:
            data = self.CONTENT 
            form = FORMS[self.FORM_ID][self.FORM_VER]
            return form['TOOC_PASS_CHECK'](data, self.IN_REASON)
        except Exception as e: 
            return True 

        return True

    def TOOC_EMP_PASS(self):
        try:
            data = self.CONTENT 
            form = FORMS[self.FORM_ID][self.FORM_VER]
            return form['TOOC_PASS_CHECK'](data, self.IN_REASON)
        except Exception as e: 
            return True 

        return True               

    @property
    def TOOC_JSON2DICT(self):
        try:
            temp = {}

            data = None
            try:
                data = json.loads(self.CONTENT)
            except Exception as e:
                data = self.CONTENT 

            #職業別
            temp['occupation']=data['occupation']['occupation']
            temp['occupation_name']=job_to_name(data['occupation']['occupation'])

            #同住家人是否居家隔離
            temp['cluster_familyQuarantineIso']=data['cluster']['familyQuarantineIso']
            #周遭朋友最近是否有發燒或呼吸道不適症狀
            temp['cluster_friendSymptom']=data['cluster']['friendSymptom']
            #同住家人最近是否有發燒或呼吸道不適症
            temp['cluster_familySymptom']=data['cluster']['familySymptom']
            #同住家人是否居家檢疫
            temp['cluster_familyQuarantineCheck']=data['cluster']['familyQuarantineCheck']
            #到期日
            temp['cluster_dueDate']=data['cluster']['dueDate']
            #工作同事最近是否有發燒或呼吸道不適症狀
            temp['cluster_colleagueSymptom']=data['cluster']['colleagueSymptom']   
            #身邊親友最近是否有接二連三發燒或呼吸道不適症狀
            temp['cluster_rfFrequentSymptom']=data['cluster']['rfFrequentSymptom']         
            #同住家人是否自主健康管理
            temp['cluster_familyHealthManage']=data['cluster']['familyHealthManage']   


            #您近期是否與確診者接觸
            temp['cluster_confirmCaseTouch']= data['cluster']['confirmCaseTouch']  if('confirmCaseTouch' in data['cluster']) else ''

            #接觸史 
            # 其他
            temp['contactHistory_others']= 'Y' if data['contactHistory']['others'] else 'N'
            # 曾參與公眾集會
            temp['contactHistory_PA']='Y' if data['contactHistory']['PA'] else 'N'                                                
            # 無
            temp['contactHistory_none']='Y' if data['contactHistory']['none'] else 'N'    
            # 曾出入機場、觀光景點及其他頻繁接觸外國人場所
            temp['contactHistory_ATF']='Y' if data['contactHistory']['ATF'] else 'N'                  
            # 曾參與開學/畢業典禮、婚喪喜慶、運動賽事等聚眾活動
            temp['contactHistory_GMS']='Y' if data['contactHistory']['GMS'] else 'N'   
            # 野生動物與禽鳥接觸
            temp['contactHistory_WB']='Y' if data['contactHistory']['WB'] else 'N'   
            # 曾至醫院、診所就醫
            temp['contactHistory_HC']='Y' if data['contactHistory']['HC'] else 'N'   
            # 曾參與宗教/政治/學術/藝文活動
            temp['contactHistory_RPEC']='Y' if data['contactHistory']['RPEC'] else 'N'   

            # 過去14日內是否出過國？
            temp['travelHistory_isSelfGoAbroad']=data['travelHistory']['isSelfGoAbroad']    
            # 過去14日內是否出過國？(國家)
            temp['travelHistory_countrySelf_Code']=data['travelHistory']['countrySelf'] 
            temp['travelHistory_countrySelf_Name']=country_to_name(data['travelHistory']['countrySelf'])   

            # 同住家屬過去14天是否曾至國外旅遊？
            temp['travelHistory_isFamilyGoAbroad']=data['travelHistory']['isFamilyGoAbroad']    
            # 同住家屬過去14天是否曾至國外旅遊？(國家)
            temp['travelHistory_countryFamily_Code']=data['travelHistory']['countryFamily']
            temp['travelHistory_countryFamily_Name']=country_to_name(data['travelHistory']['countryFamily'])

            # 經常接觸之親友過去14天是否曾至國外旅遊？
            temp['travelHistory_isFriendGoAbroad']=data['travelHistory']['isFriendGoAbroad']    
            # 經常接觸之親友過去14天是否曾至國外旅遊？(國家)
            temp['travelHistory_countryFriend_Code']=data['travelHistory']['countryFriend']
            temp['travelHistory_countryFriend_Name']=country_to_name(data['travelHistory']['countryFriend']) 

            # 健康史
            #您自己是否有以下呼吸道不適或類流感症狀？例如：咳嗽、發燒、流鼻水、肌肉痠痛、頭痛
            temp['healthHistory_selfSymptom']=data['healthHistory']['selfSymptom']  

            #陪探病證申請結果
            temp['passport']= ('N' if(isNone(self.PRN_CNT)) else ('Y' if self.PRN_CNT > 0 else 'N'))

            return temp 
        except Exception as e: 
            logger.error('_tocc_by_date :' +  str(e)) 
            return {} 

    @classmethod
    def getall(clz):
        '''***  ***'''
        try:
            data = clz.ExeQueryByClz(pg_session, """
            SELECT "MASTER_ID", "REG_DATE", "APPLY_USER_IDNO", "APPLY_USER_NAME", "PAT_IDNO", "CHART_NO", "PAT_NAME", "FORM_ID", "CONTENT", "CRE_DATE", "CRE_TIME", "CRE_USER", "DEL_DATE", "DEL_TIME", "DEL_USER", "DEL_REASON", "REASON_DESC", "INP_NO"
            FROM public.tocc_form_master               
            """)
            return data if not isNone(data) else None
        except:
            raise  



class DeptNotifyerEntity(pg_Base):
    __tablename__ = 'dept_notifyer'
    RELATIONSHIPS_TO_DICT = False

    DEPT_ID = Column(String(4), primary_key=True)
    EMP_NO = Column(String(8), primary_key=True)


    def __init__(self):
        pass
    def __repr__(self):
        return '<DEPT_ID: {0}, EMP_NO:{1}>'.format(self.DEPT_ID, self.EMP_NO)
    def __str__(self):
        return '<DEPT_ID: {0}, EMP_NO:{1}>'.format(self.DEPT_ID, self.EMP_NO)



class SendMailLogEntity(pg_Base):
    __tablename__ = 'send_mail_log'
    RELATIONSHIPS_TO_DICT = False

    LOG_ID = Column(String(64), primary_key=True)
    MAIL_FROM = Column(String(128))
    MAIL_TO = Column(String(128))
    CONTENT = Column(String())
    SYS_ID = Column(String(8))
    CRE_ID = Column(String(8))
    CRE_DATE = Column(String(8))
    CRE_TIME = Column(String(6))
    SEND_DATE = Column(String(8))
    SEND_TIME = Column(String(6))


    def __init__(self):
        pass
    def __repr__(self):
        return '<LOG_ID: {0}>'.format(self.LOG_ID)
    def __str__(self):
        return '<LOG_ID: {0}>'.format(self.LOG_ID)


@event.listens_for(SendMailLogEntity, 'before_insert')
def send_mail_log_before_insert(mapper, connection, target):
    target.LOG_ID = str(uuid.uuid1()).replace('-', '')


class OutsideEmpEntity(pg_Base):
    __tablename__ = 'outside_emp'
    RELATIONSHIPS_TO_DICT = False

    PK = Column(Integer, primary_key=True)
    NAME_CH = Column(String(80))
    EMAIL = Column(String(128))
    IN_DATE = Column(String(8))
    OUT_DATE = Column(String(8))
    LEADER = Column(String(8))
    REMARK = Column(String(1000))
    EMP_NO = Column(String(8))
    OCCUPATION = Column(String(200))
    TRAN_TYPE = Column(String(20))
    DEPT_NAME = Column(String(200))
    ORGANIZATION = Column(String(200))
    ID_NO = Column(String(20))
    DEPT_CODE= Column(String(4))

    def __init__(self):
        pass
    def __repr__(self):
        return '<ID_NO: {0}, NAME_CH:{1}, EMAIL:{2}>'.format(str(self.ID_NO), self.NAME_CH, self.EMAIL)
    def __str__(self):
        return '<ID_NO: {0}, NAME_CH:{1}, EMAIL:{2}>'.format(str(self.ID_NO), self.NAME_CH, self.EMAIL)



def to_excel(dataset, filepath, filename):
    if(isNone(dataset)):
        return False
    writer = None
    try:
        # Note, Python 2 example. For Python 3 use: output = io.BytesIO().
        output = io.BytesIO()
        # Use the StringIO object as the filehandle.
        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        #writer = pd.ExcelWriter(filepath, engine='xlsxwriter')

        #title = DEFAULT_TOCC_TITLE.keys()

        for k, v in TOCC_IN_REASON.items():
            subset = filter(v['filter'], dataset)
            xls_set = v['XLS_TITLE']
            #title = xls_set.keys()
            title=[]
            index = xls_set.keys()
            datalist = []
            for item in subset:
                d = []
                for key in index:
                    if (xls_set[key]['name'] not in title):
                        title.append(xls_set[key]['name'])
                    d.append(xls_set[key]['filter'](item))
                datalist.append(d)
            df=pd.DataFrame(columns=title,data=datalist)
            df.to_excel(writer, sheet_name=k)
        writer.save()
        output.seek(0)
        return output
        #xlsx_data = output.getvalue()

        
    except Exception as e:
        logger.error('error travelhis to_excel :' +  str(e)) 
        return False
    finally:
        if(not isNone(writer)):
            writer.close()



 
JOB_DICT = {}

def job_to_name(code):
    
    if(isNone(JOB_DICT)):
        jobs = json.loads(JOB_JSON)
        for job in jobs:
            JOB_DICT[job['value']] = job['label']

    if(not isNone(code) and not isNone(JOB_DICT) and (code in JOB_DICT) ):
        return JOB_DICT[code]

    return '' 



JOB_JSON = """
[
{
"label": "醫院工作者(例如：醫療護理醫事、非醫事人員(含外包人力)、實習學生、衛生保健志工等)",
"value": "medical"
},
{
"label": "交通運輸業(如計程車、客運司機等)",
"value": "transportation"
},
{
"label": "旅遊業(如導遊)",
"value": "travel"
},
{
"label": "旅館業(如房務、客務接待人員)",
"value": "hotel"
},
{
"label": "航空服務業(如航空機組人員等)",
"value": "aviation"
},
{
"label": "其他",
"value": "others"
}
]
"""


IN_REASON={
    "0":"無旅遊史，放行",
    "1":"有旅遊史，超過14天，放行",
    "2":"有就醫目的，放行",
    "3":"無替代照顧者，放行",
    "4":"勸離",
    "5":"個案處理",
    "6":"旅遊史超過21天放行",
    "7":"旅遊史>14天，有就醫目的，放行",
    "8":"旅遊史<21天勸離",
    "10":"顯示有『轉診採檢』，不放行",
    "11":"主動告知於公告時間到過高風險地區，不放行",
    "12":"顯示醫院工作者、航空服務業"
}
 
def reason_to_name(code):
    if(not isNone(code) and not isNone(IN_REASON) and (code in IN_REASON) ):
        return IN_REASON[code]
    return '' 
