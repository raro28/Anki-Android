#!/usr/bin/python

# Copyright (c) 2010 norbert.nagold@gmail.com
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#

# This script updates the master file(s) for crowdin.net
# There seems to a bug in the upload of translation files; it's therefore deactivated

import pycurl
import StringIO
import sys

CROWDIN_KEY = ''
PROJECT_IDENTIFIER = 'ankidroid'

path = '../res/values/'

files = ['01-core', '02-strings', '03-dialogs', '04-network', '05-feedback', '06-statistics', '07-cardbrowser', '08-widget', '09-backup', '10-preferences', '11-arrays', '12-tutorial', '13-newfeatures];
alllang = ['ar', 'ca', 'cs', 'de', 'el', 'es-ES', 'fi', 'fr', 'hu', 'id', 'it', 'ja', 'ko', 'nl', 'pl', 'pt-PT', 'ro', 'ru', 'sr', 'sv-SE', 'tr', 'vi', 'zh-CN', 'zh-TW']

def uploadtranslation(language, filename, sourcefile):
	if language == 'zh-TW':
		pathlan = 'zh-rTW'
	elif language == 'zh-CN':
		pathlan = 'zh-rCN'
	else:
		pathlan = language[:2]

	path = '../res/values-' + pathlan + '/'
	filename = filename + '.xml'
#	if selu == 's':
#		filename = 'strings.xml'
#	elif selu == 'a':
#		filename = 'arrays.xml'
#	else:
#		filename = ''		
#		print "nothing to do"
	print 'Update of Translation '+language+' for '+filename
	if filename:
		if language:
			c = pycurl.Curl()
			fields = [('files['+filename+']', (c.FORM_FILE, path + sourcefile + '.xml')), ('language', language), ('auto_approve_imported','0')]
			c.setopt(pycurl.URL, 'http://crowdin.net/api/project/' + PROJECT_IDENTIFIER + '/upload-translation?key=' + CROWDIN_KEY)
			c.setopt(pycurl.HTTPPOST, fields)
			b = StringIO.StringIO()
			c.setopt(pycurl.WRITEFUNCTION, b.write) 
			c.perform()
			c.close()
			print b.getvalue()
		else:
			print 'no language code entered'

def updateMasterFile(selu):
	if selu == '12':
		filename = 'tutorial.csv'
		curPath = path + '../../assets/'
	else:
		filename = files[int(selu)-1] + '.xml'
		curPath = path
	if filename:	
		print 'Update of Master File ' + filename
		c = pycurl.Curl()
		fields = [('files['+filename+']', (c.FORM_FILE, curPath + filename))]
		c.setopt(pycurl.URL, 'http://crowdin.net/api/project/' + PROJECT_IDENTIFIER + '/update-file?key=' + CROWDIN_KEY)
		c.setopt(pycurl.HTTPPOST, fields)
		b = StringIO.StringIO()
		c.setopt(pycurl.WRITEFUNCTION, b.write) 
		c.perform()
		c.close()
		print b.getvalue()

try:
	c = open("crowdin_key.txt","r+")
	CROWDIN_KEY = c.readline();
	c.close()
except IOError as e:
	CROWDIN_KEY = raw_input("please enter your crowdin key or create \'crowdin_key.txt\': ")

sel = raw_input("update (m)aster file, update (t)ranslation or (r)efresh builds? ")

if sel == 'm':
	# Update Master Files:
	selu = raw_input("update 0(1)-core, 0(2)-strings, 0(3)-dialogs, 0(4)-network, 0(5)-feedback, 0(6)-statistics, 0(7)-cardbrowser, 0(8)-widget, 0(9)-backup, (10)-preferences, (11)-arrays, (12)-tutorial, (13)-newfeatures? ")
	if selu == 'all':
		for n in range(1, 13):
			updateMasterFile(n)
	else:
		updateMasterFile(selu)

elif sel == 't':
	# Update Translations:
	print 'still problems with crowding here'
	language = raw_input("enter language code: ")
	selu = raw_input("update 0(1)-core, 0(2)-strings, 0(3)-dialogs, 0(4)-network, 0(5)-feedback, 0(6)-statistics, 0(7)-cardbrowser, 0(8)-widget, 0(9)-backup, (10)-preferences, (11)-arrays, (13)-newfeatures? ")
	if selu == '12':
		return
	elif selu != 'all':
		defaultSource = files[int(selu)-1]
		sourcefile = raw_input("enter source file (default: " + defaultSource + "): ")
		if sourcefile == "":
			sourcefile = defaultSource
	elif language == 'all':
		for language in alllang:
			if selu == 'all':
				for s in files:
					uploadtranslation(language, s, s)
			else:
				uploadtranslation(language, files[int(selu)-1], s)
	elif selu == 'all':
		for s in files:
			uploadtranslation(language, s, s)
	else:
		uploadtranslation(language, files[int(selu)-1], sourcefile)

elif sel == 'r':
	# Update Translations:
	print "Force translation export"
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'http://crowdin.net/api/project/' + PROJECT_IDENTIFIER + '/export?&key=' + CROWDIN_KEY)
	b = StringIO.StringIO()
	c.setopt(pycurl.WRITEFUNCTION, b.write) 
	c.perform()
	c.close()
	print b.getvalue()
else:
	print "nothing to do"
