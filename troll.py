import random
from npc import *

class Troll (NPC):

    def __init__ (self,name,loc,desc,restlessness,hunger):
        NPC.__init__(self,name,loc,desc,restlessness,10)
        self._hunger = hunger

        # Register proactive behaviors
        Player.clock.register(self.eat_people, 5)

    def eat_people (self,time):
      if not self.is_in_limbo():
        if random.randrange(self._hunger) == 0:
            people = self.people_around()
            if people:
                victim = random.choice(people)
                self.location().report(self.name() + ' takes a bite out of ' + victim.name())
                victim.suffer(random.randint(1,3))
            else:
                self.location().report(self.name() + "'s belly rumbles")

    def is_troll (self):
        return True
        