import gspread
from google.oauth2.service_account import Credentials
import pyinputplus as pyip

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('model_search')
MODELS_WORKSHEET = SHEET.worksheet('models')


def user_response(message, min_value, max_value):
    """
    Function used throughout the programme
    to validate users input from a list of choices.
    """
    input = pyip.inputInt(prompt=message, min=min_value, max=max_value)
    return input


def retrieve_records():
    """
    Function to retrieve all records found
    in the models list spreadhseet.
    """
    return MODELS_WORKSHEET.get_all_records()


def retrieve_all_models():
    """
    Function to retrieve full list of models
    """
    all_models = retrieve_records()
    print("\nNow retrieving all of your models...\n")
    for model in all_models:
        print_records_in_loop(model)


def print_records_in_loop(record):
    """
    Function to loop through all records passed
    as a parameter and print the details in a
    list of key: values.
    """
    for key, value in record.items():
        print(f"{key}: {value}")
    print("\n")


def show_menu():
    """
    Function to display menu items to user
    """
    print("\nMain menu")
    print("-----------------")
    print("1) See all Models")
    print("2) Add new Models")
    print("3) Search")
    print("4) Edit Models\n")


def menu():
    """
    User selects which task they would like to do, uses their input and runs
    elif loop to trigger the next process.
    If an invalid choice is input then the programme
    will alert user and ask for another choice.
    """
    while True:
        show_menu()
        choice = input('Enter your choice: ').lower()
        if choice == '1':
            retrieve_all_models()
        elif choice == '2':
            add_new_model()
        elif choice == '3':
            file_creation()
        elif choice == '4':
            return
        else:
            print(f'Not a correct choice: <{choice}>,try again')



def add_new_model():
    """
    Allows user to add new model information
    """
    first_name = str(pyip.inputStr('*First Name: ').capitalize())
    last_name = str(pyip.inputStr('*Last Name: ').capitalize())
    print("Please enter height in cm")
    height = int(pyip.inputInt('*Height: '))
    hair_colour = str(pyip.inputStr('*Hair Colour: ').capitalize())
    age = int(pyip.inputInt('*Age: '))
    gender = str(pyip.inputStr('*Gender: ').capitalize())

    new_model_info = [
        first_name, last_name, str(height),
        hair_colour, str(age), gender
        ]
    
    print(new_model_info)


if __name__ == '__main__':
    menu()

