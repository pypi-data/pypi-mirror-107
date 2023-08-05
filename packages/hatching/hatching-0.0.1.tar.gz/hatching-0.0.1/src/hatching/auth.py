import requests

class Auth():
    def __init__(self):
        self.__username=None
        self.__password=None
        self.state = False
    
    def enter_cred(self):
        self.__username=input("Enter Neuropark username: ")
        self.__password=input("Enter Neuropark password: ")
    
    def get_cred(self):
        return self.__username, self.__password

    def check(self):
        self.enter_cred()
        r = requests.get(f"http://neuropark.xyz/auth.php?username={self.__username}&password={self.__password}")
        print("Check",r.text)
        if r.text== self.__username + str(1):
            self.state = True













