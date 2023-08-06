import os
from swsm import security as sec


def sws_selector(word,indexes):
    """ Main function to select index positions from a word"""
    result = {}
    try:
        for elem in indexes:
            result[elem] = word[elem-1]
    except IndexError as e:
        return f"position {elem} not in word"
    else:
        results = []
        for k,v in result.items():
            results.append(f"{k} = {v}")
        return ", ".join(results)

def display_secrets(config,key):
    ''' get all secrets from file and return as dictionary'''
    secrets = sec.decrypt_secrets(config, key)
    return secrets

def add_to_secrets(secrets,word,label):
    '''add secret to secrets dictionary. if label is already in
        dictionary,ask user if label should be replaced.'''
    if label in secrets:
        ans = ''
        while ans.lower() != 'y':
            ans = input('Label already in secrets, do you want to replace it?\n(y)es or (n)o\n')
            if ans.lower() == 'y':
                secrets[label.lower()] = word
            elif ans.lower() == 'n':
                quit()
    else:
        secrets[label.lower()] = word
    return secrets


def get_salt(config):
    '''check config file for salt value. return salt value if found'''
    esalt = config.get('salt', 'salt')
    salt = esalt.encode('latin1')
    return salt

def make_salt(config,config_path):
    '''create a salt and store it in config file'''
    esalt = os.urandom(16)
    salt = esalt.decode('latin1')
    config['salt'] = {}
    config['salt']['salt'] = salt
    with open(config_path,'w',encoding='latin1') as cfg:
        config.write(cfg)
    return esalt

def reset_sws(swscfg):
    '''reset sws to default state.'''
    if os.path.isfile(swscfg):
        os.remove(swscfg)