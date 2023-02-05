
"""
    Assigment for U5 A2: Plataforma Middleware

    Author: Eloy Uziel García Cisneros (eloy.garcia@edu.uag.mx)

    usage: python node.py
"""

#Standard imports
import logging

# Custom import
import game

logging.basicConfig(level='INFO')
LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    LOGGER.info('Starting game intance...')
    g = game.Game(500,500)
    g.run()
