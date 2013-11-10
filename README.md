tulsa-fire-dept-dispatches
==========================
The TFDD application helps firefighters save critical time receiving and using dispatch information. The current version allows any registered user to receive text messages or email regarding the units they need to know about.

Getting Started
---------------
```
mkvirtualenv tfdd
git clone git@github.com:jgmize/tulsa-fire-dept-dispatches.git
cd tulsa-fire-dept-dispatches
pip install -r requirements.txt
tfdd/manage.py syncdb
tfdd/manage.py syncdb (twice for user profile signal)
tfdd/manage.py migrate
tfdd/manage.py runserver
```
