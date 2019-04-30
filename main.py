import json

# Define db class so I can easily get, clear and write data.
class db:

    # x = class.get()
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

# Basic layout

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
    "list": [1, 2, 3],
}

db = db()
data = db.get()
if data == False:
    db.write(DataBase_Init)
data["TimesRun"] = data["TimesRun"] + 1
db.clear()
db.write(data)
print(data)

#makes it easier to re-call if error.
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
print("[Player One] Please enter your details.")
p1 = {}
p2 = {}

#Ask for user's details        
getUserOne()
getUserTwo()

print("\n\n-------- Woohoo! --------\nAll users authenticated.\nLet the games begin...\n-------------------------\n")
