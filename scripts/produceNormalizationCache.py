#!/usr/bin/env python

import optparse
import os,sys
import ROOT
from subprocess import Popen, PIPE

"""
steer the script
"""
def main():

    #configuration
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--inDir',       dest='inDir',       help='input directory with files',   default='/store/cmst3/user/psilva/LJets2015/5736a2c',        type='string')
    parser.add_option(      '--HiForest',    dest='HiForest',    help='flag if these are HiForest',   default=False, action='store_true')
    parser.add_option(      '--update',      dest='update',      help='update current weight cache',   default=False, action='store_true')
    #parser.add_option(      '--mount',       dest='mount',       help='mount eos locally',   default=False, action='store_true')
    parser.add_option('-o', '--output',      dest='cache',       help='output file',                  default='data/era2016/genweights.root',                      type='string')
    (opt, args) = parser.parse_args()

    baseEOS='/eos/cms/'
    #eos_cmd = '/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select'
    #if opt.mount:
    #    baseEOS='eos/cms'
    #    Popen([eos_cmd, ' -b fuse mount', 'eos'],stdout=PIPE).communicate()

    #loop over samples available
    genweights={}
    for sample in os.listdir('%s/%s' % (baseEOS,opt.inDir)):

        #sum weight generator level weights
        wgtCounter=None
        labelH=None
        for f in os.listdir('%s/%s/%s' % (baseEOS,opt.inDir,sample ) ):
            fIn=ROOT.TFile.Open('%s/%s/%s/%s' % (baseEOS,opt.inDir,sample,f ) )
            if not opt.HiForest:
                if wgtCounter is None:
                    try:
                        wgtCounter=fIn.Get('analysis/fidcounter').ProjectionX('genwgts',1,1)
                    except:
                        print 'Check %s/%s/%s/%s probably corrupted?' % (baseEOS,opt.inDir,sample,f )
                        continue
                    wgtCounter.SetDirectory(0)
                    wgtCounter.Reset('ICE')
                labelH=fIn.Get('analysis/generator_initrwgt')
                if labelH : labelH.SetDirectory(0)                             
                try:
                    px=fIn.Get('analysis/fidcounter').ProjectionX('px',1,1)
                    wgtCounter.Add(px)
                    px.Delete()
                except:
                    print 'Check eos/cms/%s/%s/%s probably corrupted?' % (opt.inDir,sample,f )
                    continue
            else:
                if wgtCounter is None:
                    wgtCounter=ROOT.TH1F('genwgts','genwgts',1500,0,1500)
                    wgtCounter.SetDirectory(0)
                hiTree=fIn.Get('hiEvtAnalyzer/HiTree')
                for i in xrange(0,hiTree.GetEntriesFast()):
                    hiTree.GetEntry(i)
                    try:
                        ttbar_w=getattr(hiTree,'ttbar_w')
                        for ibin in xrange(0,ttbar_w.size()):
                            wgtCounter.Fill(ibin,ttbar_w[ibin])
                        if ttbar_w.size()==0: raise ValueError('simple count required')
                    except:
                        wgtCounter.Fill(0,1)
            fIn.Close()

        if wgtCounter is None: continue
        if labelH:
            for xbin in range(1,wgtCounter.GetNbinsX()+1):
                label=labelH.GetXaxis().GetBinLabel(xbin)
                for tkn in ['<','>',' ','\"','/','weight','=','\n']: label=label.replace(tkn,'')
                wgtCounter.GetXaxis().SetBinLabel(xbin,label)

        #invert to set normalization
        print sample,' initial sum of weights=',wgtCounter.GetBinContent(1)
        for xbin in xrange(1,wgtCounter.GetNbinsX()+1):
            val=wgtCounter.GetBinContent(xbin)
            if val==0: continue
            wgtCounter.SetBinContent(xbin,1./val)
            wgtCounter.SetBinError(xbin,0.)
       
        genweights[sample]=wgtCounter

    #dump to ROOT file    
    cachefile=ROOT.TFile.Open(opt.cache,'UPDATE' if opt.update else 'RECREATE')
    for sample in genweights:
        genweights[sample].SetDirectory(cachefile)
        genweights[sample].Write(sample)
    cachefile.Close()
    print 'Produced normalization cache @ %s'%opt.cache

    #if opt.mount:
    #    Popen([eos_cmd, ' -b fuse umount', 'eos'],stdout=PIPE).communicate()

    #all done here
    exit(0)



"""
for execution from another script
"""
if __name__ == "__main__":
    sys.exit(main())
