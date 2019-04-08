from google.appengine.ext import ndb


class MyDictionary(ndb.Model):
    word = ndb.StringProperty(repeated=True)
    count = ndb.IntegerProperty()
    num_letters = ndb.IntegerProperty()
    lexi_order = ndb.StringProperty()
