Sal - JSS Import
================

Pulls data from Casper 9 to Sal DB for purpose of importing into WebHelpDesk

WebHelpDesk 12.1.0 has Casper 9 integration, but in my testing, it didn't work properly - it only accepts Computers and not Mobile Devices.  Since I use Casper as an iOS MDM only, this isn't very useful for me.  I wanted a way to pull all the data from Casper and import it into WHD automatically, on a regular schedule.

This tool has now been revised to work with Docker, although it should still work on its own without any changes. 

I already make use of [Sal with WHD](https://github.com/nmcspadden/Sal-WHDImport), so I have a ready Postgres db that is already populated with Sal data.  

To use this tool to incorporate Casper 9 into WHD, you'll need a database already set up that you have access to.  If you are using Docker, I recommend using my [SalWHD container](https://github.com/nmcspadden/salWHD), which incorporates this already, and is designed to be easily linked to a Postgres-database.

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

You'll also need to edit your access file, which contains the host, database, username, and password.  This file should be called "com.github.nmcspadden.prefs.json", and is typically located in the same directory of the script.  (You'd need to modify jsspull.py if you want to put it somewhere else).  The prefs file contains this:

	"postgres_host" : "db",
	"postgres_user" : "saldbadmin",
	"postgres_db" : "sal",
	"postgres_password" : "password"

If you are using the Docker container, the only thing you need to change is the password.

I recommend you test out your connection in the python interpreter before running the script.

If you are NOT using Docker:
-------

You need to install [python-jss](https://github.com/sheagcraig/python-jss) on the host you want to run the script on.  You'll also need to create the "com.github.sheagcraig.python-jss.plist" file and place it in the appropriate location. This script was tested on a CentOS host, so it assumes that the plist is in the same directory as the script - you may have to make adjustments to jsspull.py if you intend to move it elsewhere.

