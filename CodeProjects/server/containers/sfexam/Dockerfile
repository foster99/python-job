FROM ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive
# Install Apache
RUN apt-get update && apt-get -y upgrade && apt-get -y install software-properties-common make curl gnupg python python3 build-essential
RUN apt-get update && apt-get install -y language-pack-en-base && export LC_ALL=en_US.UTF-8 && export LANG=es_ES.UTF-8 && add-apt-repository ppa:ondrej/php && apt-get update
RUN apt-get update && apt-get install -y apache2 libapache2-mod-php7.3
COPY config/virtualhost.dev.conf /etc/apache2/sites-available/000-default.conf

# Install PHP
RUN apt-get update && apt-get install -y php7.3 php7.3-mysql php7.3-intl php7.3-dom php7.3-zip \
                       php7.3-sqlite3 php7.3-mbstring php7.3-curl php7.3-gd php7.3-iconv \
                       php7.3-imagick  php7.3-json php7.3-pdo php7.3-mysqli php7.3-xml \
                       php7.3-phar php7.3-tokenizer php7.3-simplexml php7.3-mongodb php7.3-xdebug
RUN a2enmod rewrite
RUN a2enmod php7.3

# Set PHP configs
RUN sed -ie 's/memory_limit\ =\ 128M/memory_limit\ =\ -1/g' /etc/php/7.3/apache2/php.ini
RUN sed -ie 's/max_execution_time\ =\ 30/max_execution_time\ =\ 600/g' /etc/php/7.3/apache2/php.ini
RUN sed -ie 's/\;date\.timezone\ =/date\.timezone\ =\ Europe\/Madrid/g' /etc/php/7.3/apache2/php.ini
RUN sed -ie 's/upload_max_filesize\ =\ 2M/upload_max_filesize\ =\ 200M/g' /etc/php/7.3/apache2/php.ini
RUN sed -ie 's/post_max_size\ =\ 8M/post_max_size\ =\ 800M/g' /etc/php/7.3/apache2/php.ini

RUN sed -ie 's/memory_limit\ =\ 128M/memory_limit\ =\ -1/g' /etc/php/7.3/cli/php.ini
RUN sed -ie 's/max_execution_time\ =\ 30/max_execution_time\ =\ 600/g' /etc/php/7.3/cli/php.ini
RUN sed -ie 's/\;date\.timezone\ =/date\.timezone\ =\ Europe\/Madrid/g' /etc/php/7.3/cli/php.ini
RUN sed -ie 's/\allow_url_fopen\ =/allow_url_fopen\ =\ 1/g' /etc/php/7.3/cli/php.ini
RUN sed -ie 's/\default_socket_timeout\ =/default_socket_timeout\ =\ 172800/g' /etc/php/7.3/cli/php.ini

RUN echo 'xdebug.remote_autostart = 1' >> /etc/php/7.3/mods-available/xdebug.ini
RUN echo 'xdebug.remote_connect_back=1' >> /etc/php/7.3/mods-available/xdebug.ini
RUN echo 'xdebug.remote_enable = 1' >> /etc/php/7.3/mods-available/xdebug.ini
RUN echo 'xdebug.remote_host = host.docker.internal' >> /etc/php/7.3/mods-available/xdebug.ini
RUN echo 'xdebug.remote_log = /tmp/xdebug_remote.log' >> /etc/php/7.3/mods-available/xdebug.ini
RUN echo 'xdebug.remote_port = 9006' >> /etc/php/7.3/mods-available/xdebug.ini

RUN sed -ie '1iServerName\ localhost\ ' /etc/apache2/apache2.conf

# Install Locals
RUN apt-get update && apt-get install -y mysql-client git locales
RUN locale-gen es_ES.utf8
RUN touch /etc/default/locale && chmod 755 /etc/default/locale
RUN echo "LC_COLLATE=es_ES.UTF8" > /etc/default/locale && \
    echo "LC_CTYPE=es_ES.UTF8" > /etc/default/locale && \
    echo "LANG=es_ES.UTF8" > /etc/default/locale && \
    echo "LC_ALL=es_ES.UTF8" > /etc/default/locale

# Install YARN
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install yarn -y

# Install Composer
RUN curl -sS -o /usr/local/bin/composer https://getcomposer.org/download/1.9.3/composer.phar && \
    chmod +x /usr/local/bin/composer

# Configuration & App Instalation & Permissions
COPY config/installation-dev.sh /
RUN chmod 777 /installation-dev.sh

# Set WORKING DIR TO /var/www
WORKDIR /var/www

# Other Dockerfile directives are still valid
EXPOSE 22 80
ENTRYPOINT ["/installation-dev.sh"]