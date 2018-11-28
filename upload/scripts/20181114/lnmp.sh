#!/usr/bin/env bash
set -e
# Description: LNMP 环境一键安装脚本
# CreateDate: 2017/12/26
# LastModify: 2017/12/28
# Author： lei
#
# History:
#2017/12/28     增加多版本PHP支持
#               
SUPPORT_MAP=(
    nginx-1.13.8    
    nginx-1.12.2
    nginx-1.10.3
    nginx-1.8.1
    mysql-5.1.62
    php-5.6.30
    php-5.5.38
    php-5.4.40
    php-7.0.27
)
function containsElement(){
    local e match="$1"
    shift
    for e;do [[ "$e" == "$match" ]] && return 0;done
    echo "Error, $match version not support!"
    echo "----------------------------------------"
    echo "SUPPORT list:"
    for e;do echo $e;done
    echo "----------------------------------------"
    return 1
}
function show_help(){
    prompt="Usage: ./lnmp_install.sh [options]\n-h\t\t\tshow help\n-s\t\t\tshow version support\n-n 1.12.2\t\tinstall nginx-1.12.2\n-p 5.6.30\t\tinstall php-5.6.30\n-m 5.1.62\t\tinstall mysql-5.1.62\n-e\t\t\tinstall php extensions(redis/memcache)\n"
    echo -e $prompt
}
while getopts "n:p:m:ehs" arg
do
    case $arg in
        s)
            for i in ${SUPPORT_MAP[@]};do echo $i ;done
            ;;
        n)
            nginx_version=$OPTARG
            containsElement "nginx-${nginx_version}" ${SUPPORT_MAP[@]}
            echo "nginx version: ${nginx_version}"
            ;;
        p)
            php_version=$OPTARG
            containsElement "php-${php_version}" ${SUPPORT_MAP[@]}
            echo "php version: ${php_version}"
            ;;
        m)
            mysql_version=$OPTARG
            containsElement "mysql-${mysql_version}" ${SUPPORT_MAP[@]}
            echo "mysql version: ${mysql_version}"
            ;;
        e)
            php_extension_tag=1
            echo "install php_extension"
            ;;
        h)
            show_help
            ;;
        *)
            show_help
            ;;  
    esac
done
#Env define
Base_dir="/Data/apps"
NGINX_DIR=${Base_dir}"/nginx"
mysql_dir=${Base_dir}"/mysql"
php_dir=${Base_dir}"/php-fcgi"
source_url="http://raw.tansuotv.cn"
log_dir="/usr/local/src/log"
mkdir -p $log_dir
log_file=${log_dir}"/lnmp_install_$(date "+%Y%m%d%H%M").log"
#记录日志
function saveLog(){
    status=$2
    time_stm=`date "+[%Y%m%d %H:%M:%S]"`
    if [[ $status -eq 1 ]];then
        echo "$time_stm [ERROR] $1"
        echo "$time_stm [ERROR] $1" >> ${log_file}
        echo "More detail to check ${log_file}"
    elif [[ $status -eq 0 ]];then
        echo "$time_stm [SUCESS] $1"
        echo "$time_stm [SUCESS] $1" >> ${log_file}
    else
        echo "${time_stm} [INFO] $1"
        echo "${time_stm} [INFO] $1" >> ${log_file}
    fi
}
#依赖安装
function Dependency_install(){
    yum groupinstall "Development Tools" -y
    yum install pcre-devel ncurses-devel libxml2 \
        libxml2-devel  libzip zlib curl curl-devel openssl \
        openssl-devel mysql-devel gd gd-devel libpng libxslt-devel\
        libpng-devel libpng libpng-devel freetype freetype-devel -y
}
#Nginx 安装
function Nginx_install(){
    [[ ! -z $1 ]] && local version=$1 || return 1
    nginx_configure_log=${log_dir}"/nginx_configure.log"
    nginx_make_log=${log_dir}"/nginx_make.log"
    nginx_makeinstall_log=${log_dir}"/nginx_makeinstall.log"
    saveLog "nginx install......." 2
    cd /usr/local/src/
    groupadd nginx || echo "groupadd: group 'nginx' already exists"
    useradd -M -s /sbin/nologin -g nginx nginx || echo "useradd: user 'nginx' already exists"
    wget -O nginx.tgz ${source_url}/nginx/nginx-${version}.tar.gz >/dev/null 2>&1
    [[ -d ./_nginx/ ]] && rm -rf ./_nginx/* || mkdir -p ./_nginx/
    tar zxf nginx.tgz -C ./_nginx
    cd ./_nginx/nginx*/
    ./configure --prefix=${NGINX_DIR} \
        --with-http_stub_status_module \
        --with-pcre > $nginx_configure_log 2>&1 || { saveLog "nginx[configure]" 1; exit; }
    saveLog "nginx[configure]" 0
    make > $nginx_make_log 2>&1 || { saveLog "nginx[make]" 1; exit; }
    saveLog "nginx[make]" 0
    make install > $nginx_makeinstall_log 2>&1 || { saveLog "nginx[make install]" 1; exit; }
    saveLog "nginx[make]" 0
    rm -rf /usr/bin/nginx 
    ln -s ${NGINX_DIR}/sbin/nginx /usr/bin/nginx || saveLog "ln: creating symbolic link File exists"
    wget ${source_url}/conf/nginx.conf >/dev/null 2>&1
    cp -rf nginx.conf ${NGINX_DIR}/conf/
    rm -rf nginx.conf
    mkdir -p ${NGINX_DIR}/conf/vhosts/
    saveLog "nginx install OK" 0
    rm -rf /usr/local/src/_nginx /usr/local/src/nginx.tgz
    sleep 2
}
#Mysql 安装
function Mysql_install(){
    [[ ! -z $1 ]] && local version=$1 || return 1
    cmake_log="${log_dir}/mysql_cmake.log"
    make_log="${log_dir}/mysql_make.log"
    makeinstall_log="${log_dir}/mysql_makeinstall.log"
    saveLog "mysql install... ..." 2
    cd /usr/local/src/
    useradd -M -s /sbin/nologin mysql || echo "useradd: user 'mysql' already exists"
    wget -O mysql.tgz ${source_url}/mysql/mysql-${version}.tar.gz >/dev/null 2>&1
    [[ -d ./_mysql/ ]] && rm -rf ./_mysql/* || mkdir -p ./_mysql/
    tar zxf mysql.tgz -C ./_mysql
    cd ./_mysql/mysql*/
    ./configure --prefix=$mysql_dir \
        --with-mysqld-user=mysql \
        --with-unix-socket-path=$mysql_dir/mysql.sock > $cmake_log 2>&1  || { saveLog "mysql[cmake]" 1 ; exit;}
    saveLog "mysql[cmake]" 0
    make > $make_log 2>&1 || { saveLog "mysql[make]" 1 ; exit; }
    saveLog "mysql[make]" 0
    make install > $makeinstall_log 2>&1 || { saveLog "mysql[make install]" 1; exit;}
    saveLog "mysql[make install]" 0
    cp support-files/my-large.cnf /etc/my.cnf
    cp support-files/mysql.server /etc/init.d/mysqld
    chmod a+x /etc/init.d/mysqld
    $mysql_dir/bin/mysql_install_db --user=mysql
    chown -R mysql:root $mysql_dir
    saveLog "mysql install OK" 0
    rm -rf /usr/local/src/_mysql /usr/local/src/mysql.tgz
    sleep 2
}
#PHP 安装
function install_deps(){
    name=$1
    [[ ! -z $2 ]] && local args=$2 || local args=""
    cd /usr/local/src/
    [[ -d ./_${name} ]] && rm -rf ./_${name}/* || mkdir -p ./_${name}
    file ${name}.tgz | grep "gzip compressed data" >/dev/null 2>&1 && tar zxf ${name}.tgz -C ./_${name} || tar xf $name.tgz -C ./_${name}
    cd ./_${name}/${name}*
    local each_log="${log_dir}/${name}.log"
    ${php_dir}/bin/phpize >/dev/null 2>&1 || echo "$name installing ..."
    ./configure ${args} > ${each_log} 2>&1 && make > ${each_log} 2>&1 && make install > ${each_log} 2>&1 
    if [[ $name == "libmcrypt" ]];then
        /sbin/ldconfig
        ./configure --enable-ltdl-install > /dev/null 2>&1
    fi
    saveLog "$name install OK" 0
    cd /usr/local/src/
    rm -rf ./_${name} ./${name}.tgz
}
#PHP 依赖库安装
function php_dependence(){
    [[ ! -z $1 ]] && local version=$1 || local version="5"
    if [[ $version == "5" ]];then
        cd /usr/local/src/
        wget -O libiconv.tgz ${source_url}/php-${version}/libiconv-1.15.tar.gz >/dev/null 2>&1
        install_deps "libiconv" "--prefix=/usr/local/libiconv"  
        cd /usr/local/src/
        wget -O mhash.tgz ${source_url}/php-${version}/mhash-0.9.9.9.tar.gz >/dev/null 2>&1
        install_deps "mhash"
        cd /usr/local/src/
        wget -O libmcrypt.tgz ${source_url}/php-${version}/libmcrypt-2.5.7.tar.gz >/dev/null 2>&1
        install_deps libmcrypt      
        cd /usr/local/src/
        wget -O mcrypt.tgz ${source_url}/php-${version}/mcrypt-2.6.8.tar.gz >/dev/null 2>&1
        install_deps mcrypt
    fi
}
#PHP 5.4安装
function php_54_configure(){
    cd /usr/local/src/
    wget -O php.tgz ${source_url}/php-5/php-5.4.40.tar.gz >/dev/null 2>&1
    [[ -d ./_php/ ]] && rm -rf ./_php/* || mkdir -p ./_php/
    tar zxf php.tgz -C ./_php
    cd ./_php/php*
    ./configure --prefix=$php_dir  --with-config-file-path=$php_dir/etc/  --enable-fpm --enable-mbstring \
        --with-fpm-user=nginx \
        --with-fpm-group=nginx \
        --with-mysql=mysqlnd \
        --with-mysqli \
        --with-pdo-mysql \
        --with-curl \
        --with-mcrypt \
        --with-iconv \
        --with-freetype-dir \
        --with-jpeg-dir \
        --with-png-dir \
        --with-gd \
        --with-zlib \
        --with-libxml-dir=/usr \
        --enable-xml \
        --disable-rpath \
        --enable-magic-quotes \
        --enable-safe-mode \
        --enable-bcmath \
        --enable-shmop \
        --enable-sysvsem \
        --enable-inline-optimization \
        --enable-mbregex \
        --enable-ftp \
        --enable-gd-native-ttf \
        --with-openssl \
        --with-mhash \
        --enable-pcntl \
        --enable-sockets \
        --with-xmlrpc \
        --enable-zip \
        --enable-soap \
        --without-pear \
        --with-gettext \
        >> "${log_dir}/php_configure.log" 2>&1 || { saveLog "php[configure]" 1; exit; }
    saveLog "php[configure]" 0
    make >> "${log_dir}/php_make.log" 2>&1 || { saveLog "php[make]" 1; exit; }
    saveLog "php[make]" 0
    make install >> "${log_dir}/php_makeinstall.log" 2>&1 || { saveLog "php[make install]" 1; exit; }
    saveLog "php[make install]" 0
    wget ${source_url}/conf/php-fpm.conf > /dev/null 2>&1
    cp -rf php-fpm.conf $php_dir/etc/ && rm -rf php-fpm.conf
    wget ${source_url}/conf/php-fpm > /dev/null 2>&1
    cp -rf php-fpm  /etc/init.d/ && rm -rf php-fpm
    mkdir -p $php_dir/so
    ln -s $php_dir/sbin/* /usr/sbin/ || saveLog "ln: creating symbolic link File exists"
    ln -s $php_dir/bin/* /usr/bin/ || saveLog "ln: creating symbolic link File exists"
    [[ -f $php_dir/etc/php.ini ]] || cp php.ini-production $php_dir/etc/php.ini
}
function php_55_configure(){
    cd /usr/local/src/
    wget -O php.tgz ${source_url}/php-5/php-5.5.38.tar.gz >/dev/null 2>&1
    [[ -d ./_php/ ]] && rm -rf ./_php/* || mkdir -p ./_php/
    tar zxf php.tgz -C ./_php
    cd ./_php/php*
    ./configure --prefix=${php_dir} \
        --with-config-file-path=${php_dir}/etc \
        --enable-fpm \
        --enable-mbstring \
        --with-fpm-user=nginx \
        --with-fpm-group=nginx \
        --with-mysql=mysqlnd \
        --with-mysqli \
        --with-pdo-mysql \
        --enable-opcache=no \
        --with-curl \
        --with-mcrypt \
        --with-iconv \
        --with-freetype-dir \
        --with-jpeg-dir \
        --with-png-dir \
        --with-gd \
        --with-zlib \
        --with-libxml-dir=/usr \
        --enable-xml \
        --disable-rpath \
        --enable-magic-quotes \
        --enable-safe-mode \
        --enable-bcmath \
        --enable-shmop \
        --enable-sysvsem \
        --enable-inline-optimization \
        --enable-mbregex \
        --enable-ftp \
        --enable-gd-native-ttf \
        --with-openssl \
        --with-mhash \
        --enable-pcntl \
        --enable-sockets \
        --with-xmlrpc \
        --enable-zip \
        --enable-soap \
        --without-pear \
        --with-gettext \
        >> "${log_dir}/php_configure.log" 2>&1 || { saveLog "php[configure]" 1; exit; }
    saveLog "php[configure]" 0
    make >> "${log_dir}/php_make.log" 2>&1 || { saveLog "php[make]" 1; exit; }
    saveLog "php[make]" 0
    make install >> "${log_dir}/php_makeinstall.log" 2>&1 || { saveLog "php[make install]" 1; exit; }
    saveLog "php[make install]" 0
    wget ${source_url}/conf/php-fpm.conf > /dev/null 2>&1
    cp -rf php-fpm.conf $php_dir/etc/ && rm -rf php-fpm.conf
    wget ${source_url}/conf/php-fpm > /dev/null 2>&1
    cp -rf php-fpm  /etc/init.d/ && rm -rf php-fpm
    mkdir -p $php_dir/so
    ln -s $php_dir/sbin/* /usr/sbin/ || saveLog "ln: creating symbolic link File exists"
    ln -s $php_dir/bin/* /usr/bin/ || saveLog "ln: creating symbolic link File exists"
    [[ -f $php_dir/etc/php.ini ]] || cp php.ini-production $php_dir/etc/php.ini
}
#PHP 5.6安装
function php_56_configure(){
    cd /usr/local/src/
    wget -O php.tgz ${source_url}/php-5/php-5.6.30.tar.gz >/dev/null 2>&1
    [[ -d ./_php/ ]] && rm -rf ./_php/* || mkdir -p ./_php/
    tar zxf php.tgz -C ./_php
    cd ./_php/php*
    ./configure --prefix=${php_dir} \
        --with-config-file-path=${php_dir}/etc \
        --with-fpm-user=nginx \
        --with-fpm-group=nginx \
        --with-curl \
        --with-mysql=mysqlnd \
        --with-mysqli=mysqlnd \
        --with-pdo-mysql=mysqlnd \
        --with-libdir=lib64 \
        --with-iconv-dir=/usr/local \
        --with-freetype-dir \
        --with-jpeg-dir \
        --with-gettext \
        --with-pcre-regex \
        --with-png-dir \
        --with-libxml-dir=/usr \
        --enable-xml \
        --with-zlib \
        --enable-ftp \
        --enable-bcmath \
        --enable-shmop \
        --enable-sysvsem \
        --enable-mbregex \
        --enable-fpm \
        --enable-mbstring \
        --with-mcrypt \
        --with-xsl \
        --with-gd \
        --with-openssl \
        --with-mhash \
        --enable-pcntl \
        --enable-sockets \
        --with-xmlrpc \
        --enable-zip \
        --enable-soap \
        --without-pear \
        --enable-opcache=no >> "${log_dir}/php_configure.log" 2>&1 || { saveLog "php[configure]" 1; exit; }
    saveLog "php[configure]" 0
    make >> "${log_dir}/php_make.log" 2>&1 || { saveLog "php[make]" 1; exit; }
    saveLog "php[make]" 0
    make install >> "${log_dir}/php_makeinstall.log" 2>&1 || { saveLog "php[make install]" 1; exit; }
    saveLog "php[make install]" 0
    wget ${source_url}/conf/php-fpm.conf > /dev/null 2>&1
    cp -rf php-fpm.conf $php_dir/etc/ && rm -rf php-fpm.conf
    wget ${source_url}/conf/php-fpm > /dev/null 2>&1
    cp -rf php-fpm  /etc/init.d/ && rm -rf php-fpm
    mkdir -p $php_dir/so
    ln -s $php_dir/sbin/* /usr/sbin/ || saveLog "ln: creating symbolic link File exists"
    ln -s $php_dir/bin/* /usr/bin/ || saveLog "ln: creating symbolic link File exists"
    [[ -f $php_dir/etc/php.ini ]] || cp php.ini-production $php_dir/etc/php.ini
}
#PHP 5 扩展安装
function php_5_extension(){
    #APC install
    cd /usr/local/src/
    wget -O APC.tgz ${source_url}/php-5/APC-3.0.1.tar.gz  >/dev/null 2>&1
    install_deps "APC" "--with-php-config=${php_dir}/bin/php-config"
    cp $php_dir/lib/php/extensions/no-*/apc.so $php_dir/so && echo "extension=apc.so" >> $php_dir/etc/php.ini
    #Memcache install
    cd /usr/local/src/
    wget -O memcache.tgz ${source_url}/php-5/memcache-2.2.7.tgz  >/dev/null 2>&1
    install_deps "memcache" "--with-php-config=${php_dir}/bin/php-config"
    cp $php_dir/lib/php/extensions/no-*/memcache.so $php_dir/so && echo "extension=memcache.so" >> $php_dir/etc/php.ini
    cd /usr/local/src/
    wget -O redis.tgz ${source_url}/php-5/redis-php-2.2.7.tar.gz  >/dev/null 2>&1
    install_deps redis "--with-php-config=${php_dir}/bin/php-config"
    cp $php_dir/lib/php/extensions/no-*/redis.so $php_dir/so && echo "extension=redis.so" >> $php_dir/etc/php.ini
}
#PHP 安装
function Php_install(){
    [[ ! -z $1 ]] && local version=$1 || return 1
    cd /usr/local/src/
    php_dependence $(echo $version|awk -F "." '{print $1}')
    if [[ $version == "5.6.30" ]];then
        php_56_configure
    elif [[ $version == "5.5.38" ]]; then
        php_55_configure
    elif [[ $version == "5.4.40" ]]; then
        php_54_configure
    else
        echo "php-$version not support!"
        exit 1
    fi
    echo "Modify php.ini......"
    sed -i 's/upload_max_filesize = 2M/upload_max_filesize = 10M/g' $php_dir/etc/php.ini
    sed -i 's/;date.timezone =/date.timezone = PRC/g' $php_dir/etc/php.ini
    sed -i 's/; cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/g' $php_dir/etc/php.ini
    sed -i 's/; cgi.fix_pathinfo=0/cgi.fix_pathinfo=0/g' $php_dir/etc/php.ini
    sed -i 's/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/g' $php_dir/etc/php.ini
    sed -i 's/max_execution_time = 30/max_execution_time = 300/g' $php_dir/etc/php.ini
    sed -i 's/register_long_arrays = On/;register_long_arrays = On/g' $php_dir/etc/php.ini
    sed -i 's/magic_quotes_gpc = On/;magic_quotes_gpc = On/g' $php_dir/etc/php.ini
    sed -i 's#; extension_dir = "./"#extension_dir = "'$php_dir'/so"#g' $php_dir/etc/php.ini
    sed -i 's#error_reporting = E_ALL & ~E_DEPRECATED#error_reporting = E_COMPILE_ERROR|E_RECOVERABLE_ERROR|E_ERROR|E_CORE_ERROR#g' $php_dir/etc/php.ini
    sed -i 's#;error_log = php_errors.log#error_log = '$php_dir'/var/log/php_errors.log#g' $php_dir/etc/php.ini
}
rpm -q wget >/dev/null 2>&1 || yum -y install wget >/dev/null 2>&1
if [[ ! -z ${nginx_version} ]] ;then
    Dependency_install
    Nginx_install $nginx_version
fi
if [[ ! -z $mysql_version ]] ;then
    Mysql_install $mysql_version
fi
if [[ ! -z $php_version ]] ;then
    Php_install $php_version
fi
if [[ ! -z $php_extension_tag ]];then
    php_5_extension
fi