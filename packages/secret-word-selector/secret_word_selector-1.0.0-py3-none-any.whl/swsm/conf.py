import configparser
import os.path

# creates a config file in user home directory and stores
# the below messages and settings on disk which can be
# read back later.

swscfg = os.path.expanduser('~/.swscfg')

config = configparser.ConfigParser()

config['messages'] = {}
messages = config['messages']

messages['no salt'] = """Salt file not found,creating new salt file.
				NOTICE: Older encrypted secrets files
				cannot be decrypted with new salt."""
messages['create salt'] = 'creating salt file'
messages['enter password'] = 'please enter password: '
messages['invalid token'] = 'invalid token, check password.'
messages['no secrets'] = 'No secrets file found. Creating secrets file ...'
messages['secrets found'] = 'secrets already exist. moving to old secrets section.'
messages['save secret'] = 'secret word saved ...'
messages['save first'] = "Please save a word first ..."
messages['interupt'] = 'SWS interupted by user'
messages['make choice'] = 'Please select a subcommand ... '
messages['salt not found'] = 'Cannot find a salt, please check config or reset ...'
messages['secrets not found'] = 'Cannot find secrets, please check config or reset ...'


config['first run'] = {'first run':False}

config['salt'] = {}

config['secrets'] = {}

config['old secrets'] = {}

# first run of sws main program should create a fresh config file
# in user home directory using the code below.
# on import, conf.py executes the below code and creates the config
# file if it is not already present,
if not os.path.isfile(os.path.expanduser(swscfg)):
	with open(os.path.expanduser(swscfg),'w') as cfg:
		config.write(cfg)


