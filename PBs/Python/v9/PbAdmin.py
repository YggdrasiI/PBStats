# -*- coding: utf-8 -*-
# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
#
# Pitboss admin framework
# Dan McGarry 3-24-05
#
import sys
import os
import time
import string
from threading import Thread
import wx
import wx.lib.scrolledpanel

from CvPythonExtensions import *  # Do not remove this
import CvPythonExtensions as E
import Webserver

PB = E.CyPitboss()
gc = E.CyGlobalContext()
LT = E.CyTranslator()

# Add Altroot python folder as import path
pythonDir = os.path.join(gc.getAltrootDir(), '..', 'Python', 'v9')
if pythonDir not in sys.path:
    sys.path.append(pythonDir)
from Settings import Settings

PbSettings = Settings() #.instance()
CHAT_LOG_MAX_LEN = 50

# Pipe error messages into a file to avoid popup windows
errorLogFile = PbSettings.get("errorLogFile", None)
if errorLogFile is not None:
    logName = os.path.join(gc.getAltrootDir(), str(errorLogFile))
    try:
        os.unlink(logName, logName+".old")
    except Exception, e:
        pass
    try:
        os.rename(logName, logName+".old")
    except Exception, e:
        pass

    sys.stderr = open(logName, 'w')


playerWasOnline = []  # To track login and logout events
for _ in range(gc.getMAX_CIV_PLAYERS()):
    playerWasOnline.append(False)

#
# resource IDs
#
ID_ABOUT = 101
ID_SAVE = 102
ID_EXIT = 103

#
# admin frame class
#
class AdminFrame(wx.Frame):
    bShellInit = False

    # def __init__(self, parent, ID, title):  # Orig
    def __init__(self, parent, ID, title, adminApp):
        "constructor"

        super(AdminFrame, self).__init__(parent, ID, title)
        self.adminApp = adminApp

        # self.bGui = (0 == int(PbSettings.get("noGui", 0)))  # Old key name
        self.bGui = (int(PbSettings.get("gui", 1)) != 0)
        self.bAutostart = (int(PbSettings.get("autostart", 0)) != 0)
        self.bShell = (int(PbSettings.get("shell", {}).get("enable", 0)) != 0)
        self.civ4Shell = {}  #  Holds shell object and some extra variables
        self.gameTurn = -1  # For pylint

        if self.bGui:
            self.createGui(parent, ID, title)

        if self.bShell:
            self.bShellInit = True  # Init shell on first update() call
            # self.init_shell()  # To early?!

        # Webserver
        self.webserver = Webserver.ThreadedHTTPServer(
            (PbSettings['webserver']['host'], PbSettings['webserver']['port']),
            Webserver.HTTPRequestHandler)
        self.t = Thread(target=self.webserver.serve_forever)
        self.t.setDaemon(True)
        self.t.start()

        # Periodical game data upload
        self.webupload = None
        if(PbSettings['webfrontend']['sendPeriodicalData'] != 0):
            self.webupload = Webserver.PerpetualTimer(PbSettings['webfrontend'],
                                                      self.webserver, True)
            self.webupload.start()

        bRestorePassword = (int(PbSettings.get("restorePassword", 0)) != 0)
        if bRestorePassword:
            adminPwd = str(PbSettings.get("save", {}).get("adminpw", ""))
            if hasattr(E.CyGame(), "setAdminPassword"):
                E.CyGame().setAdminPassword(adminPwd, "")
                PbSettings.createSave("PostUpdate.CivBeyondSwordSave")
                PbSettings.lock.acquire()
                PbSettings.pop("restorePassword", None)
                PbSettings.lock.release()
                PbSettings.save()
            else:
                PB.consoleOut("restorePassword-Flag is set in pbSettings, "
                              "but DLL does not contain setAdminPassword "
                              "method.")

    def init_shell(self):
        self.civ4Shell = {
            "glob": globals(),
            "loc": locals(),
            "shell": start_shell(PbSettings.get("shell", {}), "pb_admin")
        }
        if self.civ4Shell.get("shell"):
            PB.consoleOut("Init shell interface in PbAdmin")
            self.civ4Shell["shell"].set_admin_iface(self.adminApp)
            self.civ4Shell["shell"].init()
        else:
            self.bShell = False

    def createGui(self, parent, ID, title):
        # Create the menu
        wx.Frame.__init__(self, parent, ID, title,
                          wx.DefaultPosition, wx.Size(675, 480))

        menu = wx.Menu()
        menu.Append(ID_ABOUT, (LT.getText("TXT_KEY_PITBOSS_ABOUT", ())), (LT.getText("TXT_KEY_PITBOSS_ABOUT_TEXT", ())))
        menu.AppendSeparator()
        menu.Append(ID_SAVE, (LT.getText("TXT_KEY_PITBOSS_SAVE", ())), (LT.getText("TXT_KEY_PITBOSS_SAVE_TEXT", ())))
        menu.Append(ID_EXIT, (LT.getText("TXT_KEY_PITBOSS_EXIT", ())), (LT.getText("TXT_KEY_PITBOSS_EXIT_TEXT", ())))
        menuBar = wx.MenuBar()
        strFile = LT.getText("TXT_KEY_PITBOSS_FILE", ())
        strFile = LT.stripHTML(strFile)
        menuBar.Append(menu, strFile)
        self.SetMenuBar(menuBar)

        # Create our arrays of information and controls
        self.nameArray = []
        self.pingArray = []
        self.scoreArray = []
        self.kickArray = []

        pageSizer = wx.BoxSizer(wx.VERTICAL)

        # Add the game name and date
        self.gameTurn = PB.getGameturn()
        self.title = wx.StaticText(self, -1, PB.getGamename() + " - " + PB.getGamedate(False))
        font = wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.title.SetFont(font)
        self.title.SetSize(self.title.GetBestSize())
        pageSizer.Add(self.title, 0, wx.ALL, 5)

        # Add the turn timer if we have one
        if (PB.getTurnTimer()):
            timerSizer = wx.BoxSizer(wx.HORIZONTAL)

            # Add a button to allow turn timer modification
            timerChangeButton = wx.Button(self, -1, LT.getText("TXT_KEY_MP_OPTION_TURN_TIMER", ()))
            self.Bind(wx.EVT_BUTTON, self.OnChangeTimer, timerChangeButton)
            timerSizer.Add(timerChangeButton, 0, wx.ALL, 5)

            timerPauseButton = wx.Button(self, -1, LT.getText("TXT_KEY_MOD_PAUSE_TIMER", ()))
            self.Bind(wx.EVT_BUTTON, self.OnChangePause, timerPauseButton)
            timerSizer.Add(timerPauseButton, 0, wx.ALL, 5)

            self.timerDisplay = wx.StaticText(self, -1, "")

            timerStr = self.getTimerString(PB.getTurnTimeLeft())
            self.timerDisplay.SetLabel(timerStr)

            font = wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL)
            self.timerDisplay.SetFont(font)
            self.timerDisplay.SetSize(self.timerDisplay.GetBestSize())
            timerSizer.Add(self.timerDisplay, 0, wx.ALL, 5)

            pageSizer.Add(timerSizer, 0, wx.ALL, 5)

        infoSizer = wx.BoxSizer(wx.HORIZONTAL)
        leftSizer = wx.BoxSizer(wx.VERTICAL)

        playerPanel = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(370, 280), style=wx.DOUBLE_BORDER)
        playerSizer = wx.BoxSizer(wx.VERTICAL)

        # Create a row for each player in the game
        rowNum = 0
        for rowNum in range(gc.getMAX_CIV_PLAYERS()):
            if (gc.getPlayer(rowNum).isEverAlive()):
                # Create the border box
                border = wx.StaticBox(playerPanel, -1, (LT.getText("TXT_KEY_PITBOSS_PLAYER", (rowNum+1, ))), (0, (rowNum*30)))
                # Create the layout mgr
                rowSizer = wx.StaticBoxSizer(border, wx.HORIZONTAL)

                # Player name
                itemSizer = wx.BoxSizer(wx.VERTICAL)
                lbl = wx.StaticText(playerPanel, -1, (LT.getText("TXT_KEY_PITBOSS_WHO", ())))
                txtValue = wx.StaticText(playerPanel, rowNum, "", size=wx.Size(100, 13))
                itemSizer.Add(lbl)
                itemSizer.Add(txtValue)
                rowSizer.Add(itemSizer, 0, wx.ALL, 5)
                self.nameArray.append(txtValue)

                # Ping times
                itemSizer = wx.BoxSizer(wx.VERTICAL)
                lbl = wx.StaticText(playerPanel, -1, (LT.getText("TXT_KEY_PITBOSS_PING", ())))
                txtValue = wx.StaticText(playerPanel, rowNum, "", size=wx.Size(70, 13))
                itemSizer.Add(lbl)
                itemSizer.Add(txtValue)
                rowSizer.Add(itemSizer, 0, wx.ALL, 5)
                self.pingArray.append(txtValue)

                # Scores
                itemSizer = wx.BoxSizer(wx.VERTICAL)
                lbl = wx.StaticText(playerPanel, -1, (LT.getText("TXT_KEY_PITBOSS_SCORE", ())))
                txtValue = wx.StaticText(playerPanel, rowNum, "", size=wx.Size(30, 13))
                itemSizer.Add(lbl)
                itemSizer.Add(txtValue)
                rowSizer.Add(itemSizer, 0, wx.ALL, 5)
                self.scoreArray.append(txtValue)

                # Kick buttons
                kickButton = wx.Button(playerPanel, rowNum, (LT.getText("TXT_KEY_PITBOSS_KICK", ())))
                rowSizer.Add(kickButton, 0, wx.ALL, 5)
                kickButton.Disable()
                self.Bind(wx.EVT_BUTTON, self.OnKick, kickButton)
                self.kickArray.append(kickButton)

                playerSizer.Add(rowSizer, 0, wx.ALL, 5)

        playerPanel.SetSizer(playerSizer)
        playerPanel.SetAutoLayout(1)
        playerPanel.SetupScrolling()
        leftSizer.Add(playerPanel, 0, wx.ALL, 5)

        # Add a button row
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add the save game button
        saveButton = wx.Button(self, -1, (LT.getText("TXT_KEY_PITBOSS_SAVE_GAME", ())))
        self.Bind(wx.EVT_BUTTON, self.OnSave, saveButton)
        buttonSizer.Add(saveButton, 0, wx.ALL, 5)

        # Add the exit game button
        exitButton = wx.Button(self, -1, (LT.getText("TXT_KEY_MAIN_MENU_EXIT_GAME", ())))
        self.Bind(wx.EVT_BUTTON, self.OnExit, exitButton)
        buttonSizer.Add(exitButton, 0, wx.ALL, 5)

        leftSizer.Add(buttonSizer, 0, wx.ALL, 5)

        # Add the left area to the info area
        infoSizer.Add(leftSizer, 0, wx.ALL, 5)

        # Now create the message area
        messageSizer = wx.BoxSizer(wx.VERTICAL)

        # Create the MotD Panel
        motdBorder = wx.StaticBox(self, -1, LT.getText("TXT_KEY_PITBOSS_MOTD_TITLE", ()))
        motdSizer = wx.StaticBoxSizer(motdBorder, wx.VERTICAL)

        # Check box whether to use MotD or not
        self.motdCheckBox = wx.CheckBox(self, -1, LT.getText("TXT_KEY_PITBOSS_MOTD_TOGGLE", ()))
        self.motdCheckBox.SetValue(len(PbSettings.get('MotD', u'')) > 0)
        motdSizer.Add(self.motdCheckBox, 0, wx.TOP, 5)

        # Add edit box displaying current MotD
        self.motdDisplayBox = wx.TextCtrl(self, -1, "", size=(225, 50), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.motdDisplayBox.SetHelpText(LT.getText("TXT_KEY_PITBOSS_MOTD_HELP", ()))

        msg_unicode = PbSettings.get('MotD', u'')
        self.motdDisplayBox.SetValue(msg_unicode.encode('cp1252'))

        motdSizer.Add(self.motdDisplayBox, 0, wx.ALL, 5)
        # Add a button to allow motd modification
        motdChangeButton = wx.Button(self, -1, LT.getText("TXT_KEY_PITBOSS_MOTD_CHANGE", ()))
        motdChangeButton.SetHelpText(LT.getText("TXT_KEY_PITBOSS_MOTD_CHANGE_HELP", ()))
        self.Bind(wx.EVT_BUTTON, self.OnChangeMotD, motdChangeButton)
        motdSizer.Add(motdChangeButton, 0, wx.ALL, 5)

        # Add the motd area to the message area
        messageSizer.Add(motdSizer, 0, wx.ALL, 5)

        # Create the dialog panel
        dialogBorder = wx.StaticBox(self, -1, LT.getText("TXT_KEY_PITBOSS_CHAT_TITLE", ()))
        dialogSizer = wx.StaticBoxSizer(dialogBorder, wx.VERTICAL)

        # Chat log
        self.chatLog = wx.TextCtrl(self, -1, "", size=(225, 100), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.chatLog.SetHelpText(LT.getText("TXT_KEY_PITBOSS_CHAT_LOG_HELP", ()))
        dialogSizer.Add(self.chatLog, 0, wx.ALL, 5)

        # Chat edit
        self.chatEdit = wx.TextCtrl(self, -1, "", size=(225, -1), style=wx.TE_PROCESS_ENTER)
        self.chatEdit.SetHelpText(LT.getText("TXT_KEY_PITBOSS_CHAT_EDIT_HELP", ()))
        dialogSizer.Add(self.chatEdit, 0, wx.ALL, 5)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSendChat, self.chatEdit)

        # Add the dialog area to the message area
        messageSizer.Add(dialogSizer, 0, wx.ALL, 5)

        # Add the message area to our info area
        infoSizer.Add(messageSizer, 0, wx.ALL, 5)

        # Add the info area to the page
        pageSizer.Add(infoSizer, 0, wx.ALL, 5)

        self.SetSizer(pageSizer)

        # Register the event handlers
        wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, ID_SAVE, self.OnSave)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)

        # Other handlers
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def getTimerString(self, turnSlices):
        # Get the time string for the turn timer...
        # See if we are out of time

        # Only update every second
        retVal = self.timerDisplay.GetLabel()
        if (turnSlices % 4 == 0):
            if (turnSlices < 0):
                retVal = "0:00:00"
            else:
                numHours = 0
                numMinutes = 0
                numSeconds = turnSlices/4
                if (numSeconds > 59):
                    numMinutes = numSeconds/60
                    numSeconds = numSeconds % 60
                    if (numMinutes > 59):
                        numHours = numMinutes/60
                        numMinutes = numMinutes % 60

                retVal = ""
                if (numHours > 0):
                    retVal = str(numHours)
                else:
                    retVal = "0"
                retVal += ":"

                if (numMinutes > 9):
                    retVal += str(numMinutes)
                elif (numMinutes > 0):
                    retVal += "0" + str(numMinutes)
                else:
                    retVal += "00"
                retVal += ":"

                if (numSeconds > 9):
                    retVal += str(numSeconds)
                elif (numSeconds > 0):
                    retVal += "0" + str(numSeconds)
                else:
                    retVal += "00"

        return retVal

    def update(self):
        if self.bGui:
            # We have the widgets created, set the values...
            if (self.gameTurn != PB.getGameturn()):
                self.title.SetLabel(PB.getGamename() + " - " + PB.getGamedate(False))
                self.gameTurn = PB.getGameturn()

            if (PB.getTurnTimer()):
                timerStr = self.getTimerString(PB.getTurnTimeLeft())
                if (timerStr != self.timerDisplay.GetLabel()):
                    self.timerDisplay.SetLabel(timerStr)

            for rowNum in range(gc.getMAX_CIV_PLAYERS()):
                if (gc.getPlayer(rowNum).isEverAlive()):
                    # Get the player data
                    playerData = PB.getPlayerAdminData(rowNum)

                    # Set the values
                    nameDisplay = ""
                    if (not playerData.bTurnActive):
                        nameDisplay += "*"

                    # PB Mod: Fix Non-ASCII decoding error
                    # .getName()-function returns unicode string
                    # which needs to be proper encoded.
                    nameDisplay += playerData.getName().encode('cp1252')

                    #nameDisplay += "Player %i" % (rowNum+1)
                    if (nameDisplay != self.nameArray[rowNum].GetLabel()):
                        self.nameArray[rowNum].SetLabel(nameDisplay)

                    if ((playerData.getPing()) != self.pingArray[rowNum].GetLabel()):
                        self.pingArray[rowNum].SetLabel((playerData.getPing()))

                    if ((playerData.getScore()) != self.scoreArray[rowNum].GetLabel()):
                        self.scoreArray[rowNum].SetLabel((playerData.getScore()))

                    bEnabled = self.kickArray[rowNum].IsEnabled()
                    bShouldEnable = (playerData.bHuman and playerData.bClaimed)
                    if (bEnabled != bShouldEnable):
                        if (bShouldEnable):
                            self.kickArray[rowNum].Enable(True)
                        else:
                            self.kickArray[rowNum].Disable()

        # Create save on login and logout events
        for rowNum in range(gc.getMAX_CIV_PLAYERS()):
            # gcPlayer = gc.getPlayer(rowNum)
            bOnline = (PB.getPlayerAdminData(rowNum).getPing()[1] == "[")
            if (bOnline != playerWasOnline[rowNum]):
                playerName = PB.getPlayerAdminData(rowNum).getName().encode('cp1252')
                PbSettings.createPlayerRecoverySave(rowNum, playerName, bOnline)
                playerWasOnline[rowNum] = bOnline

        if self.bShell:
            if self.bShellInit:
                self.bShellInit = False
                self.init_shell()
            else:
                try:
                    self.civ4Shell["shell"].update(
                        self.civ4Shell["glob"],
                        self.civ4Shell["loc"])
                except Exception, e:
                    PB.consoleOut("Civ4Shell error:" + str(e))

        if not self.bGui:
            try:
                # This try-catch clause does not omit all python error windows
                # because there exists a second .sleep call in PbMain.py. This class
                # can not be changed by a modification.
                time.sleep(0.1)
            except KeyboardInterrupt:
                self.OnExit(None)

    def OnKick(self, event):
        "'kick' event handler"
        rowNum = event.GetId()
        dlg = wx.MessageDialog(
            self,
            (LT.getText("TXT_KEY_PITBOSS_KICK_VERIFY", (PB.getName(rowNum), ))),
            (LT.getText("TXT_KEY_PITBOSS_KICK_VERIFY_TITLE", ())),
            wx.YES_NO | wx.ICON_QUESTION)

        if (dlg.ShowModal() == wx.ID_YES):
            PB.kick(rowNum)

        dlg.Destroy()

    def OnAbout(self, event):
        "'about' event handler"
        dlg = wx.MessageDialog(
            self,
            (LT.getText("TXT_KEY_PITBOSS_VERSION", (PB.getVersion(), ))),
            (LT.getText("TXT_KEY_PITBOSS_ABOUT_BOX_TITLE", ())),
            wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnSave(self, event):
        "'save' event handler"
        dlg = wx.FileDialog(
            self, message=(LT.getText("TXT_KEY_PITBOSS_SAVE_AS", ())),
            # defaultDir=r".\Saves\multi",
            defaultDir=(gc.getAltrootDir() + r".\Saves\multi"),
            defaultFile="Pitboss_"+PB.getGamedate(True)+".CivBeyondSwordSave",
            wildcard=(LT.getText("TXT_KEY_PITBOSS_SAVE_AS_TEXT", ())) +
            " (*.CivBeyondSwordSave)|*.CivBeyondSwordSave",
            style=wx.SAVE | wx.OVERWRITE_PROMPT)

        if dlg.ShowModal() == wx.ID_OK:
            # Get the file name
            path = dlg.GetPath()
            if (path != ""):
                # Got a file to save - try to save it
                if (not PB.save(path)):
                    # Saving game failed!  Let the user know
                    wx.MessageBox(
                        (LT.getText("TXT_KEY_PITBOSS_ERROR_SAVING", ())),
                        (LT.getText("TXT_KEY_PITBOSS_SAVE_ERROR", ())),
                        wx.ICON_ERROR)
                else:
                    wx.MessageBox(
                        (LT.getText("TXT_KEY_PITBOSS_SAVE_SUCCESS", (path, ))),
                        (LT.getText("TXT_KEY_PITBOSS_SAVED", ())),
                        wx.ICON_INFORMATION)

        dlg.Destroy()

    def OnChangeMotD(self, event):
        "'MotD' event handler"

        # Changing MotD - pop a modal dialog
        dlg = wx.TextEntryDialog(
            self, LT.getText("TXT_KEY_PITBOSS_MOTD_POPUP_DESC", ()),
            LT.getText("TXT_KEY_PITBOSS_MOTD_POPUP_TITLE", ()))

        # Show the modal dialog and get the response
        if dlg.ShowModal() == wx.ID_OK:
            # Set the MotD
            msg = dlg.GetValue()  # GetValue is str in cp1252 enc
            self.motdDisplayBox.SetValue(msg)
            PbSettings['MotD'] = msg.decode('cp1252')

    def OnChangePause(self, event):
        "Turn pause event handler"
        if gc.getGame().isPaused():
            # gc.sendPause(-1)  # effect not as expected
            # gc.sendChat("RemovePause", E.ChatTargetTypes.CHATTARGET_ALL)
            PB.sendChat("RemovePause")
        else:
            gc.sendPause(0)
            self.timerDisplay.SetLabel("Game paused.")

            """ Note that the index for the barbarian could
            lead to an c++ exception.
            A test case for the bug follows...
            """
            # gc.sendPause(gc.getMAX_CIV_PLAYERS()-1)


    def OnChangeTimer(self, event):
        "Turn timer event handler"

        # Changing Timer - pop a modal dialog
        dlg = wx.TextEntryDialog(
            self, LT.getText("TXT_KEY_PITBOSS_TURN_TIMER_NEW", ()),
            LT.getText("TXT_KEY_MP_OPTION_TURN_TIMER", ()))
        dlg.SetValue("%s" % (gc.getGame().getPitbossTurnTime(), ))

        # Show the modal dialog and get the response
        if dlg.ShowModal() == wx.ID_OK:
            szValue = dlg.GetValue()
            if szValue != "":
                if not self.IsNumericString(szValue):
                    dlg2 = wx.MessageDialog(
                        self, LT.getText("TXT_KEY_PITBOSS_TURNTIMER_ERROR_DESC", ()),
                        LT.getText("TXT_KEY_PITBOSS_TURNTIMER_ERROR_TITLE", ()), wx.OK | wx.ICON_EXCLAMATION)

                    if dlg2.ShowModal() == wx.ID_OK:
                        # Clear out the TurnTimer Edit box
                        dlg.SetValue("")
                else:
                    PB.turnTimerChanged((int)(dlg.GetValue()))

    def OnSendChat(self, event):
        "'Chat Send' event handler"

        # Verify we have text to send
        chat_msg = self.chatEdit.GetValue()
        if (len(chat_msg)):
            PB.sendChat(chat_msg)
            self.chatEdit.SetValue("")

            # PB Mod: Store text in log as unicode
            self.chat_log = self.chat_log[0:CHAT_LOG_MAX_LEN-1]
            self.adminApp.chat_log.append(message.decode('cp1252'))

    def OnExit(self, event):
        "'exit' event handler"
        PB.quit()
        self.webserver.shutdown()
        if self.webupload:
            self.webupload.cancel()

        if self.bShell:
            if "shell" in self.civ4Shell:
                self.civ4Shell["shell"].close()
            # global Civ4Shell
            # Civ4Shell["shell"].close()

        if event != "FromOnClose":
            self.Destroy()

    def OnCloseWindow(self, event):
        "'close window' event handler"
        # PB.quit()
        self.OnExit("FromOnClose")
        self.Destroy()

    def IsNumericString(self, myStr):
        for myChar in myStr:
            if myChar not in string.digits:
                return False
        return True
#
# main app class
#

class AdminIFace(wx.App):

    adminFrame = None
    chat_log = []

    # def __init__(self, arg1):   # Required if not derived from wx.App
    #     self.OnInit()
    #

    def OnInit(self):
        "create the admin frame"
        self.adminFrame = AdminFrame(None, -1,
                                     LT.getText("TXT_KEY_PITBOSS_SAVE_SUCCESS", (PB.getGamename(), )),
                                     self)
        if self.adminFrame.bGui:
            self.adminFrame.Show(True)
            self.SetTopWindow(self.adminFrame)

        self.adminFrame.webserver.setPbApp(self)
        return True

    def update(self):
        "process events - call in main loop"

        if self.adminFrame:  # Check avoids PyDeadObjectError
            if self.adminFrame.bGui:
                # Create an event loop and make it active.
                # save the old one
                evtloop = wx.EventLoop()
                old = wx.EventLoop.GetActive()
                wx.EventLoop.SetActive(evtloop)

                # Update our view
                self.adminFrame.update()

                # This inner loop will process any GUI events
                # until there are no more waiting.
                while evtloop.Pending():
                    evtloop.Dispatch()

                # Send idle events to idle handlers.
                time.sleep(0.1)  # Orig value was 0.01
                self.ProcessIdle()

                # restore old event handler
                wx.EventLoop.SetActive(old)
            else:
                if self.adminFrame:  # Check avoids PyDeadObjectError
                    self.adminFrame.update()

    def refreshRow(self, iRow):
        "Stub for refresh row..."
        return True

    def getMotD(self):
        "Message of the day retrieval"
        if self.adminFrame.bGui and self.adminFrame.motdCheckBox.GetValue():
            msg = self.adminFrame.motdDisplayBox.GetValue()  # str in cp1252 enc
            PbSettings["MotD"] = msg.decode('cp1252')
            return msg

        msg = PbSettings.get('MotD', u'')  # here, type is unicode
        return msg

    def setMotD(self, msg):
        if not self.adminFrame.bGui:
            return

        # msg is unicode
        self.adminFrame.motdDisplayBox.SetValue(msg.encode('cp1252'))

    def addChatMessage(self, message):
        message = LT.stripHTML(message)

        # PB Mod: Store text in log as unicode
        self.chat_log = self.chat_log[0:CHAT_LOG_MAX_LEN-1]
        # self.chat_log.append(message.decode('cp1252'))
        self.chat_log.append(message)  # already decoded

        if not self.adminFrame.bGui:
            return
        self.adminFrame.chatLog.AppendText("\n")
        self.adminFrame.chatLog.AppendText(message)

    def displayMessageBox(self, title, desc):
        outMsg = title + ":\n" + desc
        PB.consoleOut(outMsg)

    def sendChatMessage(self, message, sound_variant=0):
        # Use multiple modNetMessages to propagate text to users
        # Encoding:
        #  • Send utf-8-encoded string, but restrict
        #  • Propagate unicode string to addChatMessage
        # Function returns True or error message

        if isinstance(message, unicode):
            message = message.encode('utf-8')

        # 1. split messages into 4*4 + 3 Bytes
        first = True
        n_bytes = 4*4 + 3
        msg__ = message + " " * ((n_bytes - len(message)) % (n_bytes))

        def bytes_to_signed_int(b1, b2, b3, b4):
            # Little endian

            # Converts numbers into 0-255 (negatives =>255)
            b1, b2, b3, b4 = b1 & 0xFF, b2 & 0xFF, b3 & 0xFF, b4 & 0xFF

            if b4 > 127:
                x = (b1 << 0) | (b2 << 8) | (b3 << 16) | ((b4-128) << 24)
                x = -x
            else:
                x = (b1 << 0) | (b2 << 8) | (b3 << 16) | (b4 << 24)

            # Alternative:
            # bit_len = 32-1
            # u = (b1 << 0) | (b2 << 8) | (b3 << 16) | (b4 << 24)
            # x = (u & ((1 << bit_len) - 1)) - (u & (1 << bit_len))

            return x

        while len(msg__) > 0:
            # Grab first 18 bytes and shorten message
            c = [ord(c) for c in msg__[:n_bytes] ]
            msg__ = msg__[n_bytes:]

            # 2. Mark with flags as chat text
            flag = 0x70 # Mark as chat messages in iData5
            if first:  # First part, set bx01110100 flag
                first = False
                flag |= 0x04
            if len(msg__) == 0:  # Last part, set bx01111000 flag
                flag |= 0x08

            # Add sound flags (0-3)
            flag |= min(3, abs(sound_variant))

            # 3. Convert text chunk into signed integers
            words = [bytes_to_signed_int(c[0], c[1], c[2], c[3]),
                     bytes_to_signed_int(c[4], c[5], c[6], c[7]),
                     bytes_to_signed_int(c[8], c[9], c[10], c[11]),
                     bytes_to_signed_int(c[12], c[13], c[14], c[15]),
                     bytes_to_signed_int(c[16], c[17], c[18], flag)]
                     # Last entry set lower 3 bytes + flags

            CyMessageControl().sendModNetMessage(
                words[0], words[1], words[2], words[3], words[4])

        # 5. Store message in textbox.
        # Add message directly to chat because method is not easly reachable
        # by CvEventManager's onModNetMessage call
        try:
            self.addChatMessage(message.decode('utf-8'))
        except Exception, e:
            return "Message send, but addChatMessage failed. Error: " + str(e)

        if gc.getGame().isPaused():
            return "Warning: Message delayed until game is unpaused."

        return True

    # Short, but not working variant. Added for reference.
    def modChatMessage2(self, message, sound_variant=0):
        # Test of direct way: (Fails if triggered in this thread?!)
        gc.getGame().setActivePlayer(gc.getBARBARIAN_PLAYER(), False)
        gc.sendChat(message, -1)  # Requires active player > -1
        gc.getGame().setActivePlayer(-1, False)

        return True


# ================ PB Mod ===================
def start_shell(shell_settings, mode=""):
    if shell_settings.get("enable", 0):
        import Civ4ShellBackend
        shell_ip = str(shell_settings.get("ip", "127.0.0.1"))
        shell_port = int(shell_settings.get("port", 3333))
        shell = Civ4ShellBackend.Server(shell_ip, shell_port)
        shell.set_mode(mode)

        return shell
    else:
        return None
