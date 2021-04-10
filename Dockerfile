# Start FROM Nvidia PyTorch image https://ngc.nvidia.com/catalog/containers/nvidia:pytorch
FROM nvcr.io/nvidia/pytorch:21.02-py3

# Install linux packages
RUN apt update && apt install -y zip htop screen libgl1-mesa-glx

# Install python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache -r requirements.txt gsutil notebook

# Create working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy contents
COPY . /usr/src/app

# Set environment variables
ENV HOME=/usr/src/app
ENV DETECT_SOURCE=rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov
ENV DETECT_KEYS=suitcase,person,skateboard
ENV DETECT_STREET=xx街道
ENV DETECT_INTERVAL=10
ENV DETECT_DEVICE=cpu
ENV REPORT_URL=https://longgang.yoyoyard.com/api/v1/events

CMD [ "python", "./main.py" ]