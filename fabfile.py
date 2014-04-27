from fabric.api import run, cd, env, settings, hide, sudo, prompt, local, put
from fabric.contrib.files import exists
from fabric.utils import warn

env.hosts = ['root@162.243.102.184']

rootdir = "/var/www/"
homedir = rootdir + "campaign/"

def install():
    run("apt-get install -y --no-upgrade python-pip build-essential git libmysqlclient-dev apache2 python-dev libapache2-mod-wsgi", shell=False)
    run("pip install --upgrade pip")
    run("pip install virtualenv")
    install_mysql()
    install_code()

def install_code():
    if not exists(homedir+".git/"):
        with cd(rootdir):
            run("git clone https://github.com/idlivada/campaign.git")

    with cd(homedir):
        run("git pull")
        run("virtualenv env --no-site-packages")
        run("source %s/env/bin/activate && pip install -r %s/requirements.txt" % (homedir, homedir))
        put("campaign/secret.py", homedir+"/campaign/")
        
    apache_restart()

def install_mysql():
    with settings(hide('warnings', 'stderr'), warn_only=True):
        result = sudo('dpkg-query --show mysql-server')

    if result.failed is False:
        warn('MySQL is already installed')
        return

    mysql_password = prompt('Please enter MySQL root password:')
    sudo('echo "mysql-server-5.0 mysql-server/root_password password ' \
                              '%s" | debconf-set-selections' % mysql_password)
    sudo('echo "mysql-server-5.0 mysql-server/root_password_again password ' \
                              '%s" | debconf-set-selections' % mysql_password)
    sudo('apt-get -y --no-upgrade install mysql-server', shell=False)

def apache_restart():
    sudo("service apache2 restart")

def build_requirements():
    local("pip freeze > requirements.txt")
    


