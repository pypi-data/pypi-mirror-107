import pandas as pd, numpy as np
from dorianUtils.configFilesD import ConfigDashTagUnitTimestamp
from dorianUtils.configFilesD import ConfigDashRealTime
from dorianUtils.configFilesD import ConfigDashSpark
import subprocess as sp, os,re,glob
from dateutil import parser
from scipy import linalg,integrate
pd.options.mode.chained_assignment = None  # default='warn'


class ConfigFilesSmallPower(ConfigDashTagUnitTimestamp):
    # ==========================================================================
    #                       INIT FUNCTIONS
    # ==========================================================================

    def __init__(self,folderPkl,folderFig=None,folderExport=None,encode='utf-8'):
        self.appDir = os.path.dirname(os.path.realpath(__file__))
        self.filePLC = glob.glob(self.appDir +'/confFiles/' + '*PLC*')[0]
        super().__init__(folderPkl,self.filePLC,folderFig=folderFig,folderExport=folderExport)
        # self.typeGraphs = pd.read_csv('confFiles/typeGraph.csv',index_col=0)
        self.usefulTags = pd.read_csv(self.appDir+'/confFiles/predefinedCategories.csv',index_col=0)
        self.dfPLC      = self.__buildPLC()

    def __buildPLC(self):
        return self.dfPLC[self.dfPLC.DATASCIENTISM==True]
# ==============================================================================
#                   functions compute new variables
# ==============================================================================

    def integrateDFTag(self,df,tagname,timeWindow=60,formatted=1):
        dfres = df[df.Tag==tagname]
        if not formatted :
            dfres = self.formatRawDF(dfres)
        dfres = dfres.sort_values(by='timestamp')
        dfres.index=dfres.timestamp
        dfres=dfres.resample('100ms').ffill()
        dfres=dfres.resample(str(timeWindow) + 's').mean()
        dfres['Tag'] = tagname
        return dfres

    def integrateDF(self,df,pattern,**kwargs):
        ts = time.time()
        dfs = []
        listTags = self.getTagsTU(pattern[0],pattern[1])[self.tagCol]
        # print(listTags)
        for tag in listTags:
            dfs.append(self.integrateDFTag(df,tagname=tag,**kwargs))
        print('integration of pattern : ',pattern[0],' finished in ')
        self.utils.printCTime(ts)
        return pd.concat(dfs,axis=0)

    def convertCur2Power(self,df,voltage):
        dfOut = df.copy()
        dfOut.value*=voltage #V
        dfOut.Tag=dfOut.Tag.str.replace('_IT_','_Power' + str(voltage) + 'V_')
        return df

    def computePower(self,df,group,timeWindow=60):
        pattern = self.dictPower[group]
        if len(pattern) == 3 :
            dfPowerGroup = self.integrateDF(df,pattern=pattern[:2],timeWindow=timeWindow)
            dfPowerGroup = self.convertCur2Power(dfPowerGroup,pattern[2])
        else :
            dfPowerGroup = self.integrateDF(df,pattern=pattern,timeWindow=timeWindow)
        return dfPowerGroup

    def getTagsUsedForPower(self):
        tagList,dfs = list(self.dictPower.keys())[:-1],[]
        for group in tagList:
            pat = self.dictPower[group]
            df = self.getTagsTU(pat[0],pat[1])
            df['group'] = group
            if len(pat)==3 :
                df['voltage'] = pat[2]
            else :
                df['voltage'] = np.nan
            dfs.append(df)
        res = pd.concat(dfs)
        res.to_csv('variableUsedToComputePower.csv')
        # self.utils.printDFSpecial(res)
        return res

    def getDFtypeGraph(self,df,typeGraph='Bilan système en puissance',**kwargs):
        dfTypeGraph = []
        if typeGraph == 'Bilan système en puissance':
            df=pd.concat([self.getDFsameCat(df,'A'),self.getDFsameCat(df,'W')])
            for group in list(self.dictPower.keys())[:-1]:
                print(group)
                dftmp = self.computePower(df,group,**kwargs)
                dftmp['groupPower'] = group
                dfTypeGraph.append(dftmp)
            dfTypeGraph = pd.concat(dfTypeGraph,axis=0)
            dfTypeGraph['timestamp'] = dfTypeGraph.index
            return dfTypeGraph

    # ==============================================================================
    #                   functions computation
    # ==============================================================================

    def prepareDFforFit(self,filename,ts=None,group='temperatures Stack 1',rs='30s'):
        df = self.loadFile(filename)
        a  = self.usefulTags[group]
        df = self.getDFTagsTU(df,a[0],a[1])
        df = self.pivotDF(df,resampleRate=rs)
        if not not ts :
            df= self.getDFTime(df,ts)
        return df

    def fitDataframe(self,df,func='expDown',plotYes=True,**kwargs):
        res = {}
        period = re.findall('\d',df.index.freqstr)[0]
        print(df.index[0].freqstr)
        for k,tagName in zip(range(len(df)),list(df.columns)):
             tmpRes = self.utils.fitSingle(df.iloc[:,[k]],func=func,**kwargs,plotYes=plotYes)
             res[tagName] = [tmpRes[0],tmpRes[1],tmpRes[2],
                            1/tmpRes[1]/float(period),tmpRes[0]+tmpRes[2]]
        res  = pd.DataFrame(res,index = ['a','b','c','tau(s)','T0'])
        return res

class ConfigFilesSmallPowerSpark(ConfigDashSpark):
    def __init__(self,sparkData,confFile=None,folderFig=None,folderExport=None,encode='utf-8'):
        self.appDir = os.path.dirname(os.path.realpath(__file__))
        if not confFile : confFile=glob.glob(self.appDir +'/confFiles/' + '*PLC*')[0]
        super().__init__(sparkData=sparkData,confFile=confFile,folderFig=folderFig,folderExport=folderExport)
        self.usefulTags = pd.read_csv(self.appDir+'/confFiles/predefinedCategories.csv',index_col=0)
        self.dfPLC = self.__buildPLC()

    def __buildPLC(self):
        return self.dfPLC[self.dfPLC.DATASCIENTISM==True]

class ConfigFilesSmallPower_RealTime(ConfigDashRealTime):
    # ==========================================================================
    #                       INIT FUNCTIONS
    # ==========================================================================

    def __init__(self,confFolder,timeWindow=2*60*60,
                    folderFig=None,folderExport=None,encode='utf-8'):
        self.appDir  = os.path.dirname(os.path.realpath(__file__))
        self.filePLC = glob.glob(self.appDir +'/confFiles/' + '*PLC*')[0]
        self.connParameters ={
            'host'     : "192.168.1.222",
            'port'     : "5434",
            'dbname'   : "Jules",
            'user'     : "postgres",
            'password' : "SylfenBDD"
        }
        super().__init__(confFolder,timeWindow,self.connParameters,
                            folderFig=folderFig,folderExport=folderExport)

    def connectToJulesDataBase(self,connParameters=None):
        if not connParameters :
            connParameters ={
                'host'     : "192.168.1.222",
                'port'     : "5434",
                'dbname'   : "Jules",
                'user'     : "postgres",
                'password' : "SylfenBDD"
            }
        connReq = self.utils.connectToPSQLsDataBase(connParameters)
        return conn
