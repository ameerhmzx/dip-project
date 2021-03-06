FROM python:3.8

RUN apt-get update \
      && apt-get install --no-install-recommends --no-install-suggests -y gnupg2 ca-certificates git build-essential libgl1-mesa-glx \
      && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/AlexeyAB/darknet.git && cd darknet \
      && make LIBSO=1 AVX=1 OPENMP=1 -j $(nproc) \
      && cd .. \
      && cp -r darknet /usr/local/bin \
      && cd .. && rm -rf darknet

COPY ds_requirements.txt requirements.txt
RUN pip install -r requirements.txt && rm -rf requirements.txt

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && rm -rf requirements.txt

WORKDIR /photos
