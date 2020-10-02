import random
from texttable import Texttable

'''
class BowlingFrame
  class to contain logic of each individual game frame per player. 
  Game logic is based on frames per player rather than players per frame.

  Frames are contained within a doubly linked list. The LL is controlled by the player the frames are 
    assigned to. (See Player class below)

  Properties:
    - frameId: int between 1-10 inclusive, identifies the current frame in the game
    - strike and spare: booleans used later for creating accurate UI of scores
      - strike: boolean that assigns a given frame as a strike or not. Default is False
      - spare: boolean, same logic for strike above but applying to spares
    - total: int of the total points assigned to this frame, including bonuses from strikes and spares
    - rolls: array of the pins dropped on each of the rolls within a frame. E.g. a spare might look like [4, 6]
    - prev: reference to the previous frame node in the LL. Equals None for the first frame
    - next: reference to the next frame node int the LL. Equals None on the last frame

  Methods:
    - roll
      - roll1: first roll of the frame
      - roll2: second roll of the frame
      - Method sets the initial score of the frame and determines if strike or spare
      - Simulates third roll for tenth frames if already achieved a strike or spare
      - No return value
    
    - rollPerfect:
      - Takes no arguments
      - Applies identical logic as roll(), but with all strikes

'''
class BowlingFrame:
  def __init__(self, frameId, playerId):
    self.frameId = frameId
    self.strike = False
    self.spare = False
    self.total = 0
    self.rolls = []
    self.prev = None
    self.next = None

  def roll(self, roll1, roll2):
    self.rolls = [roll1, roll2]
    self.total += sum([roll1, roll2])
    if roll1 == 10:
      self.strike = True
    elif roll1 + roll2 == 10:
      self.spare = True

    
    if self.frameId == 10:
      if self.strike:
        roll2 = random.randint(0,10)
        self.rolls += [roll2]
        self.total += roll2
        if roll2 + random.randint(0, 10 - roll2) == 10:
          self.spare = True
        
        roll3 = random.randint(0, 10)
        self.rolls += [roll3]
        self.total += roll3

      elif self.spare:
        roll3 = random.randint(0, 10)
        self.rolls += [roll3]
        self.total += roll3
        
  def rollPerfect(self):
    roll1 = 10
    roll2 = 0

    self.rolls = [roll1, roll2]
    self.total += sum([roll1, roll2])
    if roll1 == 10:
      self.strike = True
    elif roll1 + roll2 == 10:
      self.spare = True

    
    if self.frameId == 10:
      if self.strike:
        roll2 = 10
        self.rolls += [roll2]
        self.total += roll2
        if roll2 + random.randint(0, 10 - roll2) == 10:
          self.spare = True
        
        roll3 = 10
        self.rolls += [roll3]
        self.total += roll3

      elif self.spare:
        roll3 = 10
        self.rolls += [roll3]
        self.total += roll3

'''
class Player
  class to contain logic of each individual player. 
  Each player instance contains a doubly linked list to track the player's frames and scores

  Properties:
    - playerId: int between 2-4 inclusive, identifies the current player in the game
    - head: reference to the current frame node in the LL
    - next: reference to the next frame node int the LL. Equals None on the last frame

  Methods:
    - push
      - No arguments
      - Method to add a new frame to the end of the LL, when progressing through the game
    
    - turn:
      - Simulates two rolls
      - Passes rolls to frame method to determine inital scoring
    
    - turnPerfect:
      - Simulates perfect roll
      - Calls perfect frame roll method to determine initial scoring

'''
class Player:
  def __init__(self, playerId):
    self.playerId = playerId
    self.head = None
    self.next = None

    newFrame = BowlingFrame(1, self.playerId)
    newFrame.prev = None
    self.head = newFrame 

  def push(self):
    newFrame = BowlingFrame(self.head.frameId + 1, self.playerId)
    newFrame.next = None
    lastFrame = self.head

    if self.head is None: 
      newFrame.prev = None
      self.head = newFrame 
      return

    while lastFrame.next is not None: 
      lastFrame = lastFrame.next

    lastFrame.next = newFrame 
    newFrame.prev = lastFrame

  def turn(self):
    roll1 = random.randint(0, 10)
    roll2 = random.randint(0, 10 - roll1)

    self.head.roll(roll1, roll2)

  def turnPerfect(self):
    self.head.rollPerfect()


'''
class BowlingGame
  class to contain logic of an individual bowling game. 
  Players are contained within a circular linked list (allows for ease of switching turns)

  Properties:
    - head: reference to the current player node in the LL
    - next: reference to the next player node int the LL
    - numPlayers: the selected value for the number of participants in the current game. Must be between 2-4 inclusive

  Methods:
    - addPlayer
      - playerId: int ID used to identify players amongst one another. Generated without user input
      - Method will add new player to the LL to place them within the flow of turns in the game
    
    - addAllPlayers:
      - Takes no arguments
      - Called on initialization only, adds the number of selected players to the game before starting
    
    - startGame:
      - Begins game loop of a normal, non-perfect game. Simulates 10 frames for each of the players before displaying scores
    
    - startPerfectGame:
      - Begins game loop of a perfect score game. Simulates 10 perfect frames for each of the players before displaying scores

    - drawScores:
      - Starting player: the current head node of the game's player list
      - Method to iterate over each player to call their scores to be drawn
    
    - drawPlayer:
      - playerId: ID of the player currently being scored
      - Method will calculate final bonuses and display each frame's scores for the given player
      - Texttable module used to pretty-print score tables

'''

class BowlingGame:
  def __init__(self, numPlayers = 2):
    self.head = None
    self.numPlayers = numPlayers
    self.addAllPlayers()

  def addPlayer(self, playerId):
    newPlayer = Player(playerId)
    tempNode = self.head

    newPlayer.next = self.head
    if self.head is not None: 
      while tempNode.next != self.head: 
        tempNode = tempNode.next
      tempNode.next = newPlayer
    else: 
      newPlayer.next = newPlayer
  
    self.head = newPlayer

  def addAllPlayers(self):
    for playerId in reversed(range(1, self.numPlayers + 1)):
      self.addPlayer(playerId)

  def startGame(self):
    while self.head.head.frameId in range(1,11):
      self.head.turn()
      self.head.push()

      if self.head.next.head.frameId <= 10:
        self.head.head = self.head.head.next
        
      self.head = self.head.next

    self.drawScores(self.head)

  def startPerfectGame(self):
    while self.head.head.frameId in range(1,11):
      self.head.turnPerfect()
      self.head.push()

      if self.head.next.head.frameId <= 10:
        self.head.head = self.head.head.next
        
      self.head = self.head.next

    self.drawScores(self.head)

  def drawScores(self, startingPlayer):
    while startingPlayer.playerId != self.numPlayers:
      startingPlayer = startingPlayer.next
      
    currentPlayer = startingPlayer.next
    
    while currentPlayer.playerId != startingPlayer.playerId:
      self.drawPlayer(currentPlayer)
      currentPlayer = currentPlayer.next
    
    self.drawPlayer(startingPlayer)

  def drawPlayer(self, player):
    currentFrame = player.head

    frameCount = 0
    while currentFrame.prev is not None:
      frameCount += 1
      currentFrame = currentFrame.prev
      
    frames = Texttable()
    frames.set_cols_align(["c"] * 10)
    frames.set_cols_valign(["m"] * 10)
    frames.set_cols_width([10] * 10)
    rowRolls = []
    rowTotals = []
    
    while currentFrame is not None and currentFrame.frameId <= 10:
      rolls = ["", " | ", ""]
      if currentFrame.next is not None and len(currentFrame.next.rolls) > 0:
        if currentFrame.spare:
          currentFrame.total += currentFrame.next.rolls[0]
        elif currentFrame.strike:
          currentFrame.total += currentFrame.next.rolls[0]
          
          if currentFrame.next.strike:
            currentFrame.total += 10
          else:
            currentFrame.total += currentFrame.next.rolls[1]  
      
      if currentFrame.prev is not None:      
        currentFrame.total += currentFrame.prev.total

      if len(currentFrame.rolls) > 0:
        rolls = [str(currentFrame.rolls[0])] + rolls[1:]

      if len(currentFrame.rolls) > 1:
        rolls[2] = str(currentFrame.rolls[1])

      if currentFrame.strike:
        rolls[0] = " "
        rolls[2] = "X"
      elif currentFrame.spare:
        rolls[2] = "/"

      if currentFrame.frameId == 10:
        if currentFrame.strike:
          rolls[0] = "X"

          if currentFrame.rolls[2] is not None:
            if currentFrame.rolls[2] == 10:
              rolls[2] = "X"
            else:
              rolls[2] = str(currentFrame.rolls[2])
            
          
          if currentFrame.rolls[3] is not None:
            if currentFrame.rolls[3] == 10:
              rolls += [" | X"]
            elif currentFrame.rolls[2] + currentFrame.rolls[3] == 10:
              rolls += [" | /"]
            else:
              rolls += [" | " + str(currentFrame.rolls[3])]
          

      rowRolls += ["".join(rolls)]
      rowTotals += [currentFrame.total]
      currentFrame = currentFrame.next
    
    print("Player " + str(player.playerId) + ":")
    frames.add_rows([rowRolls, rowTotals])
    print(frames.draw() + "\n\n")