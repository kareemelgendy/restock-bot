
class Profile:

    # Constructor
    def __init__(self):
        self.profiles = dict()

    # Creates a new profile
    def newProfile(self, profile_name):
        self.profiles[profile_name] = {
            'First Name': None,
            'Last Name': None,
            'Email': None,
            'Address': None,
            'Address 2': None,  # Optional
            'City': None,
            'Province': None,
            'State': None,
            'Country': None,
            'Postal Code': None, # No spaces
            'Phone': None, # No dashes or spaces
            'CC Number': None,
            'CC Name': None,
            'Expiry Month': None,  # 2 digits
            'Expiry Year': None,  # 4 digits
            'CVV': None  # 3 digits
        }

    # Deletes a profile
    def deleteProfile(self, profile_name):
        del self.profiles[profile_name]

    # Returns value of a key in given profile
    def getVal(self, profile_name, key):
        return self.profiles[profile_name][key]

    # Sets the value of a key in a dictionary
    def setVal(self, profile_name, target_key, newValue):
        profile = self.profiles[profile_name]
        for keys in profile:
            if keys == target_key:
                profile[target_key] = newValue
                break

    # Prints a profile's deetails
    def printProfileInfo(self, profile_name):
        print('Profile Name: ' + str(profile_name))
        for keys in self.profiles[profile_name]:
            print(str(keys) + ': ' + str(self.profiles[profile_name][keys]))

        # Prints all products
    def printProfiles(self):
        for profiles in self.profiles:
            print(products)

    def printAll(self):
        for profiles in self.profiles:
            print('Profile Name: ' + str(profiles))
            for keys in self.profiles[profiles]:
                print('\t' + str(keys) + ': ' + str(self.profiles[profiles][keys]))
    
    # Returns the size of the dictionary
    def size(self):
        return len(self.profiles)