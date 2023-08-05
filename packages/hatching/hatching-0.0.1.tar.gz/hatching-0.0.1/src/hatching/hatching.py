import requests
from neuropark.auth import Auth
import time
class Hatching():
    def __init__(self):
        self.modelname = None
        self.auth=Auth()
        self.auth.check()

        
    def init(self, modelname):
        self.modelname = modelname
        if (self.auth.state==True):
            u, p = self.auth.get_cred()
            r = requests.get(f"http://neuropark.xyz/init_project.php?username={u}&password={p}&modelname={modelname}")
            print(r.text)
            if (r.text == str(2)):
                print("Model already exists : ", modelname)
                return 2
            elif(r.text == str(1)):
                print("Model Created : -  ", modelname)
                return 1
            elif(r.text != str(0)):
                print("Authorization failed !")
                return 0
        elif(self.auth.state==False) : 
            print("invaild user")
            self.auth.check()
            self.init(modelname)

    def push(self, metrics):
        u, p = self.auth.get_cred()
        url = f"http://neuropark.xyz/push.php?username={u}&password={p}&modelname={self.modelname}&metrics={metrics}"
        time.sleep(0.01)
        requests.post(url)




        


















