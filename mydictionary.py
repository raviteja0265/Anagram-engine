from google.appengine.ext import ndb


class MyDictionary(ndb.Model):
    word = ndb.StringProperty()
    anagram1 = ndb.StringProperty()
    anagram2 = ndb.StringProperty()
