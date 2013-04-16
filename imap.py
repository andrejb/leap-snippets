from leap.soledad import Soledad


import common


class LeapIMAP(object):
    """
    Copy mail from CouchDB database and store it in Soledad.
    """

    def __init__(self, user, soledad_pass, couch_url, **kwargs):
        """
        Initialize LeapIMAP.

        @param user: The user adress in the form C{user@provider}.
        @type user: str
        @param soledad_pass: The password for the local database replica.
        @type soledad_pass: str
        @param couch_url: The URL of the CouchDB where email data will be
            saved.
        @type couch_url: str
        @param **kwargs: Used to pass arguments to Soledad instance. Maybe
            Soledad instantiation could be factored out from here, and maybe
            we should have a standard for all client code.
        """
        self._user = user
        self._couch_url = couch_url
        print kwargs['local_db_path']
        self._soledad = Soledad(
            user, soledad_pass,
            gnupg_home=kwargs['gnupg_home'],
            local_db_path=kwargs['local_db_path'],
            secret_path=kwargs['secret_path'])

    def get_new_mail(self):
        """
        Get new mail from CouchDB database, store locally using Soledad, and
        remove from remote db.
        """
        db = common.get_couchdb_for_user(self._couch_url, self._user)
        gen, doclist = db.get_all_docs()
        for doc in doclist:
            # create doc in local replica because this is not a sync operation
            doc.content['content'] = self._soledad.decrypt(doc.content['content'])
            self._soledad.create_doc(
                doc.content,
                doc_id=doc.doc_id)
            db.delete_doc(doc)
        # here we could make soledad sync with its remote db.
