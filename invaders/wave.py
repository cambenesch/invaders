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

Joel DeLong jkd76
Cameron Benesch cb776
12-4-2017
"""
from game2d import *
from consts import *
from models import *
import random

#consulted stack overflow
#https://stackoverflow.com/questions/869885/loop-backwards-using-indices-in-python
#where indicated (ctrl f ind2)
#consulted stack overflow, as my previous method for an empty list of the right
#parameters failed (https://stackoverflow.com/questions/2739552/2d-list-has-weird-behavor-
#when-trying-to-modify-a-single-value) where indicated (ctrl f ind1)




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

        _soundTracker: indicates which sound to play as aliens move [int]
        _moveSound: contains the first sound for alien movement, move1.wav [Sound]
        _moveSound2: contains the second sound for alien movement, move2.wav [Sound]
        _score: the player's score [int]
        _cool: the amount of time left before you can call handleBarrier again [int]
        _incr: [int]
        _numSteps: the number of steps taken by the aliens before a bullet is fired [int]
        _direction: the direction, 'right' or 'left', in which the aliens are currently moving [string]
        _edge: whether or not any aliens are touching the edge [boolean]
        _barrier1: [Barrier]
        _barrier2: [Barrier]
        _barrier3: [Barrier]
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setShipX(self,x):
        """
        A setter method to change the x coordinate of the ship to x
        RETURNS: the current value of self._health
        
        PARAMETERS:
        x:   the x value to set _ship.x to
                [GAME_WIDTH >= int >= 0]
        """
        if self._ship is not None:
            self._ship.x = x
            
    def getShipX(self):
        """
        A getter method to access the x coordinate of the ship
        
        RETURNS: the current value of _ship.x
        """
        if self._ship is not None:
            return self._ship.x
        else:
            return None
        
    def getTime(self):
        """
        A getter method to access the _time attribute
        
        RETURNS: the current value of _time
        """
        return self._time
    
    def getScore(self):
        """
        A getter method to access the _score attribute
        
        RETURNS: the current value of _score
        """
        return self._score
    
    def getLives(self):
        """
        A getter method to access the _lives attribute
        
        RETURNS: the current value of _lives
        """
        return self._lives
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes the ship.
        
        This method initializes all of the instance variables to
        their starting values, creating objects to store in their
        reference variables where applicable.
        """
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
        self._dline = GPath(points = [0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                            linewidth = 1, linecolor = 'grey')
        self._barrier1 = Barrier(GAME_WIDTH/4,DEFENSE_LINE)
        self._barrier2 = Barrier(GAME_WIDTH - 2*(GAME_WIDTH/4),DEFENSE_LINE)
        self._barrier3 = Barrier(GAME_WIDTH - (GAME_WIDTH/4),DEFENSE_LINE)
    
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the game objects to the view. Draws everything the player needs
        to see for the wave
        
        PARAMETERS:
        view:   the view to draw to
                [instance of GView]
        """
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
        """
        Method that creates a list of Alien objects, each spaced apart
        according to the specification in the instructions. Uses
        imageSelect to determine which image to use for each row of alien
        """
        counter = 0
        imageSelect = 0
        self._aliens = [[None]*ALIENS_IN_ROW for i in range(ALIEN_ROWS)] #ind1
        heightIncrementor = GAME_HEIGHT - (ALIEN_CEILING + ((ALIEN_ROWS-1) *
            (ALIEN_HEIGHT + ALIEN_V_SEP)))
        for row in range(ALIEN_ROWS):
            if counter == 2*ALIENS_IN_ROW:
                imageSelect += 1
                counter = 0
            
            if imageSelect > len(ALIEN_IMAGES)-1:
                imageSelect = 0
            for col in range(ALIENS_IN_ROW):
                self._aliens[row][col] = Alien((ALIEN_H_SEP + ALIEN_H_SEP
                                                + (col *(ALIEN_H_SEP + ALIEN_WIDTH))),
                    (heightIncrementor + (row *(ALIEN_V_SEP + ALIEN_HEIGHT))),
                    imageSelect)
                counter +=1
    
    def moveAliens(self):
        """
        Method that moves all of the aliens in _aliens by ALIEN_H_WALK except
        in the edge cases. In the edge case (the aliens would move past the border)
        it calls edgeHandler(). It then plays a sound and changes the sprite. It also
        calls _boltHelper to fire a random bolt from a random alien when applicable.
        """
        self._boltHelper()
        stop = False
        if self._edge is False:
            for row in range(ALIEN_ROWS):
                for col in range(ALIENS_IN_ROW):
                    if stop is False and self._aliens[row][col] != None:
                        if self._direction == 'left':
                            if min(self._aliens[row][col].x-ALIEN_H_WALK - (ALIEN_WIDTH/2)
                                   ,0) is 0:
                                self.playSound()
                                self._aliens[row][col].x=(self._aliens[row][col].x-ALIEN_H_WALK)
                                self._aliens[row][col].frame=(self._aliens[row][col].frame
                                                                +1)%2 #instructions
                            else:
                                self.edgeHandler(0)
                                stop = True
                        elif self._direction == 'right':
                            if max(GAME_WIDTH, self._aliens[row][col].x+ALIEN_H_WALK +
                                   (ALIEN_WIDTH/2)) is GAME_WIDTH:
                                self.playSound()
                                self._aliens[row][col].x = (self._aliens[row][col].x+
                                                            ALIEN_H_WALK)
                                self._aliens[row][col].frame = (self._aliens[row][col].frame
                                                                + 1) % 2 #instructions
                            else:
                                self.edgeHandler(1)
                                stop = True
        else:
            self.alienMoveV()

    def edgeHandler(self,d): # 0 means left, 1 means right for d
        """
        Method that handles the alien movement in the edge cases.
        parameter d indicates the direction that the aliens are moving.
        d = 0 means left and d = 1 means right. The handler moves the
        last remaining column of aliens to the edge of the game frame.
        It then sets _edge to True.
        
        PARAMETERS:
        d:      Direction that the aliens are currently moving
                [int that is 0 or 1]
        """
        startCol = 0
        first = False
        if d == 0:
            first = False
            startCol = 0
            for col in range(ALIENS_IN_ROW):
                for row in range(ALIEN_ROWS):
                    if self._aliens[row][col] is not None and first is False:
                        startCol = col; first = True
            for row2 in range(ALIEN_ROWS):
                for col2 in range(startCol,ALIENS_IN_ROW):
                    if self._aliens[row2][col2] != None:
                        self._aliens[row2][col2].x = 0 + (ALIEN_WIDTH/2 + ((col2-startCol)
                            *(ALIEN_H_SEP + ALIEN_WIDTH)))
            self._edge = True
        elif d == 1:
            first = False; endCol = ALIENS_IN_ROW
            for col in reversed(range(ALIENS_IN_ROW)): #ind2
                for row in range(ALIEN_ROWS):
                    if self._aliens[row][col] is not None and first is False:
                        endCol = col+1
                        first = True
            for row2 in range(ALIEN_ROWS):
                for col2 in range(0, endCol):
                    if self._aliens[row2][col2] != None:
                        self._aliens[row2][col2].x=GAME_WIDTH-(ALIEN_WIDTH+(endCol-1)
                            *(ALIEN_H_SEP+ALIEN_WIDTH))+ALIEN_WIDTH/2+col2*\
                        (ALIEN_H_SEP+ALIEN_WIDTH)
            self._edge = True
    
    def alienMoveV(self):
        """
        Method that handles the alien movement in the vertical direction.
        It moves all the aliens in _aliens down by ALIEN_V_WALK and changes
        the direction of movement.
        """
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
        """
        Method that handles the firing of alien bolts. An alien bolt is created
        in front of an alien randomly after _numSteps is equal to _incr.
        """
        self._incr += 1
        if self._numSteps == self._incr:
            col = random.randint(0,ALIENS_IN_ROW-1)
            row = random.randint(0,ALIEN_ROWS-1)
            while self._aliens[row][col] is None:
                col = random.randint(0,ALIENS_IN_ROW-1)
                row = random.randint(0,ALIEN_ROWS-1)
            self._bolts.append(Bolt(self._aliens[row][col].x,self._aliens[row][col].y
                                    - ALIEN_HEIGHT,-BOLT_SPEED))
            self._numSteps = random.randint(1,BOLT_RATE)
            self._incr = 0
            
    def checkCollision(self): #Gain 5 points for each alien, 15 for each row past the first
        """
        If a collision is detected, sets the value of the individual alien that was
        hit in the 2D array _aliens to None, effectively removing the alien from the
        screen. Uses the collides method to detect collisions. Also checks collisions
        for the ship itself, and removes lives or makes the ship ded accordingly.
        
        RETURNS: True if the ship is ded, False otherwise. 
        """
        a=0
        didHit = False
        dedShip = False
        while a <= len(self._bolts)-1:
            for row in range(ALIEN_ROWS):
                    for col in range(ALIENS_IN_ROW):
                        if self._aliens[row][col] is not None and\
                        self._aliens[row][col].collides(self._bolts[a]):
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
        """
        Method to handle new lives. If lives is positive, creates a new ship and
        returns True
        
        RETURNS: [True if lives is positive, False otherwise]
        """
        if self._lives > 0:
            self._ship = Ship()
            return True
        else:
            return False      
                    
    def isEmpty(self):
        """
        Method to check if _aliens is empty (all aliens have been changed to None)
        
        RETURNS: [True if all aliens are None, False otherwise]
        """
        empty = True
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self._aliens[row][col] is not None:
                    empty = False
        return empty
    
    def isOverLine(self):
        """
        Method to check if an alien crosses the defense line.
        
        RETURNS: [True if an alien is past the line, False otherwise]
        """
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self._aliens[row][col] is not None and\
                (self._aliens[row][col].y - ALIEN_HEIGHT) <= DEFENSE_LINE:
                    return True
        return False
    
    def handleBarrier(self, cooldown):
        """
        Processes everything related to the barriers on the bottom of the screen. This
        includes swapping barrier health images when the barrier is shot,
        making the barrier disappear when it has been shot 5 times, and checking for
        collisions to determine when the barrier is shot in the first place.
        Uses helper methods barrier1 and barrier2 to organize code by barrier.
        This individual method checks the first barrier for collisions. The main while
        loop checks whether each bolt has collided with the first barrier, and removes
        the bullet and decrements the barrier's health if a collision has indeed been
        detected. This method also resets the 3 arguments (excluding self) for the helper
        method barrier1.

        PARAMETERS
        cooldown:   the amount of time to subtract from _cool before you can check
                    the barrier again.
                    [type int]
        """
        self._cool -= cooldown
        if self._cool <= 0:
            didHit=False
            a=0
            tracker = 1
            while a <= len(self._bolts)-1:
                if self._barrier1 is not None and self._barrier1.collides(self._bolts[a])\
                and self._barrier1.getHealth() is not 0:
                    self._barrier1.removeHealth()
                    didHit = True
                elif self._barrier1 is not None:
                    if self._barrier1.getHealth() is 0:
                        didHit = True
                        self._barrier1 = None
                if didHit is True and tracker == 1:
                    del self._bolts[a]
                    tracker -= 1
                else:
                    a += 1
            didHit=False
            a=0
            tracker = 1
            self.barrier1(a, tracker, didHit)
            self.barrier2(a, tracker, didHit)
            
    def barrier1(self, a, tracker, didHit):
        """
        A helper for handleBarrier. 
        This individual method checks the second barrier for collisions. The main while
        loop checks whether each bolt has collided with the second barrier, and removes
        the bullet and decrements the barrier's health if a collision has indeed been
        detected. This method also resets the 3 arguments (excluding self) for the helper
        method barrier2. 
        
        PARAMETERS
        a:          The increment variable for the main while loop in this helper
                    method. Ranges from 0 to the number of bolts. 
                    [int]
        tracker:    Determines whether or not to check if the bullet collided with
                    the shield. This is reset for each bullet.
                    [int]
        didHit:     Once a collision has been detected, didHit is set to True for
                    the corresponding bullet. Otherwise, didHit is False. 
                    [boolean]
        """
        while a <= len(self._bolts)-1:
            if self._barrier2 is not None and self._barrier2.collides(self._bolts[a])\
            is True and self._barrier2.getHealth() is not 0:
                self._barrier2.removeHealth()
                didHit = True
            elif self._barrier2 is not None:
                if self._barrier2 is not None and self._barrier2.getHealth() is 0:
                        didHit = True
                        self._barrier2 = None
            if didHit is True and tracker == 1:
                del self._bolts[a]
                tracker -=1
            else:
                a += 1
        didHit=False
        a=0
        tracker = 1
        
    def barrier2(self, a, tracker, didHit):
        """
        Helper method for handleBarrier. This is called after barrier1 is completed.
        The main while loop in this method checks the third barrier for collisions.
        It checks whether each bolt has collided with the third barrier, and removes
        the bullet and decrements the barrier's health if a collision has indeed been
        detected. This method also resets didHit to False and resets the attribute
        _cool to 0.5 so that the barrier will not be checked for another 0.5 seconds.
        
        PARAMETERS
        a:          The increment variable for the main while loop in this helper
                    method. Ranges from 0 to the number of bolts. 
                    [int]
        tracker:    Determines whether or not to check if the bullet collided with
                    the shield. This is reset for each bullet.
                    [int]
        didHit:     Once a collision has been detected, didHit is set to True for
                    the corresponding bullet. Otherwise, didHit is False. 
                    [boolean]
        """
        while a <= len(self._bolts)-1:
            if self._barrier3 is not None and self._barrier3.collides(self._bolts[a])\
            is True and self._barrier3.getHealth() is not 0:
                self._barrier3.removeHealth()
                didHit = True
            elif self._barrier3 is not None:
                if self._barrier3.getHealth() is 0:
                    didHit = True
                    self._barrier3 = None
            if didHit is True and tracker == 1:
                del self._bolts[a]
                tracker -= 1
            else:
                a += 1
        didHit = False
        self._cool = .5
        
    def playSound(self):
        """
        Plays either _moveSound or _moveSound2 based on the value of _soundTracker
        """
        if self._soundTracker is 1:
            self._moveSound2.play()
            self._soundTracker += 1
        else:
            self._soundTracker = 1
            self._moveSound.play()
            
    def moveBolts(self):
        """
        Moves each bolt contained in the list _bolts, and checks if they are off
        the screen. If one is, it deletes the bolt that is off the screen
        """
        indexes = []
        a=0
        while a < len(self._bolts):
            placeHolder = self._bolts[a].moveBolt()
            if  placeHolder:
                del self._bolts[a]
            else:
                a += 1
                
    def isGoodBolt(self):
        """
        Checks if there is a player bolt on the screen. If there is returns
        True, else returns False
        RETURNS: boolean
        """
        answer = False
        for a in range(len(self._bolts)):
            if self._bolts[a].isPlayerBolt():
                answer = True
        return answer
    
    def zeroTime(self):
        """
        Sets _time to 0
        """
        self._time = 0
        
    def addBolt(self, newBolt):
        """
        Adds newBolt to the list of bolts _bolts
        
        PARAMETERS
        newBolt:   a bolt to add
                    [type Bolt]
        """
        self._bolts.append(newBolt)
            
    def addTime(self,add):
        """
        Adds add to _time
        
        PARAMETERS
        add:   an amount of time to add to _time
                    [type float or int]
        """
        self._time = self._time + add