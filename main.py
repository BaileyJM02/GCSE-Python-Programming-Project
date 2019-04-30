import json, random

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
        players = [playerOne, playerTwo]
        cards = {"p1":"", "p2":""}
        for player in players:
            print("[" + player["User"] + "] You are picking a card... (press enter to continue)")
            # Wait for enter
            input("")
            # Select card
            cardPicked = random.choice(self.playingCards)
            # Remove selected card from list
            self.playingCards.remove(cardPicked)
            # Return selected card
            print("[" + player["User"] + "] You picked: "+cardPicked.replace("-", " ") + "\n")
            cards["p"+str(players.index(player)+1)] = cardPicked

        print("Cards (pick)")
        print(cards)
        return cards

    def findWinner(self, cards):
        # split array and get colour / number
        p1 = cards["p1"]
        p2 = cards["p2"]

        p1 = p1.split('-')
        p2 = p2.split('-')

        # Format to its own object
        p1 = {"Colour": p1[0], "Number": p1[1]}
        p2 = {"Colour": p2[0], "Number": p2[1]}

        # Compare colours first.
        print(p1)
        print(p2)

        return p1

        
# Basic database layout

DataBase_Init  = {
    "TimesRun": 0,
    "Users": {
        "Bailey":{
            "Pass":"0202",
            "Wins": 0,
        },
       "Trin":{
            "Pass":"2525",
            "Wins": 0,
        },
    },
    "TopScore": 100,
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
    p1["User"] = input("[Player One] Name: ")
    if data["Users"].get(p1["User"], False):
        #ask for password
        p1["Pass"] = input("[Player One] Password: ")
        if data["Users"][p1["User"]]["Pass"] != p1["Pass"]:
            print("Password incorrect, please try again.")
            getUserOne()
    else:
        print("Username incorrect, please try again.")
        getUserOne()

def getUserTwo():
    p2["User"] = input("[Player Two] Name: ")
    if data["Users"].get(p2["User"], False) and p2["User"] != p1["User"]:
        #ask for password
        p2["Pass"] = input("[Player Two] Password: ")
        if data["Users"][p2["User"]]["Pass"] != p2["Pass"]:
            print("Password incorrect, please try again.")
            getUserTwo()
    else:
        print("Username incorrect, please try again.")
        getUserTwo()

print("-------- Developer Notes --------\nProgram has been run:", data["TimesRun"], "times\n---------------------------------\n")

print("You are now playing \"Game of Cards\", have fun!\n")

# (Other user arguments are added once logged in)
p1 = {"Points": 0}
p2 = {"Points": 0}

# Ask users for their details
print("[Player One] Please enter your details.")
getUserOne()
print("[Player Two] Please enter your details.")
getUserTwo()

# And we begin...
print("\n\n-------- Woohoo! --------\nAll users authenticated.\nLet the games begin...\n-------------------------\n")

# Init the cards
cards = cards()

aa = cards.pick(p1, p2)
print(aa)
bb = cards.findWinner(aa)
print(bb)