# -*- coding: utf-8 -*-
import sys
import os
import time
import re
import glob
import md5
from cStringIO import StringIO
import simplejson

from CvPythonExtensions import *
PB = CyPitboss()
gc = CyGlobalContext()
LT = CyTranslator()

# Add Altroot python folder as import path
pythonDir = os.path.join(gc.getAltrootDir(), '..', 'Python', 'v8')
if pythonDir not in sys.path:
    sys.path.append(pythonDir)
from Settings import Settings

PbSettings = Settings() #.instance()

def gen_answer(dict_or_info, status=None):
    # Shortcut which adds the always required '\n'
    if isinstance(dict_or_info, dict):
        if status:                        # Explicit set of return status
            dict_or_info["return"] = status
        if "return" not in dict_or_info:  # Implicit set of return status
            dict_or_info["return"] = "ok"

        return "%s\n" % (simplejson.dumps(dict_or_info),)
    else:
        if not status:                    # Implicit set of return status
            status = "ok"
        return "%s\n" % (simplejson.dumps(
            {'return': status, 'info': dict_or_info}),)

#####################################################################
# Definition of available Actions/Operations on Webinterface
#
def action_args_decorator(func):
    # Adding {} or StringIO() as default parameters is problematic
    # because this variables will be shared between all function calls.
    # To prevent this side effect, this decorator set the varables 'manually'.
    #
    def func_wrapper(inputdata=None, server=None, wfile=None):
        inputdata = inputdata or {}
        #server = server or Webserver.instance()
        wfile = wfile or StringIO()
        return func(inputdata, server, wfile)
    return func_wrapper

## Availabe actions on webinterface
#
# This functions should be written in a manner which allows to call them also
# over the Civ4Shell approach.
#
# - The default wfile-Argument is just a dummy object to omit 'if wfile:' checks
# - The try-catch-Block is optional.
#
# @action_args_decorator
# def action_template(inputdata, server, wfile):
#    try:
#        # The action commands
#        # […]
#         wfile.write(gen_answer('Reply'))
#    except:
#        if wfile:
#            wfile.write(gen_answer("Error description", "fail"))

@action_args_decorator
def action_template(inputdata, server, wfile):
    try:
        # The action commands
        # […]
        wfile.write(gen_answer('Reply'))
    except:
        if wfile:
            wfile.write(gen_answer("Error description", "fail"))


@action_args_decorator
def action_gamedata(inputdata, server, wfile):
    gamedata = createGameData()
    wfile.write(gen_answer(gamedata))


@action_args_decorator
def action_chat(inputdata, server, wfile):
    try:
        msg = str(inputdata.get("msg",
                                "Default message. Missing msg argument?!"))
        msg = msg.replace('&', '&amp;')
        msg = msg.replace('<', '&lt;')
        msg = msg.replace('>', '&gt;')
        PB.sendChat(msg)
        wfile.write(gen_answer('Send: ' + msg))
    except:
        wfile.write(gen_answer(
            'Some error occured trying to send the message. '
            'Probably a character that cannot be encoded.', "fail"))


@action_args_decorator
def action_autostart(inputdata, server, wfile):
    PbSettings.load(False)
    PbSettings.lock.acquire()
    PbSettings["autostart"] = int(inputdata.get("value", 0))
    PbSettings.lock.release()
    PbSettings.save()
    wfile.write(gen_answer('Autostart flag: '
                           '%i' % (PbSettings["autostart"],)))


@action_args_decorator
def action_headless(inputdata, server, wfile):
    PbSettings.load(False)
    PbSettings.lock.acquire()
    # PbSettings["noGui"] = int(inputdata.get("value", 0))
    PbSettings["gui"] = 1 - int(inputdata.get("value", 0))
    PbSettings.lock.release()
    PbSettings.save()
    wfile.write(gen_answer('Headless/noGui flag: '
                           '%i' % (1 - PbSettings["gui"],)))


@action_args_decorator
def action_save(inputdata, server, wfile):
    defaultFile = "Pitboss_" + PB.getGamedate(True)
    filename = "%s.CivBeyondSwordSave" % (
        str(inputdata.get("filename", defaultFile)),)
    # remove "\ or /" chars to cut of directory changes
    filename = filename[
        max(filename.rfind("/"), filename.rfind("\\")) + 1:
        len(filename)]

    ret = server.createSave(filename)
    wfile.write(gen_answer(ret))


@action_args_decorator
def action_turntimer(inputdata, server, wfile):
    iHours = int(inputdata.get("value", 24))
    PB.turnTimerChanged(iHours)
    wfile.write(gen_answer('Set turn timer on %i hours.' % (iHours,)))


@action_args_decorator
def action_currenttimer(inputdata, server, wfile):
    iSeconds = int(inputdata.get("seconds", 0))
    iMinutes = int(inputdata.get("minutes", 0))
    iHours = int(inputdata.get("hours", 0))
    iSeconds = iSeconds + 60*iMinutes + 3600*iHours
    if iSeconds < 60:
        iSeconds = 60
    gc.getGame().incrementTurnTimer(-PB.getTurnTimeLeft() +
                                    4 * iSeconds)
    wfile.write(gen_answer('Set timer for current round.'))


@action_args_decorator
def action_pause(inputdata, server, wfile):
    bPause = int(inputdata.get("value", 0))
    if bPause:
        if not gc.getGame().isPaused():
            PB.sendChat("(Webinterface) Activate pause.")
            gc.sendPause(0)
            # Note that babarian player index would
            # be nice, but leads to an error... just use index 0...
            #gc.sendPause(gc.getMAX_CIV_PLAYERS()-1)
        wfile.write(gen_answer('Activate pause.'))
    else:
        if gc.getGame().isPaused():
            PB.sendChat("(Webinterface) Deactivate pause.")
            # This removes the pause only locally.
            gc.getGame().setPausePlayer(-1)
            # This crashs on Linux/Wine
            # gc.sendPause(-1)
            # Workaround sends chat message
            gc.sendChat("RemovePause", ChatTargetTypes.CHATTARGET_ALL)
        wfile.write(gen_answer('Deactivate pause.'))


@action_args_decorator
def action_end_turn(inputdata, server, wfile):
    # Create Backup save in auto-Folder
    filename = r"Auto_" + \
        PB.getGamename() + r"_R" + str(PB.getGameturn()) + r"end_" + PB.getGamedate(False) + r".CivBeyondSwordSave"
    server.createSave(str(filename), 1)

    if(PB.getTurnTimer()):
        gc.getGame().incrementTurnTimer(-PB.getTurnTimeLeft() + 4 * 20)
        msg = 'Set timer on a few seconds.'
    else:
        # This variant made trouble with automated units
        # and KI?!
        messageControl = CyMessageControl()
        messageControl.sendTurnCompleteAll()
        msg = 'End turn'

    wfile.write(gen_answer(msg))


@action_args_decorator
def action_restart(inputdata, server, wfile):
    # Save current game and reload this save if no expicit
    # filename is given
    bReload = True

    filename = str(inputdata.get("filename", ""))
    folderIndex = int(inputdata.get("folderIndex", 0))
    # remove "\ or /" chars to cut of directory changes
    filename = filename[
        max(filename.rfind("/"), filename.rfind("\\")) + 1:
        len(filename)]

    # Use first folder if no filename is given
    if len(filename) == 0:
        folderIndex = 0

    if len(filename) > 0:
        # Save selected filename for reloading in the
        # settings file
        filename = filename + ".CivBeyondSwordSave"
        filename = filename.replace(
            "CivBeyondSwordSave.CivBeyondSwordSave",
            "CivBeyondSwordSave")
        # Now, checks if file can be found. Otherwise abort because
        # loading of missing files let crash the pb server
        # and grab 100% of cpu.
        folderpaths = PbSettings.getPossibleSaveFolders()
        try:
            folderpaths.insert(0, folderpaths[folderIndex])
        except IndexError:
            pass

        folderIndexFound = -1
        for fp in folderpaths:
            tmpFilePath = os.path.join(fp[0], filename)
            if os.path.isfile(tmpFilePath):
                folderIndexFound = fp[1]
                break

        if folderIndexFound == -1:
            # No save game with this filename found. Abort
            # reloading
            bReload = False
            wfile.write(gen_answer('Reloading failed. Can not detect path '
                                   'of save "%s".' % (filename,), "fail"))
        else:
            PbSettings.load(False)
            PbSettings.lock.acquire()
            PbSettings["save"]["filename"] = filename
            PbSettings["save"]["folderIndex"] = folderIndexFound
            PbSettings["save"]["oneOffAutostart"] = 1
            PbSettings.lock.release()
            PbSettings.save()

    else:
        PbSettings.load(False)
        PbSettings.lock.acquire()
        PbSettings["save"]["oneOffAutostart"] = 1
        PbSettings.lock.release()
        PbSettings.save()
        filename = "Reload.CivBeyondSwordSave"
        ret = server.createSave(filename)
        if ret["return"] != "ok":
            bReload = False
            wfile.write(gen_answer("Reloading failed. Was not able to "
                                   "save game.", "fail"))

    if bReload:
        # Quit server. The loop in the batch file should
        # restart the server....
        if server.adminWindow is not None:
            wfile.write(gen_answer('Set loaded file on "%s" and quit PB server'
                                   'window.' % (filename,)))
            server.adminWindow.OnExit(None)
        else:
            wfile.write(gen_answer("Reloading failed. Was not able "
                                   "to quit PB server window.", "fail"))


@action_args_decorator
def action_player_password(inputdata, server, wfile):
    playerId = int(inputdata.get("playerId", -1))
    newCivPW = str(inputdata.get("newCivPW", r""))
    ret = -1
    if playerId > -1:
        # Well, the hashing should be done in the DLL, but I forgot this
        # call and will not change the DLL in this version of the mod.
        # TODO: Move this line into the DLL for newer
        # versions of the mod.
        adminPW = str(PbSettings.temp.get(
            "adminpw", PbSettings.get("save", {}).get("adminpw", "")))
        if len(adminPW) > 0:
            adminPWHash = md5.new(adminPW).hexdigest()
        else:
            adminPWHash = ""

        ret = gc.getGame().setCivPassword(playerId, newCivPW, adminPWHash)

    if ret == 0:
        wfile.write(gen_answer('Passwort of player %i changed to "%s".'
                               "" % (playerId, newCivPW)))
    else:
        wfile.write(gen_answer("Password change failed.", "fail"))


@action_args_decorator
def action_remove_magellan(inputdata, server, wfile):
    gc.getGame().makeCircumnavigated()
    if int(inputdata.get("takebackBonus", 0)) > 0:
        """ We can not directly detect if extra moves was provided by magellan.
        Assuming simpliest case because it should be good enought in practice.
        """
        players_with_bonus = []
        for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
            gcPlayer = gc.getPlayer(iPlayer)
            iTeam = gcPlayer.getTeam()
            gcTeam = gc.getTeam(iTeam)
            if(gcTeam.getExtraMoves(DomainTypes.DOMAIN_SEA) > 0):
                gcTeam.changeExtraMoves(DomainTypes.DOMAIN_SEA, -1)
                players_with_bonus.append(gcPlayer.getName())

        if len(players_with_bonus) > 0:
            wfile.write(gen_answer("Remove magellan bonus for: %s."
                                   "" %(", ".join(players_with_bonus),)))
        else:
            wfile.write(gen_answer(
                "Disable future achievement of circumnavigagation bonus. "
                "No player had already an extra move."))
    else:
        wfile.write(gen_answer(
            "Disable future achievement of circumnavigagation bonus."))


@action_args_decorator
def action_kick_player(inputdata, server, wfile):
    playerId = int(inputdata.get("playerId", -1))
    if playerId > -1:
        PB.kick(playerId)
        wfile.write(gen_answer("Player %i was kicked." % (playerId,)))
    else:
        wfile.write(gen_answer("Wrong player id for kicking.", "fail"))


@action_args_decorator
def action_end_player_turn(inputdata, server, wfile):
    playerId = int(inputdata.get("playerId", -1))
    if playerId > -1 and playerId < gc.getMAX_CIV_PLAYERS():
        # gc.getGame().setActivePlayer(playerId, False)
        # CyMessageControl().sendTurnComplete()
        # gc.getGame().setActivePlayer(-1, False)
        gc.sendTurnCompletePB(playerId)
        wfile.write(gen_answer("Turn of player %i finished." % (playerId,)))
    else:
        wfile.write(gen_answer("Invalid player id.", "fail"))


@action_args_decorator
def action_player_color(inputdata, server, wfile):
    playerId = int(inputdata.get("playerId", -1))
    colorId = int(inputdata.get("colorId", -1))
    if playerId > -1 and colorId > -1:
        gc.getPlayer(playerId).setPlayerColor(colorId)
        wfile.write(gen_answer("Colorset of player %i changed to %i."
                               "" % (playerId, colorId)))
    else:
        wfile.write(gen_answer("Player color change failed.", "fail"))


@action_args_decorator
def action_get_motd(inputdata, server, wfile):
    try:
        motd = ""
        if server.adminApp is not None:
            motd = server.adminApp.getMotD()

        wfile.write(gen_answer({'info': 'Return MotD.', 'msg': motd}))
    except Exception, e:  # Old Python 2.4 syntax!
        wfile.write(gen_answer("Some error occured trying to get the MotD."
                               "Error msg: %s" % (str(e),), "fail"))


@action_args_decorator
def action_get_wbsave(inputdata, server, wfile):
    if not PbSettings["webserver"].get("allowWB", False):
        wfile.write(gen_answer({'return': 'ok', 'info': 'Action not allowd'}))
        return

    bCache = (inputdata.get("noCache", "0") == "0")
    bCompress = (inputdata.get("compress", "0") == "1")
    ret = server.createWBSave(bCache, bCompress)
    wfile.write(gen_answer(ret))


@action_args_decorator
def action_get_replay(inputdata, server, wfile):
    if not PbSettings["webserver"].get("allowReplay", False):
        wfile.write(gen_answer({'return': 'ok', 'info': 'Action not allowd'}))
        return

    try:
        replayInfo = gc.getGame().getReplayInfo()
        if replayInfo.isNone():
            replayInfo = CyReplayInfo()
            # (gc.getGame().getActivePlayer())
            replayInfo.createInfo(-1)

        iTurn = replayInfo.getInitialTurn()
        i = 0
        replayMessages = []
        while (i < replayInfo.getNumReplayMessages()):
            iPlayer = replayInfo.getReplayMessagePlayer(i)
            iTurn = replayInfo.getReplayMessageTurn(i)
            eMessageType = replayInfo.getReplayMessageType(i)
            eColor = replayInfo.getReplayMessageColor(i)
            colRgba = LT.changeTextColor("", eColor)
            color = colRgba[7:colRgba.find(">")]
            if eMessageType in [ReplayMessageTypes.REPLAY_MESSAGE_CITY_FOUNDED,
                                ReplayMessageTypes.REPLAY_MESSAGE_MAJOR_EVENT]:
                # Why does this not work?!
                # msgText = replayInfo.getReplayMessageText(i).decode('ascii', 'replace')
                msgText = replayInfo.getReplayMessageText(i)
                # filtering (generator syntax)
                msgText = ''.join(i for i in msgText if ord(i) < 128)
                replayMessages.append({'id': i, 'turn': iTurn,
                                       'player': iPlayer, 'color': color,
                                       'text': msgText})
            i += 1

        # Scores
        # iEnd = replayInfo.getReplayMessageTurn(i)
        iEnd = replayInfo.getFinalTurn()
        iStart = replayInfo.getInitialTurn()
        playerScores = {}
        for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
            gcPlayer = gc.getPlayer(iPlayer)
            if (gcPlayer.isEverAlive()):
                i = iStart
                score = []
                economy = []
                industry = []
                agculture = []
                while (i <= iEnd):
                    score.append(replayInfo.getPlayerScore(iPlayer, i))
                    economy.append(replayInfo.getPlayerEconomy(iPlayer, i))
                    industry.append(replayInfo.getPlayerIndustry(iPlayer, i))
                    agculture.append(replayInfo.getPlayerAgriculture(iPlayer, i))
                    i += 1
                playerScores[iPlayer] = {
                    'score': score, 'economy': economy,
                    'industry': industry, 'agriculture': agculture}

        wfile.write(gen_answer({'info': 'Return subset of replay messages.',
                                'replay': replayMessages,
                                'graphs': playerScores}))
    except Exception, e:  # Old Python 2.4 syntax!
        wfile.write(gen_answer("Some error occured trying to get the Replay. "
                               "Error msg: %s" % (str(e),), "fail"))


@action_args_decorator
def action_set_motd(inputdata, server, wfile):
    try:
        msg = str(inputdata.get("msg",
                                "No MotD given. Missing msg argument?!"))
        msg = msg.replace('&', '&amp;')
        msg = msg.replace('<', '&lt;')
        msg = msg.replace('>', '&gt;')
        PbSettings.load(False)
        PbSettings.lock.acquire()
        PbSettings["MotD"] = msg
        PbSettings.lock.release()
        PbSettings.save()

        if server.adminApp is not None:
            server.adminApp.setMotD(msg)

        wfile.write(gen_answer('New MotD: %s' % (msg,)))
    except Exception, e:  # Old Python 2.4 syntax!
        wfile.write(gen_answer("Some error occured trying to set the MotD. "
                               "Probably a character that cannot be encoded. "
                               "Error msg: %s" % (str(e),), "fail"))


@action_args_decorator
def action_set_short_names(inputdata, server, wfile):
    try:
        bShortNames = bool(inputdata.get("enable", True))
        iMaxLenName = int(inputdata.get("maxLenName", 1))
        iMaxLenDesc = int(inputdata.get("maxLenDesc", 4))
        PbSettings.load(False)
        PbSettings.lock.acquire()
        PbSettings["shortnames"] = {
            "enable": bShortNames,
            "maxLenName": iMaxLenName, "maxLenDesc": iMaxLenDesc}
        PbSettings.lock.release()
        PbSettings.save()
        gc.getGame().setPitbossShortNames(bShortNames,
                                          iMaxLenName, iMaxLenDesc)
        wfile.write(gen_answer(
            {'info': 'Short names enabled: %i'
                     ', Maximal length of Leadername: %i'
                     ', Maximal length of Civ description: %i'
                     '' % (bShortNames, iMaxLenName, iMaxLenDesc)}))
    except Exception, e:  # Old Python 2.4 syntax!
        wfile.write(gen_answer("Some error occured during setShortNames call. "
                               "Error msg: %s" % (str(e),), "fail"))


@action_args_decorator
def action_list_saves(inputdata, server, wfile):
    # Print list of saves of the selected folder.
    # This can be used for a dropdown list
    # of available saves.
    saveList = PbSettings.getListOfSaves()
    wfile.write(gen_answer({'return': 'ok', 'list': saveList}))


@action_args_decorator
def action_list_colors(inputdata, server, wfile):
    colorList = []
    for c in range(gc.getNumPlayerColorInfos()):
        playerColors = gc.getPlayerColorInfo(c)
        col = LT.changeTextColor(
            u"",
            playerColors.getColorTypePrimary())
        playerColor1 = col[7:col.find(">")]
        col = LT.changeTextColor(
            u"",
            playerColors.getColorTypeSecondary())
        playerColor2 = col[7:col.find(">")]
        col = LT.changeTextColor(
            u"",
            playerColors.getTextColorType())
        playerColor3 = col[7:col.find(">")]
        colorList.append({
            "primary": playerColor1,
            "secondary": playerColor2,
            "text": playerColor3,
            "usedBy": []
            })

    for rowNum in range(gc.getMAX_CIV_PLAYERS()):
        gcPlayer = gc.getPlayer(rowNum)
        if (gcPlayer.isEverAlive()):
            colorList[gcPlayer.getPlayerColor()]["usedBy"].append(
                {"id": rowNum, "name": gcPlayer.getName()})

    wfile.write(gen_answer({'colors': colorList}))


@action_args_decorator
def action_list_signs(inputdata, server, wfile):
    if not PbSettings["webserver"].get("allowSigns", False):
        wfile.write(gen_answer({'return': 'ok', 'info': 'Action not allowd'}))
        return

    engine = CyEngine()
    signs = []
    for i in range(engine.getNumSigns()-1, -1, -1):
        pSign = engine.getSignByIndex(i)
        sign = {
            'plot': [
                pSign.getPlot().getX(),
                pSign.getPlot().getY()],
            'id': pSign.getPlayerType(),
            'caption': pSign.getCaption()}
        signs.append(sign)

    wfile.write(gen_answer({'return': 'ok', 'info': signs}))


@action_args_decorator
def action_cleanup_signs(inputdata, server, wfile):
    if not PbSettings["webserver"].get("allowSigns", False):
        wfile.write(gen_answer({'return': 'ok', 'info': 'Action not allowd'}))
        return


    # Debugging: Reset all Signs. Remove some special chars
    engine = CyEngine()
    signs = []
    for i in range(engine.getNumSigns()-1, -1, -1):
        pSign = engine.getSignByIndex(i)
        sign = {
            'plot': [
                pSign.getPlot().getX(),
                pSign.getPlot().getY()],
            'id': pSign.getPlayerType(),
            'caption': pSign.getCaption()}
        signs.append(sign)
        engine.removeSign(
            pSign.getPlot(),
            pSign.getPlayerType())

    for sign in signs:
        caption = sign['caption']
        # caption = re.sub("[^A-z 0-9]","", caption) # not enought
        # caption = sign['caption'].encode('ascii',
        # 'ignore') # does not help
        caption = caption[0:18]  # shortening required
        caption = ''.join(
            i
            for i in caption if ord(i) < 128)  # filtering required
        sign['caption'] = caption
        engine.addSign(
            gc.getMap().plot(
                sign['plot'][0],
                sign['plot'][1]),
            sign['id'],
            caption.__str__())

    wfile.write(gen_answer({'return': 'ok', 'info': signs}))


@action_args_decorator
def action_mod_update(inputdata, server, wfile):
    """ Removes admin password, inits update and restart server.

    The updating component can be found in Assets/Python/Extra/ModUpdater.py
    Note that the internal update not works under Wine. Thus, on Windows
    machines, ModUpdater.py will be called by Civ4 itsself, but on Linux,
    by startPitboss.py!
    """
    # TODO: Update invoking over webinterface
    try:
        gc.getGame().setAdminPassword()
        wfile.write(gen_answer('Reply'))
    except:
        if wfile:
            wfile.write(gen_answer("Error description", "fail"))


@action_args_decorator
def action_unknown(inputdata, server, wfile):
    wfile.write(gen_answer(
        {'info':
         'Unknown action. Available actions are %s.'
         'For security reasons some commands require an explicit'
         'activation, see "allow*"-keys in pbSettings.json'
         '' % (', '.join(Action_Handlers.keys()),)
        }, "fail"))

Action_Handlers = {
    "chat": action_chat,
    "setAutostart": action_autostart,
    "setHeadless": action_headless,
    "save": action_save,
    "setTurnTimer": action_turntimer,
    "setCurrentTurnTimer": action_currenttimer,
    "setPause": action_pause,
    "endTurn": action_end_turn,
    "restart": action_restart,
    "setPlayerPassword": action_player_password,
    "removeMagellanBonus": action_remove_magellan,
    "kickPlayer": action_kick_player,
    "endPlayerTurn": action_end_player_turn,
    "setPlayerColor": action_player_color,
    "getMotD": action_get_motd,
    "getWBSave": action_get_wbsave,
    "getReplay": action_get_replay,
    "setMotD": action_set_motd,
    "setShortNames": action_set_short_names,
    "info": action_gamedata,
    "listSaves": action_list_saves,
    "listPlayerColors": action_list_colors,
    "listSigns": action_list_signs,
    "cleanupSigns": action_cleanup_signs,
    "modUpdate": action_mod_update,
}


#===== ?! accidential removed functions due creash ?!

def createGameData():
    # Collect all available data
    gamedata = {'gameTurn': PB.getGameturn(),
                'gameName': PB.getGamename(),
                'gameDate': PB.getGamedate(False),
                'bPaused': gc.getGame().isPaused(),
                'modName': PB.getModName(),
               }

    if(PB.getTurnTimer()):
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
            player = {'id': rowNum}
            player['finishedTurn'] = not playerData.bTurnActive
            player['name'] = gcPlayer.getName()
            player['score'] = playerData.getScore()
            player['ping'] = playerData.getPing()
            player['bHuman'] = playerData.bHuman
            player['bClaimed'] = playerData.bClaimed
            player['civilization'] = gcPlayer.getCivilizationDescription(0)
            player['leader'] = gc.getLeaderHeadInfo(
                gcPlayer.getLeaderType()).getDescription()
            player['color'] = u"%d,%d,%d" % (
                gcPlayer.getPlayerTextColorR(),
                gcPlayer.getPlayerTextColorG(),
                gcPlayer.getPlayerTextColorB())

            players.append(player)

    gamedata['players'] = players

    gamedata['bHeadless'] = PbSettings.get("noGui", 0)
    gamedata['bAutostart'] = PbSettings.get("autostart", 0)

    return gamedata

"""
def getSaveFolder(folderIndex=0):
    folderpaths = PbSettings.getPossibleSaveFolders()
    try:
        return folderpaths[folderIndex][0]
    except IndexError:
        return folderpaths[0][0]


def getListOfSaves(pattern="*", regPattern=None, num=-1):
    folderpaths = PbSettings.getPossibleSaveFolders()
    saveList = []
    fileList = []
    if regPattern:
        reg = re.compile(regPattern)

    for fp in folderpaths:
        folderpath = os.path.join(fp[0], pattern)
        for f in glob.glob(folderpath):
            fileList.append((f, fp[1]))

    # Add timestamp (as tuple)
    existingWithTimestamps = [
        (x[0], x[1], os.path.getctime(x[0])) for x in fileList]

    # Sort by timestamp
    existingWithTimestamps.sort(key=lambda xx: xx[2])

    # Remove oldest and non-saves
    existingWithTimestamps = [x for x in existingWithTimestamps if
                              x[0].endswith(".CivBeyondSwordSave")]
    if regPattern:
        existingWithTimestamps = [x for x in existingWithTimestamps if
                                  reg.search(x[0])]

    while len(existingWithTimestamps) > num and num >= 0:
        existingWithTimestamps.pop(0)

    for savefile in existingWithTimestamps:
        saveList.append({
            'name': os.path.basename(savefile[0]),
            'folder': os.path.dirname(savefile[0]),
            'folderIndex': savefile[1],
            'date': time.ctime(savefile[2]),
            'timestamp': savefile[2]
            })

    return saveList
"""
