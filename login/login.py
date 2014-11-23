import math
import random
import os
import wsgiref.handlers
from google.appengine.ext import webapp
#from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from util.sessions import Session
import json


class MainHandler(webapp.RequestHandler):
    def get (self):

      filepath = self.request.path
        
      try:
        temp = os.path.join(os.path.dirname(__file__), 'templates' + filepath)
	
      	self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(str(template.render(temp,{'path':filepath})))
        #self.response.out.write(filepath)
      except:
      	 temp = os.path.join(os.path.dirname(__file__), 'templates/login.html')
	 #self.response.out.write(temp)
	 self.response.headers['Content-Type'] = 'text/html'
	 self.response.out.write(str(template.render(temp,{'path':filepath})))
	 

def main ():
  application = webapp.WSGIApplication ([('/.*', MainHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main ()