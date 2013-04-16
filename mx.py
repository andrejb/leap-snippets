from httplib import HTTPConnection
from urlparse import urlparse
from u1db.errors import DatabaseDoesNotExist


import common


class LeapMX(object):
    """
    Receive mail and store in user's remote CouchDB.
    """

    def __init__(self, gpg, couch_url, webapi_url):
        """
        Initialize LeapMX.

        @param couch_url: The URL of the CouchDB where email data will be
            saved.
        @type couch_url: str
        @param webapi_url: The URL from where to fetch user information.
        @type couch_url: str
        """
        self._gpg = gpg
        self._couch_url = couch_url
        self._webapi_url = webapi_url

    def store_mail(self, user, maildata):
        """
        Store C{maildata} in C{user}'s CouchDB database.

        @param user: The user address in the form C{user@provider}.
        @type user: str
        @param maildata: The serialized contents of the email.
        @type maildata: str
        """
        db = common.get_couchdb_for_user(self._couch_url, user)
        doc = db.create_doc({
            'to': user,
            'content': str(self._gpg.encrypt(maildata, user, always_trust=True)),
            'id': 'xxx',
        })

