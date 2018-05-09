#!/usr/bin/env python

import sys
import os
import optparse

parser = optparse.OptionParser()
parser.add_option('-n', '--sitename', dest='sitename', help='Site name, i.e. site1,...site5')

# constant params.
db_user = "root"
db_pass = "elmismo"
wp_admin_user = "admin"
wp_admin_password = "admin"
wp_admin_email = "david.martinez@rmcoding.com"


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
print '----------------------------'
print "Let's create the database..."
os.system("mysql -u " + db_user + " -p" + db_pass + 
	" -Bse 'drop database if exists " + options.sitename + "; create database " + options.sitename + "; '")
# Now download a fresh copy of Wordpress and install it.
print '----------------------------'
os.system('wp core download --locale=es_ES')
# Create the wp-config
os.system('cp ../../config/wp-config.php .')
os.system('sed -i.bak s/wp_home_here/' + options.sitename + '/g wp-config.php')
os.system('sed -i.bak s/database_name_here/' + options.sitename + '/g wp-config.php')
os.remove('wp-config.php.bak')
# Install Wordpress
os.system('wp core install --url=' + options.sitename + '.dev --title="A Single Blank Site" --admin_user=' + 
	wp_admin_user + ' --admin_password=' + wp_admin_password + ' --admin_email=' + wp_admin_email)

# Set up a localhost into Nginx
os.system('cp ../../config/website.conf /usr/local/etc/nginx/servers/' + options.sitename + '.conf')
os.system('sed -i.bak s/website_url/' + options.sitename + '/g /usr/local/etc/nginx/servers/' + options.sitename + '.conf')
os.remove('/usr/local/etc/nginx/servers/' + options.sitename + '.conf.bak')
print '----------------------------'
print 'Sucess!.'