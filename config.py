from getpass import getpass
import os

"""
SSL Verify method

Examples:
verify = False  # don't verify
verify = 'path/to/certfile'  # path to CA_BUNDLE file
verify = os.environ['REQUESTS_CA_BUNDLE'] # use certifi
"""
verify = os.environ['REQUESTS_CA_BUNDLE']  # use certifi

"""
Use NTLM to authenticate (useful when downloading behind a proxy)
"""
ntlm = False  # change to True if behind proxy that requires NTLM authentication
if ntlm:
    from requests_ntlm import HttpNtlmAuth
    username = input('Username: ')
    password = getpass()
    auth = HttpNtlmAuth(username, password)
else:
    username = None
    password = None
    auth = None
