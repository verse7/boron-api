import re
import json
from api.emailService import EmailService

class Menu:
    """ Class representing a menu - can be used to retrieve parts of the menu """
    def __init__(self, sender=None):
        self.header = ""    # Anything before the menu title
        self.title = "MENU"  # Title in email menu
        self.entrees = ""    # Entree list under title
        self.sides = ""      # Sides following entree lsist
        self.footer = ""     # Anything after sides
        self.menu = ""       # Raw menu string
        self.menulist = []   # raw menu body split into lines (mutated during parsing)

        if sender:
            eservice = EmailService()
            self.menu = eservice.bodyText(eservice.getlatest(sender))
            self.menulist = self.menu.split("\n")
            self.parseMenu()

    def provideText(self, text):
        if type(text) == str:
            self.menu = self.filereader(text)
        elif type(text) == str:
            self.menu = text
        else:
            raise Exception("Invalid data supplied to menu. Must be filename or string")
        self.menulist = self.menu.split("\n")
        self.parseMenu()
        

    def filereader(self, filename):
        """ filereader to accept text file test cases. Outputs string in file """
        text = ""
        try:
            with open(filename) as fp:
                line = fp.readline()
                while line:
                    text += line
                    line = fp.readline()
            return text
        except:
            print("unable to open file.")
            raise IOError()
            

    def parseMenu(self):
        """ Parse body text to get data used to create all relevant menu attributes """

        def getHeader():
            """ get header of menu - returns header and title """
            menuStart = 0
            for i,line in enumerate(self.menulist):
                if line == self.title:
                    # print(i)
                    menuStart = i
                    break

            self.header = "\n".join(self.menulist[:menuStart])
            self.title = self.menulist[menuStart]
            self.menulist = self.menulist[menuStart+1:]

        def getEntrees():
            """ return entrees """
            menuParts = "\n".join(self.menulist).split("\n\n")
            self.entrees = menuParts[0]            
            self.menulist = "\n".join(menuParts[1:]).split("\n")

        def getSides():
            """ returns sides and footer """
            # clean sides data
            sidesNfooter = []
            for part in self.menulist:
                if part != "":
                    sidesNfooter += [part]

            self.menulist = sidesNfooter
            # print(self.menulist)

            # extract sides from data
            for line in self.menulist:
                matches = re.search("/+", line)
                if matches:
                    self.sides += line + "\n"
                else:
                    self.footer += line + "\n"
                
        getHeader()  
        getEntrees()
        getSides()

    def __repr__(self):
        """ custom string representation of a Menu (combining all attributes to form something different than the original "body") """
        string = ""
        string += "HEADER\n" + self.header + "\n\n"
        string += "TITLE\n" + self.title + "\n\n"
        string += "ENTREES\n" + self.entrees + "\n\n"
        string += "SIDES\n" + self.sides + "\n\n"
        string += "FOOTER\n" + self.footer + "\n\n"
        return string

    def toJSON(self, mode="simple"):
        if mode=='simple':
            return json.dumps({'entrees': self.entrees, 'sides': self.sides}, sort_keys=True, indent=4)
        else:
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)        
        
""" 
if __name__ == "__main__":
    menu = Menu("rowaneatkinson@gmail.com")
    print(menu.toJSON())
    
 """