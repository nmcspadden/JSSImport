#!/usr/bin/env python

try:
	import MySQLdb
except ImportError:
	print "No MySQLdb!"
	sys.exit(1)

try:
	import xmltodict
except ImportError:
	print "NO xmltodict!"
	sys.exit(1)

import httplib
import base64
import sys

## Code taken from http://code.activatestate.com/recipes/577081-humanized-representation-of-a-number-of-bytes/
def GetHumanReadable(size, precision=2):
	suffixes=['KB','MB','GB','TB']
	suffixIndex = 0
	while size > 1024:
		suffixIndex += 1 #increment the index of the suffix
		size = size/1024.0 #apply the division
	return "%.*f %s"%(precision,size,suffixes[suffixIndex])

## Code taken from JAMF's updateDeviceInventory.py - https://jamfnation.jamfsoftware.com/viewProductFile.html?id=209&fid=571
#JSS data
jss_host = "jss" #Example: 127.0.0.1 if run on server
jss_port = 8443
jss_path = "" #Example: "jss" for a JSS at https://www.company.com:8443/jss
jss_username = "name"
jss_password = "password"

## Create a header for the request
def getAuthHeader(u,p):
	# Compute base64 representation of the authentication token.
	token = base64.b64encode('%s:%s' % (u,p))
	return "Basic %s" % token

## Download a list of all mobile devices from the JSS API as an ElementTree
def getDeviceListFromJSS():
	print "Getting device list from the JSS..."
	headers = {"Authorization":getAuthHeader(jss_username,jss_password),"Accept":"application/xml"}
	try:
		conn = httplib.HTTPSConnection(jss_host,jss_port)
		conn.request("GET",jss_path + "/JSSResource/mobiledevices",None,headers)
		data = conn.getresponse().read()
		conn.close()
		return xmltodict.parse(data)
	except httplib.HTTPException as inst:
		print "Exception: %s" % inst
		sys.exit(1)
	except ValueError as inst:
		print "Exception decoding JSON: %s" % inst
		sys.exit(1)

## Original code
mysql_host = "mysql"
mysql_user = "user"
mysql_password = "password"
mysql_db = "db"

def getDeviceFromJSS(deviceID):
#	print "Getting device from the JSS..."
	headers = {"Authorization":getAuthHeader(jss_username,jss_password),"Accept":"application/xml"}
	try:
		conn = httplib.HTTPSConnection(jss_host,jss_port)
		conn.request("GET",jss_path + "/JSSResource/mobiledevices/id/" + deviceID,None,headers)
		data = conn.getresponse().read()
		conn.close()
		return xmltodict.parse(data)
	except httplib.HTTPException as inst:
		print "Exception: %s" % inst
		sys.exit(1)
	except ValueError as inst:
		print "Exception decoding XML: %s" % inst
		sys.exit(1)

## Update the data in the SQL table
def SubmitSQLForDevice(thisDevice, conn):
		device_name = thisDevice['mobile_device']['general']['name']
		device_username = thisDevice['mobile_device']['location']['username']
		
		sql = """INSERT INTO casperimport (id, serial, name, model, ios_version, ipaddress, macaddress, bluetooth, capacity, username, email, asset_tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE serial=VALUES(serial), name=VALUES(name), model=VALUES(model), ios_version=VALUES(ios_version), ipaddress=VALUES(ipaddress), macaddress=VALUES(macaddress), bluetooth=VALUES(bluetooth), capacity=VALUES(capacity), username=VALUES(username), email=VALUES(email), asset_tag=VALUES(asset_tag)"""
		
		sql_values=[ thisDevice['mobile_device']['general']['id'], thisDevice['mobile_device']['general']['serial_number'], (device_name or u'').encode('unicode_escape').decode().encode('latin1'), thisDevice['mobile_device']['general']['modelDisplay'], thisDevice['mobile_device']['general']['os_version'], thisDevice['mobile_device']['general']['ip_address'], thisDevice['mobile_device']['general']['wifi_mac_address'], thisDevice['mobile_device']['general']['bluetooth_mac_address'], GetHumanReadable(int(thisDevice['mobile_device']['general']['capacity'])), (device_username or u'').encode('unicode_escape').decode().encode('latin1'), thisDevice['mobile_device']['location']['email_address'], thisDevice['mobile_device']['general']['asset_tag'] ]
		
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
	
	deviceList = getDeviceListFromJSS()
	numDevices = len(deviceList)
	idList = list()
	for device in deviceList['mobile_devices']['mobile_device']:
		idList.append(device['id'])
		#We have to do this because the JSS doesn't report all the device info for a mass-dump
	
	index = 0
	print "Polling API for devices..."
	for id in idList:
		percent = "%.2f" % (float(index) / float(numDevices) / 10)
		print str(percent) + "% Complete -"
		SubmitSQLForDevice(getDeviceFromJSS(id), conn)
		index += 1
	print "100.00% Complete"
	conn.commit()
	
#Time for magic to happen.
main()