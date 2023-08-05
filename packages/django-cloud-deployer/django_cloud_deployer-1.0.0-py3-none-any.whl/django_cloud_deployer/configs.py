import pathlib
import re
import json
import sys
import os
from termcolor import colored, cprint

envFile ='.env'
ymlEnvFile = 'env.yml'
envVariablesRegex = r'\s*(.+)\s*=\s*(.+)\s*'
configFileName = 'django_cloud_deployer.json'
parentModuleRegex = r'(.*)\..*'

def setupEnvFiles():
    if not pathlib.Path(envFile).is_file():
        file = open(envFile, 'w')
        file.close()
    
    envVariables = []
    with open(envFile, 'r') as file:
        matches = re.findall(envVariablesRegex, file.read())
        for match in matches:
            envVariables.append((
                match[0].strip(), 
                match[1].strip(),
            ))
    
    with open(ymlEnvFile, 'w') as file:
        for envVariable in envVariables:
            file.write(f'{envVariable[0]}: {envVariable[1]}\n')
    return envVariables

def createConfig(projectName, paasConfig, faasConfig):
    config = {
        'projectName': projectName,
        'paasConfig': paasConfig,
        'faasConfig': faasConfig,
    }
    jsonContent = json.dumps(config, indent = 4)
    with open(configFileName, 'w') as file:
        file.write(jsonContent)

def readConfig():
    if not pathlib.Path(configFileName).is_file():
        sys.stderr.write(colored(f'No \'{configFileName}\' deployment configuration found. No resources to destroy\n', 'red'))
        sys.exit(15)
        
    with open(configFileName, 'r') as file:
        return json.load(file)

def getDjangoSettings():
    if os.environ.get('DJANGO_SETTINGS_MODULE') is not None:
        return os.environ.get('DJANGO_SETTINGS_MODULE')

    djangoSettingsModule = input(colored('Please enter the name of the Django settings module (e.g., \'mysite.settings\'): ', 'green'))
    try:
        module = __import__(djangoSettingsModule)
    except ImportError:
        sys.stderr.write(colored(f'Module \'{djangoSettingsModule}\' does not exist.\n', 'red'))
        sys.exit(16)

    return djangoSettingsModule
        
def getDjangoConfigs(djangoSettingsModule):
    try:
        module = __import__(djangoSettingsModule)
    except ImportError:
        sys.stderr.write(colored(f'Module \'{djangoSettingsModule}\' does not exist.\n', 'red'))
        sys.exit(16)

    try:
        rootUrlConfigsModule = module.settings.ROOT_URLCONF
    except AttributeError:
        sys.stderr.write(colored(f'Settings module does not include a root url configurations module specification. Please add the \'ROOT_URLCONF\' attribute to the settings module.\n', 'red'))
        sys.exit(17)

    try:
        wsgiApplicationModule = module.settings.WSGI_APPLICATION
    except AttributeError:
        sys.stderr.write(colored(f'Settings module does not include a wsgi application module specification. Please add the \'WSGI_APPLICATION\' attribute to the settings module.\n', 'red'))
        sys.exit(18)

    match = re.findall(parentModuleRegex, wsgiApplicationModule)
    if len(match) > 0:
        wsgiApplicationModule = match[-1]
    
    return rootUrlConfigsModule, wsgiApplicationModule
