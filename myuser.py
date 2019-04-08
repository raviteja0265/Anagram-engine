from google.appengine.ext import ndb
from mydictionary import MyDictionary


class MyUser(ndb.Model):
    name = ndb.StringProperty()
    num_words = ndb.IntegerProperty()
    unique = ndb.IntegerProperty()
