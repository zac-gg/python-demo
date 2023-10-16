import json
import requests
import http.client
import urllib.parse
from collections import OrderedDict

def ksort(d):
    str = ''
    for k in sorted(d.keys()):
        str+=k+'='+d[k]+'&'
    return str.strip('&')

def url_encoder(params):
    g_encode_params = {}

    def _encode_params(params, p_key=None):
        encode_params = {}
        if isinstance(params, dict):
            for key in params:
                encode_key = '{}[{}]'.format(p_key,key)
                encode_params[encode_key] = params[key]
        elif isinstance(params, (list, tuple)):
            for offset,value in enumerate(params):
                encode_key = '{}[{}]'.format(p_key, offset)
                encode_params[encode_key] = value
        else:
            g_encode_params[p_key] = params

        for key in encode_params:
            value = encode_params[key]
            _encode_params(value, key)

    if isinstance(params, dict):
        for key in params:
            _encode_params(params[key], key)
    return urllib.parse.urlencode(g_encode_params)

def curl_post(url,params):
    res = requests.post(url,params,headers={'Content-Type':'application/x-www-form-urlencoded'})
    return res