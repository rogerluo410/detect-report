FROM python:3.9

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y \
        gcc \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libopenjp2-7-dev \
        libavformat-dev \
        libpq-dev \
        libgtk2.0-dev \
        libgtkglext1-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache  --no-cache-dir --upgrade -r requirements.txt --timeout 10000

# Install opencv
WORKDIR /
ENV OPENCV_VERSION="4.5.1"
RUN wget https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip \
&& unzip ${OPENCV_VERSION}.zip \
&& mkdir /opencv-${OPENCV_VERSION}/cmake_binary \
&& cd /opencv-${OPENCV_VERSION}/cmake_binary \
&& cmake -DBUILD_TIFF=ON \
  -DBUILD_opencv_java=OFF \
  -DWITH_CUDA=OFF \
  -DWITH_OPENGL=ON \
  -DWITH_OPENCL=ON \
  -DWITH_IPP=ON \
  -DWITH_TBB=ON \
  -DWITH_EIGEN=ON \
  -DWITH_V4L=ON \
  -DBUILD_TESTS=OFF \
  -DBUILD_PERF_TESTS=OFF \
  -DCMAKE_BUILD_TYPE=RELEASE \
  -DCMAKE_INSTALL_PREFIX=$(python3.9 -c "import sys; print(sys.prefix)") \
  -DPYTHON_EXECUTABLE=$(which python3.9) \
  -DPYTHON_INCLUDE_DIR=$(python3.9 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
  -DPYTHON_PACKAGES_PATH=$(python3.9 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
  .. \
&& make install \
&& rm /${OPENCV_VERSION}.zip \
&& rm -r /opencv-${OPENCV_VERSION}
RUN ln -s \
  /usr/local/python/cv2/python-3.9/cv2.cpython-37m-x86_64-linux-gnu.so \
  /usr/local/lib/python3.9/site-packages/cv2.so

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Create working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy contents
COPY . /usr/src/app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /usr/src/app
USER appuser

# Set environment variables
ENV HOME=/usr/src/app
ENV DETECT_SOURCE=rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov
ENV DETECT_KEYS=suitcase,person,skateboard
ENV DETECT_STREET=xx街道
ENV DETECT_INTERVAL=10
ENV DETECT_DEVICE=cpu
ENV REPORT_URL=https://longgang.yoyoyard.com/api/v1/events

CMD [ "python", "./main.py" ]