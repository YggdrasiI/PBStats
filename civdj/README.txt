== New project home ==

This component of PBStats has now its own repository:
https://github.com/civ4-mp/pbspy

=== PBSpy — A Civ4 Pitboss webinterface based on Django ===

This software communicates with the PB Mod component of PBStats and provides
functions to show the game status, a game log and to administrate the game.

== Usage ==
1. Visit civ.zulan.net/pbspy or install this software on your own server.
2. Create an account on the new page and login.
3. Start/load a PitBoss-game which implements the PB Mod and click on "Register new PitBoss".
4. Enter the host name, port and password (defined in pbSettings.json), of the PB game and click on "Register".
5. As admin, you had now access on three pages:
   • 'Game overview': Available for everyone.
   • 'Edit game' page: To change connection details and the data shown in the overview.
   • 'Manage game': Administration site of the Pitboss server. Save/Load your games here.


=== Installation of Django + Django packages with pip ===

== Dependencies ==
Here, we assume python3 >= python3.8.

sudo apt-get install python3-pip node-less
pip3 install Django==2.2
pip3 install --upgrade django-polymorphic django-debug-toolbar django-erroneous \
			 django-registration-redux django-crispy-forms \
			 django-floppyforms django-sendmail-backend django-static-precompiler \
			 django_bleach \
			 mysql-connector-python pytz setuptools six sqlparse


== Configuration ==
Copy civdj/settings_local.example.py to civdj/settings_local.py
and adapt it to your environment. (See https://docs.djangoproject.com/en/dev/ref/settings/ for details.)

Without changes PBSpy will use Sqlite 3 as database backend. Look into the Django docs
for other setups.


== First run (For Debug mode. Release mode requires more steps) ==

python3 manage.py migrate
python3 manage.py migrate static_precompiler
python3 manage.py compilestatic
python3 manage.py collectstatic
python3 manage.py createsuperuser


== Start ==
python3 manage.py runserver 0.0.0.0:8000


== Known issues ==

•  Error: ENOENT: no such file or directory, mkdir '[...]/static/COMPILED/pbspy/less/defaultstyle'
  while running 'python3 manage.py compilestatic'
  Solution: Create above folder manually (simply use 'mkdir -p' instead of 'mkdir')

• Error during migrate: 
  "There is no South database module 'south.db.sqlite3' for your database. Please either choose a supported database, check for SOUTH_DATABASE_ADAPTER[S] settings, or remove South from INSTALLED_APPS."
  => Could be solved by uninstalling south, i.e.
  sudo pip uninstall South

•	Error "'Settings' object has no attribute 'H:i:s'":
  ?
