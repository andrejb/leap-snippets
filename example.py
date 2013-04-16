from mx import LeapMX
from imap import LeapIMAP
import tempfile
import gnupg

#
# Example of MX use on server side
#

# setup gpg with public key for encryption
pubkey = open('keys/leap@leap.se.pub.asc').read()
gpg = gnupg.GPG(gnupghome=tempfile.mkdtemp())
gpg.import_keys(pubkey)

# MX stores incoming mail for user 'leap@leap.se':
mx = LeapMX(gpg=gpg, couch_url='http://localhost:5984', webapi_url='')
mx.store_mail('leap@leap.se', 'From: vip@domain.org\nSubject: important!')
mx.store_mail('leap@leap.se', 'From: vip2@domain.org\nSubject: important!')
mx.store_mail('leap@leap.se', 'From: vip3@domain.org\nSubject: important!')


#
# Example of IMAP use on client side
#

# setup gpg with private key for decryption
privkey = open('keys/leap@leap.se.priv.asc').read()
tempdir = tempfile.mkdtemp()
gpg = gnupg.GPG(gnupghome=tempdir+'/gnupg')
gpg.import_keys(privkey)

# IMAP reads new mail from couch db
imap = LeapIMAP(
    'leap@leap.se',
    soledad_pass='hardpass',
    couch_url='http://localhost:5984',
    gnupg_home=tempdir+'/gnupg',
    local_db_path=tempdir+'/soledad.u1db',
    secret_path=tempdir+'/secret.gpg',
)
imap.get_new_mail()

# Access all current docs
gen, doclist = imap._soledad.get_all_docs()
for doc in doclist:
    print doc.content['content']
