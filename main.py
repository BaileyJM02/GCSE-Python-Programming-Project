import json, random, time

# Place at top to fix weird indent bug with multi-line text.
overallWinnerString = """\n\n\n
********* GAME WINNER **********
The winner of this game is:

            {User}

... with {Wins} total wins. 
********************************\n
"""
displayWinnerString = """
*******************
And the winner is of this round is
{User} with the card "{LastPicked}", congratulations!
*******************\n
"""

# Database managment
class db:
    def get(self):
        # Check if it errors
        try:
            f = open("./database.json","r")
            fr = f.read()
            f.close()
            datata = json.loads(fr)
            return datata
        
        # Return error
        except Exception as e:
            print("Error (get) : ",e)
            return False

    def write(self, param):
        # Check if it errors
        try:
            f = open("./database.json","w+")
            f.write(json.dumps(param))
            f.close()
            return True
        
        # Return error
        except Exception as e:
            print("Error: (write)",e)
            return False
        
    def clear(self):
        # Check if it errors
        try:
            f = open("./database.json","w+")
            f.truncate()
            f.close()
            return True

        # Return error
        except Exception as e:
            print("Error (clear): ",e)
            return False

class cards:
    def __init__(self):
        self.playingCards = [
            "Red-1","Red-2","Red-3","Red-4","Red-5","Red-6","Red-7","Red-8","Red-9","Red-10",
            "Black-1","Black-2","Black-3","Black-4","Black-5","Black-6","Black-7","Black-8","Black-9","Black-10",
            "Yellow-1","Yellow-2","Yellow-3","Yellow-4","Yellow-5","Yellow-6","Yellow-7","Yellow-8","Yellow-9","Yellow-10"
            ]

        #suffle cards on class call
        random.shuffle(self.playingCards)
    
    # return the cards for the class
    def get(self): 
        return self.playingCards

    # User picks a card eg. a.pick(p1, p2)
    def pick(self, playerOne, playerTwo):
        args = [playerOne, playerTwo]
        cards = {"p1":"", "p2":""}
        for player in args:
            print("[" + player["User"] + "] Pick a card... (press ↩ to continue)")
            # Wait for enter
            input("")
            # Select card
            cardPicked = random.choice(self.playingCards)
            # Remove selected card from list
            self.playingCards.remove(cardPicked)
            # Return selected card
            print("[" + player["User"] + "] You picked: "+cardPicked.replace("-", " ") + "\n")
            # Here is some maths, converted to a string, to get the correct player
            cards["p"+str(args.index(player)+1)] = cardPicked
            players["player"+str(args.index(player)+1)]["LastPicked"] = cardPicked
            players["player"+str(args.index(player)+1)]["Cards"].extend([cardPicked])

        print("Cards (pick)")
        print(cards)
        return cards

    def findWinner(self, cards):
        # split array and get colour / number
        p1 = cards["p1"]
        p2 = cards["p2"]

        p1 = p1.split('-')
        p2 = p2.split('-')

        # Format to its own object & convert number to int so we can compare correcty
        p1 = {"Colour": p1[0], "Number": int(p1[1])}
        p2 = {"Colour": p2[0], "Number": int(p2[1])}

        if p1["Colour"] == p2["Colour"]:
            # Compare number values
            if p1["Number"] > p2["Number"]:
                return {"p1": True, "p2": False}
            else:
                return {"p1": False, "p2": True}

        # If colour != colour
        else:
            if p1["Colour"] == "Red":
                # Only card Red wins against
                if p2["Colour"] == "Black":
                    return {"p1": True, "p2": False}
                else:
                    return {"p1": False, "p2": True}

            if p1["Colour"] == "Yellow":
                # Only card Yellow wins against
                if p2["Colour"] == "Red":
                    return {"p1": True, "p2": False}
                else:
                    return {"p1": False, "p2": True}
            
            if p1["Colour"] == "Black":
                # Only card Black wins against
                if p2["Colour"] == "Yellow":
                    return {"p1": True, "p2": False}
                else:
                    return {"p1": False, "p2": True}

    def displayWinner(self, winner):
        user = {}
        if winner["p1"]:
            user = players["player1"]
            players["player1"]["Wins"] += 1
        else:
            user = players["player2"]
            players["player2"]["Wins"] += 1

        print(displayWinnerString.format(**user))

    def overallWinner(self, participants):
        winner = {}
        if participants["player1"]["Wins"] > participants["player2"]["Wins"]:
            winner = participants["player1"]
        else:
            winner = participants["player2"]

        print(overallWinnerString.format(**winner))

        # Update database: 
        db = db()
        data = db.get()

        # Update user
        data[winner["User"]]["Wins"] = data[winner["User"]]["Wins"] + 1

        # Wins == Score in the database context: More wins per round.
        if data["TopScore"] < winner["Wins"]:
            data["TopScore"] == winner["Wins"]
            data[winner["User"]]["TopScoreHolder"] = True

        # Flush old data
        db.clear()

        # Write new
        db.write(data)

        
# Basic database layout

DataBase_Init  = {
    "TimesRun": 0,
    "Users": {
        "Bailey":{
            "Pass":"0202",
            "Wins": 0,
            "TopScoreHolder": False,
        },
       "Trin":{
            "Pass":"2525",
            "Wins": 0,
            "TopScoreHolder": False,
        },
    },
    "TopScore": 0,
}

db = db()
data = db.get()

# Init the database -> send default data
if data == False:
    db.write(DataBase_Init)

# Stats for us
data["TimesRun"] = data["TimesRun"] + 1

# Flush old data
db.clear()

# Write new
db.write(data)

# Makes it easier to re-call if error.
def getUserOne():
    players["player1"]["User"] = input("[Player One] Name: ")
    if data["Users"].get(players["player1"]["User"], False):
        #ask for password
        players["player1"]["Pass"] = input("[Player One] Password: ")
        if data["Users"][players["player1"]["User"]]["Pass"] != players["player1"]["Pass"]:
            print("Password incorrect, please try again.")
            getUserOne()
    else:
        print("Username incorrect, please try again.")
        getUserOne()

def getUserTwo():
    players["player2"]["User"] = input("[Player Two] Name: ")
    if data["Users"].get(players["player2"]["User"], False) and players["player2"]["User"] != players["player1"]["User"]:
        #ask for password
        players["player2"]["Pass"] = input("[Player Two] Password: ")
        if data["Users"][players["player2"]["User"]]["Pass"] != players["player2"]["Pass"]:
            print("Password incorrect, please try again.")
            getUserTwo()
    else:
        print("Username incorrect, please try again.")
        getUserTwo()

print("-------- Developer Notes --------\nProgram has been run:", data["TimesRun"], "times\n---------------------------------\n")

print("You are now playing \"Game of Cards\", have fun!\n")

# (Other user arguments are added once logged in)
players = {"player1": {"Wins": 0, "Points": 0, "Cards": [], "LastPicked": ""}, "player2": {"Wins": 0, "Points": 0, "Cards": [], "LastPicked": ""}, }

# Ask users for their details
print("[Player One] Please enter your details.")
getUserOne()
print("[Player Two] Please enter your details.")
getUserTwo()

# And we begin...
print("\n\n-------- Woohoo! --------\nAll users authenticated.\nLet the games begin...\n-------------------------\n")

# Init the cards
cards = cards()

while len(cards.get()) > 0:
    picked = cards.pick(players["player1"], players["player2"])
    winner = cards.findWinner(picked)
    cards.displayWinner(winner)
    time.sleep(2)


print(players["player1"])
print(players["player2"])