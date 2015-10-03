### About this project
When it comes to getting your voice heard by Congress, it is often said that an in-person visit to your member of Congress, is as influential as 10 calls to their office, or 100 written letters, or 1,000 emails.  

While visiting your elected officials is not always feasible, picking up the phone and giving them a call is very easy to do.  However, many people resort to emails, or even worse, doing nothing despite deeply caring about an issue.

This project makes is easy for an advocacy organization to quickly and easily launch a call campaign among a large member base on a specific set of designated issues.  Using this app, you can enable your audience to easily identify their member of the House or Senate, and be connected with them via phone by them simply clicking a button in their web browser.

### Requirements
In order to use the out of the box deployment, you need to have the following libraries pre-iinstalled
* Python 2.7 (other versions should work with some modifications)
* fabric
* Jinja2

Other miscellaneous libraries used but not required (see requirements.txt for full listing).  
* Django 1.6
* Twilio API
* Sunlight Foundation API
* MySQL
* South
* Docutils
* virtualenv
* apache2

### Pre-Deployment

*Provision your deployment (preferably Ubuntu)* (tested on 14.04 LTS x64 but should works on other versions) where you would like the app to run in production with ssh access enabled. Recommend using Digital Ocean for a quick option here.

*Get a Twilio Account*. Write down the SID and Token for this application.  You will need it in the set up process.  You will also need to fund your account to be able to call external parties such as members of Congress, so the free account will not suffice.

*Get a Sunlight Foundation API Key*.  You will need this in the set up process.

*Get a Texas A&M University Geocoding API Key (TAMU)*. https://geoservices.tamu.edu/.  By default, the application will properly attribute their service so you can register as a partner, and if approved get unlimited API calls.

*Set up DNS*.  Create a domain or subdomain with an A record pointing to the IP of the production box you provisioned.

### Deployment
Deploying to product is very easy. Simply follow the below steps:

#### Fabric Configuration
Edit fabfile.py and set the env.hosts:
```python
env.hosts = ['root@YOUR_PRODUCTION_HOST_HERE']
```
You can optionally customize the other variable and paths below env.hosts, but this should not be required if you are using the default Ubuntu settings.

#### Installing Requirements, Deploying Code, and Setting up Database
Next, On your shell, run the following:
```shell
$ fab install
```
Follow the instructions and prompts.  It's recommended that you setup the database when prompted on the initial deployment as well.

#### Populating the Database
Once you have installed the app on your deployment server, you need to populate the database initially. To do so, ssh into your deployment machine, and go to the home directory of your app (as specified by the homedir variable in your fabfile), set your PYTHONPATH, initialize virtualenv, synchronize your database using Django, then migrate your app using South.  Example:
```shell
$ cd /var/www/campaign/
$ export PYTHONPATH=$(pwd)
$ source env/bin/activate
$ python campaign/manage.py syncdb
$ python campaign/manage.py migrate core
```

You should now see your app running in your web browser.

You can now go and create your first campaign via the django admin interface /admin/ in your browser.

### Going Live
When you are ready to go live. Here's follow the Django deployment checklist https://docs.djangoproject.com/en/dev/howto/deployment/checklist/ to set proper security settings such as removing it from debug mode.
