class Calculator:
    """
    DESCRIPTION

        Calculator can performe these  actions:
        - Addition,
        - Subtraction
        - Multiplication
        - Division
        - Take (n) root of number
        - Reset memory
        - Print out memory       
    """

    def __init__(self) -> None:
        self._memory = 0.0
    
    #Adds number to memory
    def add(self, digit: float) -> float:
        try:
            self._memory += digit
        except TypeError:
            print("Please enter valid input")
        return self._memory
    
    #Substracts number from memory
    def subtract(self, digit: float) -> float:
        try:
            self._memory -= digit
        except TypeError:
             print("Please enter valid input")
        return self._memory

    #Multiplies memory by number
    def multiply(self, digit: float) -> float:
        try:
            self._memory *= digit
        except ZeroDivisionError:
            return 1.0
        except TypeError:
            print("Please enter valid input")
        return self._memory

    #Devides memory by number
    def divide(self, digit: float) -> float:
        try:
            self._memory /= digit
        except ZeroDivisionError:
            return 0.0
        except:
             print("Please enter valid input")
        return self._memory

    #Takes root out of memory
    def root(self, digit: float) -> float:
        try:
            self._memory **= (1/float(digit))
        except TypeError:
            print("Please enter valid input")
        return self._memory

    #Resets memory to zero
    def memory_reset(self) -> None :
        self._memory = 0 
        

    @property
    def return_memory(self) -> float:
        self._memory
        return self._memory
    
    @return_memory.setter
    def return_memory(self) -> None:
        print("Memory can not be changed")
    
        
#Calculator object
my_cl = Calculator()



print(f"Addition: {my_cl.add(0)}")
print(f"Subtraction: {my_cl.subtract(0)}")
print(f"Multiplication: {my_cl.multiply(0)}")
print(f"Division: {my_cl.divide(0)}")
print(f"Root of number: {my_cl.root(2)}")
print(f"Reset memory: {my_cl.memory_reset}")




