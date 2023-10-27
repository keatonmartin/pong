# =================================================================================================
# Contributing Authors:	    Keaton Martin
# Email Addresses:          ktma234@uky.edu
# Date:                     10/27/23
# Purpose:                  The pong server implementation.
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

HOST = "localhost"
PORT = 12321
MAX_CONNS = 10 # should probably be even 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))

server.listen(MAX_CONNS)

def handleGame(c1, c2):
    print("Two clients are connected to me")

while True: 
    # attempt to pair two incoming clients 
    clientSocket1, _ = server.accept()
    print("Player one has connected.")
    clientSocket2, _ = server.accept()
    print("Player two has connected.")
    
    gameThread = threading.Thread(target=handleGame, args=(clientSocket1, clientSocket2))
    gameThread.run()











