import azure.functions as func
import os
import re

from azf_wsgi import AzureFunctionsWsgi
from {{ djangoWSGIApp }} import application

urlAndSegmentsRegex = r"^(https?:\/\/)?(www)?(.*\.(net|com|app)|localhost)(:\d+)?\/(.*)$"
paasRequestsRegexes = [
{{{ runInPaaSUrls }}}]
paasURL = '{{ paasUrl }}'

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    match = re.match(urlAndSegmentsRegex, req.url, re.M|re.I)
    segments = match.groups()[-1]

    for paasRequestsRegex in paasRequestsRegexes:
        if re.search(paasRequestsRegex, segments, re.M|re.I):
            return func.HttpResponse(
                status_code = 302, 
                headers = { 
                    "location": f"{paasURL}{segments}" 
                }
            )
    return AzureFunctionsWsgi(application).main(req, context)
