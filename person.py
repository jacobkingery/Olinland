from mobile import *

class Person (MobileThing):    # Container...

    def __init__ (self,name,loc,desc):
        MobileThing.__init__(self,name,loc,desc)
        self._max_health = 5
        self._health = self._max_health
        self._pocket = []
        self._companion = None

    def max_health (self):
        return self._max_health

    def health (self):
        return self._health

    def reset_health (self):
        self._health = self._max_health
        return self._health

    def say (self,msg):
        loc = self.location()
        loc.report(self.name()+' says -- '+msg)

    def have_fit (self):
        self.say('Yaaaaah! I am upset!')

    def people_around (self):
        return [x for x in self.location().contents()
                    if x.is_person() and x is not self]

    def stuff_around (self):
        return [x for x in self.location().contents() if not x.is_person()]


    # this function should return everything that everyone in the
    # same location as this person are holding/carrying

    def peek_around (self):
        return [x for person in self.people_around() for x in person.check_pocket()]

    def check_pocket (self):
        return self._pocket

    def add_thing (self,t):
        self._pocket.append(t)

    def del_thing (self,t):
        self._pocket = [x for x in self._pocket if x is not t]

    def lose (self,t,loseto):
        self.say('I lose ' + t.name())
        self.have_fit()
        t.move(loseto)
    
    def go (self,direction):
        loc = self.location()
        exits = loc.exits()
        if direction in exits:
            t = exits[direction]
            if t.is_locked():
                loc.report(self.name()+' tries to go to '+t.name()+', but isn\'t able to get in right now')
                return False
            else:
                self.leave_room()
                loc.report(self.name()+' moves from '+ loc.name()+' to '+t.name())
                self.move(t)
                self.enter_room()
                return True
        else:
            print 'No exit in direction', direction
            return False


    def suffer (self,hits):
        self.say('Ouch! '+str(hits)+' hits is more than I want!')
        self._health -= hits
        if (self.health() <= 0):
            self.die()
        else:
            self.say('My health is now '+str(self.health()))
        if self._companion:
            self._companion.scratch()

    def die (self):
        self.location().broadcast('An earth-shattering, soul-piercing scream is heard...')
        for x in self.check_pocket():
            x.drop(self)
        self.destroy()
        

    def enter_room (self):
        people = self.people_around()
        if people:
            self.say('Hi ' + ', '.join([x.name() for x in people]))

    def leave_room (self):
        pass   # do nothing to reduce verbiage

    def take (self,actor):
        actor.say('I am not strong enough to just take '+self.name())

    def drop (self,actor):
        print actor.name(),'is not carrying',self.name()

    def give (self,actor,target):
        print actor.name(),'is not carrying',self.name()
        
    def accept (self,obj,source):
        self.say('Thanks, ' + source.name())

    def is_person (self):
        return True
