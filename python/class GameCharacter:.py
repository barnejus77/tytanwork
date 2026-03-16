class GameCharacter:
    
    def __init__(self,name):
        self._name = name
        self._health = 100
        self._mana= 50
        self._level = 1
    @property
    def name(self):
        return self._name
    @property
    def health(self):
        return self._health
    @health.setter
    def health(self,new_health):
        if new_health < 0:
            self._health = 0
        if new_health > 100:
            self._health = 100
        if  new_health <= 100 and new_health >= 0:
            self._health = new_health
    @property
    def mana(self):
        return self._mana
    @mana.setter
    def mana(self,new_mana):
        if new_mana < 0:
            self._mana = 0
        if new_mana > 50:
            self._health = 50
        if new_mana <= 50 and new_mana >= 0:
            self._mana = new_mana
    def level_up(self):
        self._level = self._level + 1
        self.health = 100   
        self.mana = 50
        print(f"{self._name} leveled up to {self._level}!")    
    @property 
    def level(self):
        return self._level
    def __str__(self):
        return f"Name: {self._name}\nLevel: {self._level}\nHealth: {self._health}\nMana: {self._mana}"
    
k=GameCharacter("Kronos")
k.health =55
k.level_up()
print(k)