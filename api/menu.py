class Menu:
    """ Class representing a menu - can be used to retrieve parts of the menu """
    """ 
    Goal variables - title, entrees, sides, header, footer, body
    """

    def __init__(self, body):
        if type(body) == str:
            # body = filereader(body).split("\n")
            pass
        elif type(body) == list:
            self.body = body.split("\n")
        else:
            raise Exception("Invalid data supplied to menu. Must be filename or list of strings")
        
        self.parseMenu()

    def filereader(self, filename):
        """ filereader to accept text file test cases. Outputs list of strings where every item is a file line"""
        pass

    def parseMenu(self):
        """ Parse body text to get data used to create all relevant menu attributes """
        menuStart = 0
        for i,line in enumerate(self.body):
            if line == "MENU":
                print(i)
                menuStart = i
                break

        self.title = self.body[menuStart]   # Title of menu -- going to be "MENU"
        self.header = "\n".join(self.body[:menuStart])  # Everything before title regarded as a "header"
        print(self.header)

        # Get Menu Food items - Entrees and sides (incomplete/wrong)
        # self.menu = self.body[menuStart+1:].split("\n\n") # Incorrect method used... need to do over
        # self.entrees = self.menu[0]
        # self.sides = self.menu[1]
        # print(self.entrees)
        # print(self.sides)

    def __repr__(self):
        """ custom string representation of a Menu (combining all attributes to form something different than the original "body") """
        pass
        

if __name__ == "__main__":
    testText = "HI \nMy Name is Rowan\nI am FULLY\nINTO\nBACK END\n\nDevelopment"
    menu = Menu(testText)
    print(menu.body)

