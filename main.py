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
from ciphers import caesar, substitution, transposition, vigenere, affine



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
	txtinput=txtinput.lower()
	mode=self.request.get('mode')
	
	if (txtinput =='show files' or txtinput == 'sf'):
	    txtinput="Show Files: Ciphers.py Subsitution.py transposition.py vigenere.py Affine.py ciphers.py"
        elif (txtinput == "help" or txtinput =='h'):
	    txtinput="Would you like to go to the tutorial for the Caesar cipher(chelp or ch), Substitution cipher(shelp or sh), Transposition cipher(thelp or th), Vigenere cipher(vhelp or vh), or Affine cipher(ahelp or ah)? You can also type toolbox(toolbox or tb) to use the ciphers."
	elif(txtinput == "chelp" or txtinput=="ch"):
		txtinput="The Caesar cipher works by substituting letters for different letters a certain number away from the original letter. For example, the letter 'A' with a key of 2 would become 'C' because C is 2 letters away from 'A'. The word 'CAT' would be encoded to say 'ECV'. To figure out the key to decode a message, you can keep trying numbers between 1 and 26 until one decodes the message into something that makes sense."
	elif(txtinput == "shelp" or txtinput=="sh"):
		txtinput="The substitution cipher has a key of 26 letters, each one in the alphabet, all reordered, and matches the old letters of the alphabet to the new ones. So if the letter 'A' maps to 'V' because it is the first letter of the key, 'B' maps to 'Q' because 'Q' is the second letter in the key. If 'T' maps to 'P', the code word for 'TAB' would be 'PVQ'."
	elif(txtinput == "thelp" or txtinput=="th"):
		txtinput="The transposition cipher works by mapping different letters to columns in a table, and then putting the rows of the table together to make the ciphertext. For example, to encode the sentence 'The apple is red.' with a key of 3, the cipher will make a table with 3 columns. Because there are 17 characters in this sentence, we take 17/3 which gives 5 with a remainder of 2. This means we need 6 rows and one space will not be used since there are 17 characters and 18 table entries. The cipher will put one letter in each column of the table so that they read [T,h,e; ,a,p;p,l,e; ,i,s; ,r,e;d,.,X] (commas separate columns, semicolumns separate rows) The resulting ciphertext will go down each column one at a time putting together the characters, giving the ciphertext 'T p  dhalir.epese'"
	elif(txtinput == "vhelp" or txtinput=="vh"):
		txtinput="The Vigenere cipher works almost like the Caesar cipher, except for every letter, the number of letters it shifts is different. The alphabet index of each letter in the key tells how many letters to shift each letter of plaintext. To encode the sentence 'The sky is blue' with the key 'cat', the index of each letter in the key 'cat' is the shift number. The first letter of the message 'T' will shift 3 letters since the first letter of the key is 'c', and its index is 3. So, the first letter of the ciphertext will be 'W'. The next letter will shift 1 because the index of a is one, so 'h' will become 'i'. The index of 't' is 20, so 'e' will shift 20 to become 'y'. When the letters in the key run out, it just starts over, so the next letter of the message 's' will shift 3 to 'v' because the next shift will be the letter 'c' again."
	elif(txtinput == "ahelp" or txtinput=="ah"):
		txtinput="The affine cipher has a few more steps than the other ciphers. First, it maps each letter of the plaintext to its alphabetic index starting at 0. The word 'SLEUTH' would map to the numbers 18, 11, 4, 20, 19, 7. Let's say we want to include special characters in our encoded alphabet, which will now have a length of 96 instead of 26. We then need to select two numbers for the key, and the first number has to be coprime with 96, meaning it does not share any factors with 96. Since 96's prime factors are 2 and 3, the first part of the key can be any number not divisible by 2 or 3. Our numbers a and b will be used in the equation ax+b, where x is the letter index and the result of which needs to be bigger than 96 for reasons we'll explain in a minute. We'll choose a to be 31 and b to be 57. When we use each letter's index as x in the equation, we get 615, 398, 181, 677, 646, 274. To map these numbers to our alphabet of symbols and letters, we need them to be mod 96. This means we want to divide them by 96 and use the remainder as the new number. After doing that, our new numbers are 39, 14, 85, 5, 70, 82. To get our key, we can multiply a by 96 and add b, which gives us 3033. Mapping the new numbers to their indexes in our alphabet gives us the ciphertext '&lTcEQ'."
	elif(txtinput == "tb" or txtinput=='toolbox'):
	    txtinput="You have selected toolbox. Please select a mode(e for Encryption, d for Decryption) and type a message( ex: d-Hello )?"
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
	else:
	    txtinput="Error, invalid command! Please type again."
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
	    txtinput="You have chosen Caesar cipher. Your mode is " + mode +" and your message is " + msg +". Please enter key size(1-26) as key-{key size} (ex ckey-22)"
	
	elif (txtinput == 'key'):
	    key=self.request.get("keynum")
	    caes = caesar.CaesarCipherTool(mode,msg)
	    #get key
	    if(int(key) >= 1 and int(key) <= 26):
		txtinput="Your key is " + key
		caes.storekey(key)
		txtinput="Your translated message: " + caes.getTranslatedMessage() + ". Please type tb for toolbox, h for help"
		
	    else:
		txtinput="Your key is not valid it must be in range (1 <= key <= 26). Please try again. key-{key size} (ex ckey-22)" + key
	
	else:
	    txtinput="Error, invalid command! Please type again. Please select which cipher you would like to use - Caesar cipher(c), Substitution cipher(s), Transposition cipher(t), Vigenere cipher(v), or Affine cipher(a). Please type \"use-cipher method\"(ex - use-s)"  
	    
	array = {'text': txtinput}	    
        
       
        # Output the JSON
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(array))

class SubstitutionHandler(webapp.RequestHandler):
    def post(self):
	self.session=Session()
	mode = self.session.get("mode")
	msg=self.session.get("msg")
	
        txtinput = self.request.get('method')
	
	if (txtinput=='s'):
	    txtinput="You have chosen Substitution. Your mode is " + mode +" and your message is " + msg +". Please enter the 26-letter string of characters to use as a key (ex skey-QWERTYUIOPASDFGHJKLZXCVBNM)" 
	elif (txtinput == 'key'):
	    key=str(self.request.get("keystr"))
	    subs = substitution.SubstitutionCipherTool(mode,msg)
	    if (subs.checkValidKey(key) != True):
			txtinput="The key you entered is not valid. Please re-enter the 26-letter string of characters to use as a key (ex skey-QWERTYUIOPASDFGHJKLZXCVBNM)"
	    else:
			subs.storekey(key)
			translated=subs.getTranslatedMessage()
			txtinput="Your translated message is " + translated
	    
	else:
	    txtinput="Error, invalid command! Please type again. Please select which cipher you would like to use - Caesar cipher(c), Substitution cipher(s), Transposition cipher(t), Vigenere cipher(v), or Affine cipher(a). Please type \"use-cipher method\"(ex - use-s)"
	array = {'text': txtinput}	    
        
       
        # Output the JSON
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(array))
	
class TransHandler(webapp.RequestHandler):
    def post(self):
	self.session=Session()
	mode = self.session.get("mode")
	msg=self.session.get("msg")
	
        txtinput = self.request.get('method')
	
	if (txtinput=='t'):
	    txtinput="You have chosen Transposition cipher. Your mode is " + mode +" and your message is " + msg +". Please enter a key(1<= key <= length of your message) (ex: tkey-3)" 
	elif (txtinput == 'key'):
	    key=int(self.request.get("keystr"))
	    maxlen=len(msg)
	    trans = transposition.TranspositionCipherTool(mode,msg,maxlen)
	    keynum=trans.display()
	    if(key >= 1 and key <= int(maxlen)):
		trans.storekey(key)
		translated=trans.getTranslatedMessage()
		txtinput="Your translated message is " + translated
	    else:
		self.session.delete_item("msg")
		txtinput="Your key is not valid. Please re-enter a new message( ex: tmsg-{'This is message'})"
	elif (txtinput=='tmsg'):
	    msg=self.request.get("keystr")
	    self.session['msg']=msg
	    txtinput="Please enter a key(1<= key <= length of your message) (ex: tkey-3)"
	else:
	    txtinput="Error, invalid command! Please type again. Please select which cipher you would like to use - Caesar cipher(c), Substitution cipher(s), Transposition cipher(t), Vigenere cipher(v), or Affine cipher(a). Please type \"use-cipher method\"(ex - use-s)"
	    
	    
	    
	   
	    
		
	    
	    
	array = {'text': txtinput}	    
        
       
        # Output the JSON
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(array))
	
class VigenereHandler(webapp.RequestHandler):
    
      def post(self):
	self.session=Session()
	mode = self.session.get("mode")
	msg=self.session.get("msg")
	
        txtinput = self.request.get('method')
	
	if (txtinput=='v'):
	    txtinput="You have chosen Vigenere cipher. Your mode is " + mode +" and your message is " + msg +". Please enter a string of letters to use as a key(ex: vkey-ELFMENG)" 
	elif (txtinput == 'key'):
	    key=self.request.get("keystr")
	    vig = vigenere.VigenereCipherTool(mode,msg)
	    vig.storekey(key)
	    translated=vig.getTranslatedMessage()
	    txtinput="Your translated message is " + translated
	else:
	    txtinput="Error, invalid command! Please type again. Please select which cipher you would like to use - Caesar cipher(c), Substitution cipher(s), Transposition cipher(t), Vigenere cipher(v), or Affine cipher(a). Please type \"use-cipher method\"(ex - use-s)"
	    
	    
	array = {'text': txtinput}	    
        
       
        # Output the JSON
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(array))

class AffineHandler(webapp.RequestHandler):
    
    
    
    def post(self):
	self.session=Session()
	mode = self.session.get("mode")
	msg=self.session.get("msg")
	symbols=""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\] ^_`abcdefghijklmnopqrstuvwxyz{|}~"""
	lenofsym=len(symbols)
	maxsize=len(msg)
        txtinput = self.request.get('method')
	
	if (txtinput=='a'):
	    txtinput="You have chosen Affine cipher. Your mode is " + mode +" and your message is " + msg + ". Please enter a key (ex: akey-87)."
	    
	elif (txtinput == 'key'):
	    key=self.request.get("keynum")
	    aff = affine.AffineCipherTool(mode,msg,maxsize,lenofsym)
	    #get key
	    if(aff.storeKey(key) == False):
	        	txtinput = aff.badKey
	    else:
		translated = aff.getTranslatedMessage()
		txtinput="Your translated message is " + translated
	else:
	    txtinput="Error, invalid command! Please type again. Please select which cipher you would like to use - Caesar cipher(c), Substitution cipher(s), Transposition cipher(t), Vigenere cipher(v), or Affine cipher(a). Please type \"use-cipher method\"(ex - use-s)"
	    
	
	    
	    
	    
	array = {'text': txtinput}	    
        
       
        # Output the JSON
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(array))
	
	
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
					('/trans', TransHandler),
					('/vig', VigenereHandler),
					('/affine', AffineHandler),
					('/.*', MainHandler)], debug=True)
					
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main ()
