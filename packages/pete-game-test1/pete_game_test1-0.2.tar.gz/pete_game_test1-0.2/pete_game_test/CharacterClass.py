from .GameClass import Game

class Character(Game):

    def __init__(self, _char_type = 'hero', _hp=12,_mp=2):
        Game.__init__(self, _hp,_mp)
        self.char_type = _char_type

    def change_to_hero(self):
        self.char_type = 'hero'

    def change_to_human(self):
        self.char_type = 'human'

    def change_to_npc(self):
        self.char_type = 'npc'

    def change_to_slave(self):
        self.char_type = 'slave'

    def show_type(self):
        print('current character type: ', self.char_type)
        return self.char_type