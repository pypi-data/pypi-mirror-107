import configparser
import os.path

# exceptions messages are stored here and imported in to main sws
# program to avoid clogging up the main program code file.

swscfg = os.path.expanduser('~/.swscfg')
config = configparser.ConfigParser()
config.read(swscfg,encoding='latin1')

def exceptions_msgs(e):
    if e.__class__.__name__ == 'NoOptionError':
        if e.option == 'salt' and not config.getboolean('first run', 'first run'):
            print(config.get('messages','save first'))
        elif e.option == 'salt':
            print(config.get('messages','salt not found'))
        elif e.option == 'secrets' and not config.getboolean('first run', 'first run'):
            print(config.get('messages', 'save first'))
        elif e.option == 'secrets':
            print(config.get('messages', 'secrets not found'))

    elif e.__class__.__name__ == 'KeyError':
        print(f"{e} is not in secrets")

    elif e.__class__.__name__ == 'InvalidToken':
        print(config.get('messages', 'invalid token'))

    elif e.__class__.__name__ == 'KeyboardInterrupt':
        print(config.get('messages','interupt'))







