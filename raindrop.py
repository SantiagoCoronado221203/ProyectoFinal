import pygame
import random
from pygame.sprite import Sprite

class Raindrop(Sprite):
    """Una clase para manejar las gotas de lluvia que caen desde la parte superior de la pantalla."""

    def __init__(self, ai_game):
        """Inicializa una gota de lluvia en una posición aleatoria en la parte superior de la pantalla."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Cargar la imagen de la gota y establecer su rect
        self.image = pygame.image.load(r"imagenes/gota.bmp") 
        self.rect = self.image.get_rect()

        # Inicia cada gota en una posición aleatoria en la parte superior de la pantalla
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = random.randint(-50, 0) 

        # Almacena la posición vertical como un valor decimal
        self.y = float(self.rect.y)

    def update(self):
        """Hace que la gota se mueva hacia abajo en la pantalla"""
        # Actualizar la posición de la gota en función de la velocidad de caída
        self.y += self.settings.raindrop_speed
        self.rect.y = self.y

    def check_disappeared(self):
        """Devuelve True si la gota ha pasado el borde inferior de la pantalla."""
        return self.rect.top >= self.settings.screen_height