from functools import wraps

def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        return f(*args, **kwargs)
    return wrapper

@my_decorator
def say_hello():
    """Greet the user."""
    print("Hello!")

say_hello()
