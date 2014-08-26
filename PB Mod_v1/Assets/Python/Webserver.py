from CvPythonExtensions import *
import CvUtil

import SocketServer
import re
import os.path
#import os.listdir
import os
import glob
import time
import thread 
from threading import Timer,Thread,Event
import urllib
#import hashlib #Python 2.4 has no haslib use md5
import md5
import simplejson 

PB = CyPitboss()
gc = CyGlobalContext()
localText = CyTranslator()


#Default settings, only works if one PB instance is running
pbDefaultSettings = {
	"webserver": {
		"host" : "", # Leave string empty
		"port" : 13373, # Port of the python web interface of this mod. Use different port for each game
		"password" : "pw" # Password for admin commands on the webinterface
	},
	"webfrontend" : {
		"url" : "http://localhost/civ/page/update.php", # Url of the pbStats file on your http webserver 
		"gameId" : 0,
		"sendPeriodicalData" : 1, # Set 0 to disable periodical sending of game data 
		"sendInterval" : 10, # Seconds during automatic sending of game data
		},
	"save" : {
		"autostart" : 0,
		"path": ".\\saves\\multi\\",
		"filename" : "A.CivBeyondSwordSave",
		"adminpw" : ""
	},
	"numRecoverySavesPerPlayer" : 5,
	"MotD" : "Welcome on the modified PitBoss Server",
	"noGui" : 0
}
pbSettings = None

#Try to load pbSettings file.
# To get a different settings file for each pitboss we need
# access to a variable in the ini file 
# We reuse a widley unused variable of the standard BTS ini file 
altrootDir = gc.getAltrootDir()
#altrootDir = "I:\\Olaf\\PBs\\PB1" 

#Cut of badly formated beginning of String [...]@ (If EMail Ini variable used)
#altrootDir = altrootDir[altrootDir.rfind("@")+1:len(altrootDir)]

# If the loading of the setting file failed the path will be set no None in getPbSettings()
pbFn = altrootDir + "\\pbSettings.json"

def getPbSettings():
	global altrootDir
	global pbFn
	global pbSettings
	global pbDefaultSettings
	if pbSettings != None: 
		return pbSettings

	if os.path.isfile(pbFn):
		fp = file(pbFn,"r")
		pbSettings = simplejson.load(fp)
		fp.close()
		return pbSettings
	elif altrootDir != "":
		pbSettings = pbDefaultSettings
		savePbSettings()
		return pbSettings
	else:
		pbSettings = pbDefaultSettings
		pbFn = None
		return pbDefaultSettings

# Attention: Use the ThreadedTCPServer.savePbSettings to wrap this into a mutex if you saved the file over the webinterface.
# This function should only be called direct if the webserver wasn't started.
def savePbSettings():
	global pbFn
	global pbSettings
	if pbFn == None: 
		return

	try:
		fp = file(pbFn,"w")
		simplejson.dump(pbSettings,fp)
	except Exception, e:
		pass



class service(SocketServer.BaseRequestHandler):
	def handle(self):
		global pbSettings
		data = 'dummy'
		#print "Client connected with ", self.client_address
		try:
			while len(data):
				rawinputdata = self.request.recv(1024)
				inputdata = simplejson.loads(rawinputdata)

				action = inputdata.get("action")

				if( action == "chat" and inputdata.get("password") == pbSettings["webserver"]["password"] ):
					msg =  str(inputdata.get("msg","Default message. Missing msg argument?!"))
					PB.sendChat( msg )
					self.request.sendall( simplejson.dumps( {'return':'ok','info':'Send: '+msg } ) +"\n" ) 

				elif( action == "setAutostart" and inputdata.get("password") == pbSettings["webserver"]["password"] ):
						self.server.lock.acquire()
						pbSettings["save"]["autostart"] = int(inputdata.get("value",0))
						self.server.lock.release()
						self.server.savePbSettings()
						self.request.sendall( simplejson.dumps( {'return':'ok','info':'Autostart flag: ' + str(pbSettings["save"]["autostart"]) } ) +"\n" )

				elif( action == "setHeadless" and inputdata.get("password") == pbSettings["webserver"]["password"] ):
						self.server.lock.acquire()
						pbSettings["noGui"] = int(inputdata.get("value",0))
						self.server.lock.release()
						self.server.savePbSettings()
						self.request.sendall( simplejson.dumps( {'return':'ok','info':'Headless/noGui flag: ' + str(pbSettings["noGui"]) } ) +"\n" )

				elif( action == "save" and inputdata.get("password") == pbSettings["webserver"]["password"] ):
					defaultFile="Pitboss_" + PB.getGamedate(True)
					filename =  str( inputdata.get("filename",defaultFile) ) + ".CivBeyondSwordSave"
					#remove "\ or /" chars to cut of directory changes
					filename = filename[max(filename.rfind("/"),filename.rfind("\\"))+1:len(filename)]

					ret = self.server.createSave(filename)
					self.request.sendall( simplejson.dumps( ret ) +"\n" ) 

				elif( action == "setTurnTimer" and inputdata.get("password") == pbSettings["webserver"]["password"] ):
						iHours = int( inputdata.get("value",24) )
						PB.turnTimerChanged(iHours);
						self.request.sendall( simplejson.dumps( {'return':'ok','info':'Deactivate pause.' } ) +"\n" )

				elif( action == "setPause" and inputdata.get("password") == pbSettings["webserver"]["password"] ):
						bPause = int(inputdata.get("value",0))
						if bPause:
							if not gc.getGame().isPaused():
								PB.sendChat( "(Webinterface) Activate pause."  )
								gc.getGame().setPausePlayer(1) 
							self.request.sendall( simplejson.dumps( {'return':'ok','info':'Activate pause.' } ) +"\n" )
						else:
							if gc.getGame().isPaused():
								PB.sendChat( "(Webinterface) Deactivate pause."  )
								gc.getGame().setPausePlayer(1) #Do not remove this line !!!
								gc.getGame().setPausePlayer(-1)
							self.request.sendall( simplejson.dumps( {'return':'ok','info':'Deactivate pause.' } ) +"\n" )

				elif( action == "endTurn" and inputdata.get("password") == pbSettings["webserver"]["password"] ):
						#Create Backup save in auto-Folder
						filename = r"Auto_" + PB.getGamename() + r"_R" + str(PB.getGameturn()) + r"end_" + PB.getGamedate(False) + r".CivBeyondSwordSave"
						self.server.createSave(str(filename), True)

						#gc.getGame().doControl(ControlTypes.CONTROL_FORCEENDTURN)#wrong
						messageControl = CyMessageControl()
						messageControl.sendTurnCompleteAll()

						self.request.sendall( simplejson.dumps( {'return':'ok','info':'Start new round.' } ) +"\n" )

				elif( action == "restart" and inputdata.get("password") == pbSettings["webserver"]["password"] ):
					# Save current game and reload this save if no expicit filename is given
					bReload = True

					filename = str(inputdata.get("filename",""))
					autoDir =  inputdata.get("autoDir",0)
					#remove "\ or /" chars to cut of directory changes
					filename = filename[max(filename.rfind("/"),filename.rfind("\\"))+1:len(filename)]

					# Disable autoDir flag if no filename was given.
					if len(filename) == 0 :
						autoDir = 0

					# Force single autostart
					self.server.lock.acquire()
					pbSettings["save"]["oneOffAutostart"] = 1
					pbSettings["save"]["autoDir"] = autoDir
					self.server.lock.release()

					if len(filename) > 0 :
						#Save selected filename for reloading in the settings file
						filename =  filename + ".CivBeyondSwordSave"
						self.server.lock.acquire()
						pbSettings["save"]["filename"] = filename
						pbSettings["save"]["autoDir"] = autoDir
						self.server.lock.release()
						self.server.savePbSettings()
					else:
						filename = "Reload.CivBeyondSwordSave"
						ret = self.server.createSave(filename)
						if ret["return"] != "ok" :
							bReload = False
							self.request.sendall( simplejson.dumps( {'return':'fail','info':'Abort reloading. Was not able to save game.' } ) +"\n" )

					if bReload:
						# Quit server. The loop in the batch file should restart the server....
						if self.server.adminWindow != None:
							self.request.sendall( simplejson.dumps( {'return':'ok','info':'Quit pb server window.' } ) +"\n" )
							#Close socket before OnExit-Method was called
							self.request.close()
							self.server.adminWindow.OnExit(None)
						else:
							self.request.sendall( simplejson.dumps( {'return':'fail','info':'Abort reloading. Was not able to quit pb server window.' } ) +"\n" )

				elif( action == "setPlayerPassword" and inputdata.get("password") == pbSettings["webserver"]["password"] ):
						playerId = int(inputdata.get("playerId",-1))
						newCivPW = str(inputdata.get("newCivPW",r""))
						ret = -1
						if playerId > -1:
							ret = gc.getGame().setCivPassword( playerId, newCivPW, str(pbSettings.get("save",{}).get("adminpw","")) )

						if ret == 0:	
							self.request.sendall( simplejson.dumps( {'return':'ok','info':'Passwort of player ' + str(playerId) + ' changed to "' + newCivPW + '"' } ) +"\n" )
						else:
							self.request.sendall( simplejson.dumps( {'return':'fail','info':'Passwort change failed.' } ) +"\n" )

				elif( action == "info" ):
					gamedata = self.server.createGamedata()

					self.request.sendall( simplejson.dumps( {'return':'ok','info':gamedata} ) +"\n" ) 

				elif( action == "listSaves" ):
					# Print list of saves of the selected folder. This can be used for a dropdown list 
					# of available saves.
					global altrootDir
					folderpaths = [ {"path":altrootDir + "\\" + str(pbSettings["save"]["path"]), "autosave":False},
							{"path":altrootDir + "\\" + str(pbSettings["save"]["path"] + "auto\\" ), "autosave":True} ]
					saveList = []

					for fp in folderpaths:
						folderpath = fp["path"]
						for savefile in os.listdir(folderpath):
							if savefile.endswith(".CivBeyondSwordSave"):
								timestamp = os.path.getctime( folderpath+savefile )
								saveList.append( {
									'name':str(savefile),
									'autosave':fp["autosave"],
									'date':time.ctime(timestamp),
									'timestamp':timestamp
										})

					self.request.sendall( simplejson.dumps( {'return':'ok','list':saveList} ) +"\n" ) 

				else:
					self.request.sendall( simplejson.dumps( {'return':'fail','info':'Wrong password or unknown action. Available actions info, chat, save, restart, listSaves, setAutostart, setHeadless'} ) +"\n" ) 

		except Exception, e:
			#print "Exception while receiving message: ", e
			data = ''
			self.request.sendall( simplejson.dumps( {'return':'fail','info': "Exception:" + str(e)} ) + "\n" )

		self.request.close()




class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	#def __init__(self):
	#	self.adminWindow = None

	def setPbWin(self, adminWindow):
		self.adminWindow = adminWindow
		self.lock = thread.allocate_lock()
	
	def createSave(self, filename, autoDir=False):
		filepath = self.getSaveFolder(autoDir) + filename

		if (filename != ""):
			self.lock.acquire()
			if ( not PB.save(filepath) ):
				ret = {'return':'fail','info':'Saving of '+filepath+' failed.' } 
				self.lock.release()
			else:
				# Update last file name info and save json file 
				pbSettings["save"]["filename"] = filename
				pbSettings["save"]["autoDir"] = autoDir
				self.lock.release()
				self.savePbSettings()
				ret = {'return':'ok','info':'File was saved in '+filepath+'.' }  

		return ret

	def getSaveFolder(self, autoDir):
		global altrootDir
		folderpath = altrootDir + "\\" + str(pbSettings["save"]["path"])
		if autoDir:	
			folderpath += "auto\\"

		return folderpath


	def createPlayerRecoverySave(self, playerId, playerName, bOnline):
		#1. Check which saves already exists for this player
		#   and remove old recovery saves
		folder = self.getSaveFolder(True)
		RecoverPrefix = 'Logoff_'
		if bOnline:
			RecoverPrefix = 'Login_'

		existingRecoverySaves = glob.glob(folder + RecoverPrefix + str(playerId) + '*.CivBeyondSwordSave')
		# Add timestamp (as tuple)
		existingRecoverySavesWithTimestamps = map(lambda x: (x,os.path.getctime(x)), existingRecoverySaves)
		# Sort by timestamp
		sorted(existingRecoverySavesWithTimestamps, key=lambda xx: xx[1])
		#	Remove oldest
		while( len(existingRecoverySavesWithTimestamps) >= pbSettings.get("numRecoverySavesPerPlayer",3) ):
			old = existingRecoverySavesWithTimestamps.pop(0)
			os.remove(old[0])

		#2. Save new recovery save
		filename = RecoverPrefix + str(int(time.time())) + '_P' + str(playerId) + '_' + playerName + '.CivBeyondSwordSave'
		self.createSave( str(filename), True)



	def createGamedata(self):
		#Collect all available data
		gamedata = {'gameTurn':PB.getGameturn(),
				'gameName':PB.getGamename(),
				'gameDate':PB.getGamedate(False),
				'bPaused':gc.getGame().isPaused(),
				}

		if( PB.getTurnTimer() ):
			gamedata["turnTimer"] = 1
			gamedata['turnTimerMax'] = gc.getGame().getPitbossTurnTime()
			gamedata['turnTimerValue'] = PB.getTurnTimeLeft()
		else:
			gamedata["turnTimer"] = 0

		players = []		
		for rowNum in range(gc.getMAX_CIV_PLAYERS()):
			gcPlayer = gc.getPlayer(rowNum)
			if (gcPlayer.isEverAlive()):
				playerData = PB.getPlayerAdminData(rowNum)
				player = {'id':rowNum}
				player['finishedTurn'] = not playerData.bTurnActive
				player['name'] = playerData.getName()
				player['score'] = playerData.getScore()
				player['ping'] = playerData.getPing()
				player['bHuman'] = playerData.bHuman
				player['bClaimed'] = playerData.bClaimed
				player['civilization'] = gcPlayer.getCivilizationDescription(0)
				player['leader'] = gc.getLeaderHeadInfo(gcPlayer.getLeaderType()).getDescription()
				player['color'] = u"%d,%d,%d" % ( gcPlayer.getPlayerTextColorR(), gcPlayer.getPlayerTextColorG(), gcPlayer.getPlayerTextColorB()  )
				
				players.append(player)

		gamedata['players'] = players	
		return gamedata


	def savePbSettings(self):
		self.lock.acquire()
		#Call non-member function
		savePbSettings()
		self.lock.release()



# Class to invoke request from to the 'client' side of webinterface

class PerpetualTimer:#():

	def __init__(self,settings,webserver):
		self.settings = settings
		self.t = settings['sendInterval']
		self.tFirst = self.t + 10
		self.webserver = webserver
		self.hFunction = self.request
		self.thread = Timer(self.tFirst,self.handle_function)

	def handle_function(self):
		self.hFunction(self.webserver)
		self.thread = Timer(self.t,self.handle_function)
		self.thread.start()

	def start(self):
		self.thread.start()

	def cancel(self):
		self.thread.cancel()

	def request(self,webserver):
		gamedata = webserver.createGamedata()
		url = self.settings["url"]
		gameId = self.settings["gameId"]
		#pwHash = hashlib.sha512(b'hello').hexdigest()
		pwHash = md5.new( pbSettings['webserver']['password'] ).hexdigest()
		params = urllib.urlencode({'action': 'update','id':gameId, 'pwHash':pwHash, 'info': simplejson.dumps({'return':'ok','info':gamedata}) })
		try:
			#f = urllib.urlopen("%s?%s" % (url,params) ) #GET method
			f = urllib.urlopen(url, params) #POST method

			#Write log file
			"""
			try:
				xxx = "Z:\\dev\\shm\\foo.txt";
				fp = file(xxx,"w")
				simplejson.dump({"A":"loop","B":f.read()},fp)
			except Exception, e:
				pass
			"""

		except:
			pass


