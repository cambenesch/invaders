"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new 
class when you add extra features to an object. So technically Bolt, which has a velocity, 
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath 
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you 
add new features to your game, such as power-ups.  If you are unsure about whether to 
make a new class or not, please ask on Piazza.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from consts import *
from game2d import *
import cornell
import random

# PRIMARY RULE: Models are not allowed to access anything in any module other than 
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.
    
    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.
    
    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW Ship
    def __init__(self):
        """
        Initializes the ship.
        
        This method calls super() to use the initializer of GImage to create the
        image of the ship. Sets the width as SHIP_WIDTH, height as SHIP_HEIGHT,
        x as GAME_WIDTH/2, y as SHIP_BOTTOM, and the image as ship.png from the images folder
        """
        super().__init__(width=SHIP_WIDTH,height=SHIP_HEIGHT,x=int((GAME_WIDTH)/2),
                         y=(SHIP_BOTTOM),source='ship.png')
    
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self, bolt):
        """
        RETURNS: True if the ship collides with an alien bolt(bolt with -velocity), False otherwise 
        
        PARAMETERS:
        
        bolt  object of type Bolt
        PRECONDITION: type Bolt
        
        
        This method uses the method contains() to check if the ship contains one of the four corners
        of an alien bolt. If it does, that means that there is a collision and it returns true. Else
        there is no collision and it returns false.
        """
        collide = False
        if bolt.isPlayerBolt() == False:
            points = [self.contains(((bolt.x - int(bolt.width/2)), bolt.y)), self.contains(
                ((bolt.x + int(bolt.width/2)), bolt.y)), self.contains((bolt.x -int(bolt.width/2),
                                                                        bolt.y + BOLT_HEIGHT)),
                      self.contains(((bolt.x + int(bolt.width/2)), (bolt.y + BOLT_HEIGHT)))]
            for a in range(len(points)):
                if points[a] == True:
                    collide = True
            return collide
        else:
            return False
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GSprite):
    """
    A class to represent a single alien.
    
    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GSprite. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,x1,y1,n):
        """
        Initializes the alien.
        
        PARAMETERS:
        x1  the x coordinate of the alien (type int)
        PRECONDITION: GAME_WIDTH >= int >= 0
        
        y1  the y coordinate of the alien (type int)
        PRECONDITION: GAME_HEIGHT >= int >= 0
        
        n   the image number of the alien (from the constant ALIEN_IMAGES) (type int)
        PRECONDITION: int that is either 0, 1, or 2
        
        This method calls super() to use the initializer of GSprite to create the
        image of the alien. Sets the width as ALIEN_WIDTH, height as ALIEN_HEIGHT,
        x as x1, y as y1, the image as ALIEN_IMAGES[n], and the format of the
        sprite sheet as 3,2.
        """
        super().__init__(width=ALIEN_WIDTH,height=ALIEN_HEIGHT,x=x1,y=y1,
                         source=ALIEN_IMAGES[n],format=(3,2))
        
    
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self, bolt):
        """
        RETURNS: True if the alien collides with a ship bolt(bolt with +velocity), False otherwise 
        
        PARAMETERS:
        
        bolt  object of type Bolt
        PRECONDITION: type Bolt
        
        
        This method uses the method contains() to check if the alien contains one of the four corners
        of a ship bolt. If it does, that means that there is a collision and it returns true. Else
        there is no collision and it returns false.
        """
        collide = False
        if bolt.isPlayerBolt():
            points = [self.contains(((bolt.x - int(bolt.width/2)), bolt.y)),
                      self.contains(((bolt.x + int(bolt.width/2)), bolt.y)),
                      self.contains((bolt.x - int(bolt.width/2), bolt.y + BOLT_HEIGHT)),
                      self.contains(((bolt.x + int(bolt.width/2)), (bolt.y + BOLT_HEIGHT)))]
            for a in range(len(points)):
                if points[a] == True:
                    collide = True
            return collide
        else:
            return False
            
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    
    Laser bolts are often just thin, white rectangles.  The size of the bolt is 
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.
    
    The class Wave will need to look at these attributes, so you will need getters for 
    them.  However, it is possible to write this assignment with no setters for the 
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a 
    helper.
    
    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.
    
    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x1,y1,velocity):
        """
        Initializes the Bolt.
        
        PARAMETERS:
        x1  the x coordinate of the bolt (type int)
        PRECONDITION: GAME_WIDTH >= int >= 0
        
        y1  the y coordinate of the bolt (type int)
        PRECONDITION: GAME_HEIGHT >= int >= 0
        
        velocity   the amount the bolt will move up or down
        PRECONDITION: type int or float
        
        This method calls super() to use the initializer of GRectangle to create the
        image of the bolt. Sets the width as BOLT_WIDTH, height as BOLT_HEIGHT,
        x as x1, y as y1, the fillcolor as grey, and the linecolor as grey.
        It then creates a sound objects, and plays the sound. The sound is different
        based on if the bolt is player or alien.
        """
        super().__init__(x=x1,y=y1,width=BOLT_WIDTH,height=BOLT_HEIGHT,fillcolor='grey',
                         linecolor='grey')
        self._velocity = velocity
        if self.isPlayerBolt() is False:
            blastSound = Sound('pew1.wav')
            blastSound.play()
        else:
            blastSound = Sound('pew2.wav')
            blastSound.play()
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        RETURNS: True if the bolt is a ship bolt(bolt with +velocity), False otherwise 

        This method checks if the absolute value of the velocity is equal to the velocity.
        if it is, then the velocity is positive and it is a player bolt. Returns true. else
        it is negative (an alien bolt) and returns false
        """
        if abs(self._velocity) == self._velocity:
            return True
        else:
            return False
    
    def moveBolt(self):
        """
        RETURNS: True if the y of the bolt is greater than the game height,
        false otherwise
        
        A method to move the bolt.
        
        This method uses the velocity to change the position of the bolt. If
        called it changes the y position of the bolt to y + self._velocity.
        It then returns true if the y of the bolt is greater than the game height,
        false otherwise
        """
        self.y = self.y + self._velocity
        if self.y > GAME_HEIGHT:
            return True
        else:
            return False

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE

class Background(GRectangle):
    """
    A class representing a Background.
    
    A solid dark grey GRactangle for use as the background of the app
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self):
        """
        Initializes the Background.

        This method calls super() to use the initializer of GRectangle to create the
        image of the background. Sets the width as GAME_WIDTH, height as GAME_HEIGHT,
        x as GAME_WIDTH/2, y as GAME_HEIGHT/2, the fillcolor as a dark grey rgb object,
        and the linecolor as a dark grey rgb object.
        """
        super().__init__(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,width=GAME_WIDTH,
                         height=GAME_HEIGHT,fillcolor=cornell.RGB(50,50,50),
                         linecolor=cornell.RGB(50,50,50))
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

class Barrier(GSprite):
    """
    A class to represent a barrier (subclass of GSprite)
    
    Barriers break and change sprites when hit with alien or ship bolts
    and delete the bolt on impact. Three are created at the beginning
    of the game.
    
    INSTANCE ATTRIBUTES:
        _health:   the health of the barrier (number of times it can be hit before deleting)
                [0 or a positive integer]
        _track:  a counter to delay the damage animation by a set number of hits
                [0 or a positive integer <= 2]

    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getHealth(self):
        """
        A getter method to access the health of the barrier
        
        RETURNS: the current value of self._health
        """
        return self._health
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,x1,y1):
        """
        Initializes the Barrier.
        
        PARAMETERS:
        x1  the x coordinate of the barrier (type int)
        PRECONDITION: GAME_WIDTH >= int >= 0
        
        y1  the y coordinate of the barrier (type int)
        PRECONDITION: GAME_HEIGHT >= int >= 0
        
        This method calls super() to use the initializer of GSprite to create the
        image of the barrier. Sets the width as 3*ALIEN_WIDTH, height as ALIEN_HEIGHT,
        x as x1, y as y1, the source as shield.png, and the format as (1,3).
        It then initializes _health as 5 and _track as 0.
        """
        super().__init__(width=3*ALIEN_WIDTH,height=ALIEN_HEIGHT,x=x1,y=y1,
                         source='shield.png',format=(1,3))
        self._health = 5
        self._track = 0
        
    
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self, bolt):
        """
        RETURNS: True if the barrier collides with a bolt(bolt with + or - velocity), False otherwise 
        
        PARAMETERS:
        
        bolt  object of type Bolt
        PRECONDITION: type Bolt
        
        
        This method uses the method contains() to check if the barrier contains one of the four corners
        of a ship bolt. If it does, that means that there is a collision and it returns true. Else
        there is no collision and it returns false.
        """
        collide = False
        if bolt is not None:
            points = [self.contains(((bolt.x - int(bolt.width/2)), bolt.y)),
                      self.contains(((bolt.x + int(bolt.width/2)), bolt.y)),
                      self.contains((bolt.x - int(bolt.width/2), bolt.y + BOLT_HEIGHT)),
                      self.contains(((bolt.x + int(bolt.width/2)), (bolt.y + BOLT_HEIGHT)))]
        for a in range(len(points)):
            if points[a] == True:
                collide = True
        return collide

            
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def removeHealth(self):
        """
        A method to remove health from the barrier and change the sprite when applicable.
        
        Adds 1 to track and subtracts 1 from health. Then checks if it should change the sprite
        and does if the conditions are met.
        """
        self._track += 1
        self._health -= 1
        if self._track == 2:
            if self.frame == 0:
                self.frame = 2
                self._track = 0
            else:
                self.frame = 1
                self._track = 0
    