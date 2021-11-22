import gspread
from google.oauth2.service_account import Credentials

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


def retrieve_records():
    """
    Function to retrieve all records found
    in the contacts list spreadhseet.
    """
    return MODELS_WORKSHEET.get_all_records()


def retrieve_all_models():
    """
    Function to retrieve full list of contacts
    """
    all_contacts = retrieve_records()
    print("\nNow retrieving all of your contacts...\n")
    for contact in all_contacts:
        print_records_in_loop(contact)


def print_records_in_loop(record):
    """
    Function to loop through all records passed
    as a parameter and print the details in a
    list of key: values.
    """
    print("Printing record...")
    for key, value in record.items():
        if key == 'phone_number':
            print(f"{key}: {value}")
        else:
            print(f"{key}: {value}")
    print("\n")


def file_creation():
    pass


def show_menu():
    print("\nMain menu")
    print("-----------------")
    print("1) See all Models")
    print("2) Add new Models")
    print("3) Search")
    print("4) Edit Models\n")


def menu():
    while True:
        show_menu()
        choice = input('Enter your choice: ').lower()
        if choice == '1':
            retrieve_all_models()
        elif choice == '2':
            file_creation()
        elif choice == '3':
            file_creation()
        elif choice == '4':
            return
        else:
            print(f'Not a correct choice: <{choice}>,try again')


if __name__ == '__main__':
    menu()




