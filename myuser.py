from google.appengine.ext import ndb
from mydictionary import MyDictionary


class MyUser(ndb.Model):
    word = ndb.StringProperty()
    mywords = ndb.StructuredProperty(MyDictionary, repeated=True)
