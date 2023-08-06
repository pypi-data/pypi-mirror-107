import sys
import re
import pathlib
import chevron
from termcolor import colored
from .command_runner import runCommand
from .provider import Provider

commands = {
    'loginCheck': 'heroku whoami',
    'create': 'heroku create --buildpack heroku/python',
    'herokuGitRemoteRemove': 'git remote remove heroku',
    'herokuGitRemoteAdd': 'git remote add heroku',
    'herokuDisableCollectStatic': 'heroku config:set DISABLE_COLLECTSTATIC=1',
    'deploy': 'git push heroku master',
    'envVarSet': 'heroku config:set',
    'destroy': 'heroku apps:destroy --confirm',
}
paasURLRegex = r'remote:\s*(.*)\s+deployed\s*to\s*Heroku'
herokuGitRepoRegex = r'(https?:\/\/git.*git)'
resourceNameRegex = r'https:\/\/(.*?)\..*'

directory = pathlib.Path(__file__).parent.absolute()
configFilesDirectoryName = 'config_files/heroku'
configFiles = [
    'Procfile',
]

class HerokuProvider(Provider):
    def isLoggedIn(self):
        return runCommand(commands['loginCheck'], outputToScreen=True)[0] == 0

    def __configHerokuGit(self):
        if not pathlib.Path('.git').is_dir():
            if runCommand('git init')[0] != 0:  
                sys.stderr.write(colored('Failed to initialize Heroku git repository.\n', 'red'))
                sys.exit(9)
        runCommand('git add -A')
        if runCommand('git commit -m "Django Cloud Deployer heroku deploy"')[0] != 0:
            sys.stderr.write(colored('Failed to commit to Heroku git repository.\n', 'red'))
            sys.exit(10)
        runCommand('git tag django_cloud_deployer')

    def createProject(self):
        self.__configHerokuGit()
        retcode, output = runCommand(commands['create'])
        if retcode != 0:   
            sys.stderr.write(colored('Failed to create Heroku project.\n', 'red'))
            sys.exit(4)

        match = re.findall(herokuGitRepoRegex, output)
        if len(match) == 0:
            sys.stderr.write(colored('Failed to retrieve remote PaaS git repository URL.\n', 'red'))
            sys.exit(5)

        repo_url = match[-1]
        runCommand(commands['herokuGitRemoteRemove'])
        runCommand(commands['herokuGitRemoteAdd'] + f' {repo_url}')
        runCommand(commands['herokuDisableCollectStatic'])
        
    def configEnvVars(self, envVars):
        for envVar in envVars:
            runCommand(commands['envVarSet'] + f' {envVar[0]}={envVar[1]}')

    def deploy(self):
        retcode, output = runCommand(commands['deploy'], outputToScreen=True)    
        if retcode != 0:  
            sys.stderr.write(colored('Failed to deploy project to Heroku.\n', 'red'))
            sys.exit(7)

        match = re.findall(paasURLRegex, output)
        if len(match) == 0:
            sys.stderr.write(colored('Failed to retrieve remote PaaS URL.\n', 'red'))
            sys.exit(8)

        url = match[-1]
        resource = re.findall(resourceNameRegex, url)[-1]
        return url, resource

    def setupConfigFiles(self):
        for fileName in configFiles:
            with open(f'{directory}/{configFilesDirectoryName}/{fileName}', 'r') as templateFile:
                content = chevron.render(templateFile, {
                    'projectName': self.projectName,
                    'djangoWSGIApp': self.djangoWSGIApp,
                })
                with open(fileName, 'w') as newFile:
                    newFile.write(content)

    def destroy(self, resourceName):
        return runCommand(commands['destroy'] + f' {resourceName}', outputToScreen=True)[0] == 0