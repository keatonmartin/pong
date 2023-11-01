# =================================================================================================
# Contributing Authors:	    Keaton Martin
# Email Addresses:          ktma234@uky.edu
# Date:                     10/29/23
# Purpose:                  The pong server implementation.
# =================================================================================================

import socket
import threading

HOST = "localhost"
PORT = 12321
MAX_CONNS = 10 # maximum number of connections supported, should be even probably

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# number of seconds to wait before timing out on a blocking operation on a socket, i.e. read/write
TIMEOUT = 20

# Author: Keaton Martin
# Purpose: handleGame facilitates the exchange of game information between two clients playing together
# Pre: handleGame expects two live users at the end of sockets c1 and c2
# Post: After handleGame finishes, the socket connections to c1 and c2 are closed. 
def handleGame(c1: socket.socket, c2: socket.socket) -> None:
    # set timeouts on sockets
    c1.settimeout(TIMEOUT)
    c2.settimeout(TIMEOUT)

    # send paddle identities to clients
    c1.send(f"left {SCREEN_WIDTH} {SCREEN_HEIGHT}".encode()) 
    c2.send(f"right {SCREEN_WIDTH} {SCREEN_HEIGHT}".encode())
    
    # start game
    while True:
        try:

            # exchange paddle, score, and ball information
            c1state = c1.recv(1024).decode()
            c2state = c2.recv(1024).decode()

            c1.send(c2state.encode())
            c2.send(c1state.encode())

       except socket.timeout:
            print("Socket timed out; quitting game.")
            break
    # close client connections
    c1.close()
    c2.close()

def main(): 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNS)
  
    while True: 
        # attempt to pair two incoming clients 
        clientSocket1, _ = server.accept()
        print("Player one has connected.")
        clientSocket2, _ = server.accept()
        print("Player two has connected.")
        
        gameThread = threading.Thread(target=handleGame, args=(clientSocket1, clientSocket2))
        gameThread.start()

if __name__ == '__main__':
    main()
