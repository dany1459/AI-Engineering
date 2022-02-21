class PlayerCharacter:  # CAMEL CASE
    membership = True  # CLASS OBJECT ATTRIBUTE

    def __init__(self, name='anonymous', age=0):
        if age >= 18:
            self.name = name  # ATTRIBUTES
            self.age = age

    def shout(self):
        print(f'My name is {self.name}')
        return f'I\'m {self.age}'

    @classmethod  # WE DON'T NEED TO INSTANTIATE -> print(PlayerCharacter.adding_things(12, 13))
    def adding_things(cls, num1, num2):
        return cls('Teddy', num1 + num2)


player1 = PlayerCharacter('Jim', 33)
player2 = PlayerCharacter('Tom', 18)
player3 = PlayerCharacter.adding_things(12, 13)  # INSTANCES - INSTANTIATING

print(player1.name)
print(player2.name)
print(player1.shout())
print(player3.age)
