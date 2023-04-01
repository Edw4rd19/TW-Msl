from cryptography.fernet import Fernet
import config
import pandas
import sys

fileloc = 'files/Cryp_Data.csv'
driver = config.driver
terminal = config.terminal
environment = config.environment

msl_login = {
                'user_field': '//*[@id="username"]',
                'password_field': '//*[@id="root"]/div[1]/main/div/div[1]/div[2]/form/div[2]/div[2]/input',
                'login_button': '//*[@id="root"]/div[1]/main/div/div[1]/div[2]/form/button'
            }


def login(tool, user_role=''):
    if user_role == '':
        print('Obtaining login info for', tool, '[' + terminal, environment + ']')
    else:
        print('Obtaining login info for',  tool, 'with', user_role.lower(), "role", '[' + terminal, environment + ']')

    user, password, role_name, url = rcrypt(tool, user_role, terminal, environment)

    if user == '':
        print('No user found for', tool)
        sys.exit()
    elif password == '':
        print('No password found for', tool)
        sys.exit()
    elif url == '':
        print('No URL found for', tool)
        sys.exit()
    else:

        if user_role == '':
            print('Performing login to', tool, '[' + terminal, environment + ']')
        else:
            print('Performing login to', tool, 'with', user_role.lower(), "role", '[' + terminal, environment + ']')

    match tool.lower():
        case 'mainsail':

            try:
                driver.get(url)
            except:
                print('Connection error: Unable to reach the server, VPN ok?')
                driver.quit()
                sys.exit()
            try:
                driver.find_element("xpath", msl_login['user_field']).send_keys(user)
            except:
                print('Login field not /error')
                driver.quit()
            try:
                driver.find_element("xpath", msl_login['password_field']).send_keys(password)
            except:
                print('Password field not found/error')
                driver.quit()
            try:
                driver.find_element("xpath", msl_login['login_button']).click()
            except:
                print('Login button not found/error')
                driver.quit()

            print('Successful login to Mainsail with', user_role.lower() + '(' + role_name + ') role [' + terminal,
                  environment + ']')

        case _:
            print("No login script found for", tool)
            sys.exit()

    print()
    return url


def rcrypt(find_tool, find_user_role, terminal, environment):

    user = ''
    password = ''
    url = ''
    role = ''

    # prepare data to match csv format
    find_tool = find_tool.capitalize()
    find_user_role = find_user_role.capitalize()
    term = terminal.upper()
    env = environment.upper()
    decrypt()
    # Obtain info
    data = pandas.read_csv(fileloc)
    for i in data.index:
        if (data.Terminal[i] == term and data.Environment[i] == env and
                data.Tool[i] == find_tool and data.Role[i] == find_user_role):
            user = data.User[i]
            password = data.Password[i]
            url = data.Url[i]
            role = data.Rolename[i]
    crypt()

    return user, password, role, url


def crypt():
    with open('files/filekey.key', 'rb') as filekey:
        fernet = Fernet(filekey.read())
    # Crypt
    with open(fileloc, 'rb') as file:
        encrypted = fernet.encrypt(file.read())
    with open(fileloc, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decrypt():
    # Key
    with open('files/filekey.key', 'rb') as filekey:
        fernet = Fernet(filekey.read())
    # Decrypt
    with open(fileloc, 'rb') as enc_file:
        decrypted = fernet.decrypt(enc_file.read())
    with open(fileloc, 'wb') as dec_file:
        dec_file.write(decrypted)
