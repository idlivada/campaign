import json
import os
import string
import random
from fabric.api import run, cd, env, settings, hide, sudo, prompt, local, put
from fabric.contrib.files import exists, upload_template
from fabric.utils import warn

env.hosts = ['root@162.243.102.184']

rootdir = "/var/www/"
homedir = rootdir + "campaign/"
apache_conf = '/etc/apache2/sites-enabled/campaign.conf'

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

        if not exists(apache_conf):
            domain = prompt('Enter domain (e.g. campaign.example.com):')
            apache_context = {'homedir' : homedir, 'servername' : domain}
            upload_template(filename='vhost.conf.jinja', destination=apache_conf, 
                            use_jinja=True, context=apache_context)
            
    apache_restart()

def install_mysql():

    # MySQL Install
    with settings(hide('warnings', 'stderr'), warn_only=True):
        result = sudo('dpkg-query --show mysql-server')
        
    root_password = None
    if result.failed is False:
        warn('MySQL is already installed')
    else:
        root_password = prompt('Please enter MySQL root password:')
        sudo('echo "mysql-server-5.0 mysql-server/root_password password ' \
                 '%s" | debconf-set-selections' % root_password)
        sudo('echo "mysql-server-5.0 mysql-server/root_password_again password ' \
                 '%s" | debconf-set-selections' % root_password)
        sudo('apt-get -y --no-upgrade install mysql-server', shell=False)

    # DB set up
    db_setup = prompt('Setup database [y/n]?')
    if db_setup == 'y':
        if root_password is None:
            root_password = prompt('Please enter MySQL root password:')
        dbname = prompt('Enter database name:')
        run_mysql_cmd('root', root_password, "CREATE DATABASE IF NOT EXISTS %s;" % dbname)
        username = prompt('Enter mysql username:')
        password = prompt('Enter mysql password:')
        run_mysql_cmd('root', root_password, 
                      "GRANT ALL PRIVILEGES ON %s.* TO '%s'@'localhost' IDENTIFIED BY '%s';" % 
                      (dbname, username, password))
    
    # Generate secrets file
    secret_path = homedir+"campaign/secret.py"
    if db_setup == 'y' and not exists(secret_path):
        secrets = {}
        secrets['tw_sid'] = prompt('Enter Twilio sid:')
        secrets['tw_token'] = prompt('Enter Twilio token:')
        secrets['tw_caller_id'] = prompt('Enter Twilio caller id (e.g. +15555555555):')
        print "The below number will be called when debugging rather than calling a member of Congress. Usually this is your phone number."
        secrets['debug_phone'] = prompt('Enter debug phone number (e.g. +15555555555):')
        secrets['BASE_URL'] = prompt('Enter base URL e.g. (http://campaign.example.com/:')
        secrets['SECRET_KEY'] = generate_secret_key()
        secrets['MYSQL_USER'] = username
        secrets['MYSQL_PASSWORD'] = password
        secrets['MYSQL_DB'] = dbname
        secrets['STATIC_ROOT'] = homedir + 'static/'
        secrets['sunlight_api_key'] = prompt('Sunlight Foundation API Key:')
        temp_path = 'secret.temp'
        f = open(temp_path, 'w')
        for key, value in secrets.iteritems():
            f.write('%s = %s' % (key, json.dumps(value))+'\n')
        f.close()
        put(temp_path, secret_path)
        os.remove(temp_path)
    # TODO: Sunlight Foundation API key

def generate_secret_key():
    return "".join([random.SystemRandom().choice(string.digits + string.letters + string.punctuation) for i in range(100)])

def run_mysql_cmd(username, password, command, database=""):
    run("echo \"%s\" | mysql -u %s -p%s %s" % (command, username, password, database))
    
def apache_restart():
    sudo("service apache2 restart")

def build_requirements():
    local("pip freeze > requirements.txt")
    

