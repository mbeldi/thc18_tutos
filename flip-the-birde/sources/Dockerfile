FROM python:2.7.14-slim-jessie

COPY pycrypto-2.6.1 /pycrypto-2.6.1
COPY socket-aes.py /
RUN apt-get update && apt-get install -y gcc g++ make libffi-dev libssl-dev
RUN cd /pycrypto-2.6.1 && python setup.py install

EXPOSE 41222
CMD ["python", "/socket-aes.py"]
