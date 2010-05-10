import os
import logging
import wsgiref.handlers
import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from util.sessions import Session
from google.appengine.ext import db

# A Model for a User
class User(db.Model):
  account = db.StringProperty()
  password = db.StringProperty()
  name = db.StringProperty()
  email = db.StringProperty()
  
# a Model for Stats
class Stats(db.Model):
  team = db.StringProperty()
  gp = db.IntegerProperty()
  w = db.IntegerProperty()
  l = db.IntegerProperty()
  t = db.IntegerProperty()
  pts = db.IntegerProperty()
  gf = db.IntegerProperty()
  ga = db.IntegerProperty()
  plusminus = db.IntegerProperty()
  sog = db.IntegerProperty()
  tpm = db.IntegerProperty()
  gfa = db.IntegerProperty()
  gaa = db.IntegerProperty()
  avg = db.IntegerProperty()
  
# A Model for an Event
class Event(db.Model):
  date = db.DateProperty()
  type = db.StringProperty()
  location = db.StringProperty()
  opponent = db.StringProperty()
  
# A Model for a ChatMessage
class ChatMessage(db.Model):
  user = db.ReferenceProperty()
  text = db.StringProperty()
  created = db.DateTimeProperty(auto_now=True)

# A helper to do the rendering and to add the necessary
# variables for the _base.htm template
def doRender(handler, tname = 'index.htm', values = { }):
  temp = os.path.join(
      os.path.dirname(__file__),
      'templates/' + tname)
  if not os.path.isfile(temp):
    return False

  # Make a copy of the dictionary and add the path and session
  newval = dict(values)
  newval['path'] = handler.request.path
  handler.session = Session()
  if 'username' in handler.session:
     newval['username'] = handler.session['username']

  outstr = template.render(temp, newval)
  handler.response.out.write(outstr)
  return True

class LoginHandler(webapp.RequestHandler):

  def get(self):
    doRender(self, 'loginscreen.htm')

  def post(self):
    self.session = Session()
    acct = self.request.get('account')
    pw = self.request.get('password')
    logging.info('Checking account='+acct+' pw='+pw)

    self.session.delete('username')
    self.session.delete('userkey')

    if pw == '' or acct == '':
      doRender(
          self,
          'loginscreen.htm',
          {'error' : 'Please specify Account and Password'} )
      return

    que = db.Query(User)
    que = que.filter('account =',acct)
    que = que.filter('password = ',pw)

    results = que.fetch(limit=1)

    if len(results) > 0 :
      user = results[0]
      self.session['userkey'] = user.key()
      self.session['username'] = acct
      doRender(self,'index.htm',{ } )
    else:
      doRender(
          self,
          'loginscreen.htm',
          {'error' : 'Incorrect password'} )

class ApplyHandler(webapp.RequestHandler):

  def get(self):
    doRender(self, 'applyscreen.htm')

  def post(self):
    self.session = Session()
    name = self.request.get('name')
    acct = self.request.get('account')
    pw = self.request.get('password')
    em = self.request.get('email')
    logging.info('Adding account='+acct)

    if pw == '' or acct == '' or name == '' or em == '':
      doRender(
          self,
          'applyscreen.htm',
          {'error' : 'Please fill in all fields'} )
      return

    # Check if the user already exists
    que = db.Query(User).filter('account =',acct)
    results = que.fetch(limit=1)

    if len(results) > 0 :
      doRender(
          self,
          'applyscreen.htm',
          {'error' : 'Account Already Exists'} )
      return

    # Create the User object and log the user in
    pkey = User(name=name, account=acct, password=pw, email=em).put()
    self.session['username'] = acct
    self.session['userkey'] = pkey
    doRender(self,'index.htm',{ })

class ManageHandler(webapp.RequestHandler):
   def get(self):
    que = db.Query(User)
    user_list = que.fetch(limit=100)
    doRender(self, 'manage.htm', {'user_list': user_list})

class ChatHandler(webapp.RequestHandler):

  def get(self):
    doRender(self,'chatscreen.htm')

  def post(self):
    self.session = Session()
    if not 'userkey' in self.session:
      doRender(
          self,
          'chatscreen.htm',
          {'error' : 'Must be logged in'} )
      return

    msg = self.request.get('message')
    if msg == '':
      doRender(
          self,
          'chat.htm',
          {'error' : 'Blank message ignored'} )
      return

    newchat = ChatMessage(user = self.session['userkey'], text=msg)
    newchat.put()
    doRender(self,'chatscreen.htm')

class MessagesHandler(webapp.RequestHandler):

  def get(self):
    que = db.Query(ChatMessage).order('-created');
    chat_list = que.fetch(limit=100)
    doRender(self, 'messagelist.htm', {'chat_list': chat_list})

class SchedulesHandler(webapp.RequestHandler):
	def get(self):
	  que = db.Query(Event)
   	  event_list = que.fetch(limit=100)
	  doRender(self, 'schedules.htm', {'event_list': event_list})
	 
class StatisticsHandler(webapp.RequestHandler):
	def get(self):
	  que = db.Query(Stats)
   	  stats_list = que.fetch(limit=100)
	  doRender(self, 'statistics.htm', {'stats_list': stats_list})

class ManageSchedHandler(webapp.RequestHandler):
  def get(self):
  	que = db.Query(Event)
  	event_list = que.fetch(limit=100)
  	doRender(self, 'manageSched.htm', {'event_list': event_list})
  
  def post(self):
  	que = db.Query(Event)
  	event_list = que.fetch(limit=100)
  	doRender(self, 'manageSched.htm', {'event_list': event_list})	

class ManageStatsHandler(webapp.RequestHandler):
	def get(self):
	  que = db.Query(Stats)
	  stats_list = que.fetch(limit=100)
	  doRender(self, 'manageStats.htm', {'stats_list' : stats_list})
	def post(self):
	  que = db.Query(Stats)
	  stats_list = que.fetch(limit=100)
	  doRender(self, 'manageStats.htm', {'stats_list' : stats_list})

class AddEventHandler(webapp.RequestHandler):
   def get(self):
   	 que = db.Query(Event)
   	 event_list = que.fetch(limit=100)
	 doRender(self, 'manageSched.htm', {'event_list': event_list})
	 
   def post(self):
     year = int(self.request.get('year'))
     month = int(self.request.get('month'))
     day = int(self.request.get('day'))
     d1 = datetime.date(year, month, day)
     ty = self.request.get('type')
     loc= self.request.get('location')
     opp= self.request.get('opponent')
     newEvent = Event(date=d1, type=ty, location=loc, opponent=opp).put()
     que = db.Query(Event)
     event_list = que.fetch(limit=100)
     doRender(self, 'manageSched.htm', {'event_list' : event_list})
     
class AddStatsHandler(webapp.RequestHandler):
   def get(self):
     que = db.Query(Stats)
     stats_list = que.fetch(limit=100)
     doRender(self, 'manageStats.htm', {'stats_list' : stats_list})
     
   def post(self):
     team = self.request.get('team')
     gp = int(self.request.get('gp'))
     w = int(self.request.get('w'))
     l = int(self.request.get('l'))
     t = int(self.request.get('t'))
     pts = int(self.request.get('pts'))
     gf = int(self.request.get('gf'))
     ga = int(self.request.get('ga'))
     plusminus = int(self.request.get('plusminus'))
     sog = int(self.request.get('sog'))
     tpm = int(self.request.get('tpm'))
     gfa = int(self.request.get('gfa'))
     gaa = int(self.request.get('gaa'))
     avg = int(self.request.get('avg'))
     newStats = Stats(team=team, gp=gp, w=w, l=l, t=t, 
     pts=pts, gf=gf, ga=ga, plusminus=plusminus, sog=sog,
     tpm=tpm, gfa=gfa, gaa=gaa, avg=avg).put()
     que = db.Query(Stats)
     stats_list = que.fetch(limit=100)
     doRender(self, 'manageStats.htm', {'stats_list' : stats_list})
  	
class LogoutHandler(webapp.RequestHandler):

  def get(self):
    self.session = Session()
    self.session.delete('username')
    self.session.delete('userkey')
    doRender(self, 'index.htm')

class MainHandler(webapp.RequestHandler):

  def get(self):
    if doRender(self,self.request.path) :
      return
    doRender(self,'index.htm')

def main():
  application = webapp.WSGIApplication([
     ('/login', LoginHandler),
     ('/apply', ApplyHandler),
     ('/manage', ManageHandler),
     ('/manageStats', ManageStatsHandler),
     ('/manageSched', ManageSchedHandler),
     ('/schedules', SchedulesHandler),
     ('/statistics', StatisticsHandler),
     ('/addEvent', AddEventHandler),
     ('/addStats', AddStatsHandler),
     ('/chat', ChatHandler),
     ('/messages', MessagesHandler),
     ('/logout', LogoutHandler),
     ('/.*', MainHandler)],
     debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
