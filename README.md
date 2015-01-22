Sal - JSS Import
================

Pulls data from Casper 9 to a Postgres database for purpose of importing into [WebHelpDesk](http://www.webhelpdesk.com/).

How To Use The Script:
------

jsspull.py supports three options:

* --dbprefs "path/to/com.github.nmcspadden.prefs.json"
	* This can be any JSON file that contains the appropriate settings like in the example prefs.json file.  
	* Defaults to "com.github.nmcspadden.prefs.json" in the same directory as the script.
* --jssprefs "path/to/com.github.sheagcraig.python-jss.plist"
	* The Plist file that contains access information for python-jss.  See the [python-jss wiki](https://github.com/sheagcraig/python-jss/wiki/Configuration#supplying-credentials-to-the-jssprefs-object) for details. 
	* Defaults to "com.github.sheagcraig.python-jss.plist" in the same directory as the script.
* -v, --verbose
	* Adds extra output so you can see the steps being taken by the script.

`./jsspull.py --dbprefs "com.github.nmcspadden.prefs.json" --jssprefs "com.github.sheagcraig.python-jss.plist"`

Background
-----

WebHelpDesk 12.1.0 has Casper 9 integration, but in my testing, it didn't work properly - it only accepts Computers and not Mobile Devices.  Since I use Casper as an iOS MDM only, this isn't very useful for me.  I wanted a way to pull all the data from Casper and import it into WHD automatically, on a regular schedule.

This tool has now been revised to work with Docker, although it should still work on its own without any changes. 

This script is intended to function with WebHelpDesk's Discovery Connections, which allows WHD to pull information from a flat database to add to its asset inventory.

To use this tool to incorporate Casper 9 into WHD, you'll need a database already set up that you have access to.  

If you are using Docker (the intended and recommended usage), I recommend using my [JSSImport container](https://github.com/nmcspadden/docker-jssimport), which incorporates this already, and is designed to be easily linked to a Postgres-database.

The script now takes care of creating the database table "casperimport" (although you could change this by editing the sql command inside the jsspull.py file).  The table should contain all the fields you want to pull, which in this case are:

1. id - int(11) - no NULL - primary key
2. serial - longtext 
3. name - longtext
4. model - longtext
5. ios_version - longtext
6. ipaddress - longtext
7. macaddress - longtext
8. bluetooth - longtext
9. capacity - longtext
10. username - longtext
11. email - longtext
12. asset_tag - longtext

You'll also need to edit your access file, which contains the host, database, username, and password.  This file should be called "com.github.nmcspadden.prefs.json", and is typically located in the same directory of the script.  The prefs file contains this:

	"postgres_host" : "db",
	"postgres_user" : "saldbadmin",
	"postgres_db" : "sal",
	"postgres_password" : "password"

You'll also need to edit your the python-jss access plist to allow for access to your JSS via API.  It's recommended you set up an API-access only user account and change settings in the plist accordingly.

If you are using the Docker container, these settings can be changed via environment variables specified at runtime.  You will not need to modify these files to use with Docker.

I recommend you test out your connection in the python interpreter before running the script.

If you are NOT using Docker:
-------

You need to install [python-jss](https://github.com/sheagcraig/python-jss) on the host you want to run the script on, and will need to provide access to an existing Postgres database.