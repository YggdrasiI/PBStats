# -*- coding: utf-8 -*-
import sys
import time
import string
import os.path
import wx
import wx.wizard
import wx.lib.scrolledpanel

from CvPythonExtensions import *
import Webserver

PB = CyPitboss()
gc = CyGlobalContext()
LT = CyTranslator()

# Add Altroot python folder as import path
pythonDir = os.path.join(gc.getAltrootDir(), '..', 'Python', 'v8')
if pythonDir not in sys.path:
    sys.path.append(pythonDir)
from Settings import Settings

msgBox = None
curPage = None
bPublic = True
bSaved = False
bScenario = False

PbSettings = Settings() #.instance()

class ModSelectPage(wx.wizard.PyWizardPage):
    # Mod Select Page (first page of wizard)

    def __init__(self, parent):
        wx.wizard.PyWizardPage.__init__(self, parent)
        self.next_page = self.prev_page = None
        self.myParent = parent

        pageSizer = wx.BoxSizer(wx.VERTICAL)

        modPanel = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(300, 600), style=wx.SUNKEN_BORDER)
        sizer = wx.BoxSizer(wx.VERTICAL)

        header = wx.StaticText(self, -1, LT.getText("TXT_KEY_PITBOSS_CHOOSE_MOD", ()))
        pageSizer.Add(header, 0, wx.ALL, 5)

        # Place the radio buttons
        self.currentMod = 0
        self.rbs = []

        # First choice is no mod
        self.rbs.append(wx.RadioButton(
            modPanel, -1, LT.getText("TXT_KEY_MAIN_MENU_NONE", ()), wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP
            ))
        sizer.Add(self.rbs[0], 0, wx.ALL, 3)

        if PB.getModName() == "":
            self.rbs[0].SetValue(True)

        index = 0
        for index in range(PB.getNumMods()):
            self.rbs.append(wx.RadioButton(
                modPanel, -1, PB.getModAt(index), wx.DefaultPosition, wx.DefaultSize
                ))
            sizer.Add(self.rbs[index+1], 0, wx.ALL, 3)

            if PB.isCurrentMod(index):
                self.currentMod = index+1
                self.rbs[index+1].SetValue(True)

        modPanel.SetSizer(sizer)
        modPanel.SetAutoLayout(1)
        modPanel.SetupScrolling()

        pageSizer.Add(modPanel, 0, wx.ALL, 5)

        self.SetSizer(pageSizer)

        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.OnPageChanging)

    def enableButtons(self):
        self.myParent.FindWindowById(wx.ID_FORWARD).Enable(True)
        self.myParent.FindWindowById(wx.ID_BACKWARD).Enable(False)

    def OnPageChanged(self, event):
        global curPage

        # Determine what buttons should be enabled
        self.enableButtons()

        # We are the current page
        curPage = self

    def OnPageChanging(self, event):
        # Check direction
        if event.GetDirection():
            # We are trying to move forward - have we selected another mod?

            # Determine our selection
            iSelection = 0
            while (not self.rbs[iSelection].GetValue() and iSelection < PB.getNumMods()):
                iSelection = iSelection+1

            # Do we need to load a mod
            if iSelection != self.currentMod:
                # Yep.
                PB.loadMod(iSelection-1)
                PB.quit()

    def SetNext(self, next_page):
        self.next_page = next_page

    def SetPrev(self, prev_page):
        self.prev_page = prev_page

    def GetNext(self):
        "Select which next page to show based on network selected"
        next_page = self.next_page

        # Determine our selection
        iSelection = 0
        while (not self.rbs[iSelection].GetValue() and iSelection < PB.getNumMods()):
            iSelection = iSelection+1

        # Do we need to load a mod
        if iSelection != self.currentMod:
            next_page = None

        return next_page

    def GetPrev(self):
        return self.prev_page


class SMTPLoginPage(wx.wizard.WizardPageSimple):
    # SMTP Login Page

    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self, parent)

        self.myParent = parent
        # header = wx.StaticText(self, -1, LT.getText("TXT_KEY_PITBOSS_SMTP_HEADER", ()))

        hostLbl = wx.StaticText(self, -1, LT.getText("TXT_KEY_PITBOSS_SMTP_HOST", ()))
        self.host = wx.TextCtrl(self, -1, PB.getSMTPHost(), size=(125, -1))
        self.host.SetHelpText(LT.getText("TXT_KEY_PITBOSS_SMTP_HOST_HELP", ()))
        self.host.SetInsertionPoint(0)

        usernameLbl = wx.StaticText(self, -1, LT.getText("TXT_KEY_PITBOSS_SMTP_LOGIN", ()))
        self.username = wx.TextCtrl(self, -1, PB.getSMTPLogin(), size=(125, -1))
        self.username.SetHelpText(LT.getText("TXT_KEY_PITBOSS_SMTP_LOGIN_HELP", ()))

        passwordLbl = wx.StaticText(self, -1, LT.getText("TXT_KEY_PITBOSS_SMTP_PASSWORD", ()))
        self.password = wx.TextCtrl(self, -1, "", size=(125, -1), style=wx.TE_PASSWORD)
        self.password.SetHelpText(LT.getText("TXT_KEY_PITBOSS_SMTP_PASSWORD_HELP", ()))

        emailLbl = wx.StaticText(self, -1, LT.getText("TXT_KEY_POPUP_DETAILS_EMAIL", ()))
        self.email = wx.TextCtrl(self, -1, PB.getEmail(), size=(125, -1))
        self.email.SetHelpText(LT.getText("TXT_KEY_POPUP_DETAILS_EMAIL", ()))

        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.OnPageChanging)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.OnPageChanged)

        sizer = wx.FlexGridSizer(cols=2, hgap=4, vgap=4)
        sizer.AddMany([hostLbl, self.host,
                       usernameLbl, self.username,
                       passwordLbl, self.password,
                       emailLbl, self.email,
                      ])
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(sizer, 0, wx.ALL, 25)
        self.SetSizer(border)
        self.SetAutoLayout(True)

    def enableButtons(self):
        self.myParent.FindWindowById(wx.ID_FORWARD).Enable(True)
        self.myParent.FindWindowById(wx.ID_BACKWARD).Enable(True)

    def OnPageChanged(self, event):
        global curPage

        # Determine what buttons should be enabled
        self.enableButtons()

        # We are the current page
        curPage = self

    def OnPageChanging(self, event):
        # Check direction
        if event.GetDirection():
            # We are trying to move forward - set the SMTP values
            PB.setSMTPValues(self.host.GetValue(), self.username.GetValue(), self.password.GetValue(), self.email.GetValue())


class NetSelectPage(wx.wizard.PyWizardPage):
    # Network Selection Page

    def __init__(self, parent):
        wx.wizard.PyWizardPage.__init__(self, parent)
        self.next_page = self.prev_page = None
        self.myParent = parent

        # Place the radio buttons
        selections = [LT.getText("TXT_KEY_PITBOSS_DIRECTIP", ()), LT.getText("TXT_KEY_PITBOSS_LAN", ()), LT.getText("TXT_KEY_PITBOSS_INTERNET", ())]
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.rb = wx.RadioBox(
            self, -1, LT.getText("TXT_KEY_PITBOSS_SELECT_NETWORK", ()), wx.DefaultPosition, wx.DefaultSize,
            selections, 1, wx.RA_SPECIFY_COLS
        )

        self.rb.SetToolTip(wx.ToolTip(LT.getText("TXT_KEY_PITBOSS_SELECT_NETWORK_HELP", ())))
        sizer.Add(self.rb, 0, wx.ALL, 5)

        self.SetSizer(sizer)

        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.OnPageChanged)

    def enableButtons(self):
        self.myParent.FindWindowById(wx.ID_FORWARD).Enable(True)
        self.myParent.FindWindowById(wx.ID_BACKWARD).Enable(True)

    def OnPageChanged(self, event):
        global curPage

        # Determine what buttons should be enabled
        self.enableButtons()

        # We are the current page
        curPage = self

    def SetNext(self, next_page):
        self.next_page = next_page

    def SetPrev(self, prev_page):
        self.prev_page = prev_page

    def GetNext(self):
        "Select which next page to show based on network selected"
        global bPublic

        next_page = self.next_page

        if self.rb.GetSelection() == 0:
            bPublic = True
            next_page = next_page.GetNext()
        elif self.rb.GetSelection() == 1:
            bPublic = False
            next_page = next_page.GetNext()
        else:
            bPublic = True

        return next_page

    def GetPrev(self):
        return self.prev_page


class LoginPage(wx.wizard.WizardPageSimple):
    # Login page (optional 2nd page)

    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self, parent)

        self.myParent = parent
        # header = wx.StaticText(self, -1, LT.getText("TXT_KEY_PITBOSS_LOGIN", ()))

        usernameLbl = wx.StaticText(self, -1, LT.getText("TXT_KEY_PITBOSS_USERNAME", ()))
        self.username = wx.TextCtrl(self, -1, "", size=(125, -1))
        self.username.SetHelpText(LT.getText("TXT_KEY_PITBOSS_USERNAME_HELP", ()))
        self.username.SetInsertionPoint(0)
        self.Bind(wx.EVT_TEXT, self.OnTextEntered, self.username)

        passwordLbl = wx.StaticText(self, -1, LT.getText("TXT_KEY_PITBOSS_PASSWORD", ()))
        self.password = wx.TextCtrl(self, -1, "", size=(125, -1), style=wx.TE_PASSWORD)
        self.password.SetHelpText(LT.getText("TXT_KEY_PITBOSS_PASSWORD_HELP", ()))
        self.Bind(wx.EVT_TEXT, self.OnTextEntered, self.password)

        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.OnPageChanging)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.OnPageChanged)

        sizer = wx.FlexGridSizer(cols=2, hgap=4, vgap=4)
        sizer.AddMany([usernameLbl, self.username,
                       passwordLbl, self.password,
                      ])
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(sizer, 0, wx.ALL, 25)
        self.SetSizer(border)
        self.SetAutoLayout(True)

    def enableButtons(self):
        if self.username.GetValue() == "" or self.password.GetValue() == "":
            # There isn't, disable the forward button
            self.myParent.FindWindowById(wx.ID_FORWARD).Disable()
            self.myParent.FindWindowById(wx.ID_BACKWARD).Enable(True)
        else:
            # Text entered, enable the forward button
            self.myParent.FindWindowById(wx.ID_FORWARD).Enable(True)
            self.myParent.FindWindowById(wx.ID_BACKWARD).Enable(True)

    def patchAvailable(self, patchName, patchUrl):
        PB.consoleOut("HEY patchAvailable(2)")
        return

    def patchComplete(self):
        PB.consoleOut("HEY patchComplete(2)")
        return

    def OnTextEntered(self, event):
        # Determine what buttons should be enabled
        self.enableButtons()

    def OnPageChanging(self, event):
        # Check direction
        if event.GetDirection():
            # We are trying to move forward - check password
            if not PB.login(self.username.GetValue(), self.password.GetValue()):
                # Login failed - let the user know
                wx.MessageBox((LT.getText("TXT_KEY_PITBOSS_LOGIN_FAILED", ())),
                              (LT.getText("TXT_KEY_PITBOSS_LOGIN_ERROR", ())),
                              wx.ICON_ERROR)
                # Veto the event to prevent moving forward
                event.Veto()

    def OnPageChanged(self, event):
        global curPage
        # Determine what buttons should be enabled
        self.enableButtons()
        # We are the current page
        curPage = self


class LoadSelectPage(wx.wizard.PyWizardPage):
    # Load Select Page

    def __init__(self, parent):
        wx.wizard.PyWizardPage.__init__(self, parent)
        self.next_page = self.prev_page = None
        self.myParent = parent

        # Place the radio buttons
        selections = [LT.getText("TXT_KEY_PITBOSS_NEWGAME", ()), LT.getText("TXT_KEY_PITBOSS_SCENARIO", ()), LT.getText("TXT_KEY_PITBOSS_LOADGAME", ())]
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.rb = wx.RadioBox(
            self, -1, (LT.getText("TXT_KEY_PITBOSS_SELECT_INIT", ())),
            wx.DefaultPosition, wx.DefaultSize, selections, 1, wx.RA_SPECIFY_COLS)

        self.rb.SetToolTip(wx.ToolTip(
            (LT.getText("TXT_KEY_PITBOSS_SELECT_INIT_HELP", ()))))
        sizer.Add(self.rb, 0, wx.ALL, 5)

        self.SetSizer(sizer)

        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.OnPageChanging)

    def enableButtons(self):
        # Fix for infinite hanging due gamespy shutdown
        self.myParent.FindWindowById(wx.ID_FORWARD).Enable(True)
        self.myParent.FindWindowById(wx.ID_BACKWARD).Enable(True)

    def patchAvailable(self, patchName, patchUrl):
        PB.consoleOut("HEY patchAvailable(3)")
        return

    def patchComplete(self):
        PB.consoleOut("HEY patchComplete(3)")
        return

    def OnPageChanged(self, event):
        global curPage
        # Determine what buttons should be enabled
        self.enableButtons()
        curPage = self

    def SetNext(self, next_page):
        self.next_page = next_page

    def SetPrev(self, prev_page):
        self.prev_page = prev_page

    def GetNext(self):
        "Determine which page to display next"
        next_page = self.next_page

        if self.rb.GetSelection() == 0:
            # If it's a new game, skip the scenario selector
            next_page = next_page.GetNext()
        if self.rb.GetSelection() == 2:
            # If it's a loaded game, launch now
            next_page = None

        return next_page

    def GetPrev(self):
        return self.prev_page

    def OnPageChanging(self, event):

        global bSaved
        global bScenario

        # Check direction
        if event.GetDirection():

            # We are trying to move forward - are we trying to init'ing or loading game?
            if self.rb.GetSelection() == 2:
                # Loading a game - popup the file browser
                bScenario = False
                dlg = wx.FileDialog(
                    self, message=(LT.getText("TXT_KEY_PITBOSS_CHOOSE_SAVE", ())),
                    defaultDir=r".\Saves\multi", defaultFile="",
                    wildcard=LT.getText(
                        "TXT_KEY_PITBOSS_SAVE_FILES",
                        ("(*.CivBeyondSwordSave)|*.CivBeyondSwordSave",)),
                    style=wx.OPEN)

                # Show the modal dialog and get the response
                if dlg.ShowModal() == wx.ID_OK:
                    # Get the file name
                    path = dlg.GetPath()
                    if path != "":
                        # Prompt for admin password
                        dlg = wx.TextEntryDialog(
                            self, LT.getText("TXT_KEY_MAIN_MENU_CIV_ADMINPWD_DESC", ()),
                            LT.getText("TXT_MAIN_MENU_CIV_PASSWORD_TITLEBAR", ()))

                        # Show the modal dialog and get the response
                        if dlg.ShowModal() == wx.ID_OK:
                            # Check the game name
                            adminPwd = dlg.GetValue()

                            # We got a save file - try to load the setup info
                            # iResult = PB.load(path, adminPwd)
                            (iResult, _) = loadSavegame(path, -1, adminPwd)
                            if iResult != 0:
                                # Loading setup info failed.  Clean up and exit
                                if iResult == 1:
                                    wx.MessageBox(
                                        LT.getText("TXT_KEY_PITBOSS_ERROR_LOADING", ()),
                                        LT.getText("TXT_KEY_PITBOSS_LOAD_ERROR", ()),
                                        wx.ICON_ERROR)
                                elif iResult == -1:
                                    wx.MessageBox(
                                        LT.getText("TXT_MAIN_MENU_CIV_PASSWORD_RETRY_DESC", ()),
                                        LT.getText("TXT_KEY_BAD_PASSWORD_TITLE", ()),
                                        wx.ICON_ERROR)
                                elif iResult == -2:
                                    wx.MessageBox(
                                        LT.getText("TXT_PB_MOD_NO_MATCHING_PASSWORD_FOUND", ()),
                                        LT.getText("TXT_PB_MOD_NO_MATCHING_PASSWORD_FOUND_TITLE", ()),
                                        wx.ICON_ERROR)
                                PB.reset()
                                event.Veto()
                            else:
                                # Successfully loaded, try hosting
                                PB.setLoadFileName(path)
                                if not PB.host(bPublic, bScenario):
                                    wx.MessageBox((LT.getText("TXT_KEY_PITBOSS_ERROR_HOSTING", ())), (LT.getText("TXT_KEY_PITBOSS_HOST_ERROR", ())), wx.ICON_ERROR)
                                    PB.reset()
                                    event.Veto()
                                else:
                                    bSaved = True
                        else:
                            # User cancelled admin password
                            PB.reset()
                            event.Veto()

                    else:
                        # Didn't get a save file - veto the page change
                        event.Veto()

                else:
                    # User hit cancel - veto the page change
                    event.Veto()

                # Destroy the dialog
                dlg.Destroy()

            else:
                bSaved = False

                # Check to make sure this is a valid option
                if self.rb.GetSelection() == 0:
                    # New game - check maps
                    if PB.getNumMapScripts() == 0:
                        wx.MessageBox(
                            (LT.getText("TXT_KEY_PITBOSS_NO_MAPS_DESC", ())),
                            (LT.getText("TXT_KEY_PITBOSS_NO_MAPS_TITLE", ())),
                            wx.ICON_EXCLAMATION)
                        event.Veto()
                        return

                if self.rb.GetSelection() == 1:
                    # New game - check scenarios
                    if PB.getNumScenarios() == 0:
                        wx.MessageBox((LT.getText("TXT_KEY_PITBOSS_NO_SCENARIOS_DESC", ())), (LT.getText("TXT_KEY_PITBOSS_NO_SCENARIOS_TITLE", ())), wx.ICON_EXCLAMATION)
                        event.Veto()
                        return

                # Hosting a new game - pop the gamename dialog
                dlg = wx.TextEntryDialog(
                    self, LT.getText("TXT_KEY_PITBOSS_NAME_GAME_DESC", ()),
                    LT.getText("TXT_KEY_PITBOSS_NAME_GAME_TITLE", ()))

                # Show the modal dialog and get the response
                if dlg.ShowModal() == wx.ID_OK:
                    # Check the game name
                    gamename = dlg.GetValue()
                    if gamename != "":
                        # We got a gamename, save it here
                        PB.setGamename(gamename)

                        # Prompt for passwords in public games
                        bOK = (not bPublic)
                        if bPublic:
                            dlg = wx.TextEntryDialog(
                                self, LT.getText("TXT_KEY_PITBOSS_PWD_GAME_DESC", ()),
                                LT.getText("TXT_KEY_PITBOSS_PWD_GAME_TITLE", ()))

                            if dlg.ShowModal() == wx.ID_OK:
                                bOK = True
                                PB.setGamePassword(dlg.GetValue())

                        if bOK:
                            # If we are starting a new game, host
                            if self.rb.GetSelection() == 0:
                                bScenario = False
                                if not PB.host(bPublic, bScenario):
                                    # Hosting failed for some reason.  Clean up and exit
                                    wx.MessageBox((LT.getText("TXT_KEY_PITBOSS_ERROR_HOSTING", ())), (LT.getText("TXT_KEY_PITBOSS_HOST_ERROR", ())), wx.ICON_ERROR)
                                    PB.reset()
                                    event.Veto()
                        else:
                            # User hit cancel
                            event.Veto()

                    else:
                        # Malicious user didn't enter a gamename...
                        event.Veto()

                else:
                    # User hit cancel
                    event.Veto()

                dlg.Destroy()

        else:
            # We are moving backward - reset the network layer
            PB.reset()
            PB.logout()


class ScenarioSelectPage(wx.wizard.WizardPageSimple):
    # Scenario Selection page (optional 4th page)

    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self, parent)

        self.myParent = parent
        pageSizer = wx.BoxSizer(wx.VERTICAL)

        scenarioPanel = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(300, 600), style=wx.SUNKEN_BORDER)
        sizer = wx.BoxSizer(wx.VERTICAL)

        header = wx.StaticText(self, -1, LT.getText("TXT_KEY_PITBOSS_CHOOSE_SCENARIO", ()))
        pageSizer.Add(header, 0, wx.ALL, 5)

        # Place the radio buttons
        self.rbs = []
        index = 0

        # PB.consoleOut("Num Scenarios: "+str(PB.getNumScenarios()))
        for index in range(PB.getNumScenarios()):
            # We need to start a group on the first one
            if index == 0:
                self.rbs.append(wx.RadioButton(
                    scenarioPanel, -1, PB.getScenarioAt(index), wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP
                    ))
            else:
                self.rbs.append(wx.RadioButton(
                    scenarioPanel, -1, PB.getScenarioAt(index), wx.DefaultPosition, wx.DefaultSize
                    ))

            sizer.Add(self.rbs[index], 0, wx.ALL, 3)

        scenarioPanel.SetSizer(sizer)
        scenarioPanel.SetAutoLayout(1)
        scenarioPanel.SetupScrolling()

        pageSizer.Add(scenarioPanel, 0, wx.ALL, 5)

        self.SetSizer(pageSizer)

        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.OnPageChanging)

    def enableButtons(self):
        self.myParent.FindWindowById(wx.ID_FORWARD).Enable(True)
        self.myParent.FindWindowById(wx.ID_BACKWARD).Enable(True)

    def OnPageChanged(self, event):
        global curPage

        # Determine what buttons should be enabled
        self.enableButtons()
        curPage = self

    def OnPageChanging(self, event):
        global bPublic
        global bScenario

        # Check direction
        if event.GetDirection():
            # Determine our selection
            iSelection = 0
            while (not self.rbs[iSelection].GetValue() and iSelection < PB.getNumScenarios()):
                iSelection = iSelection+1

            # We are trying to move forward - Set the selected scenario
            if PB.loadScenarioInfo(PB.getScenarioAt(iSelection)):
                bScenario = True
                if not PB.host(bPublic, bScenario):
                    # Hosting failed for some reason.  Clean up and exit
                    wx.MessageBox((LT.getText("TXT_KEY_PITBOSS_ERROR_HOSTING", ())), (LT.getText("TXT_KEY_PITBOSS_HOST_ERROR", ())), wx.ICON_ERROR)
                    PB.reset()
                    event.Veto()
            else:
                # Loading the scenario failed
                wx.MessageBox((LT.getText("TXT_KEY_PITBOSS_SCENARIO_ERROR", ())), (LT.getText("TXT_KEY_PITBOSS_SCENARIO_ERROR_TITLE", ())), wx.ICON_ERROR)
                PB.reset()
                event.Veto()
        else:
            # We are moving backward
            PB.reset()


class StagingPage(wx.wizard.WizardPageSimple):
    # Staging room (last page before launch)

    def __init__(self, parent):
        wx.wizard.WizardPageSimple.__init__(self, parent)
        self.myParent = parent

        # Get the game info struct
        gameData = PB.getGameSetupData()

        # Create our array of controls
        self.optionArray = []
        self.mpOptionArray = []
        self.victoriesArray = []
        self.whoArray = []
        self.civArray = []
        self.leaderArray = []
        self.teamArray = []
        self.diffArray = []
        self.statusArray = []

        # Declare storage arrays
        self.customItemSizerArray = []
        self.customMapTextArray = []
        self.customMapOptionArray = []

        # Build the initial selections
        # Map
        mapNameList = []
        for rowNum in range(PB.getNumMapScripts()):
            mapNameList.append((PB.getMapNameAt(rowNum)))

        # World size
        sizeList = []
        for rowNum in range(PB.getNumSizes()):
            sizeList.append((PB.getSizeAt(rowNum)))

        # Climate
        climateList = []
        for rowNum in range(PB.getNumClimates()):
            climateList.append((PB.getClimateAt(rowNum)))

        # Sealevel
        seaLevelList = []
        for rowNum in range(PB.getNumSeaLevels()):
            seaLevelList.append((PB.getSeaLevelAt(rowNum)))

        # Era
        eraList = []
        for rowNum in range(PB.getNumEras()):
            eraList.append((PB.getEraAt(rowNum)))

        # Game speed
        speedList = []
        for rowNum in range(PB.getNumSpeeds()):
            speedList.append((PB.getSpeedAt(rowNum)))

        # Options
        optionList = []
        for rowNum in range(PB.getNumOptions()):
            optionList.append((PB.getOptionDescAt(rowNum)))

        # Create the master page sizer
        self.pageSizer = wx.BoxSizer(wx.VERTICAL)

        # Create the game options area
        masterBorder = wx.StaticBox(self, -1, ((LT.getText("TXT_KEY_PITBOSS_GAME_SETUP", ()))))
        self.optionsSizer = wx.StaticBoxSizer(masterBorder, wx.HORIZONTAL)

        # Create the drop down side
        settingsBorder = wx.StaticBox(self, -1, ((LT.getText("TXT_KEY_PITBOSS_GAME_SETTINGS", ()))))
        self.dropDownSizer = wx.StaticBoxSizer(settingsBorder, wx.VERTICAL)

        # Create label/control pairs for map
        itemSizer = wx.BoxSizer(wx.VERTICAL)
        txt = wx.StaticText(self, -1, (LT.getText("TXT_KEY_PITBOSS_MAP", ())))
        self.mapChoice = wx.Choice(self, -1, (-1, -1), choices=mapNameList)
        self.mapChoice.SetStringSelection(gameData.getMapName())
        itemSizer.Add(txt)
        itemSizer.Add(self.mapChoice)
        self.dropDownSizer.Add(itemSizer, 0, wx.TOP, 3)
        self.Bind(wx.EVT_CHOICE, self.OnGameChoice, self.mapChoice)

        # Create label/control pairs for size
        itemSizer = wx.BoxSizer(wx.VERTICAL)
        txt = wx.StaticText(self, -1, (LT.getText("TXT_KEY_PITBOSS_SIZE", ())))
        self.sizeChoice = wx.Choice(self, -1, (-1, -1), choices=sizeList)
        self.sizeChoice.SetSelection(gameData.iSize)
        itemSizer.Add(txt)
        itemSizer.Add(self.sizeChoice)
        self.dropDownSizer.Add(itemSizer, 0, wx.TOP, 3)
        self.Bind(wx.EVT_CHOICE, self.OnGameChoice, self.sizeChoice)

        # Create label/control pairs for climate
        itemSizer = wx.BoxSizer(wx.VERTICAL)
        txt = wx.StaticText(self, -1, (LT.getText("TXT_KEY_PITBOSS_CLIMATE", ())))
        self.climateChoice = wx.Choice(self, -1, (-1, -1), choices=climateList)
        self.climateChoice.SetSelection(gameData.iClimate)
        itemSizer.Add(txt)
        itemSizer.Add(self.climateChoice)
        self.dropDownSizer.Add(itemSizer, 0, wx.TOP, 3)
        self.Bind(wx.EVT_CHOICE, self.OnGameChoice, self.climateChoice)

        # Create label/control pairs for sealevel
        itemSizer = wx.BoxSizer(wx.VERTICAL)
        txt = wx.StaticText(self, -1, (LT.getText("TXT_KEY_PITBOSS_SEALEVEL", ())))
        self.seaLevelChoice = wx.Choice(self, -1, (-1, -1), choices=seaLevelList)
        self.seaLevelChoice.SetSelection(gameData.iSeaLevel)
        itemSizer.Add(txt)
        itemSizer.Add(self.seaLevelChoice)
        self.dropDownSizer.Add(itemSizer, 0, wx.TOP, 3)
        self.Bind(wx.EVT_CHOICE, self.OnGameChoice, self.seaLevelChoice)

        # Create label/control pairs for era
        itemSizer = wx.BoxSizer(wx.VERTICAL)
        txt = wx.StaticText(self, -1, (LT.getText("TXT_KEY_PITBOSS_ERA", ())))
        self.eraChoice = wx.Choice(self, -1, (-1, -1), choices=eraList)
        self.eraChoice.SetSelection(gameData.iEra)
        itemSizer.Add(txt)
        itemSizer.Add(self.eraChoice)
        self.dropDownSizer.Add(itemSizer, 0, wx.TOP, 3)
        self.Bind(wx.EVT_CHOICE, self.OnGameChoice, self.eraChoice)

        # Create label/control pairs for speed
        itemSizer = wx.BoxSizer(wx.VERTICAL)
        txt = wx.StaticText(self, -1, (LT.getText("TXT_KEY_PITBOSS_SPEED", ())))
        self.speedChoice = wx.Choice(self, -1, (-1, -1), choices=speedList)
        self.speedChoice.SetSelection(gameData.iSpeed)
        itemSizer.Add(txt)
        itemSizer.Add(self.speedChoice)
        self.dropDownSizer.Add(itemSizer, 0, wx.TOP, 3)
        self.Bind(wx.EVT_CHOICE, self.OnGameChoice, self.speedChoice)

        # Create label/control pairs for custom map options
        self.buildCustomMapOptions(gameData.getMapName())

        self.optionsSizer.Add(self.dropDownSizer, 0, wx.RIGHT, 10)

        # Create the multiplayer option column
        centerSizer = wx.BoxSizer(wx.VERTICAL)

        mpOptionsBorder = wx.StaticBox(self, -1, ((LT.getText("TXT_KEY_PITBOSS_GAME_MPOPTIONS", ()))))
        mpOptionsSizer = wx.StaticBoxSizer(mpOptionsBorder, wx.VERTICAL)

        # Create and add Multiplayer option checkboxes
        for rowNum in range(PB.getNumMPOptions()):
            mpCheckBox = wx.CheckBox(self, (rowNum+1000), (PB.getMPOptionDescAt(rowNum)))
            mpCheckBox.SetValue(gameData.getMPOptionAt(rowNum))
            mpOptionsSizer.Add(mpCheckBox, 0, wx.TOP, 5)
            self.mpOptionArray.append(mpCheckBox)
            self.Bind(wx.EVT_CHECKBOX, self.OnOptionChoice, mpCheckBox)

        # Entry box to set turn timer time
        timerOutputSizer = wx.BoxSizer(wx.HORIZONTAL)
        timerPreText = wx.StaticText(self, -1, LT.getText("TXT_KEY_PITBOSS_TURNTIMER_A", ()))
        self.turnTimerEdit = wx.TextCtrl(self, -1, str(gameData.iTurnTime), size=(30, -1))
        timerPostText = wx.StaticText(self, -1, LT.getText("TXT_KEY_PITBOSS_TURNTIMER_B", ()))
        timerOutputSizer.Add(timerPreText, 0, wx.TOP, 5)
        timerOutputSizer.Add(self.turnTimerEdit, 0, wx.TOP, 5)
        timerOutputSizer.Add(timerPostText, 0, wx.TOP, 5)
        self.Bind(wx.EVT_TEXT, self.OnTurnTimeEntered, self.turnTimerEdit)

        mpOptionsSizer.Add(timerOutputSizer, 0, wx.ALL, 5)

        # Entry box for game turn limit
        maxTurnsSizer = wx.BoxSizer(wx.HORIZONTAL)
        maxTurnsText = wx.StaticText(self, -1, LT.getText("TXT_KEY_PITBOSS_MAX_TURN", ()))
        self.maxTurnsEdit = wx.TextCtrl(self, -1, str(gameData.iMaxTurns), size=(30, -1))
        maxTurnsSizer.Add(maxTurnsText, 0, wx.TOP, 5)
        maxTurnsSizer.Add(self.maxTurnsEdit, 0, wx.TOP, 5)
        self.Bind(wx.EVT_TEXT, self.OnMaxTurnsEntered, self.maxTurnsEdit)

        mpOptionsSizer.Add(maxTurnsSizer, 0, wx.ALL, 5)

        # Entry box for city elimination limit
        cityEliminationSizer = wx.BoxSizer(wx.HORIZONTAL)
        cityEliminationText = wx.StaticText(self, -1, LT.getText("TXT_KEY_PITBOSS_CITY_ELIMINATION", ()))
        self.cityEliminationEdit = wx.TextCtrl(self, -1, str(gameData.iCityElimination), size=(30, -1))
        cityEliminationSizer.Add(cityEliminationText, 0, wx.TOP, 5)
        cityEliminationSizer.Add(self.cityEliminationEdit, 0, wx.TOP, 5)
        self.Bind(wx.EVT_TEXT, self.OnCityEliminationEntered, self.cityEliminationEdit)

        mpOptionsSizer.Add(cityEliminationSizer, 0, wx.ALL, 5)

        centerSizer.Add(mpOptionsSizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)

        victoriesBorder = wx.StaticBox(self, -1, ((LT.getText("TXT_KEY_PITBOSS_GAME_VICTORIES", ()))))
        victoriesSizer = wx.StaticBoxSizer(victoriesBorder, wx.VERTICAL)

        # Create and add Victory option checkboxes
        for rowNum in range(PB.getNumVictories()):
            victoryCheckBox = wx.CheckBox(self, (rowNum+2000), (PB.getVictoryDescAt(rowNum)))
            victoryCheckBox.SetValue(gameData.getVictory(rowNum))
            victoriesSizer.Add(victoryCheckBox, 0, wx.TOP, 5)
            self.victoriesArray.append(victoryCheckBox)
            self.Bind(wx.EVT_CHECKBOX, self.OnOptionChoice, victoryCheckBox)

        centerSizer.Add(victoriesSizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        # Entry box for admin password
        itemSizer = wx.BoxSizer(wx.VERTICAL)
        txt = wx.StaticText(self, -1, (LT.getText("TXT_KEY_POPUP_ADMIN_PASSWORD", ())))
        self.adminPasswordEdit = wx.TextCtrl(self, -1, "", size=(100, -1))
        itemSizer.Add(txt)
        itemSizer.Add(self.adminPasswordEdit)
        mpOptionsSizer.Add(itemSizer, 0, wx.TOP, 5)
        self.Bind(wx.EVT_TEXT, self.OnAdminPasswordEntered, self.adminPasswordEdit)

        self.optionsSizer.Add(centerSizer, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # Create the CheckBox side
        optionsBorder1 = wx.StaticBox(self, -1, ((LT.getText("TXT_KEY_PITBOSS_GAME_OPTIONS", ()))))
        optionsBorder2 = wx.StaticBox(self, -1, ((LT.getText("TXT_KEY_PITBOSS_GAME_OPTIONS", ()))))
        optionsBorder3 = wx.StaticBox(self, -1, ((LT.getText("TXT_KEY_PITBOSS_GAME_OPTIONS", ()))))
        checkBoxSizer1 = wx.StaticBoxSizer(optionsBorder1, wx.VERTICAL)
        checkBoxSizer2 = wx.StaticBoxSizer(optionsBorder2, wx.VERTICAL)
        checkBoxSizer3 = wx.StaticBoxSizer(optionsBorder3, wx.VERTICAL)

        # Create and add the Options checkboxes
        import math
        rowNum1 = math.ceil(PB.getNumOptions()/3.0)
        rowNum2 = 2 * rowNum1
        for rowNum in range(PB.getNumOptions()):
            checkBox = wx.CheckBox(self, rowNum, (PB.getOptionDescAt(rowNum)))
            checkBox.SetValue(gameData.getOptionAt(rowNum))
            if rowNum < rowNum1:
                checkBoxSizer1.Add(checkBox, 0, wx.TOP, 5)
            elif rowNum < rowNum2:
                checkBoxSizer2.Add(checkBox, 0, wx.TOP, 5)
            else:
                checkBoxSizer3.Add(checkBox, 0, wx.TOP, 5)
            self.optionArray.append(checkBox)
            self.Bind(wx.EVT_CHECKBOX, self.OnOptionChoice, checkBox)

        self.optionsSizer.Add(checkBoxSizer1, 0, wx.LEFT, 10)
        self.optionsSizer.Add(checkBoxSizer2, 0, wx.LEFT, 10)
        self.optionsSizer.Add(checkBoxSizer3, 0, wx.LEFT, 10)

        # Entry box for number of advanced start points
        advancedStartPointsSizer = wx.BoxSizer(wx.HORIZONTAL)
        advancedStartPointsText = wx.StaticText(self, -1, LT.getText("TXT_KEY_ADVANCED_START_POINTS", ()))
        self.advancedStartPointsEdit = wx.TextCtrl(self, -1, str(gameData.iAdvancedStartPoints), size=(50, -1))
        advancedStartPointsSizer.Add(advancedStartPointsText, 0, wx.TOP, 5)
        advancedStartPointsSizer.Add(self.advancedStartPointsEdit, 0, wx.TOP, 5)
        self.Bind(wx.EVT_TEXT, self.OnAdvancedStartPointsEntered, self.advancedStartPointsEdit)

        mpOptionsSizer.Add(advancedStartPointsSizer, 0, wx.ALL, 5)

        # Add our options box to the page
        self.pageSizer.Add(self.optionsSizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.bPlayerPanel = False  # Delayed creation
        self._playerPanel = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(800, 300), style=wx.SUNKEN_BORDER)
        self._panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.fill_player_panel(0, 1)

        self.leaderRefresh = True

        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.OnPageChanging)

        self.SetSizer(self.pageSizer)

    def fill_player_panel(self, id_from=0, id_to=gc.getMAX_CIV_PLAYERS()):
        # Slot status - choices are static
        slotStatusList = [LT.getText("TXT_KEY_PITBOSS_HUMAN", ()), LT.getText("TXT_KEY_PITBOSS_COMPUTER", ()), LT.getText("TXT_KEY_PITBOSS_CLOSED", ())]

        # Civilizations - get from app
        civList = []
        civList.append(LT.getText("TXT_KEY_PITBOSS_RANDOM", ()))
        for rowNum in range(PB.getNumCivs()):
            civList.append((PB.getCivAt(rowNum)))

        leaderList = [LT.getText("TXT_KEY_PITBOSS_RANDOM", ())]

        teamList = []
        for rowNum in range(gc.getMAX_CIV_PLAYERS()):
            teamList.append(str(rowNum+1))

        # Handicaps - get from app
        diffList = []
        for rowNum in range(PB.getNumHandicaps()):
            diffList.append((PB.getHandicapAt(rowNum)))

        # NOTE: Takes big amount of time. construction of table was be delayed
        #       to first access to page.

        # Create a row - enough for the max players in a Pitboss game
        for rowNum in range(id_from, id_to):
            # Create the border box
            border = wx.StaticBox(self._playerPanel, -1, (LT.getText("TXT_KEY_PITBOSS_PLAYER", (rowNum+1, ))), (0, (rowNum*30)))
            # Create the layout mgr
            rowSizer = wx.StaticBoxSizer(border, wx.HORIZONTAL)

            # Get the info struct
            if rowNum > 0:
                PB.consoleOut("slow loop over players %i/%i... "
                              "" % (rowNum, id_to))
            playerData = PB.getPlayerSetupData(rowNum)

            # Slot status dropdown
            itemSizer = wx.BoxSizer(wx.VERTICAL)
            txt = wx.StaticText(self._playerPanel, -1, (LT.getText("TXT_KEY_PITBOSS_WHO", ())))
            dropDown = wx.Choice(self._playerPanel, rowNum, (-1, -1), choices=slotStatusList)
            dropDown.SetSelection(playerData.iWho)
            itemSizer.Add(txt)
            itemSizer.Add(dropDown)
            rowSizer.Add(itemSizer, 0, wx.TOP, 3)
            self.whoArray.append(dropDown)
            self.Bind(wx.EVT_CHOICE, self.OnPlayerChoice, dropDown)

            # Civ dropdown
            itemSizer = wx.BoxSizer(wx.VERTICAL)
            txt = wx.StaticText(self._playerPanel, -1, (LT.getText("TXT_KEY_PITBOSS_CIV", ())))
            dropDown = wx.Choice(self._playerPanel, rowNum, (-1, -1), choices=civList)
            dropDown.SetSelection(playerData.iCiv+1)
            itemSizer.Add(txt)
            itemSizer.Add(dropDown)
            rowSizer.Add(itemSizer, 0, wx.TOP, 3)
            self.civArray.append(dropDown)
            self.Bind(wx.EVT_CHOICE, self.OnPlayerChoice, dropDown)

            # Leader dropdown
            itemSizer = wx.BoxSizer(wx.VERTICAL)
            txt = wx.StaticText(self._playerPanel, -1, (LT.getText("TXT_KEY_PITBOSS_LEADER", ())))
            dropDown = wx.Choice(self._playerPanel, rowNum, (-1, -1), choices=leaderList)
            dropDown.SetSelection(playerData.iLeader+1)
            itemSizer.Add(txt)
            itemSizer.Add(dropDown)
            rowSizer.Add(itemSizer, 0, wx.TOP, 3)
            self.leaderArray.append(dropDown)
            self.Bind(wx.EVT_CHOICE, self.OnPlayerChoice, dropDown)

            # Team dropdown
            itemSizer = wx.BoxSizer(wx.VERTICAL)
            txt = wx.StaticText(self._playerPanel, -1, (LT.getText("TXT_KEY_PITBOSS_TEAM", ())))
            dropDown = wx.Choice(self._playerPanel, rowNum, (-1, -1), choices=teamList)
            dropDown.SetSelection(playerData.iTeam)
            itemSizer.Add(txt)
            itemSizer.Add(dropDown)
            rowSizer.Add(itemSizer, 0, wx.TOP, 3)
            self.teamArray.append(dropDown)
            self.Bind(wx.EVT_CHOICE, self.OnPlayerChoice, dropDown)

            # Difficulty dropdown
            itemSizer = wx.BoxSizer(wx.VERTICAL)
            txt = wx.StaticText(self._playerPanel, -1, (LT.getText("TXT_KEY_PITBOSS_DIFFICULTY", ())))
            dropDown = wx.Choice(self._playerPanel, rowNum, (-1, -1), choices=diffList)
            dropDown.SetSelection(playerData.iDifficulty)
            itemSizer.Add(txt)
            itemSizer.Add(dropDown)
            rowSizer.Add(itemSizer, 0, wx.TOP, 3)
            self.diffArray.append(dropDown)
            self.Bind(wx.EVT_CHOICE, self.OnPlayerChoice, dropDown)

            # Ready status
            itemSizer = wx.BoxSizer(wx.VERTICAL)
            txt = wx.StaticText(self._playerPanel, -1, (LT.getText("TXT_KEY_PITBOSS_STATUS", ())))
            statusTxt = wx.StaticText(self._playerPanel, rowNum, playerData.getStatusText())
            itemSizer.Add(txt)
            itemSizer.Add(statusTxt)
            rowSizer.Add(itemSizer, 0, wx.ALL, 5)
            self.statusArray.append(statusTxt)

            # Add row to page Sizer
            self._panelSizer.Add(rowSizer, 0, wx.ALL, 5)

        self._playerPanel.SetSizer(self._panelSizer)
        self._playerPanel.SetAutoLayout(1)
        self._playerPanel.SetupScrolling()
        self.pageSizer.Add(self._playerPanel, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.leaderRefresh = False

    def enableButtons(self):
        self.myParent.FindWindowById(wx.ID_FORWARD).Enable(True)
        self.myParent.FindWindowById(wx.ID_BACKWARD).Enable(True)

    def OnGameChoice(self, event):
        self.ChangeGameParam()

    def ChangeGameParam(self):
        maxTurnsValue = 0
        cityEliminationValue = 0
        advancedStartPointsValue = 0
        turnTimerValue = 0

        strValue = self.maxTurnsEdit.GetValue()
        if len(strValue) > 0:
            maxTurnsValue = (int)(self.maxTurnsEdit.GetValue())

        strValue = self.cityEliminationEdit.GetValue()
        if len(strValue) > 0:
            cityEliminationValue = (int)(self.cityEliminationEdit.GetValue())

        strValue = self.advancedStartPointsEdit.GetValue()
        if len(strValue) > 0:
            advancedStartPointsValue = (int)(self.advancedStartPointsEdit.GetValue())

        strValue = self.turnTimerEdit.GetValue()
        if len(strValue) > 0:
            turnTimerValue = (int)(self.turnTimerEdit.GetValue())

        PB.gameParamChanged(self.mapChoice.GetStringSelection(), self.sizeChoice.GetSelection(),
                            self.climateChoice.GetSelection(), self.seaLevelChoice.GetSelection(),
                            self.eraChoice.GetSelection(), self.speedChoice.GetSelection(), maxTurnsValue, cityEliminationValue,
                            advancedStartPointsValue, turnTimerValue, self.adminPasswordEdit.GetValue())
        PbSettings.temp["adminpw"] = self.adminPasswordEdit.GetValue()

    def OnCustomMapOptionChoice(self, event):
        # Get the option ID
        optionID = ((event.GetId()/100) - 1)
        PB.customMapOptionChanged(optionID, self.customMapOptionArray[optionID].GetSelection())

    def IsNumericString(self, myStr):
        for myChar in myStr:
            if myChar not in string.digits:
                return False
        return True

    def OnMaxTurnsEntered(self, event):
        # Check to see if there is a turn string
        if (self.maxTurnsEdit.GetValue() != ""):
            # There is, make sure it's a number
            if not self.IsNumericString(self.maxTurnsEdit.GetValue()):
                # It's not - lay the smack down
                dlg = wx.MessageDialog(
                    self, LT.getText("TXT_KEY_PITBOSS_MAXTURN_ERROR_DESC", ()),
                    LT.getText("TXT_KEY_PITBOSS_MAXTURN_ERROR_TITLE", ()), wx.OK | wx.ICON_EXCLAMATION)

                # Show the modal dialog and get the response
                if dlg.ShowModal() == wx.ID_OK:
                    # Clear out the MaxTurns Edit box
                    self.maxTurnsEdit.SetValue("")
            else:
                # It's a number
                self.ChangeGameParam()
        else:
            # It's been cleared
            self.ChangeGameParam()

    def OnCityEliminationEntered(self, event):
        # Check to see if there is an elimination string
        if (self.cityEliminationEdit.GetValue() != ""):
            # There is, make sure it's a number
            if not self.IsNumericString(self.cityEliminationEdit.GetValue()):
                # It's not - lay the smack down
                dlg = wx.MessageDialog(
                    self, LT.getText("TXT_KEY_PITBOSS_CITYELIMINATION_ERROR_DESC", ()),
                    LT.getText("TXT_KEY_PITBOSS_CITYELIMINATION_ERROR_TITLE", ()), wx.OK | wx.ICON_EXCLAMATION)

                # Show the modal dialog and get the response
                if dlg.ShowModal() == wx.ID_OK:
                    # Clear out the MaxTurns Edit box
                    self.cityEliminationEdit.SetValue("")
            else:
                # It's a number
                self.ChangeGameParam()
        else:
            # It's been cleared
            self.ChangeGameParam()

    def OnAdvancedStartPointsEntered(self, event):
        # Check to see if there is an string
        if (self.advancedStartPointsEdit.GetValue() != ""):
            # There is, make sure it's a number
            if not self.IsNumericString(self.advancedStartPointsEdit.GetValue()):
                # It's not - lay the smack down
                dlg = wx.MessageDialog(
                    self, LT.getText("TXT_KEY_PITBOSS_CITYELIMINATION_ERROR_DESC", ()),
                    LT.getText("TXT_KEY_PITBOSS_CITYELIMINATION_ERROR_TITLE", ()), wx.OK | wx.ICON_EXCLAMATION)

                # Show the modal dialog and get the response
                if dlg.ShowModal() == wx.ID_OK:
                    # Clear out the MaxTurns Edit box
                    self.advancedStartPointsEdit.SetValue("")
            else:
                # It's a number
                self.ChangeGameParam()
        else:
            # It's been cleared
            self.ChangeGameParam()

    def OnTurnTimeEntered(self, event):
        # Check to see if there is a time string
        if (self.turnTimerEdit.GetValue() != ""):
            # There is, make sure it's a number
            if not self.IsNumericString(self.turnTimerEdit.GetValue()):
                # It's not - lay the smack down
                dlg = wx.MessageDialog(
                    self, LT.getText("TXT_KEY_PITBOSS_TURNTIMER_ERROR_DESC", ()),
                    LT.getText("TXT_KEY_PITBOSS_TURNTIMER_ERROR_TITLE", ()), wx.OK | wx.ICON_EXCLAMATION)

                # Show the modal dialog and get the response
                if dlg.ShowModal() == wx.ID_OK:
                    # Clear out the TurnTimer Edit box
                    self.turnTimerEdit.SetValue("")
            else:
                # It's a number
                self.ChangeGameParam()
        else:
            # It's been cleared
            self.ChangeGameParam()

    def OnAdminPasswordEntered(self, event):
        self.ChangeGameParam()

    def OnOptionChoice(self, event):
        # Get the option ID
        optionID = event.GetId()

        # Values >= 2000 are victories
        if optionID >= 2000:
            PB.victoriesChanged((optionID-2000), self.victoriesArray[(optionID-2000)].GetValue())
        # Values >= 1000 are MP options
        elif optionID >= 1000:
            PB.mpOptionChanged((optionID-1000), self.mpOptionArray[(optionID-1000)].GetValue())
        else:
            PB.gameOptionChanged(optionID, self.optionArray[optionID].GetValue())

        bEnable = PB.getTurnTimer()
        self.turnTimerEdit.Enable(bEnable)

    def OnPlayerChoice(self, event):
        # Get the row for the player modified
        rowNum = event.GetId()

        # See if the slot status is valid
        if bScenario and not PB.getNoPlayersScenario():
            if PB.getWho(rowNum) != self.whoArray[rowNum].GetSelection():
                # Closed status is not permitted - change to AI
                if self.whoArray[rowNum].GetSelection() == 2:
                    self.whoArray[rowNum].SetSelection(1)

        # See if we need to update the leader box
        if not self.leaderRefresh:
            self.leaderRefresh = (PB.getCiv(rowNum) != (self.civArray[rowNum].GetSelection()-1))

        PB.playerParamChanged(rowNum, self.whoArray[rowNum].GetSelection(), self.civArray[rowNum].GetSelection()-1, self.teamArray[rowNum].GetSelection(),
                              self.diffArray[rowNum].GetSelection(), PB.getGlobalLeaderIndex(self.civArray[rowNum].GetSelection()-1, self.leaderArray[rowNum].GetSelection()-1))

    def OnPageChanging(self, event):
        # Check direction
        if not event.GetDirection():
            # We are trying to move backward - reset the network resources
            PB.reset()

    def OnPageChanged(self, event):
        global curPage

        if not self.bPlayerPanel:
            self.bPlayerPanel = True
            self.fill_player_panel(1)
        else:
            self.pageSizer.Add(self._playerPanel, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
            self.leaderRefresh = False

        # Determine what buttons should be enabled
        self.enableButtons()
        self.setDefaults()

        # We are the current page
        curPage = self

    def setDefaults(self):
        # Display the current initialization information
        global bSaved
        global bScenario

        # Get game data first
        PB.resetAdvancedStartPoints()
        gameData = PB.getGameSetupData()

        self.refreshCustomMapOptions(gameData.getMapName())

        # Set the selections currently in our init structure
        if self.mapChoice.FindString(gameData.getMapName()) == wx.NOT_FOUND:
            self.mapChoice.Append(gameData.getMapName())
        self.mapChoice.SetStringSelection(gameData.getMapName())
        self.mapChoice.Enable(not bSaved and not bScenario)

        self.sizeChoice.SetSelection(gameData.iSize)
        self.sizeChoice.Enable(not bSaved and not bScenario)

        self.climateChoice.SetSelection(gameData.iClimate)
        self.climateChoice.Enable(not bSaved and not bScenario)

        self.seaLevelChoice.SetSelection(gameData.iSeaLevel)
        self.seaLevelChoice.Enable(not bSaved and not bScenario)

        self.eraChoice.SetSelection(gameData.iEra)
        self.eraChoice.Enable(not bSaved and not bScenario)

        self.speedChoice.SetSelection(gameData.iSpeed)
        self.speedChoice.Enable(not bSaved and not PB.forceSpeed())

        self.maxTurnsEdit.SetValue(str(gameData.iMaxTurns))
        self.maxTurnsEdit.Enable(not bSaved and not PB.forceMaxTurns())

        self.cityEliminationEdit.SetValue(str(gameData.iCityElimination))
        self.cityEliminationEdit.Enable(not bSaved and not PB.forceCityElimination())

        self.advancedStartPointsEdit.SetValue(str(gameData.iAdvancedStartPoints))
        self.advancedStartPointsEdit.Enable(not bSaved and not PB.forceAdvancedStart())

        self.turnTimerEdit.SetValue(str(gameData.iTurnTime))
        if not bSaved:
            bEnable = PB.getTurnTimer()
            self.turnTimerEdit.Enable(bEnable)
        else:
            self.turnTimerEdit.Disable()

        # Set selections of map options
        optionNum = 0
        for optionNum in range(PB.getNumCustomMapOptions(gameData.getMapName())):
            self.customMapOptionArray[optionNum].SetSelection(gameData.getCustomMapOption(optionNum))
            self.customMapOptionArray[optionNum].Enable(not bSaved and not bScenario)

        # set the mp options selection
        for rowNum in range(PB.getNumMPOptions()):
            self.mpOptionArray[rowNum].SetValue(gameData.getMPOptionAt(rowNum))
            self.mpOptionArray[rowNum].Enable(not bSaved)

        # set the victories selected
        for rowNum in range(PB.getNumVictories()):
            self.victoriesArray[rowNum].SetValue(gameData.getVictory(rowNum))
            self.victoriesArray[rowNum].Enable(not bSaved and not PB.forceVictories() and not PB.isPermanentVictory(rowNum))

        # Set the options selected
        for rowNum in range(PB.getNumOptions()):
            self.optionArray[rowNum].SetValue(gameData.getOptionAt(rowNum))
            self.optionArray[rowNum].Enable(not bSaved and not PB.forceOptions() and PB.isOptionValid(rowNum))

        # Have the app suggest number of players based on map size
        PB.suggestPlayerSetup()

        for rowNum in range(gc.getMAX_CIV_PLAYERS()):
            # Get the player data
            playerData = PB.getPlayerSetupData(rowNum)

            # We may need to add/remove items from who box
            self.refreshWhoBox(rowNum, playerData.iWho)
            self.whoArray[rowNum].SetSelection(playerData.iWho)
            if playerData.iWho == 1:    # AI
                self.whoArray[rowNum].Enable(not bSaved and PB.isPlayableCiv(rowNum))

            # Civ choices are static inside the instance
            civChoice = playerData.iCiv+1
            self.civArray[rowNum].SetSelection(civChoice)
            self.civArray[rowNum].Enable(not bSaved and (not bScenario or PB.getNoPlayersScenario()))

            # We may need to add/remove items from the leader box
            self.refreshLeaderBox(rowNum, playerData.iCiv)
            self.leaderRefresh = False
            self.leaderArray[rowNum].SetSelection(PB.getCivLeaderIndex(civChoice-1, playerData.iLeader)+1)
            self.leaderArray[rowNum].Enable(not bSaved and (not bScenario or PB.getNoPlayersScenario()))

            # Team choices are static
            self.teamArray[rowNum].SetSelection(playerData.iTeam)
            self.teamArray[rowNum].Enable(not bSaved and (not bScenario or PB.getNoPlayersScenario()))

            # Difficulty choices are static
            self.diffArray[rowNum].SetSelection(playerData.iDifficulty)
            self.diffArray[rowNum].Enable(not bSaved and not PB.forceDifficulty())

            # Status is static
            self.statusArray[rowNum].SetLabel(playerData.getStatusText())

    def refreshRow(self, iRow):

        global bSaved

        # Disable finish button if all players not ready to start
        bAllReady = True

        # Don't wait for ready's if we're loading
        if not bSaved:
            index = 0
            for index in range(gc.getMAX_CIV_PLAYERS()):
                if PB.getWho(index) == 3:  # If a row is taken by a human
                    if PB.getReady(index) is False:  # If this human is not ready for the event to begin
                        # Don't allow a launch
                        bAllReady = False
                        break
            if bAllReady and PB.isPendingInit():
                bAllReady = False

        self.myParent.FindWindowById(wx.ID_FORWARD).Enable(bAllReady)

        # Get information from the app for this row
        playerData = PB.getPlayerSetupData(iRow)

        # Refresh the choices in this slot
        self.refreshWhoBox(iRow, playerData.iWho)
        self.whoArray[iRow].SetSelection(playerData.iWho)

        # Get the Civ and see if we should refresh the list of leaders
        dropDown = self.civArray[iRow]
        civChoice = playerData.iCiv+1
        if not self.leaderRefresh:
            self.leaderRefresh = (civChoice != dropDown.GetSelection())
        dropDown.SetSelection(civChoice)

        if self.leaderRefresh:
            self.refreshLeaderBox(iRow, playerData.iCiv)
            self.leaderRefresh = False

        # Get the Leader
        dropDown = self.leaderArray[iRow]
        dropDown.SetSelection(PB.getCivLeaderIndex(civChoice-1, playerData.iLeader)+1)

        # Get the Team
        dropDown = self.teamArray[iRow]
        dropDown.SetSelection(playerData.iTeam)

        # Get the Difficulty
        dropDown = self.diffArray[iRow]
        dropDown.SetSelection(playerData.iDifficulty)

        # Modify Status
        self.statusArray[iRow].SetLabel(playerData.getStatusText())

    def refreshWhoBox(self, iRow, iWho):
        # Add or remove choices depending on the state and the change
        dropDown = self.whoArray[iRow]

        if iWho < 3:  # Status changing to non-taken state
            # Remove the player name from the drop down if it is there
            if dropDown.GetCount() > 3:
                dropDown.Delete(3)
        else:            # Slot taken!
            if dropDown.GetCount() == 3:
                # Add and display the player name
                dropDown.Append((PB.getName(iRow)))
            else:
                # Set the current player name with the new one
                dropDown.SetString(3, (PB.getName(iRow)))

    def refreshLeaderBox(self, iRow, iCiv):
        # Need to reset the leader choices - first clear the list
        dropDown = self.leaderArray[iRow]
        dropDown.Clear()

        # Give the Random choice
        dropDown.Append((LT.getText("TXT_KEY_PITBOSS_RANDOM", ())))

        civChoice = iCiv+1
        if civChoice != 0:
            # If there are leaders to list, list them
            i = 0
            iNumLeaders = PB.getNumLeaders(civChoice-1)
            for i in range(iNumLeaders):
                dropDown.Append((PB.getCivLeaderAt(civChoice-1, i)))

        dropDown.SetSelection(0)

    def refreshCustomMapOptions(self, szMapName):
        # Clear the widgets from the custom option area
        i = 0
        for i in range(len(self.customItemSizerArray)):
            self.Unbind(wx.EVT_CHOICE, self.customMapOptionArray[i])
            currentSizer = self.customItemSizerArray[i]
            success = currentSizer.Remove(1)  # dropDown
            success = currentSizer.Remove(0)  # txt
            success = self.dropDownSizer.Remove(currentSizer)
            self.customMapOptionArray[i].Destroy()
            self.customMapTextArray[i].Destroy()

        self.buildCustomMapOptions(szMapName)

        # Now rebuild the sizers
        self.dropDownSizer.Layout()
        self.optionsSizer.Layout()
        self.pageSizer.Layout()
        self.Layout()

    def refreshAdvancedStartPoints(self, iPoints):
        self.advancedStartPointsEdit.SetValue(str(iPoints))

    def buildCustomMapOptions(self, szMapName):
        gameData = PB.getGameSetupData()

        self.customItemSizerArray = []
        self.customMapTextArray = []
        self.customMapOptionArray = []

        # Create label/control pairs for custom map option
        customMapOptionsList = []

        optionNum = 0
        for optionNum in range(PB.getNumCustomMapOptions(gameData.getMapName())):
            customMapOptionValuesList = []
            for rowNum in range(PB.getNumCustomMapOptionValues(optionNum, gameData.getMapName())):
                customMapOptionValuesList.append(PB.getCustomMapOptionDescAt(optionNum, rowNum, gameData.getMapName()))
            customMapOptionsList.append(customMapOptionValuesList[:])

        optionNum = 0
        for optionNum in range(PB.getNumCustomMapOptions(szMapName)):
            itemSizer = wx.BoxSizer(wx.VERTICAL)
            txt = wx.StaticText(self, -1, PB.getCustomMapOptionName(optionNum, szMapName))
            optionDropDown = wx.Choice(self, ((optionNum+1)*100), (-1, -1), choices=customMapOptionsList[optionNum])
            optionDropDown.SetSelection(gameData.getCustomMapOption(optionNum))
            itemSizer.Add(txt)
            itemSizer.Add(optionDropDown)
            self.customItemSizerArray.append(itemSizer)
            self.customMapTextArray.append(txt)
            self.customMapOptionArray.append(optionDropDown)
            self.dropDownSizer.Add(itemSizer, 0, wx.TOP, 3)
            self.Bind(wx.EVT_CHOICE, self.OnCustomMapOptionChoice, self.customMapOptionArray[optionNum])


class StartupIFace(wx.App):
    # main app class

    def __init__(self, arg):
        # self.bGui = (int(PbSettings.get("noGui", 0)) == 0)  # Old key name
        self.bGui = (int(PbSettings.get("gui", 1)) != 0)
        self.bAutostart = (int(PbSettings.get("autostart", 0)) != 0)
        self.bShell = (int(PbSettings.get("shell", {}).get("enable", 0)) != 0)
        self.civ4Shell = {}  #  Holds shell object and some extra variables

        self.bQuitWizard = False
        self.updateTimer = None
        self.wizard = None
        # Made syntax checker happy...
        self.modSelect = None 
        self.smtpLogin = None
        self.netSelect = None
        self.login = None
        self.loadSelect = None
        self.scenarioSelect = None
        self.staging = None

        # Handle one time autostart flag
        bForcedAutostart = (int(PbSettings.get("save",{}).get(
            "oneOffAutostart", 0)) != 0)
        if bForcedAutostart:
            bAutostart = bForcedAutostart
            PbSettings.get("save",{}).pop("oneOffAutostart", None)
            PbSettings.save()

        PB.consoleOut("Startflags:\n\tgui: %i\n\tautostart: %i\n\tshell: %i"
                      "" % (self.bGui, self.bAutostart, self.bShell))

        if not self.bGui and not self.bAutostart and not self.bShell:
            PB.consoleOut("Attention, start without gui, autostart or shell "
                          "detected. Enabling gui...")
            self.bGui = True

        if self.bShell:  # and not self.bAutostart: # wird in OnInit gestoppt, falls laden von save klappte
            self.init_shell()

        super(StartupIFace, self).__init__(arg)

    def Destroy(self):
        PB.consoleOut("HEY, Destroy of PbWizard called. Shell running: %i"
                      "" % (self.civ4Shell.get("shell") is not None ))
        #stop_shell(self.civ4Shell)  # Give port free for new instance in PbAdmin
    """
    def Destroy(self):
        #stop_shell(self.civ4Shell)  # Give port free for new instance in PbAdmin
                      # (Re-using of this instance does not work (?!)
        self.wizard.Destroy()
        super(StartupIFace, self).Destroy()
    """

    def OnInit(self):
        PB.consoleOut("OnInit called.")
        global curPage

        if self.bAutostart and self.load_by_config():
            stop_shell(self.civ4Shell)
            # return False  # Would quit civ
            return True

        if self.bGui:
            #if self.bAutostart and self.load_by_config():
            if False:
                # return False  # Would quit civ
                # NOTE: Without Binding timer Civ4 will crash...
                timerID = wx.NewId()
                self.updateTimer = wx.Timer(self, timerID)
                self.Bind(wx.EVT_TIMER, self.OnTimedUpdate, id=timerID)
                self.updateTimer.Start(250)
                self.updateTimer.Stop()
                stop_shell(self.civ4Shell)
                return True

            # Autostart not enabled or failed...
            self.create_wizard_pages()
            curPage = self.modSelect
            self.wizard.FitToPage(curPage)

        # Create a timer callback that will handle our updates
        # TODO: Das immer erstellen?!
        timerID = wx.NewId()
        self.updateTimer = wx.Timer(self, timerID)
        self.Bind(wx.EVT_TIMER, self.OnTimedUpdate, id=timerID)
        self.updateTimer.Start(250)
        return True

    def create_wizard_pages(self):
        "Create the Pitboss Setup Wizard"
        self.wizard = wx.wizard.Wizard(None, -1, (LT.getText("TXT_KEY_PITBOSS_TITLE", ())))

        # Create each wizard page
        self.modSelect = ModSelectPage(self.wizard)
        self.smtpLogin = SMTPLoginPage(self.wizard)
        self.netSelect = NetSelectPage(self.wizard)
        self.login = LoginPage(self.wizard)
        self.loadSelect = LoadSelectPage(self.wizard)
        self.scenarioSelect = ScenarioSelectPage(self.wizard)
        self.staging = StagingPage(self.wizard)

        self.modSelect.SetNext(self.smtpLogin)
        self.smtpLogin.SetPrev(self.modSelect)
        self.smtpLogin.SetNext(self.netSelect)
        self.netSelect.SetPrev(self.smtpLogin)
        self.netSelect.SetNext(self.login)
        self.login.SetPrev(self.netSelect)
        self.login.SetNext(self.loadSelect)
        self.loadSelect.SetPrev(self.netSelect)
        self.loadSelect.SetNext(self.scenarioSelect)
        self.scenarioSelect.SetPrev(self.loadSelect)
        self.scenarioSelect.SetNext(self.staging)
        self.staging.SetPrev(self.loadSelect)

        PB.consoleOut("Creation of wizard pages finished")
        # self.progressDlg = None

    def init_shell(self):
        self.civ4Shell = {
            "glob": globals(),
            "loc": locals(),
            "shell": start_shell(PbSettings.get("shell", {}), "pb_wizard")
        }
        if self.civ4Shell["shell"]:
            PB.consoleOut("Init shell interface in PbWizard")
            # Propagate self to give shell the ability to close the wizard
            self.civ4Shell["shell"].set_startup_iface(self)
            self.civ4Shell["shell"].init()
        else:
            self.bShell = False

    """
    def init_shell(self):
        global Civ4Shell
        Civ4Shell = {
            "glob": globals(),
            "loc": locals(),
            "shell": start_shell(PbSettings.get("shell", {}), "pb_wizard")
        }
        if Civ4Shell["shell"]:
            PB.consoleOut("Init shell interface in PbWizard")
            # Propagate self to give shell the ability to close the wizard
            Civ4Shell["shell"].set_startup_iface(self)
            Civ4Shell["shell"].init()
        else:
            self.bShell = False
    """

    def load_by_config(self):
        # global bSaved
        global bPublic
        global bScenario

        adminPwd = str(PbSettings.get("save", {}).get("adminpw", ""))
        folderIndex = int(PbSettings.get("save", {}).get("folderIndex", 0))
        filename = str(PbSettings["save"]["filename"])
        (iResult, filepath) = loadSavegame(filename, folderIndex, adminPwd)

        if iResult == 0:
            PB.setLoadFileName(filepath)
            if not PB.host(bPublic, bScenario):  # host call auch beim laden notwendig
                PB.reset()
                return False
            else:
                # bSaved = True
                PB.getDone()
                PB.launch()
                return True
        else:
            # Loading of savegame failed. Thus, autostart was not possible
            # Missing error message for user here...
            PB.quit()
            return True  # False would restart updateTimer, but we want quit.

    def load_by_config2(self):
        global bPublic
        global bScenario

        adminPwd = str(PbSettings.get("save", {}).get("adminpw", ""))
        folderIndex = int(PbSettings.get("save", {}).get("folderIndex", 0))
        filename = str(PbSettings["save"]["filename"])
        (iResult, filepath) = loadSavegame(filename, folderIndex, adminPwd)

        if iResult == 0:
            PB.setLoadFileName(filepath)
            if not PB.host(True, False):
                PB.reset()
                return False
            else:
                return True
                # Zu viel des guten?!
                PB.getDone()
                PB.launch()
                return True
        else:
            # Loading of savegame failed. Thus, autostart was not possible
            # Missing error message for user here...
            PB.quit()
            return True  # False would restart updateTimer, but we want quit.

    # Called from EXE => name fixed
    def startWizard(self):
        # PB.consoleOut("StartWizard called")
        if self.bAutostart:
            #PB.consoleOut("StartWizard called by EXE, but autostart flag is"
            #              " set. Return immediately 'True' to inform EXE it"
            #              " could continue...")
            return True

        if not self.bGui:
            if self.bShell:
                #while self.updateTimer.IsRunning(): # Hm, Timer wird nicht ausgelöst ohne wx-Window
                #    PB.consoleOut("Wait...")
                #    time.sleep(0.25)

                while self.updateTimer.IsRunning():
                    self.OnTimedUpdate(None)
                    time.sleep(0.25)

            else:
                PB.quit()
                return False  # Quit Civ4

        global curPage

        # Try starting the wizard
        if self.wizard is None or curPage is None:
            # curPage is None if game was automaticly loaded
            #return None
            return True
        else:
            if self.wizard.RunWizard(curPage) and not PB.getDone():
                # launch game here
                self.updateTimer.Stop()
                stop_shell(self.civ4Shell)
                PB.launch()
                return True  # Continue with PbAdmin window...
            else:
                # user cancelled...
                self.updateTimer.Stop()
                stop_shell(self.civ4Shell)
                PB.quit()
                return False  # Quit Civ4

    def refreshRow(self, iRow):
        if not self.bGui or self.bAutostart:
            return True

        global curPage
        # Get the latest data from the app and display in the view
        if curPage == self.staging:
            # In the staging room, update the row
            curPage.refreshRow(iRow)

    def OnTimedUpdate(self, event):
        # PB.consoleOut("OnTimedUpdate ...")
        if self.bQuitWizard:
            self.updateTimer.Stop()
            if self.bGui:
                #self.wizard.Destroy()  # Triggers restart because RunWizard returns False
                self.wizard.ShowPage(None, True)  # Finishes Wizard without restart
            PB.consoleOut("Load save given by config: " +
                          str(self.load_by_config()))

        if self.bShell:
            try:
                self.civ4Shell["shell"].update(
                    self.civ4Shell["glob"],
                    self.civ4Shell["loc"])
            except Exception, e:
                PB.consoleOut("Civ4Shell error:" + str(e))


        # Handle received net messages
        PB.handleMessages()

    def displayMessageBox(self, title, desc):
        if self.bGui and False:
            global msgBox
            msgBox = wx.MessageDialog(self, desc, title, wx.OK)
            msgBox.Show(True)
        else:
            outMsg = title + ":\n" + desc
            PB.consoleOut(outMsg)

    def patchAvailable(self, patchName, patchUrl):
        PB.consoleOut("HEY patchAvailable")
        return

    def patchProgress(self, bytesRecvd, bytesTotal):
        PB.consoleOut("HEY patchProgress")
        return

    def cancelDownload(self):
        PB.consoleOut("HEY cancelDownload")
        return

    # Called from EXE?!
    def patchDownloadComplete(self, bSuccess):
        PB.consoleOut("HEY patchDownloadComplete")
        return

    def upToDate(self):
        PB.consoleOut("HEY upToDate")
        return

    def refreshCustomMapOptions(self, szMapName):
        global curPage

        # Refresh the page if we in the staging window
        if curPage == self.staging:
            # Update the custom map options in the staging room
            curPage.refreshCustomMapOptions(szMapName)

    def refreshAdvancedStartPoints(self, iPoints):
        global curPage

        # Refresh the page if we in the staging window
        if curPage == self.staging:
            # Update the custom map options in the staging room
            curPage.refreshAdvancedStartPoints(iPoints)


# ================ PB Mod ===================
def loadSavegame(filename, folderIndex=0, adminPwd=""):
    """Check if filename can be found in several folders
    and try to load this file

    If filename already contains the full path use
    folderIndex = -1.
    """
    filepath = None

    if folderIndex == -1:
        if os.path.isfile(filename):
            filepath = filename
    else:
        folderpaths = PbSettings.getPossibleSaveFolders()
        try:
            folderpaths.insert(0, folderpaths[folderIndex])
        except IndexError:
            pass

        for fp in folderpaths:
            tmpFilePath = os.path.join(fp[0], filename)
            if os.path.isfile(tmpFilePath):
                filepath = tmpFilePath
                break

    if filepath is None:
        iResult = -1
    else:
        pbPasswords = PbSettings.getPbPasswords()
        # pbPasswords.append(adminPwd)
        matchingPwd = Webserver.searchMatchingPassword(filepath, pbPasswords)
        if matchingPwd is None:
            iResult = -2
        else:
            iResult = PB.load(filepath, str(matchingPwd))  # should be 0
            # Store matching password hash for later usage.
            PbSettings.temp["adminpw"] = matchingPwd

    return (iResult, filepath)


def start_shell(shell_settings, mode=""):
    if shell_settings.get("enable", 0):
        # pythonDir = os.path.join(gc.getAltrootDir(), '..', 'Python', 'v8')
        # sys.path.append(pythonDir)
        import Civ4ShellBackend
        shell_ip = str(shell_settings.get("ip", "127.0.0.1"))
        shell_port = int(shell_settings.get("port", 3333))
        shell = Civ4ShellBackend.Server(shell_ip, shell_port)
        shell.set_mode(mode)

        return shell
    else:
        return None

def stop_shell(civ4Shell):
    if "shell" in civ4Shell:
        PB.consoleOut("Stop shell and wait on join")
        civ4Shell["shell"].close()
        # self.civ4Shell["shell"].t.join()  # TODO: Hangs if shell sends "pb_start"
        civ4Shell.clear()

