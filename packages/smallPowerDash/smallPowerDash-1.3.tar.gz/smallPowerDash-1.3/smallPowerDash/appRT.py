import sys,re,importlib,pandas as pd
import configFiles,smallPowerDash
import tabs.tabMultiUnit as muTab, tabs.tabUnitSelector as usTab
from libs import dccExtended as dccExt
from libs import utils as ut

importlib.reload(configFiles)
importlib.reload(smallPowerDash)
importlib.reload(muTab)
importlib.reload(usTab)
importlib.reload(ut)
importlib.reload(dccExt)

baseFolder = "/home/sylfen/smallPowerExploreDash/"
# ==============================================================================
#                       INSTANCIATIONS
# ==============================================================================

folderFig  = baseFolder + 'figuresSmallPower/'
folderData   = baseFolder + 'pkl/'
folderExport = '/home/sylfen/share/dataScientismProd/Alpha/exportData/'
# confFile     = '/home/sylfen/share/dataScientismProd/Alpha/fichierDeConfiguration/' + 'SmallPower-10002-001-ConfigurationPLC.csv'
confFile     = '/home/sylfen/share/dataScientismProd/Alpha/Real_Data/fichierDeConfiguration/SmallPower-10002-001-ConfigurationPLC.csv'
cfg          = configFiles.ConfigFiles(folderData,confFile,folderFig=folderFig,
                                        folderExport = folderExport,encode='utf-8')
skipEveryHours = 3


utils = ut.Utils()
dccE  = dccExt.DccExtended()
cfg   = configFiles.ConfigFiles(folderData,confFile,folderFig=folderFig,folderExport=folderExport,encode='utf-8')# latin-1 ?
spd   = smallPowerDash.SmallPowerDash(cfg,port = 44999,skipEveryHours=skipEveryHours)
mut   = muTab.MultiUnitTab(cfg,spd,utils,dccE)
ust   = usTab.UnitSelectorTab(cfg,spd,utils,dccE)
# ==============================================================================
#                               TABS
# ==============================================================================
tab1 = spd.createTab(ust.tagUnit_in_RT('ustrt1_',widthG=85,heightGraph=800),'realTime 1')
content = spd.createTabs([tab1])
#
spd.basicLayout("real Time smallPower DATA",content)

# ==============================================================================
#                               SERVE
# ==============================================================================
spd.runServer(host= '0.0.0.0',use_reloader=False,debug=False, processes=1,threaded=True)
