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


class AddPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user==None:
            template_values = {
                'login_url': users.create_login_url(self.request.url)
            }
            template = JINJA_ENVIRONMENT.get_template('loginpage.html')
            self.response.write(template.render(template_values))
            return

        template_values = {
            'logout_url': users.create_logout_url(self.request.url)
        }
        template = JINJA_ENVIRONMENT.get_template('addanagram.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')

        if action == 'Submit':
            word = self.request.get('word')
            num_letters = len(word)
            lexi_order = reduce(lambda x, y: x+y, sorted(word))
            if word == '':
                self.redirect('/')

            else:
                user = users.get_current_user()
                mydictionary_key = user.user_id() + lexi_order
                mydictionary_key_get = ndb.Key(MyDictionary, mydictionary_key)
                mydictionary_list = mydictionary_key_get.get()
                myuser_key = ndb.Key('MyUser', user.user_id())
                myuser = myuser_key.get()

                if mydictionary_list==None:
                    mydictionary_list_all = MyDictionary(id=mydictionary_key, lexi_order=lexi_order.lower(),
                                                         num_letters=num_letters, count=1)
                    #num_words = myuser.num_words+1
                    #unique = myuser.unique+1
                    #myuser = MyUser(id=user.user_id(), num_words=num_words, unique=unique)
                    #myuser.put()
                    mydictionary_list_all.word.append(word)
                    mydictionary_list_all.put()
                    self.redirect('/')

                else:
                    counter = len(mydictionary_list.word) + 1
                    mydictionary_list.count = counter
                    mydictionary_list.word.append(word)
                    mydictionary_list.put()
                    #num_words = myuser.num_words+1
                    #unique = myuser.unique
                    #myuser = MyUser(id=user.user_id(), num_words=num_words, unique=unique)

                    #myuser.put()
                    template_values = {
                        'display': 'successful'
                    }
                    template = JINJA_ENVIRONMENT.get_template('addanagram.html')
                    self.response.write(template.render(template_values))
