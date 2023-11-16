# =================================================================================================
# Contributing Authors:	    Keaton Martin
# Email Addresses:          ktma234@uky.edu
# Date:                     10/29/23
# Purpose:                  The pong server implementation.
# =================================================================================================

import socket
import threading

# to expose over eduroam, run ifconfig and change the host to the ip looking like 10.xx.xx.xx
HOST = "localhost"
PORT = 12321
MAX_CONNS = 10  # maximum number of connections supported, must be even

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# number of seconds to wait before timing out on a blocking operation on a socket, i.e. read/write
TIMEOUT = 5

# byte buffer size for io
BUF_SIZE = 128 

# Author: Keaton Martin
# handleClient represents one end of the bidirectional exchange of information between clients
# Pre: handleGame expects c1 to be the socket of a player, and c2 to be the socket of the player's opponent
# Post: After handleGame finishes, the socket connection to c1 is closed.
def handleClient(c1: socket.socket, c2: socket.socket) -> None:
    while True:
        try:
            # send paddle direction to opponent
            state = c1.recv(BUF_SIZE).decode()
            if len(state) == 0: break # recv returns 0 bytes if client closed
            c2.send(state.encode())
        except socket.TimeoutError:
            print("Socket timed out. Check connection.")
            break
    print("Closing client...")
    c1.close()

# Author: Keaton Martin
# Purpose: handleGame sets up the bidirectional exchange of game state between 
# two clients by spawning a handleClient thread for each client
# Pre: handleGame expects two live users at the end of sockets c1 and c2
# Post: After handleGame finishes, the socket connections to c1 and c2 are closed.
def createGame(c1: socket.socket, c2: socket.socket) -> None:

    # send paddle identities to clients
    c1.send(f"left {SCREEN_WIDTH} {SCREEN_HEIGHT}".encode())
    c2.send(f"right {SCREEN_WIDTH} {SCREEN_HEIGHT}".encode())

    # spawn client threads
    clientThread1 = threading.Thread(
            target=handleClient, args=(c1, c2)
    )
    clientThread2 = threading.Thread(
            target=handleClient, args=(c2, c1)
    )
    clientThread1.start()
    clientThread2.start()

# Author: Keaton Martin
# Purpose: main sets up the server socket and
# attempts to pair two clients and then spawns handleGame to perform game setup
# Pre: n/a
# Post: main shouldn't exit the while loop
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(MAX_CONNS)
    socket.setdefaulttimeout(TIMEOUT)
    while True:
        # attempt to pair two incoming clients
        clientSocket1, _ = server.accept()
        print("Player one has connected.")
        clientSocket2, _ = server.accept()
        print("Player two has connected.")
        
        # Although the logic in createGame is suitable to be contained in this while loop,
        # we spawn a separate thread so server can immediately accept and pair more connections
        gameThread = threading.Thread(
            target=createGame, args=(clientSocket1, clientSocket2)
        )
        gameThread.start()


if __name__ == "__main__":
    main()
