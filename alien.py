import pygame
from pygame.sprite import Sprite

class Alien (Sprite):
    """Una clase para representar un solo alien en la flota"""
    
    def __init__(self, ai_game):
        """Inicializa el alien y establece su posición inical"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        #Cargue la imagen alien y establesca su atibuto
        self.image = pygame.image.load (r"imagenes/alien.bmp")
        self.rect = self.image.get_rect()
        
        #Comienza cada nuevo alien cerca de la parte superior izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #Almacena la posición extacta del alien.
        self.x = float (self.rect.x)
        
        
    def update (self):
        """Mueve los aliens a la derecha o izquierda"""
        self.x += (self.settings.alien_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x
        
    def check_edges (self):
        """Devuelve True si un alien esta en el borde de la pantalla"""
        screen_rect = self.screen.get_rect()
        
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True