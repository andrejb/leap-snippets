from leap.soledad.backends.couch import CouchDatabase


def get_couchdb_for_user(couch_url, user):
    db_url = couch_url + '/user-%s' % _get_user_id(user)
    return CouchDatabase.open_database(db_url, create=True)

def _get_user_id(user):
    # TODO: implement this method properly when webapi is available.
    query = 'users/_design/User/_view/by_email_or_alias/'
    query += '?key="%s"&reduce=false' % user
    #response = json.loads(_get('https://webapi/uid/%s/' % query))
    #uid = response['rows'][0]['id']
    import hmac
    uid = hmac.new('uuid', user).hexdigest()  # remove this!
    return uid

def _get(url):
    """
    Send a GET request to URL.

    @param url: URL for GET request.
    @type url: str

    @return: Body of request response.
    @rtype: str
    """
    url = urlparse(url)
    conn = HTTPConnection(url.hostname, url.port)
    conn.request('GET', url.path+url.query)
    return conn.getresponse().fp.read()
