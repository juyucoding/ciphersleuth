import math
import random
import os
import wsgiref.handlers
from google.appengine.ext import webapp
#from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from util.sessions import Session
	  
class LoginHandler(webapp.RequestHandler):
  def get(self):
   
    existing=self.request.get('ex') 
    #self.response.out.write(existing)
    
    #checking if it is for an existing member or a new member
    if existing == '1':
	temp=os.path.join(os.path.dirname(__file__), 'templates/existingmem.html')
	#self.response.out.write(temp)
    else:
        temp=os.path.join(os.path.dirname(__file__), 'templates/newmem.html')
	#self.response.out.write(temp)
	
    
    #temp = os.path.join(os.path.dirname(__file__), 'login/login.html')
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(str(template.render(temp, {})))
    
  def post(self):
    
    self.session = Session()
    acct = self.request.get('id')
    pw = self.request.get('pwd')
  
    if (acct == 'admin' and pw == 'admin'):
      self.session['username'] = acct
      temp = os.path.join(os.path.dirname(__file__), 'setting/game_control.html')
      self.response.headers['Content-Type'] = 'text/html'
      self.response.out.write(str(template.render(temp, {'username':acct})))
    
    else:
	temp = os.path.join(os.path.dirname(__file__), 'login/login.html')
        self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp, {'error':"Error! Please type a correct ID and a password!"})))

class MainHandler(webapp.RequestHandler):
    def get (self):

      filepath = self.request.path
        
      try:
        temp = os.path.join(os.path.dirname(__file__), 'templates' + filepath)
	
      	self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(str(template.render(temp,{'path':filepath})))
        #self.response.out.write(filepath)
      except:
      	 temp = os.path.join(os.path.dirname(__file__), 'templates/main.html')
	 #self.response.out.write(temp)
	 self.response.headers['Content-Type'] = 'text/html'
	 self.response.out.write(str(template.render(temp,{'path':filepath})))
	 
class sampleHandler(webapp.RequestHandler):
   
    def get (self):
      
      data=self.request.get('sample')
      array={'data':data}
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write(json.dumps(array))
      
def main ():
  application = webapp.WSGIApplication ([('/sample', sampleHandler),
					('/login', LoginHandler),
					('/.*', MainHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main ()
