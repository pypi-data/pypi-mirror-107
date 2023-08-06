# Class as highest level game for interitance testing

class Game:
    
    def __init__(self, _hp = 10, _mp = 5):
        self.hp = _hp
        self.mp = _mp

    
    def get_current_hp(self):
        return self.hp

    def set_hp(self, _hp):
        self.hp = _hp

    def show_hp(self):
        print('current hp = ',self.hp)