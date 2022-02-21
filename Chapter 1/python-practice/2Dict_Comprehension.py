simple_dict = {'a': 1,
               'b': 2
               }

my_dict = {k: v**2 for k, v in simple_dict.items() if v % 2 == 0}
print(my_dict)

my_dict1 = {num: num*2 for num in [1, 2, 3]}
print(my_dict1)

# EXERCISE - check duplicates

some_list = ['a', 'b', 'c', 'd', 'b', 'm', 'n', 'n']
duplicates = [i for i in some_list if some_list.count(i) > 1]
print(list(set(duplicates)))
