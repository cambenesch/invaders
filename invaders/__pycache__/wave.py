"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.  
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted 
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen. 
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you 
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of 
    aliens.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.
    
    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None] 
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Invaders.  Only add the getters and setters that you need for 
    Invaders. You can keep everything else hidden.
    
    You may change any of the attributes above as you see fit. For example, may want to 
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setShipX(self,x):
        if self._ship is not None:
            self._ship.x = x
    def getShipX(self):
        if self._ship is not None:
            return self._ship.x
        else:
            return None
    def playSound(self):
        if self._soundTracker is 1:
            self._moveSound2.play()
            self._soundTracker += 1
        else:
            self._soundTracker = 1
            self._moveSound.play()
            
    def getTime(self):
        return self._time
    def getScore(self):
        return self._score
    def getLives(self):
        return self._lives
    def addTime(self,add):
        self._time = self._time + add
    def zeroTime(self):
        self._time = 0
    def addBolt(self, newBolt):
        self._bolts.append(newBolt)
    def moveBolts(self):
        indexes = []
        a=0
        while a < len(self._bolts):
            placeHolder = self._bolts[a].moveBolt()
            if  placeHolder:
                del self._bolts[a]
            else:
                a += 1
    def isGoodBolt(self):
        answer = False
        for a in range(len(self._bolts)):
            if self._bolts[a].isPlayerBolt():
                answer = True
        return answer
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        self._didHit=False
        self._tracker = 1
        self._soundTracker = 1
        self._moveSound = Sound('move1.wav')
        self._moveSound2 = Sound('move2.wav')
        self._cool = 0
        self._score = 0
        self._lives = 3
        self._incr = 0
        self._numSteps = random.randint(1,BOLT_RATE)
        self._direction = 'right'
        self._bolts = []
        self._edge = False
        self._time = 0
        self.drawAliens()
        self._ship = Ship()
        self._dline = GPath(points = [0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE], linewidth = 1, linecolor = 'grey')
        self._barrier1 = Barrier(GAME_WIDTH/4,DEFENSE_LINE)
        self._barrier2 = Barrier(GAME_WIDTH - 2*(GAME_WIDTH/4),DEFENSE_LINE)
        self._barrier3 = Barrier(GAME_WIDTH - (GAME_WIDTH/4),DEFENSE_LINE)
    
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self._aliens[row][col] is not None:
                    self._aliens[row][col].draw(view)
        if self._ship is not None:
            self._ship.draw(view)
        if self._barrier1 is not None:
            self._barrier1.draw(view)
        if self._barrier2 is not None:
            self._barrier2.draw(view)
        if self._barrier3 is not None:
            self._barrier3.draw(view)
        self._dline.draw(view)
        for a in range(len(self._bolts)):
            self._bolts[a].draw(view)
    
    # HELPER METHODS FOR COLLISION DETECTION
    def drawAliens(self):
        counter = 0
        imageSelect = 0
        self._aliens = [[None]*ALIENS_IN_ROW for i in range(ALIEN_ROWS)] #consulted stack overflow, as my previous method for an empty list of the right parameters failed (https://stackoverflow.com/questions/2739552/2d-list-has-weird-behavor-when-trying-to-modify-a-single-value)
        heightIncrementor = GAME_HEIGHT - (ALIEN_CEILING + ((ALIEN_ROWS-1) * (ALIEN_HEIGHT + ALIEN_V_SEP)))
        for row in range(ALIEN_ROWS):
            if counter == 2*ALIENS_IN_ROW:
                imageSelect += 1
                counter = 0
            
            if imageSelect > len(ALIEN_IMAGES)-1:
                imageSelect = 0
            for col in range(ALIENS_IN_ROW):
                self._aliens[row][col] = Alien((ALIEN_H_SEP + ALIEN_H_SEP + (col *(ALIEN_H_SEP + ALIEN_WIDTH))),(heightIncrementor + (row *(ALIEN_V_SEP + ALIEN_HEIGHT))),imageSelect)
                counter +=1
    
    def moveAliens(self):
        self._boltHelper()
        stop = False
        if self._edge is False:
            for row in range(ALIEN_ROWS):
                for col in range(ALIENS_IN_ROW):
                    if stop is False and self._aliens[row][col] != None:
                        if self._direction == 'left':
                            if min(self._aliens[row][col].x-ALIEN_H_WALK - (ALIEN_WIDTH/2),0) is 0:
                                self.playSound()
                                self._aliens[row][col].x = (self._aliens[row][col].x-ALIEN_H_WALK)
                                self._aliens[row][col].frame = (self._aliens[row][col].frame + 1) % 2 #instructions
                            else:
                                self.edgeHandler(0)
                                stop = True
                        elif self._direction == 'right':
                            if max(GAME_WIDTH, self._aliens[row][col].x+ALIEN_H_WALK + (ALIEN_WIDTH/2)) is GAME_WIDTH:
                                self.playSound()
                                self._aliens[row][col].x = (self._aliens[row][col].x+ALIEN_H_WALK)
                                self._aliens[row][col].frame = (self._aliens[row][col].frame + 1) % 2 #instructions
                            else:
                                self.edgeHandler(1)
                                stop = True
        else:
            self.alienMoveV()


    def edgeHandler(self,d): # 0 means left, 1 means right for d
        startCol = 0
        first = False
        if d == 0:
            first = False
            startCol = 0
            for col in range(ALIENS_IN_ROW):
                for row in range(ALIEN_ROWS):
                    if self._aliens[row][col] is not None and first is False:
                        startCol = col
                        first = True
            for row2 in range(ALIEN_ROWS):
                for col2 in range(startCol,ALIENS_IN_ROW):
                    if self._aliens[row2][col2] != None:
                        self._aliens[row2][col2].x = 0 + (ALIEN_WIDTH/2 + ((col2-startCol) *(ALIEN_H_SEP + ALIEN_WIDTH)))
            self._edge = True
        elif d == 1:
            first = False
            endCol = ALIENS_IN_ROW
            for col in reversed(range(ALIENS_IN_ROW)): #stack overflow https://stackoverflow.com/questions/869885/loop-backwards-using-indices-in-python
                for row in range(ALIEN_ROWS):
                    if self._aliens[row][col] is not None and first is False:
                        endCol = col+1
                        first = True
            for row2 in range(ALIEN_ROWS):
                for col2 in range(0, endCol):
                    if self._aliens[row2][col2] != None:
                        self._aliens[row2][col2].x = GAME_WIDTH - (ALIEN_WIDTH + ((endCol-1) *(ALIEN_H_SEP + ALIEN_WIDTH))) + (ALIEN_WIDTH/2 + ((col2) *(ALIEN_H_SEP + ALIEN_WIDTH)))
            self._edge = True
    
    def alienMoveV(self):
        if self._direction == 'left':
                self._direction = 'right'
        else:
            self._direction = 'left'
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self._aliens[row][col] != None:
                    self._aliens[row][col].y = self._aliens[row][col].y - ALIEN_V_WALK
        self._edge = False
        
    def _boltHelper(self):
        self._incr += 1
        if self._numSteps == self._incr:
            col = random.randint(0,ALIENS_IN_ROW-1)
            row = random.randint(0,ALIEN_ROWS-1)
            while self._aliens[row][col] is None:
                col = random.randint(0,ALIENS_IN_ROW-1)
                row = random.randint(0,ALIEN_ROWS-1)
            self._bolts.append(Bolt(self._aliens[row][col].x,self._aliens[row][col].y - ALIEN_HEIGHT,-BOLT_SPEED))
            self._numSteps = random.randint(1,BOLT_RATE)
            self._incr = 0
            
    def checkCollision(self): #gain 5 points for each alien, + 15 for each row past the first
        a=0
        didHit = False
        dedShip = False
        while a <= len(self._bolts)-1:
            for row in range(ALIEN_ROWS):
                    for col in range(ALIENS_IN_ROW):
                        if self._aliens[row][col] is not None and self._aliens[row][col].collides(self._bolts[a]):
                            self._aliens[row][col] = None
                            self._score += 5
                            for x in range(row):
                                self._score += 15
                            didHit = True
            if self._ship is not None and self._ship.collides(self._bolts[a]) is True:
                self._ship = None
                self._lives -= 1
                didHit = True
                dedShip = True
            if didHit is True:
                del self._bolts[a]
                didHit = False
            else:
                a += 1
        return dedShip
    
    def newLife(self):
        if self._lives > 0:
            self._ship = Ship()
            return True
        else:
            return False
                    
    def isEmpty(self):
        empty = True
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self._aliens[row][col] is not None:
                    empty = False
                    
        return empty
    
    def isOverLine(self):
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self._aliens[row][col] is not None and (self._aliens[row][col].y - ALIEN_HEIGHT) <= DEFENSE_LINE:
                    return True
        return False
    
    def handleBarrier(self, cooldown):
        self._cool -= cooldown
        if self._cool <= 0:
            self._didHit = False
            self._tracker = 1
            self.handleBarrierHelper(self._barrier1)
            self._didHit = False
            self._tracker = 1
            self.handleBarrierHelper(self._barrier2)
            self._didHit = False
            self._tracker = 1
            self.handleBarrierHelper(self._barrier3)
            self._cool = .5
            
    def handleBarrierHelper(self,barrier):
        a=0
        while a <= len(self._bolts)-1:
            if barrier is not None and barrier.collides(self._bolts[a]) is True and barrier.getHealth() is not 0:
                barrier.removeHealth()
                self._didHit = True
            elif barrier is not None:
                if barrier.getHealth() is 0:
                    self._didHit = True
                    barrier = None
            if self._didHit is True and self._tracker == 1:
                del self._bolts[a]
                self._tracker -= 1
            else:
                a += 1