import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

from myuser import MyUser
from mydictionary import MyDictionary

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
            myuser = MyUser(id=user.user_id())
            myuser.put()

        template_values = {
            'logout_url': users.create_logout_url(self.request.url)
        }

        template = JINJA_ENVIRONMENT.get_template('homepage.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action = self.request.get('button')
        if action == 'Save Anagram':
            word = self.request.get('word')
            anagram1 = self.request.get('anagram1')
            anagram2 = self.request.get('anagram2')
            mydictionary_list = MyDictionary.query()

            mydictionary_list = mydictionary_list.fetch()

            user = users.get_current_user

            mydictionary_key = ndb.Key('MyUser', word)
            mydictionary = mydictionary_key.get()

            mydictionary.mywords.append(mydictionary_list)
            mydictionary.put()

            template_values = {
                'mydictionary_list': mydictionary_list,
                'anagram1': anagram1,
                'anagram2': anagram2
            }

            template = JINJA_ENVIRONMENT.get_template('homepage.html')
            self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        if action == 'Save Anagram':
            word = self.request.get('word')
            anagram1 = self.request.get('anagram1')
            anagram2 = self.request.get('anagram2')

            user = users.get_current_user()

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            mydictionary_key = ndb.Key('MyDictionary', word)
            mydictionary = mydictionary_key.get()
            if mydictionary == None:
                new_word = MyDictionary(word=word, anagram1=anagram1, anagram2=anagram2)
                myuser.mywords.append(new_word)
                new_word.put()

                self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
