"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There 
is no need for any additional classes in this module.  If you need more classes, 99% of 
the time they belong in either the wave module or the models module. If you are unsure 
about where a new class should go, post a question on Piazza.

Joel DeLong jkd76
Cameron Benesch cb776
12-2-2017
"""
import cornell
import random
from consts import *
from game2d import *
from wave import *

#CITATION: used large parts of demo code state.py where indicated





# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.
    
    The primary purpose of this class is to manage the game state: which is when the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
                STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.
    
    For a complete description of how the states work, see the specification for the
    method update.
    
    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be 
    documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _lastkeys: the number of keys pressed last frame
                [int >= 0]
        _text2: The message displayed when the ship is shot. 
                [GLabel, or None if there is no message to display]
        _text3: The message saying 'Lives' preceding the number of lives remaining. 
                [GLabel, or None if there is no message to display]
        _text4: The message displaying number of lives remaining. 
                [GLabel, or None if there is no message to display]
        _text5: The message saying 'Score' preceding the number of lives remaining. 
                [GLabel, or None if there is no message to display]
        _text6: The message displaying the player's score. 
                [GLabel, or None if there is no message to display]
        _bye:   Whether the game has begun. 
                [boolean] (False if it has, True if it has not)
        _bye2:  Whether the game is active. If it's paused, over, or hasn't begun, this
                is False.
                [boolean]
        _background: The background of the game (a subclass of GObject)
                [Instance of the GRectangle subclass Background]
        _open:  The 'SPACE INVADERS' image from the opening screen. 
                [instance of GImage, or None]
        _right: The image of 3 aliens, to the right of the 'SPACE INVADERS' text on the
                opening screen.
                [instance of GImage, or None]
        _left:  The image of 3 aliens, to the left of the 'SPACE INVADERS' text on the
                opening screen.
                [instance of GImage, or None]
        _win:   Whether the player has won at the conclusion of the game.
                [boolean]
        _nope:  Whether to draw or not draw _wave (False to draw, True to not draw)
                [boolean]
        _alreadyDrew: Whether the opening screen was already created once (to avoid slowing down the program)
                [boolean. True if the opening screen has already been created, False otherwise]
        """
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _text) saying that the user should press to play a game.
        """
        self._state = STATE_INACTIVE
        self._nope = False #boolean to say weether or not to draw the wave
        self._wave = None
        self._open = None
        self._right = None
        self._left = None
        self._text2 = None
        self._text3 = GLabel(text="", font_name = "Arcade", font_size = 40, linecolor = 'white')
        self._text3.x = GAME_WIDTH - 100
        self._text3.y = GAME_HEIGHT - 40
        self._text4 = GLabel(text="", font_name = "Arcade", font_size = 40, linecolor = 'orange')
        self._text4.x = GAME_WIDTH - 20
        self._text4.y = GAME_HEIGHT - 40
        self._text5 = GLabel(text="", font_name = "Arcade", font_size = 40, linecolor = 'white')
        self._text5.x = 70
        self._text5.y = GAME_HEIGHT - 40
        self._text6 = GLabel(text="", font_name = "Arcade", font_size = 40, linecolor = 'orange')
        self._text6.x = 160
        self._text6.y = GAME_HEIGHT - 40
        self._alreadyDrew = False
        self._lastkeys = 0
        self._bye = False
        self._bye2 = False
        self._background = Background()
        
        
    
    def update(self,dt):
        """
        Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.
        
        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these 
        does its own thing and might even needs its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the 
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).
        
        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen. 
        The application switches to this state if the state was STATE_INACTIVE in the 
        previous frame, and the player pressed a key. This state only lasts one animation 
        frame before switching to STATE_ACTIVE.
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        STATE_CONTINUE: This state restores the ship after it was destroyed. The 
        application switches to this state if the state was STATE_PAUSED in the 
        previous frame, and the player pressed a key. This state only lasts one animation 
        frame before switching to STATE_ACTIVE.
        
        STATE_COMPLETE: The wave is over, and is either won or lost.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._startTextChecker()
        self._dedTextChecker()
        if self._state == STATE_INACTIVE:
            self._openingMethod()
        elif self._state == STATE_NEWWAVE:
            self._wave = Wave()
            self._state = STATE_ACTIVE
        elif self._state == STATE_ACTIVE:
            self._activeHandler()
        elif self._state == STATE_PAUSED:
            self._text2 = GLabel(text="You Died", font_name = "Arcade", font_size = 60, linecolor = 'orange')
            self._text2.x = 400
            self._text2.y = 400
            self._text = GLabel(text="Press Any Key to Respawn", font_name = "Arcade", font_size = 60, linecolor = 'grey')
            self._text.x = 400
            self._text.y = 350
            self._bye2 = False
        elif self._state == STATE_COMPLETE:
            self._completeHandler()

            
            
    
    def draw(self):
        """
        Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in 
        Wave. In order to draw them, you either need to add getters for these attributes 
        or you need to add a draw method to class Wave.  We suggest the latter.  See 
        the example subcontroller.py from class.
        """
        self._background.draw(self.view)
        if self._text != None:
            self._text.draw(self.view)
        if self._open != None:
            self._open.draw(self.view)
        if self._right != None:
            self._right.draw(self.view)
        if self._left != None:
            self._left.draw(self.view)
        if self._text2 != None:
            self._text2.draw(self.view)
        self._text3.draw(self.view)
        self._text4.draw(self.view)
        self._text5.draw(self.view)
        self._text6.draw(self.view)
        if self._wave != None and self._state is not STATE_PAUSED and self._nope is False:
            self._wave.draw(self.view)
        
    
    # HELPER METHODS FOR THE STATES GO HERE
    
    #CITATION: used large parts of demo code state.py
    def _startTextChecker(self):
        """
        When a key is pressed in the start screen, this method initiates the 
        transition from the start screen to gameplay and changes the
        game-state to STATE_NEWWAVE.
        
        To check whether a key is pressed, we require that first no keys are being
        pressed, then in the next update a key is pressed.
        """
        if self._bye is False:
            # Determine the current number of keys pressed
            curr_keys = self.input.key_count
        
            # Only change if we have just pressed the keys
            change = curr_keys > 0 and self._lastkeys == 0
        
            if change:
                self._state = STATE_NEWWAVE
                self._text = None
                self._open = None
                self._right = None
                self._left = None
                self._bye = True
        
            # Update last_keys
            self._lastkeys= curr_keys
            
    def _dedTextChecker(self):
        """
        When a key is pressed in the paused screen (after the player has lost a life), this
        method initiates the transition from the paused screen to gameplay and changes the
        game-state to STATE_ACTIVE.
        
        To check whether a key is pressed, we require that first no keys are being
        pressed, then in the next update a key is pressed.
        """
        if self._bye2 is False:
            # Determine the current number of keys pressed
            curr_keys = self.input.key_count
        
            # Only change if we have just pressed the keys
            change = curr_keys > 0 and self._lastkeys == 0
        
            if change:
                self._state = STATE_ACTIVE
                self._text = None
                self._text2 = None
                self._bye2 = True
        
            # Update last_keys
            self._lastkeys= curr_keys
            
    def _moveShip(self):
        """
        This method moves the ship to the right when the right arrow key is pressed
        and left when the left arrow key is pressed. If moving the ship by SHIP_MOVEMENT
        will cause it to go over the edge, it will be moved up to the edge.
        Input is received from the arrow keys and the ship is moved the number of
        pixels contained in the constant SHIP_MOVEMENT from consts.py.
        """
        if self.input.is_key_down('left'):
            if self._wave.getShipX() is not None and min(self._wave.getShipX()-SHIP_MOVEMENT - (SHIP_WIDTH/2),0) is 0:
                self._wave.setShipX(self._wave.getShipX()-SHIP_MOVEMENT)
            elif self._wave.getShipX is not None:
                self._wave.setShipX(0 + (SHIP_WIDTH/2))
        if self.input.is_key_down('right'):
            if self._wave.getShipX() is not None and max(self._wave.getShipX()+SHIP_MOVEMENT + (SHIP_WIDTH/2),GAME_WIDTH) is GAME_WIDTH:
                self._wave.setShipX(self._wave.getShipX()+SHIP_MOVEMENT)
            elif self._wave.getShipX is not None:
                self._wave.setShipX(GAME_WIDTH - (SHIP_WIDTH/2))
                
    def _openingMethod(self):
        """
        This method contains the code to be run during STATE_INACTIVE. It creates
        the start screen and updates _alreadyDrew. It only runs if _alreadyDrew is
        False
        """
        if self._alreadyDrew is False:
            self._open = GImage(source='opening.png', width = 300, height = 300)
            self._open.x = GAME_WIDTH/2
            self._open.y = 500
            self._right = GImage(source='right.png', width = 150, height = 150)
            self._right.x = 3*(GAME_WIDTH/4) + 30
            self._right.y = 500
            self._left = GImage(source='left.png', width = 150, height = 150)
            self._left.x = (GAME_WIDTH/4) - 30
            self._left.y = 500
            self._text = GLabel(text="Press Any Key to Begin", font_name = "Arcade", font_size = 60, linecolor = 'orange')
            self._text.x = GAME_WIDTH/2
            self._text.y = 250
            self._alreadyDrew = True
            
    def _activeHandler(self):
        """
        This method contains the code to be run during STATE_INACTIVE. It creates
        the start screen and updates _alreadyDrew. It only runs if _alreadyDrew is
        False
        """
        self._wave.handleBarrier(.1)
        self._moveShip()
        self._wave.moveBolts()
        self._wave.addTime(.017)
        self._text3.text = "Lives:"
        self._text4.text = str(self._wave.getLives())
        self._text5.text = "Score:"
        self._text6.text = str(self._wave.getScore())
        if len(str(self._wave.getScore())) > 3:
            self._text6.x = 160 + (len(str(self._wave.getScore())) - 3)*15
            
        dedShip = self._wave.checkCollision()
        if dedShip is True and self._wave.newLife() is True:
            self._state = STATE_PAUSED
        elif dedShip is True and self._wave.newLife() is False:
            self._state = STATE_COMPLETE
            self._win = False
        if self._wave.getTime() >= ALIEN_SPEED:
            self._wave.zeroTime()
            self._wave.moveAliens()
        if self._wave.isOverLine():
            self._state = STATE_COMPLETE
            self._win = False
        if self.input.is_key_down('spacebar') and self._wave.isGoodBolt() is False and self._wave.getShipX() is not None:
            self._wave.addBolt(Bolt(self._wave.getShipX(),SHIP_BOTTOM + (SHIP_HEIGHT/2),BOLT_SPEED))
        if self._wave.isEmpty():
            self._state = STATE_COMPLETE
            self._win = True
            
    def _completeHandler(self):
        """
        This method contains the code to be run during STATE_COMPLETE. It creates
        the end screen (a bunch of GLabels) based on if the game was won or lost
        (_win is True or False)
        """
        if self._win is False:
            self._nope = True
            self._text2 = GLabel(text="You Were Defeated by the Enemy", font_name = "Arcade", font_size = 40, linecolor = 'orange')
            self._text2.x = 400
            self._text2.y = 400
            self._text = GLabel(text="Good Luck Next Time", font_name = "Arcade", font_size = 80, linecolor = 'grey')
            self._text.x = 400
            self._text.y = 350
        else:
            self._text2 = GLabel(text="You Defeated the Enemy!", font_name = "Arcade", font_size = 45, linecolor = 'orange')
            self._text2.x = 400
            self._text2.y = 400
            self._text = GLabel(text="Great Job", font_name = "Arcade", font_size = 80, linecolor = 'grey')
            self._text.x = 400
            self._text.y = 350