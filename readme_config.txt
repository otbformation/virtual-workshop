cd ~/Install/OTB-7.0.0-Linux64/
. otbenv.profile
ctest -S share/otb/swig/build_wrapping.cmake -VV
python3 -m venv ~/Dev/venv_OTB7.0
. ~/Dev/venv_OTB7.0/bin/activate
pip install rasterio==1.1.8
pip install jupyter
pip install matplotlib ipyleaflet folium
