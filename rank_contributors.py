import requests, json
from operator import itemgetter
# TODO revision limit is 500, get all revisions
# TODO support any wiki language

global lang, project, url

lang = 'hy'
project = 'wikipedia'
url = 'https://{}.{}.org/w/api.php'.format(lang, project)


def run(cat):
    pages_in_cat = get_category_members(cat)
    ranked_users = {}

    for page in pages_in_cat:
        revisions = get_contributors(page)
        for rev in revisions:
            user = rev['user']
            size = rev['size']
            if user in ranked_users:
                ranked_users[user] += size
            else:
                ranked_users[user] = size
    return sorted(ranked_users.items(), key=itemgetter(1), reverse=True)


def get_category_members(cat):
    cmtitle = 'Category:' + cat
    response = (requests.get(url, params = {
                        'action': 'query',
                        'list': 'categorymembers',
                        'cmtitle': cmtitle,
                        'format': 'json',
                        'utf8': ''
                        }))
    assert response.status_code == 200, 'API error, server response: {}'.format(response.status_code)

    # Decode to make sure non-latin characters are displayed correctly
    js = json.loads(response.content.decode('utf-8'))
    pages = []
    for page in js['query']['categorymembers']:
        if page['ns'] == 0:
            pages.append(page['title'])

    return pages


def get_contributors(page):
    response = (requests.get(url, params = {
                        'action': 'query',
                        'prop': 'revisions',
                        'titles': page,
                        'rvprop': 'user|size',
                        'rvlimit': 500,
                        'format': 'json',
                        'utf8': ''
                        }))
    assert response.status_code == 200, 'API error, server response: {}'.format(response.status_code)

    # Decode to make sure non-latin characters are displayed correctly
    js = json.loads(response.content.decode('utf-8'))

    item = list(js['query']['pages'].keys())[0]
    return js['query']['pages'][item]['revisions']
