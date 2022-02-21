# my_list = []
# for char in 'hello':
#     my_list.append(char)
# print(my_list)

my_list = [char for char in 'hello']
print(my_list)

my_set = {char for char in 'hello'} # SETS HAVE UNIQUE VALUES
print(my_set)

my_list2 = [num for num in range(1, 101)]
print(my_list2)

my_list3 = [num**2 for num in range(1, 101)]
print(my_list3)

# my_list4 = [num for num in my_list3 if num % 2 == 0]
my_list4 = [num**2 for num in range(1, 101) if num % 2 == 0]
print(my_list4)

print(my_list4[0])