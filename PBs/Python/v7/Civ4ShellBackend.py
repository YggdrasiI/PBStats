#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

import sys
from StringIO import StringIO
from threading import Thread, Timer
from time import sleep

TCP_IP = '127.0.0.1'
TCP_PORT = 3333
BUFFER_SIZE = 1024
REMAP_STDOUT = True
EOF = '\x04'

class Server:
    def __init__(self, tcp_ip=TCP_IP, tcp_port=TCP_PORT):
        self.t = None
        self.code_store = list()  # Holds input for game loop thread.
        self.output_store = list() # Holds output for polling 
        self.run = False
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port

    def __del__(self):
        # Stop server
        self.run = False
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.tcp_ip, self.tcp_port))
        self.s.listen(1)
        self.conn, self.addr = self.s.accept()
        self.run = True

        while self.run:
            data = self.conn.recv(BUFFER_SIZE)
            if not data:
                print "(Civ4Shell) Client disconnects"
                self.conn, self.addr = self.s.accept()
                continue

            while data[-1] != EOF:
                if not data: break
                data += self.conn.recv(BUFFER_SIZE)

            data = data.rstrip(EOF)
            self.code_store.append(data)

            # Wait until other thread had handled one slice (everya. 0.25s)
            sleep(0.35)

            # Fetch output
            if len(self.output_store) > 0:
                self.conn.send("\n".join(self.output_store) + EOF)
                self.output_store[:] = []
            else:
                # Client expect message
                self.conn.send(EOF)

        if self.conn is not None:
            self.conn.close()

    def init(self):
        """ Should be called by game loop thread. """
        if self.t is None:
          self.t = Thread(target=self.start)
          self.t.setDaemon(True)
          self.t.start()

    def update(self, glob=globals(), loc=locals()):
        """ Should be called by game loop thread. """

        while len(self.code_store) > 0:
            data = self.code_store.pop(0)
            if data[0:2] == "P:":  # Call code
                # Execute input
                (out, err) = self.run_code(data[2:], glob, loc)

                # Propagate stdout and stderr
                if len(err) > 0:
                    err = '\n' + err
                self.output_store.append("%s%s%c" % ( out, err, EOF))
            elif data[0:2] == "Q:":  # Quit
                return False
            elif data[0:2] == "S:":  # Search/Completion
                # TODO
                break
            else:
                self.output_store.append("%s%c" % ( "No action defined for this input.", EOF))

        return True

    def run_code(self, code, glob, loc):
        """ Should be called by game loop thread only. """
        orig_filehandler = (sys.stdin, sys.stdout, sys.stderr)
        new_filehandler = (None, StringIO(), StringIO())

        if REMAP_STDOUT:
            sys.stdout = new_filehandler[1]
            sys.stderr = new_filehandler[2]

        try:
            exec(code, glob, loc)
        except:
            orig_filehandler[2].write(str(sys.exc_info()[0]))
            orig_filehandler[2].write('\n')
            orig_filehandler[2].flush()
            new_filehandler[2].write('\n')

        ret = (new_filehandler[1].getvalue(), new_filehandler[2].getvalue())

        if REMAP_STDOUT:
            sys.stdout = orig_filehandler[1]
            sys.stderr = orig_filehandler[2]
            # sys.stdout.write(ret[0])
            # sys.stderr.write(ret[1])

        return ret

# '''
from CvPythonExtensions import *
gc = CyGlobalContext()
class GameDummy:
    """ Simulates periodical call of game event loop in second thread.  """

    def __init__(self, seconds=2):
        self.slice = 0
        self.seconds = seconds
        self.timer = Timer(self.seconds, self.handle_function)
        self.timer.start()
        self.glob = globals()
        self.loc = locals()

    def handle_function(self):
        self.slice += 1
        if self.onGameUpdate((((self.slice,),),)):
            # Restart
            self.timer = Timer(self.seconds, self.handle_function)  # New context
            self.timer.start()

    """ Similar to definition in CvEventManager.py """
    def onGameUpdate(self, argsList):
        'sample generic event, called on each game turn slice'
        genericArgs = argsList[0][0]  # tuple of tuple of my args
        turnSlice = genericArgs[0]

        self.loc["turnSlice"] = turnSlice
        if civ4Console:
            return civ4Console.update(self.glob, self.loc);
        else:
            return False


if __name__ == "__main__":        
    civ4Console = Server()
    civ4Console.init()

    GameDummy(0.25)  # Loop
# '''
