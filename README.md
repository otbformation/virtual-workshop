## Virtual Workshop: Remote sensing from space and applications

### Training material for an introduction to OTB

This repository is a fork of David Youssefi workshop for Malta university (https://gitlab.orfeo-toolbox.org/dyoussef/2020-otb-malta)
with some notebooks initially prepared for the "OTB Guided Tour" (https://gitlab.orfeo-toolbox.org/dyoussef/otb-guided-tour).
This repository contain different notebooks, designed to be run on Python environment, locally or remote (for instance, with Google Colab or Binder).
The wiki pages associatd with this repo contain some slides as well as some datapackages.

#### Planning (example) 

* 09.00 - 10.00	 	Introduction to the Orfeo Toolbox
* 10:15 - 11:30		A brief tour of Monteverdi + OTB-Applications
* 11.30 - 12.30 	OTB guided tour : build a small remote sensing chain in Python with OTB

* 14:00 - 15:30		OTB Processing in Python (Classification 1/2)
* 15:30 - 17:00		OTB Processing in Python (Classification 2/2)

## Installation Instructions: Linux

In order to install the Orfeo Toolbox you need to install the prerequisites. You can do this using the following commands
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-dev
sudo apt-get install python3 numpy
sudo apt install cmake
sudo apt-get install build-essential
sudo apt-get install libgl1-mesa-dev
```
Download the 64-bit Linux installation of the Orfeo Toolbox
```
mkdir -p install && cd install
wget https://www.orfeo-toolbox.org/packages/OTB-7.2.0-Linux64.run
```

This package is a self-extractable archive. You may uncompress it with a double-click on the file, or from the command line as follows:

```
chmod +x OTB-7.2.0-Linux64.run
./OTB-7.2.0-Linux64.run
cd OTB-7.2.0-Linux64/
ctest -S share/otb/swig/build_wrapping.cmake -VV
```

To activate the python virtual environment, use the following commands
```
source ./otbenv.profile
```
Finally, use the following script to test that the Orfeo Toolbox is working

```
python3
>>> import otbApplication
```
You are now ready to start using the Orfeo Toolbox.
