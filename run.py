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
            search_models()
        elif choice == '4':
            return
        else:
            print(f'Not a correct choice: <{choice}>,try again')


def add_new_model():
    """
    Allows user to add new model information
    """
    while True:
        first_name = pyip.inputStr('*First Name: ')
        if first_name.isalpha():
            break
        else:
            print("Enter letters only")
    while True:
        last_name = pyip.inputStr('*Last Name: ')
        if last_name.isalpha():
            break
        else:
            print("Enter letters only")
    print("Please enter height in cm, for example 123")
    height = int(pyip.inputInt('*Height: '))
    while True:
        hair_colour = pyip.inputStr('*Hair Colour: ')
        if hair_colour.isalpha():
            break
        else:
            print("Enter letters only")
    age = int(pyip.inputInt('*Age: '))
    gender = pyip.inputMenu(['Male', 'Female', 'Other'], numbered=True)

    new_model_info = [
        first_name, last_name, str(height),
        hair_colour, str(age), gender
        ]
    print(f'The data you have entered is: <{new_model_info}>')
    print("\nWould you like to save?\n")
    save = pyip.inputMenu(['Yes', 'No'], numbered=True)
    if save == 'Yes':
        MODELS_WORKSHEET.append_row(new_model_info)
        print("\nworksheet updated sucessfully")
    else:
        print("worksheet no updated")


def test(choice, search_by):
    models = SHEET.worksheet("models")
    columns = []
    header = models.row_values(1)
    index = header.index(choice)
    index = index + 1
    column = models.col_values(index)
    rows_print = []
    for i in range(len(column)):
        if column[i] == search_by:
            x = i + 1
            rows_print.append(x)
        else:
            pass
    
    if len(rows_print) > 0:
        print("Number of Models found:", len(rows_print))
        for r in rows_print:
            row = models.row_values(r)
            print(row)
    else:
        print("\nNo model/s match this search")
        """
    for ind in range(1, 7):
       column = models.col_values(ind)
        columns.append(column[1:])
    """
    return columns


def search(choice):
    search_by = pyip.inputStr(f'\nEnter {choice}: ').capitalize()
    # Filter function used to search within the worksheet
    print("\nLoading model/s...\n")
    """
    values = MODELS_WORKSHEET.findall(search_by)
    if len(values) > 0:
        for r in values:
            print(", ".join(MODELS_WORKSHEET.row_values(r.row)))
    else:
        print("\nNo model/s match this search")
    """

    test(choice, search_by)

    """
    result = list(filter(
        lambda record: record[choice] == search_by or
        search_by in record[choice], retrieve_records()
        ))
    """
    # If there are any results found
    """
    if len(result) != 0:
        print("Contact found")
        print_records(result)
    """


def search_models():
    """
    Allows the user to search for specific models),
    either by first name, last name, height, hair colour or gender.
    Function will then print all matches if they are found.
    """
    print("\nHow would you like to search?\n\
\n1. By First name\n\
2. By Last name\n\
3. By Height\n\
4. By Hair Colour\n\
5. By Age\n\
6. By Gender\n")
    while True:
        user_input = user_response(
            "\nPlease enter a number from the above options: ", 1, 100
            )
        if user_input == 1:
            search('First Name')
        elif user_input == 2:
            search('Last Name')
        elif user_input == 3:
            search('Height')
        elif user_input == 4:
            search('Hair Colour')
        elif user_input == 5:
            search('Age')
        elif user_input == 6:
            search('Gender')
        else:
            pass
        return False


if __name__ == '__main__':
    menu()
