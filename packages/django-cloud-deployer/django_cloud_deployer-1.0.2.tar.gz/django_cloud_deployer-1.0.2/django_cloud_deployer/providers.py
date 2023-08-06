from .heroku import HerokuProvider
from .azure import AzureProvider

paasProviders = {
    'heroku': HerokuProvider,
}

faasProviders = {
    'azure': AzureProvider,
}
