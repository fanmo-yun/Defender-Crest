class A:
    def __init__(self) -> None:
        print(self.__class__.__name__)

a = A()