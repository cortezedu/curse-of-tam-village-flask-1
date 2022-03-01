import json

# Class for the fighting characters (including the main hero)
class Player:
    # Initialize values for created Player.
    def __init__(self, name="", health=100, max_health=100, strength=5, defense=0,inventory=None):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.strength = strength
        self.defense = defense
        if (inventory == None):
            self.inventory = []
        else:
            self.inventory = inventory
    
    # String format when Player printed.
    def __repr__(self):
        return "{name}\tHealth: {health}%\n".format(name=self.name, health=self.health)
    
    def add_item(self, item):
        self.inventory.append(item)
    
    # Method when Player uses a heal item. Health cannot go beyond max health.
    def heal(self, item):
        self.health += item.points
        if self.health > self.max_health:
            self.health = self.max_health
        self.inventory.remove(item)
        print("{player_name} used {item} +{points}.\n\t{player}".format(player_name=self.name,item=item,points=item.points,player=self))
    
    # Method when Player uses armor item.
    def add_armor(self, item):
        self.defense += item.points
        self.inventory.remove(item)

    # Method when Player uses weapon item.
    def add_weapon(self, item):
        self.strength += item.points
        self.inventory.remove(item)

    # Method when Player gives the key item.
    def give_item(self, item, receiver):
        print("{giver} game {item} to {receiver}".format(giver=self.name,item=item,receiver=receiver.name))
        self.inventory.remove(item)
        receiver.add_item(item)
    
    # Method for attacking
    def attack(self, opponent):
        attack_points = int(self.strength - (opponent.defense/self.strength))
        opponent.health -= attack_points
        if (opponent.health < 0):
            opponent.health = 0
        print("{attacker} attacked {opponent_name}\n\t{opponent}".format(attacker=self.name,opponent_name=opponent.name,opponent=opponent))

    # Heal player
    def heal_player(self):
        if (len(self.inventory) >= 1):
            for item in self.inventory:
                if (item.category == "heal"):
                    item.use_item(self)

    # Check for heal item in inventory
    def check_heal(self):
        if (len(self.inventory) >=1):
            for item in self.inventory:
                if (item.category == "heal"):
                    return item
        else:
            return False
    
# Class for game items.
class Item:
    # Initialize game items.
    def __init__(self, name, category, points):
        self.name = name
        self.category = category
        self.points = points
    
    # String format when Item printed.
    def __repr__(self):
        return self.name
    
    # Method for using an item.
    def use_item(self, player_use):
        if (self.category == "armor"):
            player_use.add_armor(self)
        elif (self.category == "heal"):
            player_use.heal(self)
        elif (self.category == "weapon"):
            player_use.add_weapon(self)
        elif (self.category == "key"):
            player_use.give_item(self)

def to_json(my_object):
    if (type(my_object) == Player):
        for i in range(len(my_object.inventory)):
            my_object.inventory[i] = to_json(my_object.inventory[i])
        return json.dumps(my_object.__dict__)
    else:
        return json.dumps(my_object.__dict__)

def from_json(json_str):
    obj = json.loads(json_str)
    if (len(obj) == 3):
        return Item(obj['name'], obj['category'], obj['points'])
    else:
        for i in range(len(obj['inventory'])):
            obj['inventory'][i] = from_json(obj['inventory'][i])
        return Player(name=obj['name'], health=obj['health'], max_health=obj['max_health'], strength=obj['strength'], defense=obj['defense'],inventory=obj['inventory'])    