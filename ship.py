import pygame
from pygame.sprite import Sprite

class Ship (Sprite):
    """Una clase para manejar la nave"""
    
    def __init__(self, ai_game):
        """Inicializa la nave y establece su posición inicial."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect ()
        self.settings = ai_game.settings
        
        #Cargue la imagen de la nave u obtenga su rect.
        self.image = pygame.image.load(r"imagenes/nave.bmp")
        self.rect = self.image.get_rect()
        
        #Comienza cada nueva nave en la parte inferior central de la pantalla
        self.rect.midbottom = self.screen_rect.midbottom
        
        #Almacena un valor decimal para la posición horizontal del barco
        self.x = float (self.rect.x)
        
        #Movimiento de bandera
        self.moving_right = False
        self.moving_left = False
        
    def update (self):
        """Actualiza la posición del barco en funcion de la bandera de movimiento"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            
        #Actualizar el objeto rect de sefl.x
        self.rect.x = self.x
        
    def blitme (self):
        """Dibiuja la nave en su ubicación actual."""
        self.screen.blit(self.image, self.rect)
        
        
    def center_ship(self):
        """centrar el barco en la pantalla"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)