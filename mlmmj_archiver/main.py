#!/usr/bin/env python
## @package mlmmj_archiver
#
#  Wrapper around hypermail to generate mlmmj HTML archives. The script is configured through a YAML file which makes it easy to manage more than one mlmmj list.
#  This script was created from Martin Leopold's update-archive.sh script. You can find the original version on his webpage: http://www.leopold.dk/~martin/mlmmj-scripts.html
import argparse
import yaml
import os

## Parses the YAML file and creates the config for every list defined.
#
class Config(object):
	
	def __init__(self, args):
		self.configfile = open(args.config, "r")
		self.lists = yaml.load(self.configfile)
		self.configfile.close()

		# Looping through the defined lists in the config file.
		for list in self.lists.keys():

			self.lists[list]['options']['parsed_output'] = ''

			if self.lists[list].has_key('options'):
				# If the list defines custom output options
				if self.lists[list]['options'].has_key('output'):
					# Create the environment variables for hypermail according to the output options
					for output in self.lists[list]['options']['output']:
						if output == 'showreplies':
							self.lists[list]['options']['parsed_output'] = self.lists[list]['options']['parsed_output'] + 'HM_SHOWREPLIES=1 '
						else:
							print "Unkown option '%s' in %s list!" % ( output, list )
							exit(1)
			else:
				self.lists[list]['options'] = { }
			
			# Do we want to generate extra index?
			if self.lists[list]['options'].has_key('index'):
				if self.lists[list]['options']['index'] == 'monthly':
					self.lists[list]['options']['parsed_output'] = self.lists[list]['options']['parsed_output'] + 'HM_MONTHLY_INDEX=1'
				elif self.lists[list]['options']['index'] == 'yearly':
					self.lists[list]['options']['parsed_output'] = self.lists[list]['options']['parsed_output'] + 'HM_YEARLY_INDEX=1'
				else:
					print "Unkown index option '%s' in %s list!" % ( self.lists[list]['options']['index'], list )

			# Set some default values if they're not defined by the config file
			if not self.lists[list]['options'].has_key('ordering'):
				self.lists[list]['options']['ordering'] = 'thread'
			if not self.lists[list]['options'].has_key('threadlevels'):
				self.lists[list]['options']['threadlevels'] = 100
			if not self.lists[list]['options'].has_key('lang'):
				self.lists[list]['options']['lang'] = 'en'
			
			# Create the target archive directory if it does not exist.
			if not os.path.exists(self.lists[list]['archive']):
				os.mkdir(self.lists[list]['archive'])

			# If we are updating an existing archive then use the archive's last value
			if os.path.exists(self.lists[list]['archive'] + '/last'):
				indexfile = open(self.lists[list]['archive'] + '/last', 'r')
				self.lists[list]['lastindex'] = int(indexfile.read())
				if self.lists[list]['lastindex'] == 0:
					self.lists[list]['lastindex'] = 1
				indexfile.close()
			# Else start from the beginning
			else:
				self.lists[list]['lastindex'] = 1
			
			# Parse additional arguments which affect hypermail behaviour
			self.lists[list]['options']['hypermail_args'] = ''
			if args.overwrite == True:
				self.lists[list]['options']['hypermail_args'] = self.lists[list]['options']['hypermail_args'] + '-x '
				self.lists[list]['lastindex'] = 1
			if args.progress == True:
				self.lists[list]['options']['hypermail_args'] = self.lists[list]['options']['hypermail_args'] + '-p '

			# Get the latest index value from mlmmj
			indexfile = open(self.lists[list]['list'] + '/index', 'r')
			self.lists[list]['newindex'] = int(indexfile.read())
			indexfile.close()

## The run looop.
#
#  Runs through the parsed config and calls hypermail with the defined arguments.
#  @param args
#  The arguments passed to the script.
def run(args):

	## @var config
	#  The parsed config.
	config = Config(args)
	
	# Loop over the lists
	for list in config.lists.keys():

		# Loop over the new messages according to the index files
		for id in range(config.lists[list]['lastindex'], config.lists[list]['newindex']):

			# Call hypermail
			os.system( ("env %s HM_DEFAULTINDEX=%s HM_THRDLEVELS=%i HM_FOLDER_BY_DATE='%%Y/%%m' hypermail -g -l %s -L %s -u -d %s %s < %s") % ( \
				config.lists[list]['options']['parsed_output'], \
				config.lists[list]['options']['ordering'], \
				config.lists[list]['options']['threadlevels'], \
				list, \
				config.lists[list]['options']['lang'], \
				config.lists[list]['archive'], \
				config.lists[list]['options']['hypermail_args'], \
				config.lists[list]['list'] + "/archive/" + str(id) ) )

		# Update the index in the archive
		indexfile = open(config.lists[list]['archive'] + '/last', 'w')
		indexfile.write(str(config.lists[list]['newindex']))
		indexfile.close()

def main():
	parser = argparse.ArgumentParser(description='mlmmj archive generator')
	parser.add_argument('-c', '--config', default='/etc/mlmmj-archiver/config.yml', help='use alternate config file (default: %(default)s)')
	parser.add_argument('-x', '--overwrite', action="store_const", const=True, help='overwrite archives')
	parser.add_argument('-p', '--progress', action="store_const", const=True, help='show progress')
	args = parser.parse_args()
	run(args)

