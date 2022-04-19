#!/bin/bash
set -e
PROGNAME=$0
usage() {
    cat << EOF >&2
Usage: $PROGNAME [-f]
       -f: install from scratch (compiling OTB ~20min)
EOF
    exit 1
}

FROM_SCRATCH=0
while getopts f o; do
    case $o in
	(f) FROM_SCRATCH=1;;
	(*) usage
    esac
done
shift "$((OPTIND - 1))"

# install ubuntu packages
echo ">> (1/4) Install Ubuntu packages (expected duration: ~2min)"
SECONDS=0
add-apt-repository -y  ppa:ubuntugis/ubuntugis-unstable 1>/dev/null 2>&1
apt-get update 1>/dev/null 2>&1 && apt-get install --no-install-recommends -y \
    cmake-curses-gui \
    git \
    wget \
    file \
    apt-utils \
    gcc \
    g++ \
    make \
    python3 \
    python3-pip \
    python3-numpy \
	python3-opencv \
    unzip \
    ninja-build \
    libboost-date-time-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-program-options-dev \
    libboost-system-dev \
    libboost-thread-dev \
    libgdal-dev \
    libinsighttoolkit4-dev \
	libopencv-dev \
    libopenthreads-dev \
    libossim-dev \
    libtinyxml-dev \
    libmuparser-dev \
    libmuparserx-dev \
    libsvm-dev \
    swig \
    libfftw3-dev \
    python3-virtualenv 1>/dev/null 2>&1 \
    && rm -rf /var/lib/apt/lists/*
echo "Elapsed time: ${SECONDS} seconds"

SECONDS=0
if [ "$FROM_SCRATCH" -eq 0 ]
then
    # download pre-compiled-otb
    echo ">> (2/4) Download pre-compiled-otb (expected duration: <1s)"
	# Download Google Drive file --no-check-certificate
    wget 'https://docs.google.com/uc?export=download&id=1xEapXzECWKf2DkqV0xk7MoLQGRo-Njd8' -O /content/otb.tar.gz 1>/dev/null 2>&1

else
    # create orfeo toolbox archive
    echo ">> (2/4) Create pre-compiled-otb (expected duration: ~20min)"
    SECONDS=0
    mkdir -p /opt/otb && cd /opt/otb && \
	wget -q https://www.orfeo-toolbox.org/packages/archives/OTB/OTB-8.0.0.zip -O /tmp/OTB-8.0.0.zip && \
	unzip -q /tmp/OTB-8.0.0.zip && rm /tmp/OTB-8.0.0.zip

    mkdir -p /opt/otb/build && cd /opt/otb/build && cmake \
	"-DBUILD_COOKBOOK:BOOL=OFF" "-DBUILD_EXAMPLES:BOOL=OFF" "-DBUILD_SHARED_LIBS:BOOL=ON" \
	"-DBUILD_TESTING:BOOL=OFF" "-DOTB_USE_6S:BOOL=OFF" "-DOTB_USE_CURL:BOOL=ON" \
	"-DOTB_USE_GLEW:BOOL=OFF" "-DOTB_USE_GLFW:BOOL=OFF" "-DOTB_USE_GLUT:BOOL=OFF" \
	"-DOTB_USE_GSL:BOOL=OFF" "-DOTB_USE_LIBKML:BOOL=OFF" "-DOTB_USE_LIBSVM:BOOL=ON" \
	"-DOTB_USE_MPI:BOOL=OFF" "-DOTB_USE_MUPARSER:BOOL=ON" "-DOTB_USE_MUPARSERX:BOOL=ON" \
	"-DOTB_USE_OPENCV:BOOL=ON" "-DOTB_USE_OPENGL:BOOL=OFF" "-DOTB_USE_OPENMP:BOOL=OFF" \
	"-DOTB_USE_QT:BOOL=OFF" "-DOTB_USE_QWT:BOOL=OFF" "-DOTB_USE_SIFTFAST:BOOL=ON" \
	"-DOTB_USE_SPTW:BOOL=OFF" "-DOTB_WRAP_PYTHON:BOOL=ON" "-DCMAKE_BUILD_TYPE=Release" \
	"-DOTB_USE_SHARK:BOOL=OFF" "-DBUILD_EXAMPLES:BOOL=OFF" \
	-DCMAKE_INSTALL_PREFIX="/usr/local/otb" -GNinja .. 1>/dev/null 2>&1 && \
	ninja install && \
	rm -rf /opt/otb
    cd /usr/local && tar cvfz otb.tar.gz otb && mv otb.tar.gz /content/.
    cd /content
fi
echo "Elapsed time: ${SECONDS} seconds"

# untar pre-compiled otb
echo ">> (3/4) Untar pre-compiled-otb	(expected duration: <1s)"
SECONDS=0
tar --strip-components 1 -xvf otb.tar.gz -C /usr 1>/dev/null 2>&1
echo "Elapsed time: ${SECONDS} seconds"

# finalize
echo ">> (4/4) Finalize python env (expected duration: <1min)"
SECONDS=0
# set variables for cars installation
export OTB_APPLICATION_PATH="/usr/lib/otb/applications"
# copy some files to avoid changing environment variables
cp /usr/lib/otb/python/otbApplication.py /usr/local/lib/python3.7/dist-packages/.
cp /usr/lib/otb/python/_otbApplication.so /usr/local/lib/python3.7/dist-packages/.
pip install --upgrade pip
pip install rasterio --no-binary rasterio
pip uninstall -y datascience
pip install --upgrade folium geojson
echo "Elapsed time: ${SECONDS} seconds"

