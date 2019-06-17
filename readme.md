# SETT

### System for Enhancing simulated images, Training darkflow models, and Tracking

## Setup

SETT is organized into several submodules, each of which can be used independently from the others. When SETT is first cloned, each submodule will only be represented by an empty folder. In order to retrieve the contents of each submodule, use the command 
```
git submodule update --init --recursive
```
Future pulls can be done using
```
git pull --recurse-submodules
```

The system has been tested using anaconda with python 3.6 on both linux and windows.
to get requirements run 
```
pip install -r requirements.txt
```

Darkflow has its own setup that needs to be run inside the main darkflow folder. Choose one of three options. The first option is recommended, however all three will work.

1. Just build the Cython extensions in place. NOTE: If installing this way you will have to use `./flow` in the cloned darkflow directory instead of `flow` as darkflow is not installed globally.
 ```
    python setup.py build_ext --inplace
```
2. Let pip install darkflow globally in dev mode (still globally accessible, but changes to the code immediately take effect)
```
    pip install -e .
```

3. Install with pip globally
```
    pip install .
```

All requirements should now be installed and SETT will be ready for usage.

## Basic SETT usage
SETT is run by feeding .yml config files to overlord.py using 
```
python overlord.py config.yml
```
The default config.yml file shows what layout the config files should have. Groups of .yml files can also be run through SETT to run a series of jobs. This is also done be running a .yml file to overlord.py, similar to executing a single config file. 
```
python overlord.py jobs.yml
```
The default jobs.yml file shows the format needed for the batch job execution behavior. The option macro controls whether a .yml file is interpretted as a batch scheduler or a single job.

## Functionality
SETT implements a multi-stage process for developing machine learning models from simulated images. The system is designed to be fully modular, allowing components to be swapped in or out and run independently

The full workflow is as follows when all meta options are set to yes (except for runName)

Run Simulation: A simulation is run that generates simulated images. The simulation script location is pointed to by paths: simRunner and the function at paths:simFunc is called. Along with simulated images, an xml file for each image should be generated containing the locations of the bounding boxes for objects to be detected. The default simulation generates images and annotations for topological defects.

Extract Smart Noise: If you have an experimental image, the smartNoise module can extract the fourier noise from that image. The extracted noise is periodic noise, generally caused by camera or lighting inaccuracies.



