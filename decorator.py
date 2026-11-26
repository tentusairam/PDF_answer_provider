def decorator(func):
    def wrapper():
        func()
        print("thefunction has ended")
    return wrapper
def hello():
    print("these are the line of function being executed")
hello_var=decorator(hello)
hello_var()