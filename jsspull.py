#!/usr/bin/env python

import sys
try:
	import MySQLdb
except ImportError:
	print "No MySQLdb!"
	sys.exit(1)

try:
	import jss
except ImportError:
	print "NO jss!"
	sys.exit(1)

## Code taken from http://code.activatestate.com/recipes/577081-humanized-representation-of-a-number-of-bytes/
def GetHumanReadable(size, precision=2):
	suffixes=['KB','MB','GB','TB']
	suffixIndex = 0
	while size > 1024:
		suffixIndex += 1 #increment the index of the suffix
		size = size/1024.0 #apply the division
	return "%.*f %s"%(precision,size,suffixes[suffixIndex])

## Original code

## Download a list of all mobile devices from the JSS API as an ElementTree
def getDeviceListFromJSS():
	print "stuff"


mysql_host = "host"
mysql_user = "user"
mysql_password = "password"
mysql_db = "db"

## Update the data in the SQL table
def SubmitSQLForDevice(thisDevice, conn, j):
		device_name = thisDevice['device_name']
		device_username = thisDevice['username']
		
		sql = """INSERT INTO casperimport (id, serial, name, model, ios_version, ipaddress, macaddress, bluetooth, capacity, username, email, asset_tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE serial=VALUES(serial), name=VALUES(name), model=VALUES(model), ios_version=VALUES(ios_version), ipaddress=VALUES(ipaddress), macaddress=VALUES(macaddress), bluetooth=VALUES(bluetooth), capacity=VALUES(capacity), username=VALUES(username), email=VALUES(email), asset_tag=VALUES(asset_tag)"""
		
		sql_values=[ thisDevice['id'], thisDevice['serial_number'], (device_name or u'').encode('unicode_escape').decode().encode('latin1'), thisDevice['modelDisplay'], j.MobileDevice(thisDevice['id']).findtext('general/os_version'), j.MobileDevice(thisDevice['id']).findtext('general/ip_address'), thisDevice['wifi_mac_address'], j.MobileDevice(thisDevice['id']).findtext('general/bluetooth_mac_address'), GetHumanReadable(int(j.MobileDevice(thisDevice['id']).findtext('general/capacity'))), (device_username or u'').encode('unicode_escape').decode().encode('latin1'), j.MobileDevice(thisDevice['id']).findtext('location/email_address'), j.MobileDevice(thisDevice['id']).findtext('location/asset_tag') ]
		
		cursor = conn.cursor()
		cursor.execute(sql, sql_values)
		cursor.close()

## Where the magic happens
def main():
	try:
		conn = MySQLdb.connect(mysql_host, mysql_user, mysql_password, mysql_db)
	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	
	try:
		jss_prefs = jss.JSSPrefs("com.github.sheagcraig.python-jss.plist")
		j = jss.JSS(jss_prefs)
	except:
		print "Couldn't access preferences file."
		sys.exit(1)

	deviceList = j.MobileDevice()

	for device in deviceList:
		SubmitSQLForDevice(device, conn, j)
	
	conn.commit()
	
#Time for magic to happen.
main()