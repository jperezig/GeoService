FROM mongo:latest

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		ca-certificates \
		python3-minimal \
		python3-pip \
	&& rm -rf /var/lib/apt/lists/*

COPY *.py /root/
COPY geoservice.conf /root/
COPY requirements.txt /root/
COPY *.csv /root/

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN pip3 install -r /root/requirements.txt
WORKDIR /root
RUN python3 -m unittest -v

EXPOSE 5000