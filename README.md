Sal - JSS Import
================

Pulls data from Casper 9 to Sal DB for purpose of importing into WebHelpDesk

WebHelpDesk 12.1.0 has Casper 9 integration, but in my testing, it didn't work properly.  I wanted a way to pull all the data from Casper and import it into WHD automatically, on a regular schedule.

I already make use of [Sal with WHD](https://github.com/nmcspadden/Sal-WHDImport), so I have a ready MySQL db that is already populated with data.  

It was easy to extend the db for more functionality.

To use this tool to incorporate Casper 9 into WHD, you'll need a MySQL database already set up that you have access to.  

First, you need to install [python-jss](https://github.com/sheagcraig/python-jss) on the host you want to run the script on.  You'll also need to create the "com.github.sheagcraig.python-jss.plist" file and place it in the appropriate location. This script was built to run on a CentOS host, so it assumes that the plist is in the same directory as the script.

Second, you need to create a mysql table named "casperimport" (although you could change this by editing the sql command inside the jsspull.py file).  The mysql table should contain all the fields you want to pull, which in this case are:

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

All fields except the id tag should allow for NULL entries, and the id column should be the primary key.

Once you have the table setup, you'll need to edit jsspull.py with your information in the mysql variable fields:

mysql_host = "host"  
mysql_user = "user"  
mysql_password = "password"  
mysql_db = "db"  

I recommend you test out your connection in the python interpreter before running the script.