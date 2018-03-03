FROM rastasheep/ubuntu-sshd

RUN apt-get update && \
    apt-get install -y gcc gdb libc6 libc6-dev
RUN apt-get install -y g++-multilib

RUN useradd -m thc18 -p thc18 && \
    usermod -d /home/thc18 thc18
RUN echo "thc18:thc18" | chpasswd
RUN echo "root:challSYSadm1n" | chpasswd

COPY chall.c /home/thc18/
COPY flag /home/thc18/

RUN gcc -m32 -fno-stack-protector -mpreferred-stack-boundary=2 /home/thc18/chall.c -o /home/thc18/chall
RUN chmod 600 /home/thc18/chall.c
RUN chmod 600 /home/thc18/flag
RUN chmod 755 /home/thc18/chall
RUN chmod u+s /home/thc18/chall



