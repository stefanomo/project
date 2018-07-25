import datetime
import webapp2
import jinja2
import os

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime

class ReserveHandler(webapp2.RequestHandler):
    def get(self):  # for a get request
        a_template = the_jinja_env.get_template('index.html')
        self.response.out.write(a_template.render())

class AppUser(ndb.Model):
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  time = ndb.StringProperty()
  group_size = ndb.StringProperty()
  
class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    # If the user is logged in...
    if user:
        signout = users.create_logout_url('/')
        email_address = user.nickname()
        app_user = AppUser.get_by_id(user.user_id())
        a_template = jinja_env.get_template('index.html')
        self.response.out.write(a_template.render(signout=signout))
      # If the user has previously been to our site, we greet them!
        if app_user:
            signout_link_html = '<a href="%s">sign out</a>' % (
              users.create_logout_url('/'))
        
      # If the user hasn't been to our site, we ask them to sign up
        else:
            a_template = jinja_env.get_template('index.html')
            self.response.out.write(a_template.render())
    # Otherwise, the user isn't logged in!
    else:
      self.response.write('''
        Please log in to use our site! <br>
        <a href="%s">Sign in</a>''' % (
          users.create_login_url('/')))
  def post(self):
    user = users.get_current_user()
    if not user:
      # You shouldn't be able to get here without being logged in
      self.error(500)
      return
    timestamp = datetime.now()
    first_name=self.request.get('first_name')
    last_name=self.request.get('last_name') 
    time=self.request.get('times'),
    group_size= self.request.get('group_size')
    app_user = AppUser(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        
        time=self.request.get('times'),
        group_size= self.request.get('group_size'),
        id=user.user_id())
        
    app_user.put()
    a_template = jinja_env.get_template('index.html')
    self.response.write(a_template.render(group_size=group_size,time=time))
class RegisterHandler(webapp2.RequestHandler):
  def get(self):
    a_template = jinja_env.get_template('register.html')
    self.response.write(a_template.render())

class ReserveHandler(webapp2.RequestHandler):
  def get(self):
    a_template = jinja_env.get_template('reserve.html')
    self.response.write(a_template.render())

class ReservePittHandler(webapp2.RequestHandler):
  def get(self):
    a_template = jinja_env.get_template('/templates/reservepitt.html')
    self.response.write(a_template.render())
    
class HoursHandler(webapp2.RequestHandler):
  def get(self):
    a_template = jinja_env.get_template('hours.html')
    self.response.write(a_template.render())
    
class LoginHandler(webapp2.RequestHandler):
  def get(self):
    a_template = jinja_env.get_template('login.html')
    self.response.write(a_template.render())
    
  def post(self):
    user = users.get_current_user()
    if user:
      # Redirect to homepage
      return
      # You are logged in!

class LocationHoursHandler(webapp2.RequestHandler):
  def get(self):
    a_template = jinja_env.get_template('locationhours.html')
    self.response.write(a_template.render())

class ReserveHandler(webapp2.RequestHandler):
  def get(self):
    a_template = jinja_env.get_template('reserve.html')
    self.response.write(a_template.render())
    
class AdminHandler(webapp2.RequestHandler):
  def post(self):
    first_name=self.request.get('first_name')
    last_name=self.request.get('last_name') 
    time=self.request.get('times')
    group_size= self.request.get('group_size')
    app_user = AppUser(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        
        time=self.request.get('times'),
        group_size= self.request.get('group_size'))
        
    app_user.put()
    a_template = jinja_env.get_template('admin.html')
    self.response.write(a_template.render(time = time, group_size=group_size))
    

app = webapp2.WSGIApplication([
('/', MainHandler),
('/admin', AdminHandler),
('/register', RegisterHandler),
('/hours', HoursHandler),
('/reserve', ReserveHandler),
('/login', LoginHandler),
('/locationhours', LocationHoursHandler),
('/reservepitt', ReservePittHandler)],
debug=True)