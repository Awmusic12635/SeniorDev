from pinax.eventlog.models import log
from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES
from django.conf import settings
from django.http import HttpResponse


def setup_ldap():
    server = Server('ldap.rit.edu', port=636, use_ssl=True, get_info=ALL)
    conn = Connection(server, 'uid='+settings.LDAP_USERNAME+',ou=people,dc=rit,dc=edu',
                      settings.LDAP_PASSWORD, auto_bind=True)

    return conn


def get_user_by_username(user_id):
    conn = setup_ldap()
    print(conn)
    conn.search('ou=people,dc=rit,dc=edu', '(uid='+user_id+')', attributes=[ALL_ATTRIBUTES])

    print(conn)
    entry = conn.entries[0]
    conn.unbind()

    return entry


# this method doesn't work yet
def get_user_by_universityid(uni_id):
    conn = setup_ldap()
    conn.search('ou=people,dc=rit,dc=edu', '(universityid='+uni_id+')', attributes=[ALL_ATTRIBUTES])

    entry = conn.entries[0]
    conn.unbind()

    return entry


# For these you send in an entry that is returned by the user search.
def get_first_name(user):
    return user.cn.split()[0]


def get_last_name(user):
    return user.cn.split()[1]


def get_email(user):
    return user.uid + "@rit.edu"


# at least I think this is the what this Id is
def get_ldap_id(user):
    return user.uidNumber


# If student it returns "Student". I believe it returns Professor for professors
# Not sure if it is better to return this or ou attribute instead
def get_user_type(user):
    return user.ritEduAccountType


