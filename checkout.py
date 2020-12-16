
from profileDict import Profile

def getUserInfo(profile_dict):

    if(len(profile_dict) == 0):
        print('\nCreate your profile below: ')
        createProfile(profile_dict)
    else:
        print('\nWhich profile would you like to use: ') #####
        print('list all profiles here.')


def createProfile(profile_dict):
    profile_name = input('\nProfile Name: ')
    profile_dict.newProfile(profile_name)

    current_profile = profile_dict.getProfile(profile_name);

    current_profile.setVal('Email', input('Email: '))
    current_profile.setVal('First Name', input('First Name: '))
    current_profile.setVal('Last Name', input('Last Name: '))
    current_profile.setVal('Address', input('Address 1: '))
    current_profile.setVal('Address 2', input('Address 2 (optional): '))

    country = input('Country: ')
    current_profile.setVal('Country', country)

    if country[0] == 'U':
        current_profile.setVal('State', input('State: '))
    elif country[0] == 'C':
        current_profile.setVal('Province', input('Province: '))

    current_profile.setVal('City', input('City: '))
    current_profile.setVal('Postal Code', input('Postal Code: '))
    current_profile.setVal('Phone', input('Phone Number: ').strip(' -'))

    current_profile.setVal('CC Number', input('Credit Card Number: ').strip(' '))
    current_profile.setVal('CC Name', input('Name on CC: '))
    current_profile.setVal('Expiry Month', input('Expiry Month (2 Digits): '))
    current_profile.setVal('Expiry Year', input('Expiry Year (4 Digits): '))
    current_profile.setVal('CVV', input('CVV: '))