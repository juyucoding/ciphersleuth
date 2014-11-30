import math
import random
import os
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from util.sessions import Session
import json
#from django.utils import simplejson as json
from random import randint
from ciphers import caesar



class TeacherDB(db.Model):
    teacher_name = db.StringProperty()
    teacher_id=db.StringProperty()
    teacher_class_id=db.StringProperty()
	

class StudentDB(db.Model):
    student_name = db.StringProperty()
    student_id = db.StringProperty()
    game_id = db.StringProperty()
    classid = db.StringProperty()
    level_1 = db.BooleanProperty(default=False)
    level_2 = db.BooleanProperty(default=False)
    level_3 = db.BooleanProperty(default=False)
    level_4 = db.BooleanProperty(default=False)
    level_5 = db.BooleanProperty(default=False)
    attempt = db.IntegerProperty(default=0)
    last_login = db.DateTimeProperty(auto_now=True)

class GameDB(db.Model):
    student_id= db.StringProperty()
    game_id = db.StringProperty()
    current_level=db.IntegerProperty()
    completion=db.BooleanProperty(default=False)
    active_time=db.DateTimeProperty(auto_now=True)
    
class ExistingHandler(webapp.RequestHandler):
    
    def post(self):
	
	self.session=Session()
	role=self.request.get("role")
	id_lookup= self.request.get("idlookup")
	
	
	if (role == "student"):
	    temp=os.path.join(os.path.dirname(__file__), 'templates/studentmain.html')
	    #lookup=StudentDB.gql("WHERE student_id = :1",id_lookup)
	    lookup=(db.GqlQuery("SELECT * FROM StudentDB WHERE student_id = :1", id_lookup)).get()
	    sName = lookup.student_name
	    sClass = lookup.classid
    
	    sid=id_lookup
	    #sName=id_lookup
	    existMsg=""
	    if (sName):
		self.session['id'] = sid
		self.session['username'] = sName
		self.session['role'] = 'student'

		existMsg="Welcome back, " + sName
	    else:
		existMsg="Sorry you are not registered yet student"
	    
	elif (role == "teacher"):
	    temp=os.path.join(os.path.dirname(__file__), 'templates/teachermain.html')
	    lookup=(db.GqlQuery("SELECT * FROM TeacherDB WHERE teacher_id = :1", id_lookup)).get()
	    tName = lookup.teacher_name
	    tClass = lookup.teacher_class_id
    
	    tid=id_lookup
	    existMsg=""
	    if (tName):
		self.session['id'] = tid
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
    self.response.out.write(str(template.render(temp,{"tid":tid, "tid_msg":"UserID is:  ", "tclassid_msg":"Class id is:  ", "tclassid":tclassid})))
    

class sNewHandler(webapp.RequestHandler):

  
  def post(self):

    self.session = Session()
    
    #que = db.Query(StudentDB)
    #db.delete(que)
	      
    sname=self.request.get("sname")
    sid=sname+str(randint(10000,99999))
    self.session['id'] = sid
    self.session['username'] = sname
    self.session['role'] = 'student'
	
    sclassid=self.request.get('sclassid')
	    
    #Create new db for student
    newDB = StudentDB(student_name=sname, student_id=sid, classid=sclassid)
    newDB.put()
	     
    temp=os.path.join(os.path.dirname(__file__), 'templates/logins.html')
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(str(template.render(temp,{"sid":sid, "sid_msg":"UserID is:  ", "sclassid_msg":"Class id is:  ", "sclassid":sclassid})))	
	
class ExitHandler(webapp.RequestHandler):
    def get(self):
	self.session=Session()
	self.session.delete_item('username')
	self.session.delete_item('role')
	self.session.delete_item('tid')
	self.session.delete_item('level')
	self.session.delete_item('game_id')
	
	msg="Thank you for playing. Bye!"
	
	temp = os.path.join(os.path.dirname(__file__), 'templates/logout.html')
	
      	self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(str(template.render(temp,{"logoutmsg":msg})))
	
class LogoutHandler(webapp.RequestHandler):
    
    def get(self):
	
	    
	self.session=Session()
	self.session.delete_item('username')
	self.session.delete_item('role')
	self.session.delete_item('tid')
	self.session.delete_item('level')
	self.session.delete_item('game_id')
	
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
	elif existing == '0':
	    temp=os.path.join(os.path.dirname(__file__), 'templates/newmem.html')

     
	role=self.request.get("role")
	if (role=='1'):
	    temp=os.path.join(os.path.dirname(__file__), 'templates/logint.html')
	elif(role=='2'):
	    temp=temp=os.path.join(os.path.dirname(__file__), 'templates/logins.html')
	
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
	
	userid=self.session.get("id")
	username = self.session.get("username")
	operation = self.request.get("op")
	error_msg=""
	goback=""
	#control
	if(operation=='0'):
	    result=(db.GqlQuery("SELECT * FROM GameDB WHERE student_id = :1", userid)).fetch(limit=100)
	    
	    temp = os.path.join(os.path.dirname(__file__), 'templates/scontrol.html')
	    self.response.headers['Content-Type'] = 'text/html'
	    self.response.out.write(str(template.render(temp,{"loggedUser":username, "result":result})))
	#start a new game
	elif(operation=='1'):
	    temp = os.path.join(os.path.dirname(__file__), 'templates/sgameintro.html')
	    self.response.headers['Content-Type'] = 'text/html'
	    self.response.out.write(str(template.render(temp,{"username":username})))
	elif(operation=='2'):
	    greeting="Hello, "
	    temp = os.path.join(os.path.dirname(__file__), 'templates/gameload.html')
	    
	    result=(db.GqlQuery("SELECT * FROM GameDB WHERE student_id = :1", userid)).fetch(limit=100)
	    if (len(result) == 0):
		error_msg="Error! No saved game!"
		goback="Back to Main"
	    self.response.headers['Content-Type'] = 'text/html'
	    self.response.out.write(str(template.render(temp,{"greeting": greeting, "username":userid, "result":result,"error_msg":error_msg, "goback":goback})))
    	else:
	    temp = os.path.join(os.path.dirname(__file__), 'templates/main.html')
	    self.response.headers['Content-Type'] = 'text/html'
	    self.response.out.write(str(template.render(temp,{})))

class DetailHandler(webapp.RequestHandler):
    def get(self):
	self.session=Session()
	logged_id=self.session.get("id")
	sid=self.request.get("id")
	result=(db.GqlQuery("SELECT * FROM StudentDB WHERE student_id = :1", sid)).fetch(limit=100)
	
	temp = os.path.join(os.path.dirname(__file__), 'templates/tdetail.html')
	self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp,{'loggedUser':logged_id, "result":result})))
	
class TmainHandler(webapp.RequestHandler):
    def get(self):
	self.session=Session()
	logged_name=self.session.get("username")
	logged_id=self.session.get("id")
	greeting="Hello"
	
	lookup=(db.GqlQuery("SELECT * FROM TeacherDB WHERE teacher_id = :1", logged_id)).get()
	classid_teacher=lookup.teacher_class_id
	result=(db.GqlQuery("SELECT * FROM StudentDB WHERE classid = :1", classid_teacher)).fetch(limit=100)
	 	
	temp = os.path.join(os.path.dirname(__file__), 'templates/tcontrol.html')
	self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp,{'loggedUser':logged_id, "greeting":greeting,"result":result})))

class GameloadHandler(webapp.RequestHandler):
    
    def get(self):
	self.session=Session()
	start_msg=""	
	gid=self.request.get("gid")
	
	self.session['game_id']=gid
	#get current level for game id
	result_game=(db.GqlQuery("SELECT * FROM GameDB WHERE game_id = :1", gid)).get()
    	glevel=result_game.current_level
	if (glevel):
	    start_msg="START THE GAME"
	#level=self.request.get("level")
	if (self.session.get('level')):
	    self.session.delete_item('level')
	self.session['level']=glevel

	
	temp = os.path.join(os.path.dirname(__file__), 'templates/gameload.html')
	self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp,{"start_msg":start_msg,"level":glevel})))
	
	
class GameHandler(webapp.RequestHandler):
    
    
    def get(self):
	self.session=Session()

	self.session['userCheck']=0
	userid=self.session.get("id")
	username=self.session.get("username")
	level=self.request.get("level")
	if (self.session.get('level')):
	    self.session.delete_item('level')
	self.session['level']=level
	final=self.request.get("c")
	errormsg=""
    	
	
	result_student=(db.GqlQuery("SELECT * FROM StudentDB WHERE student_id = :1", userid)).get()
	
	if (level=='1'):
	    self.session.delete_item('userCheck')
	    self.session['userCheck']=1
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game1.html')
	    
	    current_level=int(level)
	    #create a new gamedb for the user
	    if (self.session.get('game_id')):
		gameid=self.session.get('gid')
	    else:	
		gameid=userid + "_" + str(randint(1,99999))
		self.session['game_id']=gameid
		
	    newDB = GameDB(student_id=userid, game_id=gameid,current_level=current_level)
	    newDB.put()
	    
	    #update StudentDB with the new gameid
	    result_student.game_id=gameid
	    result_student.attempt=0
	    result_student.level_1=False
	    result_student.level_2=False
	    result_student.level_3=False
	    result_student.level_4=False
	    result_student.level_5=False
	    result_student.put()
	    
	    
	elif (level=='2'):
	    self.session.delete_item('userCheck')
	    self.session['userCheck']=2
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game2.html')
	    current_level=int(level)
	    gameid=self.session.get("game_id")
	    result_game=(db.GqlQuery("SELECT * FROM GameDB WHERE game_id = :1", gameid)).get()
	    
	    #update game DB with current level
	    result_game.current_level=current_level
	    result_game.put()
	    
	    #update student DB with current level
	    result_student.attempt=current_level
	    result_student.put()
	    
	elif (level=='3'):
	    self.session.delete_item('userCheck')
	    self.session['userCheck']=3
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game3.html')
	    current_level=int(level)
	    
	    gameid=self.session.get("game_id")
	    result_game=(db.GqlQuery("SELECT * FROM GameDB WHERE game_id = :1", gameid)).get()
	    result_game.current_level=current_level
	    result_game.put()
	    
	    #update student DB with current level
	    result_student.attempt=current_level
	    result_student.put()	
	elif (level=='4'):
	    self.session.delete_item('userCheck')
	    self.session['userCheck']=4
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game4.html')
	    current_level=int(level)
	    
	    gameid=self.session.get("game_id")
	    result_game=(db.GqlQuery("SELECT * FROM GameDB WHERE game_id = :1", gameid)).get()
	    
	    result_game.current_level=current_level
	    result_game.put()
	    
	    #update student DB with current level
	    result_student.attempt=current_level
	    result_student.put()	
	elif (level=='5'):
	    self.session.delete_item('userCheck')
	    self.session['userCheck']=5
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game5.html')
	    current_level=int(level)
	    
	    gameid=self.session.get("game_id")
	    result_game=(db.GqlQuery("SELECT * FROM GameDB WHERE game_id = :1", gameid)).get()
	    
	    result_game.current_level=current_level
	    result_game.put()
	    
	    #update student DB with current level
	    result_student.attempt=current_level
	    result_student.put()	
	elif (level=='0'):
	    self.session['userCheck']=0
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game0.html')
	    
	    gameid=self.session.get("game_id")
	    result_game=(db.GqlQuery("SELECT * FROM GameDB WHERE game_id = :1", gameid)).get()
	    
	    result_game.completion=True
	    result_game.put()
	    
	elif (final=="1"):
	    temp = os.path.join(os.path.dirname(__file__), 'templates/gameterm.html')
	    
	self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp,{"username":username, "level":level+" / 5", "error_msg":errormsg})))
    
    def post(self):
	self.session=Session()
	userid=self.session.get("id")
	username=self.session.get("username")
	level=self.session.get("level")
	operation=self.request.get("op")
	decoded=self.request.get("decodedmsg")
	error_msg=""
	msg=""
	solved=None
	flag=True
	
	result=(db.GqlQuery("SELECT * FROM StudentDB WHERE student_id = :1", userid)).get()
	
	decoded=decoded.upper()
	if (operation=='11'):
	    
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game1.html')
	    if(decoded=='GO TO LIBRARY'):	
		result.level_1=True
		msg="CONTINUE"
		solved=1
		flag=False
	    #start session for putting the level into the db
	elif (operation=='12'):
	
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game2.html')
	    if(decoded=='GET MYSTERY OF TIME AND GO TO AIRPORT'):
		result.level_2=True
		flag=False
		solved=1
		msg="CONTINUE"	
	    
	elif (operation=='13'):
	    
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game3.html')
	    if(decoded=='HE HAS BROWN HAIR, RED SCARF, YELLOW SHOES'):
		result.level_3=True
		flag=False
		solved=1
		msg="CONTINUE"	
	    
	elif (operation=='14'):
	    
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game4.html')
	    if(decoded=='I LOVE YELLOW AND SKY IS PURPLE'):
		result.level_4=True
		flag=False
		solved=1
		msg="CONTINUE"
		
	elif (operation=='15'):
	    
	    temp = os.path.join(os.path.dirname(__file__), 'templates/game5.html')
	    if(decoded=='GO TO GRANDMA HOUSE CODE IS 42'):
		result.level_5=True
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
	    
	result.put()
	self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp,{"username":username, 'error_msg': error_msg, 'msg':msg, "level":level+" / 5", "solved":solved})))

class SavingHandler(webapp.RequestHandler):
    def get(self):
	self.session=Session()
	level=self.session.get("userCheck")
	username=self.session.get("username")
	userid=self.session.get("id")    
	#Create new db for student

	result=(db.GqlQuery("SELECT * FROM StudentDB WHERE student_id = :1", userid)).get()
	result.attempt=level
	result.put()
	
	level=str(level)
	
	addr="game" + level
	msg="Your game is saved"
	temp=os.path.join(os.path.dirname(__file__), 'templates/'+addr +'.html')
	self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp,{"username":username,'msg':msg, "level":level+" / 5"})))

class TerminalHandler(webapp.RequestHandler):
    def post(self):
	echo=self.request.get("msg")
	username=''
	msg=''
	level=''
	
	temp=os.path.join(os.path.dirname(__file__), 'templates/game1.html')
	self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp,{"username":username,'msg':msg, "level":level+" / 5", "echo":echo})))
	
class CipherInterfaceHandler(webapp.RequestHandler):
    def get(self):
	temp=os.path.join(os.path.dirname(__file__), 'templates/sample.html')
	self.response.headers['Content-Type'] = 'text/html'
	self.response.out.write(str(template.render(temp,{})))
	
    def post(self):
        # Our POST Input
	self.session=Session()
        txtinput = self.request.get('txtValue')
	mode=self.request.get('mode')
	
	if (txtinput == 'show files'):
	    txtinput="Show Files: Ciphers.py Subsitution.py"
        elif (txtinput == "help" or txtinput =='h'):
	    txtinput="Would you like to go to the tutorial for the Caesar cipher(c), Substitution cipher(s), Transposition cipher(t), Vigenere cipher(v), or Affine cipher(a)? You can also type toolbox(tb) to use the ciphers."  
	elif(txtinput == "tb"):
	    txtinput="You have selected toolbox. Please select a mode(e for Encryption, d for Decryption) and type a message( ex- d(mode),Hello(message) )?"
	elif(mode=='e' or mode=='d'):
	    self.session.delete_item('mode')
	    self.session['mode']=mode
	    msg=self.request.get('msg')
	    self.session.delete_item('msg')
	    self.session['msg']=msg
	    if (mode =='e'):
		mo="Encryption"
	    else:
		mo="Decryption"
	    txtinput="You have chosen " + mo +" and your message is " + msg + ". Please select which cipher you would like to use - Caesar cipher(c), Substitution cipher(s), Transposition cipher(t), Vigenere cipher(v), or Affine cipher(a). Please type \"use-cipher method\"(ex - use-s)"
	
	array = {'text': txtinput}	    
        
       
        # Output the JSON
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(array))

class CaesarHandler(webapp.RequestHandler):
    def post(self):
	self.session=Session()
	mode = self.session.get("mode")
	msg=self.session.get("msg")
	
        txtinput = self.request.get('method')
	
	if (txtinput=='c'):
	    txtinput="You have chosen Caesar cipher. Your mode is " + mode +" and your message is " + msg +". Please enter key size(1-26) as key-{key size} (ex key-22)" 
	elif (txtinput == 'key'):
	    key=self.request.get("keynum")
	    caes = caesar.CaesarCipherTool(mode,msg)
	    #get key
	    if(int(key) >= 1 and int(key) <= 26):
		txtinput="Your key is " + key
		caes.storekey(key)
		txtinput="Your translated message: " + caes.getTranslatedMessage() + ". Please type tb for toolbox, h for help"
		
	    else:
		txtinput="Your key is not valid it must be in range (1 <= key <= 26). Please try again. key-{key size} (ex key-22)" + key
	    
	    
	array = {'text': txtinput}	    
        
       
        # Output the JSON
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(array))

class SubstitutionHandler(webapp.RequestHandler):
    
	
	
def main ():
  application = webapp.WSGIApplication ([('/tdetail', DetailHandler),
					('/gameload',GameloadHandler),
					('/saving', SavingHandler),
					('/smain', SmainHandler),
					('/game', GameHandler),
					('/logout', LogoutHandler),
					('/tnew', tNewHandler),
					('/snew', sNewHandler),
					('/login', LoginHandler),
					('/existing', ExistingHandler),
					('/tmain', TmainHandler),
					('/exiting', ExitHandler),
					('/terminal', TerminalHandler),
					('/cipherInter', CipherInterfaceHandler),
					('/caesar', CaesarHandler),
					('/sub', SubstitutionHandler),
					('/.*', MainHandler)], debug=True)
					
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main ()
