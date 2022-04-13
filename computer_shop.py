#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# |
# |        File:  computer_shop.py
# |      Author:  Tan Duc Mai
# |          Id:  517925
# | Description:  Practical 1, exercise 1 -
# | This is my own work as defined by the Academic Integrity policy.
# |
# ----------------------------------------------------------------------------


# ------------------------------- Module Import -------------------------------
import abc


# ------------------------------ Class Definitions ----------------------------
class ComputerPart(metaclass=abc.ABCMeta):
    """
        An abstract class.
        The superclass for other ComputerPart types.
    """

    def __init__(self, name, price):
        """
            Initialises name and price by calling theirs mutator methods.
            Called by subclasses using super().__init__()
        """
        self.set_name(name)
        self.set_price(price)

    def get_name(self):
        """
            Returns the name attribute.
            Called by subclasses using super().get_name()
        """
        return self.__name

    def get_price(self):
        """
            Returns the price attribute.
            Called by subclasses using super().get_price()
        """
        return self.__price

    def set_name(self, name):
        """
            Sets the name attribute to the argument
            Only if the argument is a non-empty string.
        """
        if not isinstance(name, str):
            raise TypeError(
                f'Argument was {repr(name)}, type {type(name)}. '
                f'Must be a string.'
            )
        elif name == '':
            raise ValueError('ValueError: Name must not be empty.')
        self.__name = name

    def set_price(self, price):
        """
            Sets the price attribute to the argument
            Only if the argument is a positive float.
        """
        if not isinstance(price, float):
            raise TypeError(
                f'Argument was {repr(price)}, type {type(price)}. '
                f'Must be a float.'
            )
        elif price <= 0:
            raise ValueError('ValueError: Price must not be negative.')
        self.__price = price

    def csv_string_to_list(self, csv_string):
        """
            Splits the csv_string into separate values stored as a list.
            Called by subclasses using super().csv_string_to_list(csv_string)
        """
        result = []
        for letter in csv_string:
            item = ''
            if letter != ',':
                item += letter
            else:
                result.append(item)
        return result

    def equals(self, other):
        """
            Returns True if the calling object is equal to the other argument.
            Returns False otherwise.
            This method will be overridden in each subclass.
        """
        pass
        # if isinstance(self, other) and
        #     return True
        # return False

    @abc.abstractmethod
    def to_csv_string(self):
        """
            An abstract method.
            Returns the name of the class followed by each of the instance
            variables separated by commas.
        """
        pass

    @abc.abstractmethod
    def __str__(self):
        """
            An abstract method.
            Returns the variables as a String.
        """
        pass

    @abc.abstractmethod
    def parse(self):
        """
            An abstract method.
            Splits the csv_string into separate values and parses them to the
            correct datatypes.
            Uses these values to construct and return a new ComputerPart.
        """
        pass

    @abc.abstractmethod
    def input(self):
        """
            An abstract method.
            Takes input for each of the necessary variables.
            Uses these input values to construct and return a new ComputerPart.
        """
        pass


class CPU(ComputerPart):
    """
        A subclass of the ComputerPart class.
    """

    def __init__(self, cores, frequency_ghz):
        """
            Initialises cores and frequency_ghz by calling theirs
            mutator methods.
        """
        self.set_cores(cores)
        self.set_frequency_ghz(frequency_ghz)

    def get_cores(self):
        """
            Returns the cores attribute.
        """
        return self.__cores

    def get_frequency_ghz(self):
        """
            Returns the frequency_ghz attribute.
        """
        return self.__frequency_ghz

    def set_cores(self, cores):
        """
            Sets the cores attribute to the argument
            Only if the argument is a positive integer.
        """
        if not isinstance(cores, int):
            raise TypeError(
                f'Argument was {repr(cores)}, type {type(cores)}. '
                f'Must be an integer.'
            )
        elif cores <= 0:
            raise ValueError(
                'ValueError: Number of Cores must not be negative.'
            )
        self.__cores = cores

    def set_frequency_ghz(self, frequency_ghz):
        """
            Sets the frequency_ghz attribute to the argument
            Only if the argument is a positive float.
        """
        if not isinstance(frequency_ghz, float):
            raise TypeError(
                f'Argument was {repr(frequency_ghz)}, type '
                f'{type(frequency_ghz)}. Must be a float.'
            )
        elif frequency_ghz <= 0:
            raise ValueError('ValueError: Frequency must not be negative.')
        self.__frequency_ghz = frequency_ghz

    def equals(self, other):
        """
            Returns True if the calling object and the other argument are both
            CPUs and the values of their variables are the same.
            Returns False otherwise.
        """
        def compare_each_variable(self, other):
            if len(self) == len(other):
                for self_variable, self_other in self, other:
                    if not isinstance(self_variable, self_other):
                        return False
                return True
            return False

        if isinstance(self, other) and isinstance(other, CPU) and compare_each_variable(self, other):
            return True
        return False

    def to_csv_string(self):
        """
            Return the name of the class followed by each of the class
            variables separated by commas.
            Format: "CPU,name,price,cores,frequency_ghz".
        """
        return (
            f'"CPU,{self.get_name()},{self.get_price()},'
            f'{self.get_cores()},{self.get_frequency_ghz()}"'
        )

    def __str__(self):
        """
            Return the variables as a string.
            For example "Intel i7: 4 cores @ 3.2GHz for $990.00".
        """
        return (
            f'"{self.get_name()}: {self.get_cores()} cores, @ '
            f'{self.get_frequency_ghz()}GHz for ${self.get_price():.2f}"'
        )

    def parse(self, csv_string):
        """
            Calls the superclass's csv_string_to_list() method to get the
            values as a list.
            Parses these values to the correct datatypes.
            Uses these values to construct and return a new CPU.
        """
        csv_list = super().csv_string_to_list(csv_string)

        csv_list[2] = float(csv_list[2])
        csv_list[3] = int(csv_list[3])
        csv_list[4] = float(csv_list[4])

        return CPU(
            csv_list[0], csv_list[1], csv_list[2], csv_list[3], csv_list[4],
        )

    def input(self):
        """
            Takes input for the name, price, frequency, and number of cores.
            Uses these input values to construct and return a new CPU.
        """
        name = input('Enter the name: ')
        price = float(input('Enter the price: '))
        cores = int(input('Enter the number of cores: '))
        frequency_ghz = float(input('Enter the frequency in GHz: '))

        return CPU(name, price, cores, frequency_ghz)


class GraphicsCard(ComputerPart):
    """
        A subclass of the ComputerPart class.
    """

    def __init__(self, frequency_mhz, memory_gb):
        """
            Initialises frequency_mhz and memory_gb by calling theirs
            mutator methods.
        """
        self.set_frequency_mhz(frequency_mhz)
        self.set_memory_gb(memory_gb)

    def get_frequency_mhz(self):
        """
            Returns the frequency_mhz attribute.
        """
        return self.__frequency_mhz

    def get_memory_gb(self):
        """
            Returns the memory_gb attribute.
        """
        return self.__memory_gb

    def set_frequency_mhz(self, frequency_mhz):
        """
            Sets the frequency_mhz attribute to the argument
            Only if the argument is a positive integer.
        """
        if not isinstance(frequency_mhz, int):
            raise TypeError(
                f'Argument was {repr(frequency_mhz)}, type '
                f'{type(frequency_mhz)}. Must be an integer.'
            )
        elif frequency_mhz <= 0:
            raise ValueError('ValueError: Frequency must not be negative.')
        self.__frequency_mhz = frequency_mhz

    def set_memory_gb(self, memory_gb):
        """
            Sets the memory_gb attribute to the argument
            Only if the argument is a positive integer.
        """
        if not isinstance(memory_gb, int):
            raise TypeError(
                f'Argument was {repr(memory_gb)}, type {type(memory_gb)}. '
                f'Must be an integer.'
            )
        elif memory_gb <= 0:
            raise ValueError('ValueError: Memory must not be negative.')
        self.__memory_gb = memory_gb

    def equals(self, other):
        """
            Returns True if the calling object and the other argument are both
            GraphicsCards and the values of their variables are the same.
            Returns False otherwise.
        """
        def compare_each_variable(self, other):
            if len(self) == len(other):
                for self_variable, self_other in self, other:
                    if not isinstance(self_variable, self_other):
                        return False
                return True
            return False

        if isinstance(self, other) and isinstance(other, GraphicsCard) and compare_each_variable(self, other):
            return True
        return False

    def to_csv_string(self):
        """
            Return the name of the class followed by each of the class
            variables separated by commas.
            Format: "GraphicsCard,name,price,frequency_mhz,memory_gb".
        """
        return (
            f'"GraphicsCard,{self.get_name()},{self.get_price()},'
            f'{self.get_frequency_mhz()},{self.get_memory_gb()}"'
        )
 
    def __str__(self):
        """
            Return the variables as a string.
            For example "NVIDIA GeForce 1080: 8GB @ 1607MHz for $925.00".
        """
        return (
            f'"{self.get_name()}: {self.get_memory_gb()}GB @ '
            f'{self.get_frequency_mhz()}MHz for ${self.get_price():.2f}"'
        )

    def parse(self, csv_string):
        """
            Calls the superclass's csv_string_to_list() method to get the
            values as a list.
            Parses these values to the correct datatypes.
            Uses these values to construct and return a new GraphicsCard.
        """
        csv_list = super().csv_string_to_list(csv_string)

        csv_list[2] = float(csv_list[2])
        csv_list[3] = int(csv_list[3])
        csv_list[4] = int(csv_list[4])

        return GraphicsCard(
            csv_list[0], csv_list[1], csv_list[2], csv_list[3], csv_list[4],
        )

    def input(self):
        """
            Takes input for the name, price, memory, and frequency.
            Uses these input values to construct and return a new GraphicsCard.
        """
        name = input('Enter the name: ')
        price = float(input('Enter the price: '))
        frequency_mhz = int(input('Enter the frequency in MHz: '))
        memory_gb = int(input('Enter the memory in GB: '))

        return GraphicsCard(name, price, frequency_mhz, memory_gb)


class Memory(ComputerPart):
    """
        A subclass of the ComputerPart class.
    """

    def __init__(self, capacity_gb, frequency_mhz):
        """
            Initialises capacity_gb and frequency_mhz by calling theirs
            mutator methods.
        """
        self.set_capacity_gb(capacity_gb)
        self.set_frequency_mhz(frequency_mhz)
        self.set_ddr(ddr)

    def get_capacity_gb(self):
        """
            Returns the capacity_gb attribute.
        """
        return self.__capacity_gb

    def get_frequency_mhz(self):
        """
            Returns the frequency_mhz attribute.
        """
        return self.__frequency_mhz

    def get_ddr(self):
        """
            Returns the ddr attribute.
        """
        return self.__ddr

    def set_capacity_gb(self, capacity_gb):
        """
            Sets the capacity_gb attribute to the argument
            Only if the argument is a positive integer.
        """
        if not isinstance(capacity_gb, int):
            raise TypeError(
                f'Argument was {repr(capacity_gb)}, type '
                f'{type(capacity_gb)}. Must be an integer.'
            )
        elif capacity_gb <= 0:
            raise ValueError('ValueError: Capacity must not be negative.')
        self.__capacity_gb = capacity_gb

    def set_frequency_mhz(self, frequency_mhz):
        """
            Sets the frequency_mhz attribute to the argument
            Only if the argument is a positive integer.
        """
        if not isinstance(frequency_mhz, int):
            raise TypeError(
                f'Argument was {repr(frequency_mhz)}, '
                f'type {type(frequency_mhz)}. Must be an integer.'
            )
        elif frequency_mhz <= 0:
            raise ValueError('ValueError: Frequency must not be negative.')
        self.__frequency_mhz = frequency_mhz

    def set_ddr(self, ddr):
        """
            Sets the ddr attribute to the argument
            Only if the argument is a non-empty string.
        """
        if not isinstance(ddr, str):
            raise TypeError(
                f'Argument was {repr(ddr)}, type {type(ddr)}. '
                f'Must be a string.'
            )
        elif ddr == '':
            raise ValueError('ValueError: DDR must not be empty.')
        self.__ddr = ddr

    def equals(self, other):
        """
            Returns True if the calling object and the other argument are both
            Memory and the values of their variables are the same.
            Returns False otherwise.
        """
        def compare_each_variable(self, other):
            if len(self) == len(other):
                for self_variable, self_other in self, other:
                    if not isinstance(self_variable, self_other):
                        return False
                return True
            return False

        if isinstance(self, other) and isinstance(other, Memory) and compare_each_variable(self, other):
            return True
        return False

    def to_csv_string(self):
        """
            Return the name of the class followed by each of the class
            variables separated by commas.
            Format: "Memory,name,price,capacity_gb,frequency_mhz,ddr".
        """
        return (
            f'"Memory,{self.get_name()},{self.get_price()},'
            f'{self.get_capacity_gb()},{self.get_frequency_mhz()}, '
            f'{self.get_ddr()}"'
        )

    def __str__(self):
        """
            Return the variables as a string.
            For example "Corsair Vengeance: 16GB, DDR4 @ 3000MHz for $239.00".
        """
        return (
            f'"{self.get_name()}: {self.get_capacity_gb()}GB, '
            f'{self.get_ddr()} @ {self.get_frequency_mhz()}MHZ '
            f'for ${self.get_price():.2f}"'
        )

    def parse(self, csv_string):
        """
            Calls the superclass's csv_string_to_list() method to get the
            values as a list.
            Parses these values to the correct datatypes.
            Uses these values to construct and return a new Memory.
        """
        csv_list = super().csv_string_to_list(csv_string)

        csv_list[2] = float(csv_list[2])
        csv_list[3] = int(csv_list[3])
        csv_list[4] = int(csv_list[4])

        return Memory(
            csv_list[0], csv_list[1], csv_list[2],
            csv_list[3], csv_list[4], csv_list[5],
        )

    def input(self):
        """
            Takes input for the name, price, memory, and frequency.
            Uses these input values to construct and return a new Memory.
        """
        name = input('Enter the name: ')
        price = float(input('Enter the price: '))
        capacity_gb = int(input('Enter the capacity in GB: '))
        frequency_mhz = int(input('Enter the frequency in MHz: '))
        ddr = input('Enter the DDR: ')

        return Memory(name, price, capacity_gb, frequency_mhz, ddr)


class Storage(ComputerPart):
    """
        A subclass of the ComputerPart class.
    """

    def __init__(self, capacity_gb, frequency_mhz):
        """
            Initialises capacity_gb and frequency_mhz by calling theirs
            mutator methods.
        """
        self.set_capacity_gb(capacity_gb)
        self.set_storage_type(storage_type)

    def get_capacity_gb(self):
        """
            Returns the capacity_gb attribute.
        """
        return self.__capacity_gb

    def get_storage_type(self):
        """
            Returns the storage_type attribute.
        """
        return self.__storage_type

    def set_capacity_gb(self, capacity_gb):
        """
            Sets the capacity_gb attribute to the argument
            Only if the argument is a positive integer.
        """
        if not isinstance(capacity_gb, int):
            raise TypeError(
                f'Argument was {repr(capacity_gb)}, type '
                f'{type(capacity_gb)}. Must be an integer.'
            )
        elif capacity_gb <= 0:
            raise ValueError('ValueError: Capacity must not be negative.')
        self.__capacity_gb = capacity_gb

    def set_storage_type(self, storage_type):
        """
            Sets the storage_type attribute to the argument
            Only if the argument is a not one of HDD/SSD/SSHD.
        """
        if not isinstance(storage_type, str):
            raise TypeError(
                f'Argument was {repr(storage_type)}, '
                f'type {type(storage_type)}. Must be a string.'
            )
        elif storage_type not in ('HDD', 'SSD', 'SSHD'):
            raise ValueError(
                'ValueError: Storage type must be one of HDD, SSD, or SSHD.'
            )
        self.__storage_type = storage_type

    def equals(self, other):
        """
            Returns True if the calling object and the other argument are both
            Storage and the values of their variables are the same.
            Returns False otherwise.
        """
        def compare_each_variable(self, other):
            if len(self) == len(other):
                for self_variable, self_other in self, other:
                    if not isinstance(self_variable, self_other):
                        return False
                return True
            return False

        if isinstance(self, other) and isinstance(other, Storage) and compare_each_variable(self, other):
            return True
        return False

    def to_csv_string(self):
        """
            Return the name of the class followed by each of the class
            variables separated by commas.
            Format: "Storage,name,price,capacity_gb,storage_type".
        """
        return (
            f'"Storage,{self.get_name()},{self.get_price()},'
            f'{self.get_capacity_gb()}, {self.get_storage_type()}"'
        )

    def __str__(self):
        """
            Return the variables as a string.
            For example "Seagate Barracuda: 1000GB HDD for $60.00".
        """
        return (
            f'"{self.get_name()}: {self.get_capacity_gb()}GB, '
            f'{self.get_storage_type()} for ${self.get_price():.2f}"'
        )

    def parse(self, csv_string):
        """
            Calls the superclass's csv_string_to_list() method to get the values
            as a list.
            Parses these values to the correct datatypes.
            Uses these values to construct and return a new Storage.
        """
        csv_list = super().csv_string_to_list(csv_string)

        csv_list[2] = float(csv_list[2])
        csv_list[3] = int(csv_list[3])

        return Storage(
            csv_list[0], csv_list[1], csv_list[2], csv_list[3], csv_list[4],
        )

    def input(self):
        """
            Takes input for the name, price, memory, and frequency.
            Uses these input values to construct and return a new Storage.
        """
        name = input('Enter the name: ')
        price = float(input('Enter the price: '))
        capacity_gb = int(input('Enter the capacity in GB: '))
        storage_type = input('Enter the storage type (HDD/SSD/SSHD): ')

        return Storage(name, price, capacity_gb, frequency_mhz, storage_type)


# ------------------------------- Main Function -------------------------------
def main():
    # TODO Write your main program code here...
    print("~~ Welcome to the Computer Store ~~")
    print()
    shop = ComputerPartShop()  # Construct object
    shop.command_prompt()      # Call method to start the program


# --------------------------- Call the Main Function --------------------------
if __name__ == '__main__':
    main()
