import urllib


def url_with_querystring(path, **kwargs):
    return path + "?" + urllib.parse.urlencode(kwargs)
