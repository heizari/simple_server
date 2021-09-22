from view.dynamic.simple_post import simple_post as SPost
import urllib.parse
from pprint import pformat
import ast
import cgi

def Post(path, params_origin):
    simple_post = SPost()
    print((urllib.parse.parse_qs(params_origin)))
    params = ast.literal_eval(pformat(urllib.parse.parse_qs(params_origin, keep_blank_values=True)))
    if path == 'simple_post':
        body = simple_post.post(params)
    else:
        print(error)

    return body.encode()

def Get(path):
    print('here')
    simple_post = SPost()
    params = ''
    parses = urllib.parse.urlparse(path)
    query = parses.query
    path = parses.path

    print(query)
    print(path)

    params = urllib.parse.parse_qs(query, keep_blank_values=True)
    if path == 'index':
        body = simple_post.index(params)
    elif path == 'simple_get':
        body = simple_post.get(params)
    else:
        print(error)

    return body.encode()