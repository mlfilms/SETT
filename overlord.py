import yaml
import argparse
import importlib
import os
import shutil
import sys
import imp

def executeFile(filePath,functionName,cfg):
    #this function will execute a script, using the folder
    # the script is located in as the working directory
    #print(filePath)
    path, exFile = os.path.split(filePath)
    mainDir = os.getcwd()
    fullPath = os.path.join(mainDir,path)
    sys.path.append(fullPath)
    os.chdir(fullPath)

    sim = imp.load_source('packages', exFile)
    method = getattr(sim,functionName)
    method(cfg)
    #i = importlib.import_module(exFile)

    os.chdir(mainDir)

def executeConfig(configName):
    mainDir = os.getcwd()
    with open(configName,'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    saveDir = os.path.join('runData',cfg['meta']['runName'])
    if cfg['meta']['saveRun']:
        if os.path.exists(saveDir):
            shutil.rmtree(saveDir)
        os.makedirs(saveDir)

    cfg["temp"] = {}
    cfg["temp"]["rootDir"] = mainDir

    if cfg['meta']['runSimulation']:
        print("Running Simulation")
        simString = cfg['paths']['simRunner']
        functionName = cfg['paths']['simFunc']
        executeFile(simString,functionName,cfg)

    if cfg['meta']['extractSmartNoise']:
        print("Extracting Smart Noise")
        path = cfg['paths']['noiseExtractor']
        noiseExtraction = imp.load_source('packages', os.path.join(path,'noiseExtractor.py'))
        noiseExtraction.noiseExtractor(cfg)

    if cfg['meta']['enhanceImages']:
        print("Enhancing Simulation Images")
        path = cfg['paths']['artifactPath']
        artifacts = imp.load_source('packages', os.path.join(path,'addArtifacts.py'))
        artifacts.addArtifacts(cfg)

    if cfg['meta']['trainModel']:
        print("Training Model")
        trainString = os.path.join(cfg['paths']['darkflow'],'trainFlow.py')
        functionName = 'trainFlowCFG'
        executeFile(trainString,functionName,cfg)

    if cfg['meta']['correctImages']:
        print("Correcting Images")
        path = cfg['paths']['imageCorrection']
        artifacts = imp.load_source('packages', os.path.join(path,'correctImages.py'))
        artifacts.correctImagesCFG(cfg)

    if cfg['meta']['runModel']:
        print("Running Model")
        trainString = os.path.join(cfg['paths']['darkflow'],'runFlowPB.py')
        functionName = 'runFlowCFG'
        executeFile(trainString,functionName,cfg)

    if cfg['meta']['validate']:
        print("Validating")
        path = cfg['paths']['validation']
        artifacts = imp.load_source('packages', os.path.join(path,'validate.py'))
        artifacts.validateCFG(cfg)
        os.chdir(cfg['temp']['rootDir'])
        if cfg['meta']['saveRun']:
            resultsPath = os.path.join(cfg['temp']['rootDir'],cfg['paths']['validation'],'results','results.txt')
            newResultspath = os.path.join(cfg['temp']['rootDir'],saveDir,'results.txt')
            shutil.copyfile(resultsPath,newResultspath)


        #simString = cfg['paths']['simRunner']
        #functionName = cfg['paths']['simFunc']
        #executeFile(simString,functionName,cfg)





        #simString = simString.replace('/','.')
        #print(simString)
        #i = importlib.import_module(simString)

    #runSimulation: yes
    #extractSNoise: yes
    #enhanceImages: yes
    #trainModel: yes
    #runModel: yes



def executeJobs(configName):
    
    print("Using jobs file: "+configName)
    with open(configName,'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    for config in cfg['jobs']:
        print("Executing config file: "+config)
        print("Rootdir: "+ os.getcwd())
        executeConfig(config)
        print("Finished: "+config)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("config",nargs='?',type = str, default='config.yml', help='config file to execute')
    args= parser.parse_args()
    config = args.config

    with open(config,'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    if not cfg['macro']:
        executeConfig(config)
    elif cfg['macro']:
        executeJobs(config)
    else:
        print("Invalid Config")