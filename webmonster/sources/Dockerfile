FROM php:7.0-apache

# set up web server
RUN mkdir /var/www/chall
# index file: public
COPY index.php /var/www/chall
# get flag file: public
COPY get_flag.php /var/www/chall
# functions file: private
COPY ext_func.php /usr/share
# flag: private
COPY flag /usr/share
# conf file - change root directory
COPY 000-default.conf /etc/apache2/sites-enabled

# install ssh
RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
COPY sshd_config /etc/ssh/

# add user and group
#RUN echo 'root:toor' | chpasswd
RUN useradd -m webmonster -p 99x@wMonstex && \
    usermod -d / webmonster

# setup ssh key authentication
COPY authorized_keys /etc/ssh/

# services
COPY commands.sh /root/

EXPOSE 22
CMD ["/bin/sh", "/root/commands.sh"]
