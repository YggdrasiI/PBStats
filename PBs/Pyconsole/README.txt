== Shell for Civ4 ==

This extensions expands the Civ4 application by
a local TCP interface. You can send arbitary 
python commands to the running instance.


== Short description for PBStats ==

If shell is enabled in pbSettings.json type
         'python [-u] Pyconsole [port]'
into a terminal to connect you to the running game instance.

== Example usage ==

a) Call Python code directly to finish turn for Playerid X .

> python Pyconsole 3333
>       print(gc.getPlayer(X).getName())
>       gc.getGame().setActivePlayer(X, False)
>       CyMessageControl().sendTurnComplete()
>       gc.getGame().setActivePlayer(-1, False)  # Default for PB Host is -1
>       bye

b) Use predifined macro for above task. (Type 'help' to get a list of all commands)
> python Pyconsole 3333
>       pb_end_turn X
>       bye

c) List saves, edit config and restart server with new save.
> python Pyconsole 3333
>       list Playername
>       list Logoff.*P0
>       config edit save/filename=Logoff_P0_UserXY_T1507924088.CivBeyondSwordSave
>       config show
>       
Reload.CivBeyondSwordSave


== Setup  ==

1. Place Civ4ShellBackend.py into [Your mod]\Assets\Python

2. Add the following lines into your CvEventManager.py:

    # At head of file:
    CIV4_SHELL = True
    if CIV4_SHELL:
        import Civ4ShellBackend
        civ4Console = Civ4ShellBackend.Server(tcp_port=3333)

    # In CvEventManager.__init__:
            if CIV4_SHELL:
                self.glob = globals()
                self.loc = locals()
                civ4Console.init()

    # In CvEventManager.onGameUpdate
            if CIV4_SHELL:
                civ4Console.update(self.glob, self.loc)

3. Start Civ4 and load a game.

4. Type
     'python [-u] Pyconsole [port]' 
   into a local terminal window.  

5. Run 'test' in the new subshell to
   send a few commands to the Civ4 instance.

6. (Optional/Win-Only) Install pyreadline for
   command history, etc, https://pypi.python.org/pypi/pyreadline
   Pip command: pip install pyreadline

