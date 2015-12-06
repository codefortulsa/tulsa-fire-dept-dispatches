tulsa-fire-dept-dispatches
==========================
The TFDD application helps firefighters save critical time receiving and using dispatch information. The current version allows any registered user to receive text messages or email regarding the units they need to know about.

Getting Started Locally
-----------------------
Sorry for the rough instructions ...
```
git clone git@github.com:codefortulsa/tulsa-fire-dept-dispatches.git
cd tulsa-fire-dept-dispatches
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env-dist .env
source .env
tfdd/manage.py syncdb (will error the first time)
tfdd/manage.py syncdb (twice for user profile signal)
tfdd/manage.py migrate
tfdd/manage.py fetch_dispatches
tfdd/manage.py runserver
```
