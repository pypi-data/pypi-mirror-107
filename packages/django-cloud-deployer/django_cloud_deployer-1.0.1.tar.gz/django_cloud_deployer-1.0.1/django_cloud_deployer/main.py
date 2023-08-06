import pkg_resources
import pathlib
import sys
import django
import os
from termcolor import colored, cprint
from .heroku import HerokuProvider
from .azure import AzureProvider
from .urls_annotator import getCloudUrls
from .configs import setupEnvFiles, createConfig, readConfig, getDjangoConfigs, getDjangoSettings
from .providers import paasProviders, faasProviders

def deploy(paasProviderName, faasProviderName):
    projectName = input(colored('Please enter a name for your project: ', 'green'))
    djangoSettingModule = getDjangoSettings()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', djangoSettingModule)
    rootUrlConfigsModule, wsgiApplicationModule = getDjangoConfigs(djangoSettingModule)

    paasProvider = paasProviders[paasProviderName](projectName, wsgiApplicationModule)
    faasProvider = faasProviders[faasProviderName](projectName, wsgiApplicationModule)

    django.setup()
    runInFaaSUrls, runInPaaSUrls = getCloudUrls()

    if len(runInFaaSUrls) > 0:
        cprint(f'\nThe following urls will run in {faasProviderName}:', 'green')
        for url in runInFaaSUrls:
            print(url)
    else:
        cprint(f'\nWarning: No urls will run in {faasProviderName}.', 'yellow')

    if len(runInPaaSUrls) > 0:
        cprint(f'\nThe following urls will run in {paasProviderName}:', 'green')
        for url in runInPaaSUrls:
            print(url)
    else:
        cprint(f'\nWarning: No urls will run in {paasProviderName}.', 'yellow')

    if len(runInFaaSUrls) == 0 and len(runInPaaSUrls) == 0:
        cprint(f'\nNo urls found. Stopping.', 'red')
        sys.exit(2)

    cprint(f'\nChecking if user is logged in to {paasProviderName} ...', 'green')
    if not paasProvider.isLoggedIn():  
        sys.stderr.write(colored(f'Not logged in to {paasProviderName}. Please login to {paasProviderName} and try again.\n', 'red'))
        sys.exit(3)
    else:
        cprint(f'User is logged in to {paasProviderName}.\n', 'green')

    cprint(f'Checking if user is logged in to {faasProviderName} ...', 'green')
    if not faasProvider.isLoggedIn():  
        sys.stderr.write(colored(f'Not logged in to {faasProviderName}. Please login to {faasProviderName} and try again.\n', 'red'))
        sys.exit(4)
    else:
        cprint(f'User is logged in to {faasProviderName}.\n', 'green')
    
    cprint('Setting up config files ...', 'green')
    paasProvider.setupConfigFiles()
    faasProvider.setupConfigFiles()
    envVars = setupEnvFiles()
    cprint('Config files setup completed.\n', 'green')

    cprint(f'Deploying project to {paasProviderName} PaaS ...', 'green')
    paasProvider.createProject()
    paasProvider.configEnvVars(envVars)
    paasURL, paasResourceName = paasProvider.deploy()
    paasURLstr = colored(paasURL, 'blue', attrs=['underline'])
    faasProvider.setupCloudRouter(paasURL, runInPaaSUrls)
    cprint(f'Project deploying to {paasProviderName} PaaS completed. Resource \'{paasResourceName}\' is available at {paasURLstr}\n', 'green')

    cprint(f'Configuring Serverless Framework node packages ...', 'green')
    if not faasProvider.configServerlessNodePackages():
        sys.stderr.write(colored('Failed to install Serveless Framework node dependencies.\n', 'red'))
        sys.exit(14)
    else:
        cprint(f'Serverless Framework node packages installed.\n', 'green')

    cprint(f'Deploying project to {faasProviderName} FaaS ...', 'green')
    faasURL, faasResourceName = faasProvider.deploy()
    faasURLstr = colored(faasURL, 'blue', attrs=['underline'])
    cprint(f'Project deploying to {faasProviderName} FaaS completed. Resource \'{faasResourceName}\' is available at {faasURLstr}\n', 'green')

    createConfig(
        projectName,
        {
            'provider': paasProviderName,
            'resource': paasResourceName,
            'url': paasURL,
        },
        {
            'provider': faasProviderName,
            'resource': faasResourceName,
            'url': faasURL,
        },
    )

    cprint('Completed.', 'green')

def destroy():
    config = readConfig()
    projectName = config['projectName']

    paasProviderName = config['paasConfig']['provider']
    paasProviderResource = config['paasConfig']['resource']
    cprint(f'Destroying PaaS resource in {paasProviderName} ...', 'green')
    paasProvider = paasProviders[paasProviderName](projectName)
    if not paasProvider.destroy(paasProviderResource):
        sys.stderr.write(colored('Failed to destroy PaaS resource.\n\n', 'red'))
    else:
        cprint(f'PaaS resource destroyed.\n\n', 'green')

    faasProviderName = config['faasConfig']['provider']
    faasProviderResource = config['faasConfig']['resource']
    cprint(f'Destroying FaaS resource in {faasProviderName} ...', 'green')
    faasProvider = faasProviders[faasProviderName](projectName)
    if not faasProvider.destroy(faasProviderResource):
        sys.stderr.write(colored('Failed to destroy PaaS resource.\n\n', 'red'))
    else:
        cprint(f'FaaS resource destroyed.\n\n', 'green')

    cprint('Completed.', 'green')

def check_deploy():
    djangoSettingModule = getDjangoSettings()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', djangoSettingModule)
    rootUrlConfigsModule, wsgiApplicationModule = getDjangoConfigs(djangoSettingModule)
    django.setup()
    runInFaaSUrls, runInPaaSUrls = getCloudUrls()

    if len(runInFaaSUrls) > 0:
        cprint(f'\nThe following urls will run in the FaaS provider:', 'green')
        for url in runInFaaSUrls:
            print(url)
    else:
        cprint(f'\nWarning: No urls will run in the FaaS provider.', 'yellow')

    if len(runInPaaSUrls) > 0:
        cprint(f'\nThe following urls will run in the PaaS provider:', 'green')
        for url in runInPaaSUrls:
            print(url)
    else:
        cprint(f'\nWarning: No urls will run in the PaaS provider.', 'yellow')

    if len(runInFaaSUrls) == 0 and len(runInPaaSUrls) == 0:
        cprint(f'\nNo urls found.', 'red')
        sys.exit(2)
