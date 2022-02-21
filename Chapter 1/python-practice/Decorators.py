# HIGHER ORDER FUNCTION HOC
# def greet(func):
#     func()
# def greet2():
#     def func():
#         return 5
#     return func

# DECORATOR PATERN
def my_decorator(func):
    def wrap_func(*args, **kwargs):
        print('*********')
        func(*args, **kwargs)
        print('*********')
    return wrap_func
# DECORATOR PATERN

@my_decorator
def hello(greeting, emoji=':('):
    print(greeting, emoji)

hello('hi')

# my_decorator(hello)('hi')
