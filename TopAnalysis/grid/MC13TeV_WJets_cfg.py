from WMCore.Configuration import Configuration
import os
config = Configuration()

config.section_("General")
config.General.requestName = "MC13TeV_WJets"
config.General.workArea = "grid"
config.General.transferOutputs=True

config.section_("JobType")
config.JobType.pluginName = "Analysis"
config.JobType.psetName = "/afs/cern.ch/work/q/qhassan/top2017/CMSSW_9_4_0/src/TopLJets2015/TopAnalysis/test/runMiniAnalyzer_cfg.py"
config.JobType.disableAutomaticOutputCollection = False
config.JobType.pyCfgParams = ['runOnData=False','era=era2017']
config.JobType.inputFiles = ['jec_MC.db']

config.section_("Data")
config.Data.inputDataset = "/WjetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v1/MINIAODSIM"
config.Data.inputDBS = "global"
config.Data.splitting = "FileBased"
config.Data.unitsPerJob = 4
config.Data.ignoreLocality = False
config.Data.publication = False
config.Data.outLFNDirBase = "/store/group/cmst3/group/top/psilva/997546d/"

config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"
