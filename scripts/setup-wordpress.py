#!/usr/bin/env python

import sys
import os
import optparse

parser = optparse.OptionParser()
parser.add_option('-n', '--sitename', dest='sitename', help='Site name, i.e. site1,...site5')

# constant params.
admin_user = 'admin'
admin_password = 'admin123'
admin_email = 'admin@example.com'

(options, args) = parser.parse_args()

if options.sitename is None:
	print '----------------------------'
	print 'Error!: Please provide a name for the site you want to set up. (site1, site2,..., site5)'
	print 'Good Bye'
	exit()

# remove current directory if exists
os.chdir('../src/')
os.system('rm -rf ' + options.sitename)
os.mkdir(options.sitename)
os.chdir(options.sitename)
# Let's create the database for this site.
os.system('docker exec -it mysql_5.7 mysql -u root -pelmismo -Bse "drop database if exists ' + options.sitename + '; create database ' + options.sitename + ';"')
# Now download a fresh copy of Wordpress and install it.
os.system('wp core download --locale=es_ES')
# Create the wp-config
os.system('cp ../../conf/wp-config.php .')
os.system('sed -i.bak s/wp_home_here/' + options.sitename + '/g wp-config.php')
os.system('sed -i.bak s/database_name_here/' + options.sitename + '/g wp-config.php')
os.remove('wp-config.php.bak')
# Install Wordpress
os.system('wp core install --url=' + options.sitename + '.local --title="A Single Blank Site" --admin_user=' + admin_user + ' --admin_password=' + admin_password + ' --admin_email=' + admin_email)