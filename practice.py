# class Dog:
    # species = "Canine"

    # def __init__(self, name, age):
        # self.name = name
        # self.age = age

# dog1 = Dog("Buddy", 3)

# print(dog1.name)
# print(dog1.species)


# class Dog:

    # def __init__(self,name, age):
        # self.name = name
        # self.age = age

    # def bark(self):
        # print(self.name)

# dog1 = Dog("buddy", 3)
# dog1.bark()


# class Dog:
    # def __init__(self, name, age):
        # self.name = name
        # self.age = age


# dog1 = Dog("Buddy", 3)
# print(dog1.name)


#  Class and Instance Variables

# class Dog:
    # class variable
    # species = "Canine"

    # def __init__(self, name, age):
        # instance variable
        # self.name = name
        # self.age = age

# creating dog object
# dog1 = Dog("Buuddy", 3)
# dog2 = Dog("Charlie", 5)

# accessing class and instance variables
# print(dog1.species)   #class variable
# print(dog1.name)  #instance variable
# print(dog2.name)  #instance variable

# modify instance variables
# dog1.name = "Max"
# print(dog1.name) #updated instance variable

# modify class 
# Dog.species = "Feline"
# print(dog1.species)
# print(dog2.species)



# INHERITANCE 

# Single Inheritance
# class Dog:
    # def __init__(self, name):
        # self.name = name

    # def display_name(self):
        # print(f"Dog's Name: {self.name}")

# class Labrador(Dog):   # Single Inheritance
    # def sound(self):
        # print("labrador Woofs!")

# class GuideDog(Labrador):# Multilevel Inheritance
    # def guide(self):
        # print(f"{self.name} Guides the way!")

# Multilevel Inheritance
# class Friendly:
    # def greet(self):
        # print("Friendly!")

# class GoldenRetriever(Dog, Friendly): # Multiple Inheritance
    # def sound(self):
        # print("Golden Retriever Barks")

# lab = Labrador("Buddy")
# lab.display_name()
# lab.sound()

# guide_dog = GuideDog("Max")
# guide_dog.display_name()
# guide_dog.guide()

# retriever = GoldenRetriever("Charlie")
# retriever.display_name()
# retriever.greet()
# retriever.sound()

# Python Polymorphism

# class Dog:
    # def sound(self):
        # print("dog sound")

# Run-Time Polymorphism: Method Overriding
# class Labrador(Dog):
    # def sound(self):
        # print("Labrador woofs!")

# class Beagle(Dog):
    # def sound(self):
        # print("Beagle Woofs!")


# Compile-Time Polymorphism: Method Overloading Mimic
# class Calculator:
    # def add(self, a, b=0, c=0):
        # return a + b + c  # Supports multiple ways to call add()
    

# Run-Time Polymorphism
# dogs = [Dog(), Labrador(), Beagle()]
# for dog  in dogs:
    # dog.sound() # Calls the appropriate method based on the object type

# Compile-Time Polymorphism (Mimicked using default arguments)
# calc = Calculator()
# print(calc.add(5, 10))  # Two arguments
# print(calc.add(5, 10, 15))  # Three arguments


#  >>>>>> Python Encapsulation  <<<<<<

# class Dog:
    # def __init__(self, name, breed, age):
        # self.name = name  # Public attribute
        # self._breed = breed # Protected attribute
        # self.__age = age  # Private attribute

    # Public method
    # def get_info(self):
        # return f"Name: {self.name}, Breed: {self._breed}, Age: {self.__age}"
    
    # Getter and Setter for private attribute
    # def get_age(self):
        # return self.__age
    
    # def set_age(self, age):
        # if age > 0:
            # self.__age = age
        # else:
            # print("Invalid age!")

# dog = Dog("Buddy", "Labrador", 3)

# Accessing public member
# print(dog.name)  # Accessible

# Accessing protected member
# print(dog._breed)  # Accessible but discouraged outside the class

# Accessing private member using getter
# print(dog.get_age())

# Modifying private member using setter
# dog.set_age(5)
# print(dog.get_info())


#  >>>> Data Abstraction <<<<

# from abc import ABC, abstractmethod

# class Dog(ABC):
    # def __init__(self, name):
        # self.name = name

    # @abstractmethod
    # def sound(self): # Abstract Method
        # pass

    # def display_name(self):  # Concrete Method
        # print(f"Dog's Name: {self.name}")


# class Labrador(Dog):  # Partial Abstraction
    # def sound(self):
        # print("Labrador Woof!")

# class Beagle(Dog):  # Partial Abstraction
    # def sound(self):
        # print("Beagle Bark!")

# dogs = [Labrador("Buddy"), Beagle("Charlie")]
# for dog in dogs:
    # dog.display_name() # Calls concrete method
    # dog.sound() # Calls implemented abstract method



# >>>EXAMPLE 1

# class Dog:
    # def __init__(self, name, breed, age):
        # self.name = name
        # self.breed = breed
        # self.age = age

    # def say_name(self):
        # print(f"WOOF! {self.name}! Woof!")

    # def birthday(self):
        # self.age += 1
        # print(f"{self.name} you are now {self.age}! Goodboy ! ")

    # def get_age(self):
        # return self.age
    
# my_dog = Dog("Gaspode", "Terrier", 10)

# print("My dog's age is", my_dog.get_age())
# my_dog.say_name()
# my_dog.birthday()
# print("My dog's age is now", my_dog.get_age())

# >>>>>EXAMPLE 2
# class PasswordManager:
    # def __init__(self,min_password_len=8):
        # self._password = None
        # self._min_password_len = min_password_len

    # def set_password(self, password):
        # if self._validate(password):
            # self._password = password
            # print("password set successfully")
        # else:
            # print(f"Password must be atleast {self._min_password_len} characters long.")

    # def _validate(self, password):
        # return len(password) >= self._min_password_len
    
# gmail_password = PasswordManager()
# gmail_password.set_password("ThisisAlONgPasswordWithSomeNumbers1234")

# uwo_password = PasswordManager(10)
# uwo_password.set_password("TooShort")

# Static and Class Methods

class Utils:
    @staticmethod
    def add(a, b):
        return a + b

    @classmethod
    def description(cls):
        return f"This is the {cls.__name__} class."

print(Utils.add(5, 10))
print(Utils.description())

        

     