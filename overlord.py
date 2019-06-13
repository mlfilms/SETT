import yaml
import argparse
import importlib
import os
import shutil
import sys
import imp

def executeFile(filePath,functionName,cfg):

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

    cfg["temp"] = {}
    cfg["temp"]["rootDir"] = mainDir

    if cfg['meta']['runSimulation']:
        simString = cfg['paths']['simRunner']
        functionName = cfg['paths']['simFunc']
        executeFile(simString,functionName,cfg)

    if cfg['meta']['enhanceImages']:
        path = cfg['paths']['artifactPath']
        artifacts = imp.load_source('packages', os.path.join(path,'addArtifacts.py'))
        artifacts.addArtifacts(cfg)

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






if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("config",nargs='?',type = str, default='config.yml', help='config file to execute')

    args= parser.parse_args()
    executeConfig(args.config)