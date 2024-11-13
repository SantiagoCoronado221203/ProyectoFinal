import pygame

class Settings:
    """Una clase para almacenar todos los ajustes de ALien Invasion"""
    
    def __init__(self):
        """Inicializa la configuración del juego"""
        #Configuración de pantalla
        self.screen_width = 2000
        self.screen_height = 800
        self.bg_color = (230,255,255)
        
        #Coinfiguración del barco
        self.ship_limit = 3
        
        #Configuracion balas
        self.bullets_allowed = 1000
        
        #Configuración aliens
        self.fleet_drop_speed = 10.0
        
        #Rapidez con la que se acelera el juego
        self.speedup_scale = 1.1
        
        #Rapidez con la que aumentan los puntos de los aliens.
        self.score_scale = 1.5
        
        #Velocidad de la lluvia
        self.raindrop_speed = 25
        
    def initialize_dynamic_settings(self):
        """Restablece la configuracion que cambia durante el juego"""
        self.ship_speed = 4.0
        self.bullet_speed = 5.0
        self.alien_speed = 3.0
        
        # fleet_direction: 1 representa derecha, -1 representa izquierda
        self.fleet_direction = 1
        
        #Puntuacion
        self.alien_points = 50
        
        
    def increase_speed (self):
        """Incrementa configuracion de velocidad y los puntos de los aliens"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
        
        
        