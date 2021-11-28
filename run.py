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
    another_task()


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
    Function to display menu items to user.
    This function is called from the menu function.
    """
    print("\nWelcome to the Model Search application!\n")
    print("Main menu")
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
        choice = input('Please enter a choice from the above numbers: ')
        if choice == '1':
            retrieve_all_models()
        elif choice == '2':
            add_new_model()
        elif choice == '3':
            search_models()
        elif choice == '4':
            edit_search()
        else:
            print(f'Not a valid choice: <{choice}>,try again')


def another_task():
    """
    Function to take users back to the
    main menu if they have something else
    they would like to do.
    This is called at the end of the
    other processes.
    """
    print("\nWould you like to complete another task?\n")
    print("1. Yes, back to main menu\n\
2. No, end programme")
    while True:
        user_input = user_response(
            "\nPlease enter a number from the above options: ", 1, 2
            )
        if user_input == 1:
            print("\nNow taking you back to the main menu...\n")
            menu()
            break
        else:
            print(
                "Programme shutting down...\n")
            raise SystemExit


def add_new_model():
    """
    Function to allow users to enter a new model's
    information. If the user tries to enter
    invalid characters, they will be alerted.
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
    gender = pyip.inputMenu(['M', 'F', 'Other'], numbered=True)
    new_model_info = [
        first_name, last_name, height,
        hair_colour, age, gender
        ]
    print(f'The data you have entered is: <{new_model_info}>')
    print("\nWould you like to save?\n")
    save = pyip.inputMenu(['Yes', 'No'], numbered=True)
    if save == 'Yes':
        MODELS_WORKSHEET.append_row(new_model_info)
        print("\nWorksheet updated sucessfully")
    else:
        print("Worksheet not updated")
    another_task()


def search_display(choice, search_by):
    """
    Function to display search results.
    Called in the search function and used
    in the edit_search function.
    """
    models = SHEET.worksheet("models")
    header = models.row_values(1)
    index = header.index(choice)
    index = index + 1
    column = models.col_values(index)
    rows_ids = []
    rows_data = []
    for i in range(len(column)):
        if column[i] == search_by:
            x = i + 1
            rows_ids.append(x)
        else:
            pass
    if len(rows_ids) > 0:
        print("Number of Models found: ", len(rows_ids))
        for r in rows_ids:
            row = models.row_values(r)
            rows_data.append(row)
            print(r, row)
    else:
        print("\nNo Models match this search")
        another_task()
    return rows_ids


def search(choice):
    """
    Function to display gender choices to
    the user if they would like to search by gender,
    and display an input field for the user to choose how
    they would like to search.
    """
    if choice == 'Gender':
        search_by = pyip.inputMenu(['M', 'F', 'Other'], numbered=True)
    else:
        search_by = pyip.inputStr(f'\nEnter {choice}: ').capitalize()
        print("\nLoading Models...\n")
    rows_ids = search_display(choice, search_by)
    return rows_ids


def search_models():
    """
    Allows the user to search for specific models),
    either by first name, last name, height, hair colour or gender.
    The search function is then called to display the results
    to the user.
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
            "\nPlease enter a number from the above options: ", 1, 6
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
        another_task()
        return False


def edit_search():
    """
    Function to allow user to search models
    by First Name or Last Name.
    """
    models = SHEET.worksheet("models")
    print("\nHow would you like to search?\n\
\n1. By First name\n\
2. By Last name\n")
    while True:
        user_input = user_response(
            "\nPlease enter a number from the above options: ", 1, 2
            )
        if user_input == 1:
            rows_ids = search('First Name')
            break
        elif user_input == 2:
            rows_ids = search('Last Name')
            break
        else:
            pass
    while True:
        model_row = int(pyip.inputInt('\nPlease enter the number that is \
next to the model you would like to select: '))
        if model_row in rows_ids:
            break
        else:
            pass
    print("\
\n1. First name\n\
2. Last name\n\
3. Height\n\
4. Hair Colour\n\
5. Age\n\
6. By Gender\n")
    user_input = user_response(
            "\nWhich value would you like to change: ", 1, 6
            )
    if user_input == 1:
        while True:
            updated_value = pyip.inputStr('*New First Name: ')
            if updated_value.isalpha():
                break
            else:
                print("Enter letters only")
    if user_input == 2:
        while True:
            updated_value = pyip.inputStr('*New Last Name: ')
            if updated_value.isalpha():
                break
        else:
            print("Enter letters only")
    if user_input == 3:
        updated_value = int(pyip.inputInt('*New Height: '))
    if user_input == 4:
        while True:
            updated_value = pyip.inputStr('*New Hair Colour: ')
            if updated_value.isalpha():
                break
            else:
                print("Enter letters only")
    if user_input == 5:
        updated_value = int(pyip.inputInt('*New Age: '))
    if user_input == 6:
        updated_value = pyip.inputMenu(['M', 'F'], numbered=True)

    updated_model_info = models.row_values(model_row)
    index = user_input - 1
    updated_model_info[index] = updated_value

    print(f'The updated model will be: <{updated_model_info}>')
    print("\nWould you like to save?\n")
    save = pyip.inputMenu(['Yes', 'No'], numbered=True)
    if save == 'Yes':
        update_model(model_row, user_input, updated_value)
        print("\nWorksheet updated sucessfully")
    else:
        print("Worksheet not updated")
    print(updated_value)
    another_task()


def update_model(model_row, model_column, updated_value):
    """
    Function to update the google spreadsheet
    when the user updates a model's information
    """
    MODELS_WORKSHEET.update_cell(model_row, model_column, updated_value)


if __name__ == '__main__':
    menu()
