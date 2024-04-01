import httpx
import sqlite_utils

class TechnitiumDnsClient(object):

    def __init__(self):
        pass

    def get_token(self):
        with httpx.Client() as dnsclient:
            pass