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
  group_size = ndb.IntegerProperty()
  
class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    # If the user is logged in...
    if user:
      email_address = user.nickname()
      app_user = AppUser.get_by_id(user.user_id())
      signout_link_html = '<a href="%s">sign out</a>' % (
          users.create_logout_url('/'))
      # If the user has previously been to our site, we greet them!
      if app_user:
        self.response.write('''
            Welcome %s %s (%s)! <br> %s <br>''' % (
              app_user.first_name,
              app_user.last_name,
              email_address,
              signout_link_html))
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
    app_user = AppUser(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        
        time=self.request.get('times'),
        group_size=int(self.request.get('group_size')),
        id=user.user_id())
        
    app_user.put()
    self.response.write("Thanks for signing up, your reservation is at" + str(app_user.time)  +  "with a group size of"  +  str(app_user.group_size))

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
    a_template = jinja_env.get_template('reservepitt.html')
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

class LocationReserveHandler(webapp2.RequestHandler):
  def get(self):
    a_template = jinja_env.get_template('locationreserve.html')
    self.response.write(a_template.render())
    

app = webapp2.WSGIApplication([
('/', MainHandler),
('/register', RegisterHandler),
('/hours', HoursHandler),
('/reserve', ReserveHandler),
('/login', LoginHandler),
('/locationhours', LocationHoursHandler),
('/locationreserve', LocationReserveHandler),
('/reservepitt', ReservePittHandler)],
debug=True)