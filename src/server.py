"""
    Assigment for U5 A2: Plataforma Middleware

    Author: Eloy Uziel García Cisneros (eloy.garcia@edu.uag.mx)

    usage: python server.py
"""

# Stabdard imports
import socket
import threading
import random
import pickle
import time
import logging

# Third-party
from pygame.rect import Rect

logging.basicConfig(level='INFO')
LOGGER = logging.getLogger(__name__)

SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVER, PORT = 'localhost', 20001
SOCK.bind((SERVER, PORT))
SOCK.listen(10)


PLAYERS = {}
HUNTER = {'player': None, 'since': time.time()}
COIN_COLOR = (255, 215, 0, 255)

COLORS = [(255, 105, 180, 255),
          (238, 0, 0, 255),
          (135, 206, 235, 255),
          (0, 255, 127, 255),
          (255, 99, 71, 255),
          (238, 58, 140, 255),
          (92, 172, 238, 255),
          (255, 140, 105, 255),
          (238, 180, 180, 255),
          (145, 44, 238, 255)]

P_SIZE = (50, 50)
C_SIZE = (25, 25)

def spawn_coin():
    global HUNTER
    time.sleep(9)
    while True:
        time.sleep(1)
        if 'coin' in PLAYERS:
            continue
        
        if HUNTER.get('player') and HUNTER['since'] + 10 > time.time():
            continue

        init_pos = [random.randint(0,450), random.randint(0,450)]
        PLAYERS['coin'] =  {'id_': 'coin', 'color': COIN_COLOR, 'rect': Rect(*init_pos, *C_SIZE)}
        HUNTER['player'] = None

def threaded_client(conn, addr):
    LOGGER.info('Starting client thread.')
    global PLAYERS, COLORS, HUNTER

    init_pos = [random.randint(0,450), random.randint(0,450)]
    color = random.randint(0, len(COLORS)-1)

    # Registering player
    PLAYERS[addr] = {'color': COLORS[color], 'id_': addr, 'rect': Rect(*init_pos, *P_SIZE)}
    data = pickle.dumps(PLAYERS[addr])
    conn.send(data)

    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            PLAYERS[addr]['rect'].x = data['x']
            PLAYERS[addr]['rect'].y = data['y']

            if coin := PLAYERS.get('coin'):
                if coin['rect'].colliderect(PLAYERS[addr]['rect']):
                    del PLAYERS['coin']
                    HUNTER['player'] = addr
                    HUNTER['since'] = time.time()
            elif (hunter_id := HUNTER.get('player', addr)) is not None and hunter_id != addr:
                # Player dead, keep connection open to keep client as spectator.
                if PLAYERS[addr]['rect'].colliderect(PLAYERS[hunter_id]['rect']):
                    PLAYERS[addr]['dead'] = True

            conn.sendall(pickle.dumps(PLAYERS))
        except Exception:
            break

    LOGGER.info("Connection Closed %s", addr)
    if PLAYERS.get(addr):
        del PLAYERS[addr]
    conn.close()

if __name__ == '__main__':
    LOGGER.info('Starting coin thread')
    threading.Thread(target=spawn_coin, daemon=True).start()

    while True:
        LOGGER.info('Waiting for next player...')
        conn, addr = SOCK.accept()
        LOGGER.info("%s Connected!", addr)

        threading.Thread(target=threaded_client, args=(conn, addr), daemon=True).start()
