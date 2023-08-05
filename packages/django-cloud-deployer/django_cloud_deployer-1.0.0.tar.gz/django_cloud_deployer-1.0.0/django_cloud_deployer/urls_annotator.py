from django.urls import get_resolver, URLPattern, URLResolver
    
paasPatterns = set()
def runInPaaS(urlpattern):
    if isinstance(urlpattern, URLResolver):
        for p in urlpattern.url_patterns:
            runInPaaS(p)
    else:
        paasPatterns.add(urlpattern)
    return urlpattern

faasPatterns = set()
def runInFaaS(urlpattern):
    if isinstance(urlpattern, URLResolver):
        for p in urlpattern.url_patterns:
            runInFaaS(p)
    else:
        faasPatterns.add(urlpattern)
    return urlpattern

def trimUrlRegex(urlRegex):
    startIndex = 0 if urlRegex[0] != '^' else 1
    endIndex = len(urlRegex) if urlRegex[-1] != '$' else len(urlRegex) - 1
    return urlRegex[startIndex:endIndex]

def getDjangoProjectUrls():
    urls = {}

    def visitUrl(resolver, parent='^'):
        for url_pattern in resolver.url_patterns:
            if isinstance(url_pattern, URLResolver):
                visitUrl(url_pattern, f'{parent}{trimUrlRegex(url_pattern.pattern.regex.pattern)}')
            elif isinstance(url_pattern, URLPattern):
                p = f'{parent}{trimUrlRegex(url_pattern.pattern.regex.pattern)}'
                p += '?' if p[-1] == '/' else '/?'
                urls[url_pattern] = f'{p}$'

    visitUrl(get_resolver())
    return urls

def getCloudUrls():
    faasUrlPatterns = []
    paasUrlPatterns = []
    urls = getDjangoProjectUrls()

    for pattern, url in urls.items():
        if pattern in paasPatterns and pattern not in faasPatterns:
            paasUrlPatterns.append(url)
        else:
            faasUrlPatterns.append(url)
    
    return faasUrlPatterns, paasUrlPatterns

