
# specify text file to load user credential from:
BP_USER_PATH = R'C:\Users\justi\Documents\beaptport_creds.txt'
with open(BP_USER_PATH, 'r', encoding='utf-8') as file:
    user_info = file.readlines()
    username, password = user_info[0], user_info[1]

# or just overwrite these variables with your username and password. 
USERNAME = username
PASSWORD = password

