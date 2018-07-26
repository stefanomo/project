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
  date = ndb.StringProperty()
  seat = ndb.StringProperty()
  time = ndb.StringProperty()
  group_size = ndb.StringProperty()
  location = ndb.StringProperty()
  user_date = ndb.StringProperty()

  
class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    time = self.request.get('group_size')
    print time
    if time:
        self.response.write('''
        <button id = "myBtn"> Check Reservation</button>
         <div id="myModal" class="modal">

    <!-- Modal content -->
      <div class="modal-content">
        <span class="close">&times;</span>
        <p>Reserved!</p>
      </div>''')
    # If the user is logged in...
    if user:
        app_user = AppUser.get_by_id(user.user_id())
        a_template = jinja_env.get_template('index.html')

      # If the user has previously been to our site, we greet them!
        if app_user:
            signout = users.create_logout_url('/')
            self.response.out.write(a_template.render(signout=signout))
        else:
            # If the user hasn't been to our site, we ask them to sign up
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
    timestamp = datetime.now(),
    first_name=self.request.get('first_name'),
    last_name=self.request.get('last_name'),
    date=self.request.get('date'),
    time=self.request.get('time'),
    group_size= self.request.get('group_size'),
    seat=self.request.get('seat'),
    location=self.request.get('location')
    
    
    app_user = AppUser(
        user_date = self.request.get('user_date'),
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        seat=self.request.get('seat'),
        date=self.request.get('date'),
        time=self.request.get('time'),
        group_size= self.request.get('group_size'),
        location=self.request.get('location')
      )
        
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

class LocationReserveHandler(webapp2.RequestHandler):
  def get(self):
    a_template = jinja_env.get_template('locationreserve.html')
    self.response.write(a_template.render())

class ReservePittHandler(webapp2.RequestHandler):
  def get(self):
    a_template = jinja_env.get_template('reservepitt.html')
    self.response.write(a_template.render())
    
class ReservePhillyHandler(webapp2.RequestHandler):
  def get(self):
    a_template = jinja_env.get_template('reservephilly.html')
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
  
class MenuHandler(webapp2.RequestHandler):
  def get(self):
    a_template = jinja_env.get_template('menupicture.html')
    self.response.write(a_template.render())
    
class AdminHandler(webapp2.RequestHandler):
  def get(self):
    chosen_date = self.request.get("user_date")
    reservation = AppUser.query().filter(AppUser.date == chosen_date).fetch()
    self.response.write('<form> <input type = "text" name = "user_date"> <input type="submit"> </form>')
    for reserves in reservation:
        self.response.write('''Location: %s <br> Name: %s %s <br> Reservation Time: %s <br> Group Size: %s <br> Date: %s <br> Seat: %s <br>''' % (reserves.location,reserves.first_name,reserves.last_name,reserves.time,reserves.group_size,reserves.date,reserves.seat))

    

app = webapp2.WSGIApplication([
('/', MainHandler),
('/admin', AdminHandler),
('/register', RegisterHandler),
('/locationreserve', LocationReserveHandler),
('/reservepitt', ReservePittHandler),
('/reservephilly', ReservePhillyHandler),
('/menupicture', MenuHandler),
('/reserve', ReserveHandler),
('/login', LoginHandler),
('/locationhours', LocationHoursHandler),
('/menupicture', MenuHandler)],
debug=True)