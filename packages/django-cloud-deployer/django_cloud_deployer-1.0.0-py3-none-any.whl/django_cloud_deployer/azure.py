import sys
import re
import pathlib
import chevron
from termcolor import colored
from .command_runner import runCommand
from .provider import Provider

commands = {
    'loginCheck': 'az account show',
    'deploy': 'sls deploy',
    'installDependencies': 'npm i',
    'destroy': 'sls remove',
}
faasURLRegex = r'Serverless:.*\[\*\]\s*(.*)api.*'
resourceNameRegex = r'Serverless:\s+Creating\s+resource\s+group:\s+(.*)\s*'

directory = pathlib.Path(__file__).parent.absolute()
configFilesDirectoryName = 'config_files/azure'
configFiles = [
    'serverless.yml',
    'package.json',
    'package-lock.json',
    'host.json',
]
cloudRouterFile = 'cloud_router.py'

class AzureProvider(Provider):
    def isLoggedIn(self):
        return runCommand(commands['loginCheck'], outputToScreen=True)[0] == 0

    def deploy(self):
        retcode, output = runCommand(commands['deploy'], outputToScreen=True)    
        if retcode != 0:  
            sys.stderr.write(colored('Failed to deploy project to Azure.\n', 'red'))
            sys.exit(12)

        match = re.findall(faasURLRegex, output)
        if len(match) == 0:
            sys.stderr.write(colored('Failed to retrieve remote FaaS URL.\n', 'red'))
            sys.exit(13)
        url = f'https://{match[-1]}'

        match = re.findall(resourceNameRegex, output)
        if len(match) == 0:
            sys.stderr.write(colored('Failed to retrieve FaaS resource name.\n', 'red'))
            sys.exit(14)
        resource = match[-1]

        return url, resource

    def configServerlessNodePackages(self):
        return runCommand(commands['installDependencies'], outputToScreen=True)[0] == 0

    def setupConfigFiles(self):
        for fileName in configFiles:
            with open(f'{directory}/{configFilesDirectoryName}/{fileName}', 'r') as templateFile:
                content = chevron.render(templateFile, {'projectName': self.projectName})
                with open(fileName, 'w') as newFile:
                    newFile.write(content)

    def setupCloudRouter(self, paasURL, runInPaaSUrls):
        if paasURL[-1] != '/':
            paasURL += '/'

        with open(f'{directory}/{configFilesDirectoryName}/{cloudRouterFile}', 'r') as templateFile:
            content = chevron.render(templateFile, {
                'projectName': self.projectName,
                'djangoWSGIApp': self.djangoWSGIApp,
                'paasUrl': paasURL,
                'runInPaaSUrls': ''.join(list(map(lambda url: f'\tr\'{url}\',\n', runInPaaSUrls))),
            })
            with open(cloudRouterFile, 'w') as newFile:
                newFile.write(content)

    def destroy(self, resourceName):
        return runCommand(commands['destroy'], outputToScreen=True)[0] == 0
