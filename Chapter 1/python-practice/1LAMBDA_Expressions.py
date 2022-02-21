my_list = [1, 2, 3]

from functools import reduce

# MAP FILTER REDUCE with LAMBDA

print(list(map(lambda item: item * 2, my_list)))
print(list(filter(lambda item: item % 2 != 0, my_list)))
print(reduce(lambda acc, item: acc + item, my_list))

LAMBDA = anonymous functions/used 1 time only

EXERCISE - square
my_list1 = [5, 4, 3]
print(list(map(lambda item: item ** 2, my_list1)))

EXERCISE - list sorting - by the second item in each tuple
a = [(0, 2), (4, 3), (9, 9), (10, -1)]
a.sort(key=lambda x: x[1])
print(a)