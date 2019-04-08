import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

from myuser import MyUser
from mydictionary import MyDictionary
from addanagram import AddPage

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class StoreFile(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user == 'None':
            template_values = {
                'login_url': users.create_login_url(self.request.url)
            }
            template = JINJA_ENVIRONMENT.get_template('loginpage.html')
            self.request.write(template.render(template_values))
            return
        template_values = {
            'logout_url': users.create_logout_url(self.request.url)
        }
        template = JINJA_ENVIRONMENT.get_template('store.html')
        self.request.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        file = self.request.get('StoreFile')

        if action == 'Store':
            openFile = open(file)
            readLine = openFile.readline()
            while readLine:
                words = (readLine.strip('\n\r')).lower()
                lexi_order = reduce(lambda x, y: x+y, sorted(words))
                num_letters = len(words)
                mydictionary_key = user.user_id() + lexi_order
                mydictionary_list = ndb.Key(MyDictionary, mydictionary_key)
                mydictionary_list_all = mydictionary_list.get()

                if mydictionary_list_all == 'None':
                    display_all = MyDictionary(id=mydictionary_key, lexi_order=lexi_order.lower(),
                                               num_letters=num_letters, count=1)
                    num_words = myuser.num_words + 1
                    unique = myuser.unique + 1

                    myuser = MyUser(id=user.user_id(), num_words=num_words, unique=unique)
                    myuser.put()
                    display_all.word.append(words)
                    display_all.put()
                    self.redirect('/')

                else:
                    counter = len(mydictionary_list_all.word) + 1
                    mydictionary_list_all.count = counter
                    mydictionary_list_all.word.append(words)
                    mydictionary_list_all.put()
                    num_words = myuser.num_words + 1
                    unique = myuser.unique
                    myuser = MyUser(id = user.user_id(), num_words=num_words, unique=unique)
                    myuser.put()

                readLine = openFile.readline()


            openFile.close()

        template_values = {
            'display': 'Successful'
        }

        template = JINJA_ENVIRONMENT.get_template('store.html')
        self.response.write(template.render(template_values))
