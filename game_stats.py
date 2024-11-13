import json

class GameStats:
    """Estadisticas de seguimiento para Alien Invasion"""
    
    def __init__(self, ai_game):
        """Inicializar estadisticas"""
        self.settings = ai_game.settings
        self.reset_stats()
        
        #Iniciar el juego en un estado
        self.game_active = False
        
        #Cargar la puntuacion mas alta nunca reset
        self.high_score = self._load_high_score()
        
        
    def reset_stats(self):
        """Inicializa estadisticas que pueden cambiar durante el juego"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        
    def _load_high_score(self):
        """Carga la puntuacion mas alta desde un archivo"""
        try:
            with open("high_score.json", "r") as f:
                return int(json.load(f))
        except (FileNotFoundError, ValueError):
            return 0
        
    def save_high_score (self):
        """Guarda la puntuacion mas alta en un archivo"""
        with open ("high_score.json", "w") as f:
            json.dump(self.high_score, f)
            
    def reset_high_score (self):
        """Reinicia la puntuacion maxima a 0 y la guarda"""
        self.high_score = 0
        self.save_high_score()