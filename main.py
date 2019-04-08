import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

from myuser import MyUser
from mydictionary import MyDictionary
from addanagram import AddPage
from store import StoreFile

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        if user == None:
            template_values = {
                'login_url': users.create_login_url(self.request.url)
            }

            template = JINJA_ENVIRONMENT.get_template('loginpage.html')
            self.response.write(template.render(template_values))
            return
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if myuser == None:
            myuser = MyUser(id=user.user_id(), num_words=0, unique=0)
            myuser.put()

        template_values = {
            'logout_url': users.create_logout_url(self.request.url),
            'user': user,
            'allvalues': MyDictionary.query().fetch(),
            'num_words': myuser.num_words,
            'unique': myuser.unique
        }

        template = JINJA_ENVIRONMENT.get_template('homepage.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')

        user = users.get_current_user()

        if action == 'Search':
            word = self.request.get('word')
            lexi_order = reduce(lambda x, y: x+y, sorted(word))
            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            if word == '':
                self.redirect('/')

            else:
                mydictionary_key = user.user_id() + lexi_order
                mydictionary_list = ndb.Key(MyDictionary, mydictionary_key)
                mydictionary_list_all = mydictionary_list.get()
            template_values = {
                'allvalues': mydictionary_list_all,
                'user': user,
                'num_words': myuser.num_words,
                'unique': myuser.unique
            }

            template = JINJA_ENVIRONMENT.get_template('homepage.html')
            self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/addanagram', AddPage),
    ('/store', StoreFile)
], debug=True)
