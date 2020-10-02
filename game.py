from classes import BowlingGame


print("Welcome to Triple-B Lanes")
bowling = True

#Loop to control state in or out of game, exiting of game
while bowling:
  print("Please enter the number of people in your group (2, 3, or 4), then press Enter\n")
  
  numPlayers = 2
  #Input validation loop for number of players
  while True:
    numPlayers = input()
    try:
      if int(numPlayers) not in [2,3,4]:
        print("Please enter a valid number of people in your group: 2, 3, or 4:\n")
      else:
        break
    except:
      print("Please enter a valid number of people in your group: 2, 3, or 4:\n")


  print("Would you like to see a perfect game? Enter Y or N:\n")
  perfect = "N"
  #Input validation loop for perfect game
  while True:
    perfect = input()
    
    if perfect not in ["Y","y","N","n"]:
      print("Please enter either Y or N:\n\n")
    else:
      break

  print("Post game scores are shown below:\n\n")
  #Simulate bowling and display scores
  if perfect == "Y" or perfect == "y":
    BowlingGame(numPlayers=int(numPlayers)).startPerfectGame()
  else:
    BowlingGame(numPlayers=int(numPlayers)).startGame()
  
  print("\n\nWould you like to play again? Enter Y or N:\n")
  again = "Y"
  #Input validation loop to play again
  while True:
    again = input()
    
    if again not in ["Y","y","N","n"]:
      print("Please enter either Y or N:\n\n")
    else:
      break

  if again == "N" or again == "n":
    break

print("Thanks for playing!")