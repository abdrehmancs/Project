import random

class House:
    def __init__(self):
        self.name = input("Enter your name in hogwarts: ")
        self.house = random.choice(["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"])
        
        print(f"Welcome {self.name}! You have been sorted into {self.house}.")
        
    @property
    def house(self):
        return self._house
    
    @house.setter
    def house(self, value):
        if value not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house. Please choose from Gryffindor, Hufflepuff, Ravenclaw, or Slytherin.")
        self._house = value    
        
        
        
def main():
    student = House()
    print("Running the program...")


main()