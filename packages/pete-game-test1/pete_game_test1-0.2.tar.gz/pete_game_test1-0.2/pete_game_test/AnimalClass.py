# from .Game import Game
from .CharacterClass import Character

class Animal(Character):

    def __init__(self, _type = 'penguin', _hp = 10, _mp=5):
        Character.__init__(self, 'npc',_hp, _mp)
        self.type = _type

    def animal_bark(self):
        print('anime bark with type: ', self.type)
        return self.type
