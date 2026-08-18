def shout(text: str) -> str:
    """Decorator that converts the return value of a function to uppercase."""
    return text.upper() + "!!!"


yell = shout
print(shout("hello world"))  # Output: "HELLO WORLD!!!"
print(yell("hello world"))  # Output: "HELLO WORLD!!!"
