import pymysql
from PetClass import Pet

#SQL Command to retrieve the desired data
petConnector = """
    select 
        pets.id,
        pets.name as petName,
        pets.age,
        owners.name as ownerName, 
        types.animal_type as animalType
    from pets 
        join owners on pets.owner_id = owners.id 
        join types on pets.animal_type_id = types.id;
    """

# Defines valid strings to quit. Input will be lower cased and checked against this list
quitCommands = {"q", "quit"}

# A function that prints a friendly message before exiting the program.
def quitter():
    print("Thanks for using the pet database! Bye!")
    exit()

# A function for waiting for user input before proceeding, with error catchers built in if the user tries something
# odd
def waiter():
    try:
        input("Press [ENTER] to continue.")
    # Error messages in case the user tries something odd with the waiting message
    except EOFError:
        print("Detected quit command from user, exiting...")
        quitter()
    except Exception as e:
        print(f"Unhandled exception: {e}. Quitting for safety.")
        quitter()

# Asks for mysql password and creates connection to mySQL. Allows for quitting, both by QUIT command or ctrl-D
try:
    password = input("Input mysql password (or type QUIT):")
    if password.lower() in quitCommands:
        quitter()
    myConnection = pymysql.connect(host="localhost",
                                   user="root",
                                   password=password,
                                   db="pets",
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
except EOFError:
    print("Detected quit command from user, exiting...")
    quitter()
except Exception as e:
    print(f"An error has occurred: {e}")
    print("Exiting...")
    print()
    exit()

# Executes SQL command defined at beginning then moves all information into a dictionary.
with myConnection.cursor() as cursor:
    cursor.execute(petConnector)
    petDict = cursor.fetchall()

# Takes dictionary and turns it into a list of Pet objects
listOfPets = list()
for pet in petDict:
    listOfPets.append(Pet(pet["petName"],
                          pet["ownerName"],
                          pet["age"],
                          pet["animalType"]))

# Loop to display options. Note that loop will continue until program is exited
while True:
    # Prints list, with one line for each pet.
    print("Choose a pet from the list below:")
    for i in range(0, len(listOfPets)):
        print("[", i+1, "]", listOfPets[i].petName)
    print("[ Q ] Quit")

    # After printing list, asks for input.
    try:
        choice = input()
        # Check if quit command is inputted
        if choice.lower() in quitCommands:
            quitter()
        # Attempts to turn input into integer
        choice = int(choice)
        if choice not in range(1, len(listOfPets) + 1):
            raise ValueError
    # Returns error message and waits if input is not an integer in the range.
    # Note we return to beginning of while loop after this message.
    except ValueError:
        print("Invalid selection. Please choose a number on the list.")
        print()
        waiter()
    # Allows quitting with Ctrl-D
    except EOFError:
        print("Detected quit command from user, exiting...")
        quitter()
    # Exits for unhandled exceptions
    except Exception as e:
        print(f"Unhandled exception: {e}. Quitting for safety.")
        quitter()
    # If valid input is detected, print pet information. Note loop restarts afterwards
    else:
        print("You have chosen " + listOfPets[choice - 1].petName + " the " + listOfPets[choice - 1].animalType + ".",
              listOfPets[choice - 1].petName + " is " + str(listOfPets[choice - 1].petAge) + " years old.",
              listOfPets[choice - 1].petName + "'s owner is " + listOfPets[choice - 1].ownerName + ".")
        print()
        waiter()