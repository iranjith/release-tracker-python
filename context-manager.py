# class Timer:
#     def __enter__(self):
#         print("Timer started.")
#         return self

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print("Timer stopped.")


# with Timer():
#     print("Doing some work...")

from contextlib import contextmanager


@contextmanager
def timer():
    print("Timer started.")
    yield
    print("Timer stopped.")


with timer():
    print("Doing some work...")
