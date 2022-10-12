class Profile:
    """
    Holds personal information to be used at checkout
    @param name: name of the profile
    @param profile: personal information for the profile
    """
    def __init__(self, name, profile):
        self.name = name
        self.first_name = profile['First Name']
        self.last_name = profile['Last Name']
        self.email = profile['Email']
        self.address = profile['Address']
        self.address2 = profile['Address 2 (optional)']
        self.city = profile['City']
        self.province = profile['Province']
        self.country = profile['Country']
        self.postal_code = profile['Postal Code']
        self.phone = profile['Phone Number']
        self.payment = profile['Payment']


    # Accessor methods
    def get_name(self) -> str:
        return self.name


    def get_first_name(self) -> str:
        return self.first_name
    

    def get_last_name(self) -> str:
        return self.last_name


    def get_email(self) -> str:
        return self.email


    def get_address(self) -> str:
        return self.address


    def get_address2(self) -> str:
        return self.address2


    def get_city(self) -> str:
        return self.city


    def get_province(self) -> str:
        return self.province


    def get_country(self) -> str:
        return self.country


    def get_postal(self) -> str:
        return self.postal_code


    def get_phone(self) -> str:
        return self.phone


    def get_cc(self) -> dict[str, str]:
        return self.payment