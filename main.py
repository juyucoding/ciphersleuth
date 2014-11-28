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
from random import randint


class TeacherDB(db.Model):
    teacher_name = db.StringProperty
    teacher_id=db.StringProperty
    teacher_class_id=db.StringProperty
	
class StudentDB(db.Model):
	student_name = db.StringProperty()
	student_id = db.StringProperty()
	gameid = db.IntegerProperty()
	classid = db.IntegerProperty()
	level_1 = db.BooleanProperty(default=False)
	level_2 = db.BooleanProperty(default=False)
	level_3 = db.BooleanProperty(default=False)
	level_4 = db.BooleanProperty(default=False)
	level_5 = db.BooleanProperty(default=False)
	attempt = db.IntegerProperty(default=0)
	last_login = db.DateTimeProperty(auto_now=True)
	'''
	@classmethod
	def newID(cls):
		num = random.randint(10000,99999)
		sid = 'S%s' % num
		studentprof = StudentDB.get_by_id(sid)
		while studentprof:
			num = random.randint(10000,99999)
			sid = 'S%s' % num
			studentprof = StudentDB.get_by_id(sid)
		return sid
	@classmethod
	def oldID(cls, id_num):
		studentprof = StudentDB.get_by_id(id_num)
		if studentprof:
			return True
		else:
			return False
	@classmethod
	def existingStudent(cls, id_num):
		return StudentDB.get_by_id(id_num)
	'''
class ExistingHandler(webapp.RequestHandler):
    
    def post(self):
	
	self.session=Session()
	role=self.request.get("role")
	id_lookup= self.request.get("idlookup")
	
	
	if (role == "student"):
	    temp=os.path.join(os.path.dirname(__file__), 'templates/studentmain.html')
	    #sid_lookup=StudentDB.gql("WHERE student_id=" + id_lookup)
	    #sid=sid_lookup.student_id
	    #sName = sid_lookup.student_name
	    #sClass = sid_lookup.classid
    
	    sName=id_lookup
	    existMsg=""
	    if (sName):
		#self.session['id'] = sid
		self.session['username'] = sName
		self.session['role'] = 'student'

		existMsg="Welcome back, " + sName
	    else:
		existMsg="Sorry you are not registered yet student"
	    
	elif (role == "teacher"):
	    temp=os.path.join(os.path.dirname(__file__), 'templates/teachermain.html')
	    #tid_lookup=TeacherDB.gql("WHERE teacher_id=" + id_lookup)
	    #tName = tid_lookup.teacher_name
    
	    tName=id_lookup
	    
	    existMsg=""
	    if (tName):
		#self.session['id'] = tid
		self.session['username'] = tName
		self.session['role'] = 'teacher'

		existMsg="Welcome back, " + tName
	    else:
		existMsg="Sorry you are not registered yet"
	
	
	self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp,{"emsg":role})))
  
class tNewHandler(webapp.RequestHandler):

  
  def post(self):

    self.session = Session()
    
    que = db.Query(TeacherDB)
    db.delete(que)
	      
    tname=self.request.get("tname")
	    
    if (self.request.get("teacherid")):
	tid=tname+str(randint(10000,99999))
	self.session['id'] = tid
	self.session['username'] = tname
	self.session['role'] = 'teacher'
	
    tclassid=self.request.get('tclassid')
	    
    #Create new db for teacher
    newDB = TeacherDB(teacher_name=tname, teacher_id=tid, teacher_class_id=tclassid)
    newDB.put()
	     
    temp=os.path.join(os.path.dirname(__file__), 'templates/logint.html')
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(str(template.render(temp,{"tid":tid, "tid_msg":"Your userID is:  ", "tclassid_msg":"Your class id is:  ", "tclassid":tclassid})))
    

class sNewHandler(webapp.RequestHandler):

  
  def post(self):

    self.session = Session()
    
    que = db.Query(StudentDB)
    db.delete(que)
	      
    sname=self.request.get("sname")
    sid=sname+str(randint(10000,99999))
    self.session['id'] = sid
    self.session['username'] = sname
    self.session['role'] = 'student'
	
    sclassid=self.request.get('sclassid')
	    
    #Create new db for student
    newDB = StudentDB(username=sname, sid=sid, classid=sclassid)
    newDB.put()
	     
    temp=os.path.join(os.path.dirname(__file__), 'templates/logins.html')
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(str(template.render(temp,{"sid":sid, "sid_msg":"Your userID is:  ", "sclassid_msg":"Your class id is:  ", "sclassid":sclassid})))	
	

class LogoutHandler(webapp.RequestHandler):
    
    def get(self):
	
	    
	self.session=Session()
	self.session.delete_item('username')
	self.session.delete_item('role')
	self.session.delete_item('tid')
	
	logoutmsg="You are now logged out"
	
	temp = os.path.join(os.path.dirname(__file__), 'templates/logout.html')
	
      	self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(str(template.render(temp,{"logoutmsg":logoutmsg})))
	
	
class LoginHandler(webapp.RequestHandler):
  
  def get (self):
	#self.response.out.write(self.request.get('out'))
	existing = self.request.get("exist")
    
	if existing == '1':
	    temp=os.path.join(os.path.dirname(__file__), 'templates/existingcheck.html')
	else:
	    temp=os.path.join(os.path.dirname(__file__), 'templates/newmem.html')

		
	self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp,{})))
     
    
  def post(self):
    
    #self.session = Session()
    role=self.request.get("role")
    #self.response.out.write(test)
    
    if (role=='TEACHER'):
	temp=os.path.join(os.path.dirname(__file__), 'templates/logint.html')
    else:
	temp=temp=os.path.join(os.path.dirname(__file__), 'templates/logins.html')
	
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(str(template.render(temp,{})))
	
    '''
    self.session['username'] = acct
    temp = os.path.join(os.path.dirname(__file__), 'setting/game_control.html')
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(str(template.render(temp, {'username':acct})))
    
    
    temp = os.path.join(os.path.dirname(__file__), 'login/login.html')
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(str(template.render(temp, {'error':"Error! Please type a correct ID and a password!"})))
    '''
class MainHandler(webapp.RequestHandler):
    def get (self):

	    
	#filepath = self.request.path
	self.session = Session()
      
	loggedUser=""
	greeting=""
	if (self.session.get('username')):
		greeting="Welcome, "
		loggedUser = self.session.get('username')
      	
	
	if (self.session.get('role') == 'teacher'):
	    
	   
	    temp = os.path.join(os.path.dirname(__file__), 'templates/teachermain.html')
	     #self.response.out.write(temp)
	    self.response.headers['Content-Type'] = 'text/html'
	    self.response.out.write(str(template.render(temp,{'loggedUser':loggedUser, "greeting":greeting})))
	 
	elif (self.session.get('role') == 'student'):
	    
	    temp = os.path.join(os.path.dirname(__file__), 'templates/studentmain.html')
	     #self.response.out.write(temp)
	    self.response.headers['Content-Type'] = 'text/html'
	    self.response.out.write(str(template.render(temp,{'loggedUser':loggedUser, "greeting":greeting})))
	 
	else:
	    
	    temp = os.path.join(os.path.dirname(__file__), 'templates/main.html')
	    self.response.headers['Content-Type'] = 'text/html'
	    self.response.out.write(str(template.render(temp,{'loggedUser':loggedUser, "greeting":greeting})))
      
class SmainHandler(webapp.RequestHandler):
   
    def get(self):
	self.session=Session()
	
	username = self.session.get("username")
	operation = self.request.get("op")
	
	#control
	if(operation=='0'):
	    temp = os.path.join(os.path.dirname(__file__), 'templates/scontrol.html')
	    self.response.headers['Content-Type'] = 'text/html'
	    self.response.out.write(str(template.render(temp,{})))
	#start a new game
	elif(operation=='1'):
	    temp = os.path.join(os.path.dirname(__file__), 'templates/sgameintro.html')
	    self.response.headers['Content-Type'] = 'text/html'
	    self.response.out.write(str(template.render(temp,{"username":username})))
	else:
	    temp = os.path.join(os.path.dirname(__file__), 'templates/main.html')
	    self.response.headers['Content-Type'] = 'text/html'
	    self.response.out.write(str(template.render(temp,{})))
	    
class GameHandler(webapp.RequestHandler):
    
    
    def get(self):
	self.session=Session()
	self.session['userCheck']=0
	username=self.session.get("username")
	level=self.request.get("level")
	self.session['level']=level
	final=self.request.get("c")
	errormsg=""
	
	currentlevel=self.session.get('userCheck')
	
	if (level=='1'):
	    self.session.delete_item("userCheck")
	    self.session['userCheck']=1
	    currentlevel=self.session.get('userCheck')
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game1.html')
	
	elif (level=='2'):
	    currentlevel=self.session.get("userCheck")
	    if (currentlevel <= 1):
		errormsg="You are not allowed to the page!"
		temp = os.path.join(os.path.dirname(__file__), 'templates/game' + str(currentlevel)+'.html')
	    else:
		self.session.delete_item("userCheck")
		self.session['userCheck']=2
		currentlevel=self.session.get('userCheck')
		temp = os.path.join(os.path.dirname(__file__), 'templates/game2.html')
		
	elif (level=='3'):
	    currentlevel=self.session.get("userCheck")
	    if (currentlevel <= 2):
		errormsg="You are not allowed to the page!"
		temp = os.path.join(os.path.dirname(__file__), 'templates/game' + str(currentlevel)+'.html')
	    else:
		self.session.delete_item("userCheck")
		self.session['userCheck']=2
		currentlevel=self.session.get('userCheck')
		temp = os.path.join(os.path.dirname(__file__), 'templates/game3.html')    
	    
	elif (level=='4'):
	    self.session['userCheck']=4
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game4.html')
	elif (level=='5'):
	    self.session['userCheck']=5
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game5.html')
	elif (level=='0'):
	    self.session['userCheck']=0
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game0.html')
	elif (final=="1"):
	    temp = os.path.join(os.path.dirname(__file__), 'templates/gameterm.html')
	    
	self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp,{"username":username, "level":level+" / 5", "error_msg":currentlevel})))
    
    def post(self):
	self.session=Session() 
	username=self.session.get("username")
	level=self.session.get("level")
	operation=self.request.get("op")
	decoded=self.request.get("decodedmsg")
	error_msg=""
	msg=""
	solved=None
	flag=True
	
	
	if (operation=='11'):
	    
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game1.html')
	    if(decoded=='apple'):
		msg="CONTINUE"
		solved=1
		flag=False
	    #start session for putting the level into the db
	elif (operation=='12'):
	
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game2.html')
	    if(decoded=='banana'):
		flag=False
		solved=1
		msg="CONTINUE"	
	    
	elif (operation=='13'):
	    
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game3.html')
	    if(decoded=='kiwi'):
		flag=False
		solved=1
		msg="CONTINUE"	
	    
	elif (operation=='14'):
	    
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game4.html')
	    if(decoded=='tomato'):
		flag=False
		solved=1
		msg="CONTINUE"
		
	elif (operation=='15'):
	    
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game5.html')
	    if(decoded=='pineapple'):
		flag=False
		solved=1
		msg="CONTINUE"	
	elif (operation=='0'):
	    
	    
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game0.html')
	    if(decoded=='42'):
		
		flag=False
		solved=1
		msg="CONTINUE"
	
	
	if(flag):
	    error_msg="I'm sorry. Your decode seems incorrect. Please try again."
	    
	
	self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp,{"username":username, 'error_msg': error_msg, 'msg':msg, "level":level+" / 5", "solved":solved})))
	
def main ():
  application = webapp.WSGIApplication ([('/smain', SmainHandler),
					('/game', GameHandler),
					('/logout', LogoutHandler),
					('/tnew', tNewHandler),
					('/snew', sNewHandler),
					('/login', LoginHandler),
					('/existing', ExistingHandler),
					('/.*', MainHandler)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main ()
