
class Profile:

    # Constructor
    def __init__(self):
        self.profiles = dict()

    # Creates a new profile
    def new_profile(self, profile_name):
        self.profiles[profile_name] = {
            'First Name': None,
            'Last Name': None,
            'Email': None,
            'Address': None,
            'Address 2 (optional)': None,  # Optional
            'City': None,
            'Province': None,
            'Country': None,
            'Postal Code': None, 
            'Phone': None, 
            'CC Number': None,
            'CC Name': None,
            'CC Expiry Date (MM/YY)': None,  
            'CVV': None 
        }

    # Deletes a profile
    def delete_profile(self, profile_name):
        del self.profiles[profile_name]
    
    # Checks if a profile is in the dictionary
    def get_profile(self, profile_name):
        try:
            return self.profiles[profile_name]
        except KeyError:
            return None

    # Returns value of a key in given profile
    def get_val(self, profile_name, key):
        return self.profiles[profile_name][key]

    # Sets the value of a key in a dictionary
    def set_val(self, profile_name, target_key, newValue):
        profile = self.profiles[profile_name]
        for keys in profile:
            if keys == target_key:
                profile[target_key] = newValue
                break

    # Prints all profile names
    def print_profiles(self):
        for profiles in self.profiles:
            print(profiles)
            
    # Prints a profile's details
    def print_profile_info(self, profile_name):
        print('Profile Name: {}'.format(profile_name))
        for keys in self.profiles[profile_name]:
            print('{}: {}'.format(keys, self.profiles[profile_name][keys]))

    # Prints all profiles and their information
    def print_all(self):
        for profiles in self.profiles:
            print('Profile Name: {}'.format(profiles))
            for keys in self.profiles[profiles]:
                print('\t{}: {}'.format(keys, self.profiles[profiles][keys]))
    
    # Returns the size of the dictionary
    def size(self):
        return len(self.profiles)

    # Returns if the dictionary is empty or not
    def is_empty(self):
        if len(self.profiles) == 0:
            return True
        else:
            return False
