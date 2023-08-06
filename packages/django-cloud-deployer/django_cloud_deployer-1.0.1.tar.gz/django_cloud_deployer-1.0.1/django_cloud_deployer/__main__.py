import sys
from termcolor import colored, cprint
from .main import deploy, destroy, check_deploy
from .providers import paasProviders, faasProviders

packageName = 'django_cloud_deployer'
operations = [
    'deploy',
    'check_deploy',
    'destroy',
]

def printPackageUsage():
    sys.stderr.write(colored('Usage:\n', 'red'))
    sys.stderr.write(colored(f'{packageName} <operation>\n\n', 'red'))
    sys.stderr.write(colored('Available operations:\n', 'red'))
    for operation in operations:
        sys.stderr.write(colored(f'\t- {operation}\n', 'red'))

def printAvailablePaasProviders():
    sys.stderr.write(colored('Available PaaS providers:\n', 'red'))
    for provider in paasProviders:
        sys.stderr.write(colored(f'\t- {provider}\n', 'red'))

def printAvailableFaasProviders():
    sys.stderr.write(colored('Available FaaS providers:\n', 'red'))
    for provider in faasProviders:
        sys.stderr.write(colored(f'\t- {provider}\n', 'red'))

if len(sys.argv) < 2:
    sys.stderr.write(colored('Operation missing.\n\n', 'red'))
    printPackageUsage()
    sys.exit(2)

operation = sys.argv[1]
if not operation in operations:
    sys.stderr.write(colored(f'Invalid operation \'{operation}\'.\n\n', 'red'))
    printPackageUsage()
    sys.exit(2)

if operation == 'deploy':
    if len(sys.argv) < 4:
        sys.stderr.write(colored('Providers specification.\n\n', 'red'))
        sys.stderr.write(colored('Usage:\n', 'red'))
        sys.stderr.write(colored(f'{packageName} deploy <paas provider> <faas provider>\n\n', 'red'))
        printAvailablePaasProviders()
        printAvailableFaasProviders()
        sys.exit(3)

    paasProvider = sys.argv[2]
    if not paasProvider in paasProviders:
        sys.stderr.write(colored('Invalid PaaS provider.\n\n', 'red'))
        printAvailablePaasProviders()
        sys.exit(4)

    faasProvider = sys.argv[3]
    if not faasProvider in faasProviders:
        sys.stderr.write(colored('Invalid FaaS provider.\n\n', 'red'))
        printAvailableFaasProviders()
        sys.exit(5)

    deploy(paasProvider, faasProvider)
elif operation == 'destroy':
    destroy()
elif operation == 'check_deploy':
    check_deploy()
