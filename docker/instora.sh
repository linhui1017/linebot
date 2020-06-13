cp ./oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm /tmp/
cp ./oracle-instantclient12.2-sqlplus-12.2.0.1.0-1.x86_64.rpm /tmp/
cp ./oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm /tmp/

# copy to ./bashrc
export NLS_LANG=AMERICAN_AMERICA.AL32UTF8
export ORACLE_HOME=/usr/lib/oracle/12.2/client64
export PATH=$PATH:$ORACLE_HOME/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME/lib
export TNS_ADMIN=$ORACLE_HOME/network/admin
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

sudo apt-get update \
    && apt-get install -y --no-install-recommends apt-utils \
    && apt-get install -y sqlite3 \
    && apt-get -y install alien libaio1 \
    && apt-get -y install locales locales-all \
    && alien -i /tmp/oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm \
    && alien -i /tmp/oracle-instantclient12.2-sqlplus-12.2.0.1.0-1.x86_64.rpm \
    && alien -i /tmp/oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm \
    && mkdir -p /opt/oracle/network \
    && ln -snf /usr/lib/oracle/12.2/client64 /opt/oracle \
    && ln -snf /etc/oracle /opt/oracle/network/admin \
    && apt-get clean && rm -rf /var/cache/apt/* /var/lib/apt/lists/* /tmp/* /var/tmp/*

mkdir -p $TNS_ADMIN
cp ./tnsnames.ora $ORACLE_HOME/network/admin/tnsnames.ora
