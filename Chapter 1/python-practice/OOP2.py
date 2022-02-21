class User:
    def __init__(self, email):
        self.email = email

    def sign_in(self):
        print('Logged in')


class Wizard(User):
    def __init__(self, name, power, email):
        super().__init__(email)
        self.name = name
        self.power = power

    def attack(self):
        print(f'Attacking with power of {self.power}')


class Archer(User):
    def __init__(self, name, arrows, email):
        super().__init__(email)
        self.name = name
        self.arrows = arrows

    def attack(self):
        print(f'Attacking with arrows: arrows left - {self.arrows}')

    def run(self):
        print('Ran really fast')


wizard1 = Wizard('Merlin', 50, 'merlin@gmail.com')
archer1 = Archer('Robin', 100, 'robin@gmail.com')
print(wizard1.email)
wizard1.sign_in()
wizard1.attack()
archer1.attack()
