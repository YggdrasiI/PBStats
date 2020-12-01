== Project moved ==

This part of PBStats has a new home:
https://github.com/civ4-mp/pyconsole

== Shell for Civ4 ==

This extensions expands the Civ4 by a local TCP interface.
You can send arbitary python commands to the running instance.


== Short description for PBStats variant (Shell access to Pitboss server) ==

If shell is enabled in pbSettings.json type
         'python [-u] Pyconsole [port]'
into a terminal to connect you to the running game instance.


== Minimal working example: Pyconsole mod ==

1. Copy Mods/Pyconsole into your Civ4:BTS Mods folder.
2. Start Civ4 with Pyconsole mod, i.e.
   'wine Civ4BeyondSword.exe "mod= Pyconsole"'

3. Open terimnal window and type 
   > cd [..]/PBStats/test/Pyconsole
   > python -u Pyconsole 3333
   into a local terminal window.  

4. Run 'test' in the new subshell to
   send a few commands to the Civ4 instance.

5. (Optional/Win-Only) Install pyreadline for
   command history, etc, https://pypi.python.org/pypi/pyreadline
   Pip command: pip install pyreadline


== Integration of shell into your mod  ==

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


== Example usage of Pitboss variant ==

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
>       list PlayerX
>       list Logoff.*P0
>       config edit save/filename=Logoff_P0_PlayerX_T1507924088.CivBeyondSwordSave
>       config show
>       pb_start
>       bye

d) List 10 saves, and restart with second save of list
> python Pyconsole 3333
>       list 10
>       load 2
>       pb_start
>       bye


