class Toy:
    def __init__(self, age, color):
        self.color = color
        self.age = age
        self.my_dict = {'name': 'Tom',
                        'has_pets': False
                        }

    def __getitem__(self, i):
        return self.my_dict[i]


action_figure = Toy('red', 0)
print(action_figure['name'])
