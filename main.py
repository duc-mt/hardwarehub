#!/usr/bin/python3
# -*- coding: utf-8 -*-

# =============================================================================
#
#        FILE:  main.py
#      AUTHOR:  Tan Duc Mai
#       EMAIL:  henryfromvietnam@gmail.com
#     CREATED:  2022-04-13
# DESCRIPTION:  Creates a Computer shop which allows customers
#               to select and purchase computer parts.
#   I hereby declare that I completed this work without any improper help
#   from a third party and without using any aids other than those cited.
#
# =============================================================================


# ------------------------------- Module Import -------------------------------
# Stdlib
import abc
import collections
import csv
import getpass

# Third party
import icontract
from rich import print
from rich.console import Console

# Local application/library specific imports
from exceptions import InvalidEmail
from authenticator import (Authenticator,
                           InvalidPassword,
                           UsernameAlreadyExists)


# ------------------------------- Named Constant ------------------------------
console = Console()


# ------------------------------- Computer Part -------------------------------
class ComputerPart(metaclass=abc.ABCMeta):
    """An abstract class. The superclass for other ComputerPart types."""

    def __init__(self, name, price, stock=1):
        """Initialise name and price.

        Called by subclasses using super().__init__()
        """
        self.__name = name
        self.__price = price
        self.__stock = stock

    @abc.abstractclassmethod
    def parse(cls):  # noqa: N805
        """An abstract class method.

        Split the csv_string into separate values and parses them to the
        correct datatypes.
        Use these values to construct and return a new ComputerPart.
        """
        pass

    @abc.abstractclassmethod
    def input(cls):  # noqa: N805
        """An abstract class method.

        Take input for each of the necessary variables.
        Use these input values to construct and return a new ComputerPart.
        """
        pass

    @abc.abstractmethod
    def __str__(self):
        """An abstract method.

        Return the variables as a String.
        """
        pass

    @abc.abstractmethod
    def to_csv_string(self):
        """An abstract method.

        Return the name of the class followed by each of the instance
        variables separated by commas.
        """
        pass

    @classmethod
    @icontract.ensure(lambda result: isinstance(result, str) & (result != ''))
    def input_name(cls):
        """A class method.

        Set the name attribute to the argument
        Only if the argument is a non-empty string.
        """
        name = None
        valid = False
        while name is None or not valid:
            name = input('Enter the name: ')
            if not isinstance(name, str):
                raise TypeError(
                    f'Argument was {repr(name)}, type {type(name)}. '
                    f'Must be a string.'
                )
            elif name == '':
                raise ValueError('Name must not be empty.')
            else:
                valid = True
        return name

    @classmethod
    @icontract.ensure(lambda result: isinstance(result, float) & (result > 0))
    def input_price(cls):
        """A class method.

        Set the price attribute to the argument
        Only if the argument is a positive float.
        """
        price = None
        valid = False
        while price is None or not valid:
            price = float(input('Enter the price: '))
            if not isinstance(price, float):
                raise TypeError(
                    f'Argument was {repr(price)}, type {type(price)}. '
                    f'Must be a float.'
                )
            elif price <= 0:
                raise ValueError('Price must not be negative.')
            else:
                valid = True
        return price

    @classmethod
    @icontract.require(lambda csv_string: isinstance(csv_string, str))
    @icontract.ensure(lambda result: isinstance(result, list))
    def csv_string_to_list(cls, csv_string):
        csv_list = []
        value = ''
        for index, letter in enumerate(csv_string):
            if letter != ',':
                value += letter
                if index == (len(csv_string) - 1):
                    if value == 'OUT OF STOCK':
                        csv_list.append('0')
                    else:
                        csv_list.append(value[1:])
                        value = ''
            else:
                csv_list.append(value)
                value = ''
        return csv_list

    @property
    def name(self):
        """Return the name attribute.

        Called by subclasses using self.name
        """
        return self.__name

    @property
    def price(self):
        """Return the price attribute.

        Called by subclasses using self.price
        """
        return self.__price

    @property
    def stock(self):
        """Return the stock attribute.

        Called by subclasses using self.stock
        """
        return self.__stock

    @icontract.ensure(lambda result: isinstance(result, bool))
    def equals(self, other):
        """Return a boolean value.

        1. True if the calling object and the other argument are both
           Memory and the values of their variables are the same.
        2. False otherwise.
        """
        if isinstance(other, type(self)):
            if (self.name == other.name and
                    self.price == other.price):
                return True
        return False


class CPU(ComputerPart):
    """A subclass of the ComputerPart class."""

    def __init__(self, name, price, cores, frequency_ghz, stock=1):
        """Initialise cores and frequency_ghz."""
        super().__init__(name, price, stock)
        self.__cores = cores
        self.__frequency_ghz = frequency_ghz

    @icontract.ensure(lambda result: isinstance(result, str))
    def __str__(self):
        """Return the variables as a string.

        For example "Intel i7: 4 cores @ 3.2GHz for $990.00".
        """
        return (
            f'{self.name}: {self.cores} cores @ '
            f'{self.frequency_ghz}GHz for ${self.price:.2f}'
        )

    @classmethod
    @icontract.require(lambda csv_list: isinstance(csv_list, list))
    @icontract.ensure(lambda result: isinstance(result, CPU))
    def parse(cls, csv_list):
        """Return a CPU object. Perform the following procedure.

        Check the last element of the argument csv_list.
        Parse all elements to the correct datatypes.
        Use these values to construct and return a new CPU.
        """
        if csv_list[-1] == 'OUT OF STOCK':
            csv_list[-1] = '0'
        else:
            csv_list[-1] = str(csv_list[-1])[1:]

        csv_list[2] = float(csv_list[2])
        csv_list[3] = int(csv_list[3])
        csv_list[4] = float(csv_list[4])
        csv_list[5] = int(csv_list[5])

        return CPU(
            csv_list[1],
            csv_list[2],
            csv_list[3],
            csv_list[4],
            csv_list[5],
        )

    @classmethod
    @icontract.ensure(lambda result: isinstance(result, CPU))
    def input(cls):
        """
        Take input for the name, price, frequency, and number of cores.
        Use these input values to construct and return a new CPU.
        """
        return cls(
            ComputerPart.input_name(),
            ComputerPart.input_price(),
            cls.input_cores(),
            cls.input_frequency_ghz(),
        )

    @classmethod
    @icontract.ensure(lambda result: isinstance(result, int) & (result > 0))
    def input_cores(cls):
        """
        Set the cores attribute to the argument
        Only if the argument is a positive integer.
        """
        cores = None
        valid = False
        while cores is None or not valid:
            cores = int(input('Enter the number of cores: '))
            if not isinstance(cores, int):
                raise TypeError(
                    f'Argument was {repr(cores)}, type {type(cores)}. '
                    f'Must be an integer.'
                )
            elif cores <= 0:
                raise ValueError('Number of Cores must not be negative.')
            else:
                valid = True
        return cores

    @classmethod
    @icontract.ensure(lambda result: isinstance(result, float) & (result > 0))
    def input_frequency_ghz(cls):
        """
        Set the frequency_ghz attribute to the argument
        Only if the argument is a positive float.
        """
        frequency_ghz = None
        valid = False
        while frequency_ghz is None or not valid:
            frequency_ghz = float(input('Enter the frequency in GHz: '))
            if not isinstance(frequency_ghz, float):
                raise TypeError(
                    f'Argument was {repr(frequency_ghz)}, type '
                    f'{type(frequency_ghz)}. Must be a float.'
                )
            elif frequency_ghz <= 0:
                raise ValueError('Frequency must not be negative.')
            else:
                valid = True
        return frequency_ghz

    @property
    def cores(self):
        """Return the cores attribute."""
        return self.__cores

    @property
    def frequency_ghz(self):
        """Return the frequency_ghz attribute."""
        return self.__frequency_ghz

    @icontract.ensure(lambda result: isinstance(result, bool))
    def equals(self, other):
        """Return a boolean value.

        1. True if the calling object and the other argument are both
           Memory and the values of their variables are the same.
        2. False otherwise.
        """
        if super().equals(other):
            if (self.cores == other.cores and
                    self.frequency_ghz == other.frequency_ghz):
                return True
        return False

    @icontract.ensure(lambda result: isinstance(result, str))
    def to_csv_string(self):
        """Return the name of the class followed by each of its variables.

        Format: "CPU,name,price,cores,frequency_ghz".
        """
        return (
            f'CPU,{self.name},{self.price},'
            f'{self.cores},{self.frequency_ghz}'
        )


class GraphicsCard(ComputerPart):
    """A subclass of the ComputerPart class."""

    def __init__(self, name, price, frequency_mhz, memory_gb, stock=1):
        """
        Initialise frequency_mhz and memory_gb by calling theirs
        mutator methods.
        """
        super().__init__(name, price, stock)
        self.__frequency_mhz = frequency_mhz
        self.__memory_gb = memory_gb

    @icontract.ensure(lambda result: isinstance(result, str))
    def __str__(self):
        """
        Return the variables as a string.
        For example "NVIDIA GeForce 1080: 8GB @ 1607MHz for $925.00".
        """
        return (
            f'{self.name}: {self.memory_gb}GB @ '
            f'{self.frequency_mhz}MHz for ${self.price:.2f}'
        )

    @classmethod
    @icontract.require(lambda csv_list: isinstance(csv_list, list))
    @icontract.ensure(lambda result: isinstance(result, GraphicsCard))
    def parse(cls, csv_list):
        """Return a CPU object. Perform the following procedure.

        Check the last element of the argument csv_list.
        Parse all elements to the correct datatypes.
        Use these values to construct and return a new GraphicsCard.
        """
        if csv_list[-1] == 'OUT OF STOCK':
            csv_list[-1] = '0'
        else:
            csv_list[-1] = str(csv_list[-1])[1:]

        csv_list[2] = float(csv_list[2])
        csv_list[3] = int(csv_list[3])
        csv_list[4] = int(csv_list[4])
        csv_list[5] = int(csv_list[5])

        return GraphicsCard(
            csv_list[1],
            csv_list[2],
            csv_list[3],
            csv_list[4],
            csv_list[5],
        )

    @classmethod
    @icontract.ensure(lambda result: isinstance(result, GraphicsCard))
    def input(cls):
        """
        Take input for the name, price, memory, and frequency.
        Use these input values to construct and return a new GraphicsCard.
        """
        return cls(
            ComputerPart.input_name(),
            ComputerPart.input_price(),
            cls.input_frequency_mhz(),
            cls.input_memory_gb(),
        )

    @classmethod
    @icontract.ensure(lambda result: isinstance(result, int) & (result > 0))
    def input_frequency_mhz(cls):
        """
        Set the frequency_mhz attribute to the argument.
        Only if the argument is a positive integer.
        """
        frequency_mhz = None
        valid = False
        while frequency_mhz is None or not valid:
            frequency_mhz = int(input('Enter the frequency in MHz: '))
            if not isinstance(frequency_mhz, int):
                raise TypeError(
                    f'Argument was {repr(frequency_mhz)}, type '
                    f'{type(frequency_mhz)}. Must be an integer.'
                )
            elif frequency_mhz <= 0:
                raise ValueError('Frequency must not be negative.')
            else:
                valid = True
        return frequency_mhz

    @classmethod
    @icontract.ensure(lambda result: isinstance(result, int) & (result > 0))
    def input_memory_gb(cls):
        """
        Set the memory_gb attribute to the argument.
        Only if the argument is a positive integer.
        """
        memory_gb = None
        valid = False
        while memory_gb is None or not valid:
            memory_gb = int(input('Enter the memory in GB: '))
            if not isinstance(memory_gb, int):
                raise TypeError(
                    f'Argument was {repr(memory_gb)}, type {type(memory_gb)}. '
                    f'Must be an integer.'
                )
            elif memory_gb <= 0:
                raise ValueError('Memory must not be negative.')
            else:
                valid = True
        return memory_gb

    @property
    def frequency_mhz(self):
        """Return the frequency_mhz attribute."""
        return self.__frequency_mhz

    @property
    def memory_gb(self):
        """Return the memory_gb attribute."""
        return self.__memory_gb

    @icontract.ensure(lambda result: isinstance(result, bool))
    def equals(self, other):
        """Return a boolean value.

        1. True if the calling object and the other argument are both
           Memory and the values of their variables are the same.
        2. False otherwise.
        """
        if super().equals(other):
            if (self.memory_gb == other.memory_gb and
                    self.frequency_mhz == other.frequency_mhz):
                return True
        return False

    @icontract.ensure(lambda result: isinstance(result, str))
    def to_csv_string(self):
        """Return the name of the class followed by each of its variables.

        Format: "GraphicsCard,name,price,frequency_mhz,memory_gb".
        """
        return (
            f'GraphicsCard,{self.name},{self.price},'
            f'{self.frequency_mhz},{self.memory_gb}'
        )


class Memory(ComputerPart):
    """A subclass of the ComputerPart class."""

    def __init__(self, name, price, capacity_gb, frequency_mhz, ddr, stock=1):
        """
        Initialise capacity_gb and frequency_mhz by calling theirs
        mutator methods.
        """
        super().__init__(name, price, stock)
        self.__capacity_gb = capacity_gb
        self.__frequency_mhz = frequency_mhz
        self.__ddr = ddr

    @icontract.ensure(lambda result: isinstance(result, str))
    def __str__(self):
        """
        Return the variables as a string.
        For example "Corsair Vengeance: 16GB, DDR4 @ 3000MHz for $239.00".
        """
        return (
            f'{self.name}: {self.capacity_gb}GB, '
            f'DDR{self.ddr} @ {self.frequency_mhz}MHZ '
            f'for ${self.price:.2f}'
        )

    @classmethod
    @icontract.require(lambda csv_list: isinstance(csv_list, list))
    @icontract.ensure(lambda result: isinstance(result, Memory))
    def parse(cls, csv_list):
        """Return a CPU object. Perform the following procedure.

        Check the last element of the argument csv_list.
        Parse all elements to the correct datatypes.
        Use these values to construct and return a new Memory.
        """
        if csv_list[-1] == 'OUT OF STOCK':
            csv_list[-1] = '0'
        else:
            csv_list[-1] = str(csv_list[-1])[1:]

        csv_list[2] = float(csv_list[2])
        csv_list[3] = int(csv_list[3])
        csv_list[4] = int(csv_list[4])
        csv_list[6] = int(csv_list[6])

        return Memory(
            csv_list[1],
            csv_list[2],
            csv_list[3],
            csv_list[4],
            csv_list[5],
            csv_list[6],
        )

    @classmethod
    @icontract.ensure(lambda result: isinstance(result, Memory))
    def input(cls):
        """
        Take input for the name, price, memory, and frequency.
        Use these input values to construct and return a new Memory.
        """
        return cls(
            ComputerPart.input_name(),
            ComputerPart.input_price(),
            cls.input_capacity_gb(),
            cls.input_frequency_mhz(),
            cls.input_ddr(),
        )

    @classmethod
    @icontract.ensure(lambda result: isinstance(result, int) & (result > 0))
    def input_capacity_gb(cls):
        """
        Set the capacity_gb attribute to the argument.
        Only if the argument is a positive integer.
        """
        capacity_gb = None
        valid = False
        while capacity_gb is None or not valid:
            capacity_gb = int(input('Enter the capacity in GB: '))
            if not isinstance(capacity_gb, int):
                raise TypeError(
                    f'Argument was {repr(capacity_gb)}, type '
                    f'{type(capacity_gb)}. Must be an integer.'
                )
            elif capacity_gb <= 0:
                raise ValueError('Capacity must not be negative.')
            else:
                valid = True
        return capacity_gb

    @classmethod
    @icontract.ensure(lambda result: isinstance(result, int) & (result > 0))
    def input_frequency_mhz(cls):
        """
        Set the frequency_mhz attribute to the argument.
        Only if the argument is a positive integer.
        """
        frequency_mhz = None
        valid = False
        while frequency_mhz is None or not valid:
            frequency_mhz = int(input('Enter the frequency in MHz: '))
            if not isinstance(frequency_mhz, int):
                raise TypeError(
                    f'Argument was {repr(frequency_mhz)}, '
                    f'type {type(frequency_mhz)}. Must be an integer.'
                )
            elif frequency_mhz <= 0:
                raise ValueError('Frequency must not be negative.')
            else:
                valid = True
        return frequency_mhz

    @classmethod
    @icontract.ensure(lambda result: isinstance(result, str) & (result != ''))
    def input_ddr(cls):
        """
        Set the ddr attribute to the argument
        Only if the argument is a non-empty string.
        """
        ddr = None
        valid = False
        while ddr is None or not valid:
            ddr = input('Enter the DDR: ')
            if not isinstance(ddr, str):
                raise TypeError(
                    f'Argument was {repr(ddr)}, type {type(ddr)}. '
                    f'Must be a string.'
                )
            elif ddr == '':
                raise ValueError('DDR must not be empty.')
            else:
                valid = True
        return ddr

    @property
    def capacity_gb(self):
        """Return the capacity_gb attribute."""
        return self.__capacity_gb

    @property
    def frequency_mhz(self):
        """Return the frequency_mhz attribute."""
        return self.__frequency_mhz

    @property
    def ddr(self):
        """Return the ddr attribute."""
        return self.__ddr

    @icontract.ensure(lambda result: isinstance(result, bool))
    def equals(self, other):
        """Return a boolean value.

        1. True if the calling object and the other argument are both
           Memory and the values of their variables are the same.
        2. False otherwise.
        """
        if super().equals(other):
            if (self.frequency_mhz == other.frequency_mhz and
                self.capacity_gb == other.capacity_gb and
                    self.ddr == other.ddr):
                return True
        return False

    @icontract.ensure(lambda result: isinstance(result, str))
    def to_csv_string(self):
        """Return the name of the class followed by each of its variables.

        Format: "Memory,name,price,capacity_gb,frequency_mhz,ddr".
        """
        return (
            f'Memory,{self.name},{self.price},'
            f'{self.capacity_gb},{self.frequency_mhz},'
            f'{self.ddr}'
        )


class Storage(ComputerPart):
    """A subclass of the ComputerPart class."""

    def __init__(self, name, price, capacity_gb, storage_type, stock=1):
        """Initialise capacity_gb and frequency_mhz."""
        super().__init__(name, price, stock)
        self.__capacity_gb = capacity_gb
        self.__storage_type = storage_type

    @icontract.ensure(lambda result: isinstance(result, str))
    def __str__(self):
        """Return the variables as a string.

        For example "Seagate Barracuda: 1000GB HDD for $60.00".
        """
        return (
            f'{self.name}: {self.capacity_gb}GB '
            f'{self.storage_type} for ${self.price:.2f}'
        )

    @classmethod
    @icontract.require(lambda csv_list: isinstance(csv_list, list))
    @icontract.ensure(lambda result: isinstance(result, Storage))
    def parse(cls, csv_list):
        """Return a CPU object. Perform the following procedure.

        Check the last element of the argument csv_list.
        Parse all elements to the correct datatypes.
        Use these values to construct and return a new Storage.
        """
        if csv_list[-1] == 'OUT OF STOCK':
            csv_list[-1] = '0'
        else:
            csv_list[-1] = str(csv_list[-1])[1:]

        csv_list[2] = float(csv_list[2])
        csv_list[3] = int(csv_list[3])
        csv_list[5] = int(csv_list[5])

        return Storage(
            csv_list[1],
            csv_list[2],
            csv_list[3],
            csv_list[4],
            csv_list[5],
        )

    @classmethod
    @icontract.ensure(lambda result: isinstance(result, Storage))
    def input(cls):
        """
        Take input for the name, price, memory, and frequency.
        Use these input values to construct and return a new Storage.
        """
        return cls(
            ComputerPart.input_name(),
            ComputerPart.input_price(),
            cls.input_capacity_gb(),
            cls.input_storage_type(),
        )

    @classmethod
    @icontract.ensure(lambda result: isinstance(result, int) & (result > 0))
    def input_capacity_gb(cls):
        """
        Set the capacity_gb attribute to the argument.
        Only if the argument is a positive integer.
        """
        capacity_gb = None
        valid = False
        while capacity_gb is None or not valid:
            capacity_gb = int(input('Enter the capacity in GB: '))
            if not isinstance(capacity_gb, int):
                raise TypeError(
                    f'Argument was {repr(capacity_gb)}, '
                    f'type {type(capacity_gb)}. Must be an integer.'
                )
            elif capacity_gb <= 0:
                raise ValueError('Capacity must not be negative.')
            else:
                valid = True
        return capacity_gb

    @classmethod
    @icontract.ensure(lambda result: result in {'HDD', 'SSD', 'SSHD'})
    def input_storage_type(cls):
        """
        Set the storage_type attribute to the argument.
        Only if the argument is a not one of HDD/SSD/SSHD.
        """
        storage_type = None
        valid = False
        while storage_type is None or not valid:
            storage_type = input('Enter the storage type (HDD/SSD/SSHD): ')
            if not isinstance(storage_type, str):
                raise TypeError(
                    f'Argument was {repr(storage_type)}, '
                    f'type {type(storage_type)}. Must be a string.'
                )
            elif storage_type not in {'HDD', 'SSD', 'SSHD'}:
                raise ValueError('Storage type must be one of '
                                 'HDD, SSD, or SSHD.')
            else:
                valid = True
        return storage_type

    @property
    def capacity_gb(self):
        """Return the capacity_gb attribute."""
        return self.__capacity_gb

    @property
    def storage_type(self):
        """Return the storage_type attribute."""
        return self.__storage_type

    @icontract.ensure(lambda result: isinstance(result, bool))
    def equals(self, other):
        """Return a boolean value.

        1. True if the calling object and the other argument are both
           Memory and the values of their variables are the same.
        2. False otherwise.
        """
        if super().equals(other):
            if (self.capacity_gb == other.capacity_gb and
                    self.storage_type == other.storage_type):
                return True
        return False

    @icontract.ensure(lambda result: isinstance(result, str))
    def to_csv_string(self):
        """Return the name of the class followed by each of its variables.

        Format: "Storage,name,price,capacity_gb,storage_type".
        """
        return (
            f'Storage,{self.name},{self.price},'
            f'{self.capacity_gb},{self.storage_type}'
        )


# ------------------------------- Data Structure ------------------------------
class Partlist():
    """
    A subclass of the Wishlist class.
    Stores the computer parts (instances of the ComputerPart class)
    available in stock.
    """

    def __init__(self):
        """Initialise Partlist object."""
        # A variable to store the items (ComputerParts) listed in the store.
        self.__items = []
        """
        A dictionary
        1. Key is the computer part.
        2. Value is the number of stock that key has in stock.
        """
        self.__stock = {}

    @icontract.ensure(lambda result: isinstance(result, str))
    def __str__(self):
        """Return a string that represents the Partlist in the format:

        "---- Partlist ----
        NVIDIA Quadro RTX: 48GB @ 1005.0MHz for $6300.00 (x1)
        AMD Ryzen 3: 4.0 cores @ 3.7GHz for $97.99 (OUT OF STOCK)
        Corsair Vengeance LED: 16GB, DDR4 @ 3000MHz for $239.00 (x4)
        Seagate FireCuda: 1000GB SSHD for $105.00 (x45)
        --------------------"
        """
        result = '---- Partlist ----\n'
        for item in self.items:
            result += item.__str__()
            # Check how many stock left.
            stock = self.stock[item.name]
            if stock:
                # Print that number if it is greater than 0.
                result += ' (x' + str(stock) + ')'
            else:
                # Otherwise, write out of stock.
                result += ' (OUT OF STOCK)'
            result += '\n'
        result += '--------------------'
        return result

    @icontract.ensure(lambda self, result: result == len(self.items))
    def __len__(self):
        """
        Get the length of the items attribute.
        Called within Partlist class using len(self)
        Called outside Partlist class using len(object)
            - Where object is an instance of the Partlist class.
        """
        return len(self.items)

    @property
    def items(self):
        """Return the items attribute."""
        return self.__items

    @items.deleter
    def items(self):
        """Clean up the items list."""
        self.__items.clear()

    @property
    def stock(self):
        """Return the stock attribute."""
        return self.__stock

    @stock.deleter
    def stock(self):
        """Clean up the stock dictionary."""
        self.__stock.clear()

    @icontract.require(
        lambda new_part, print_status:
            isinstance(new_part, ComputerPart)
            & isinstance(print_status, bool))
    @icontract.ensure(lambda result: result is None)
    def add_to_partlist(self, new_part, print_status=False):
        """
        Add a new item to the store.
        If it is duplicate, the available stock must be incremented by 1.
        """
        name_of_new_part = new_part.name
        try:
            self.__stock[name_of_new_part]
        except KeyError:
            self.__items.append(new_part)
            self.__stock[name_of_new_part] = new_part.stock
        else:
            # Duplicate item, so increment available stock by 1.
            self.__stock[name_of_new_part] += 1

        stock = self.__stock[name_of_new_part]

        if print_status:
            console.print(f'Added {new_part.__str__()} (x{stock})',
                          style='green')
        print()

    @icontract.require(
        lambda part_name: isinstance(part_name, str) & (part_name != ''))
    def get_part_using_name(self, part_name):
        """Return a ComputerPart object or an error string.

        Find and access a part using its name.
        Check to see if that part name is in store.
        """
        found = False
        i = 0
        while i < len(self) - 1:
            if self.__items[i].name == part_name:
                result = self.__items[i]
                found = True
            i += 1
        if found:
            return result
        return f'Could not find {part_name}!'

    @icontract.require(lambda part_position: isinstance(part_position, int))
    def get_part_using_position(self, part_position):
        """Return a ComputerPart object or an error string.

        Find and access a part using its position.
        Check to see if the argument is less than the length of the list.
        """
        if part_position < len(self):
            return self.__items[part_position]
        return f'{part_position} out of range 1 - {len(self)}'

    @icontract.require(
        lambda part_name: isinstance(part_name, str) & (part_name != ''))
    def remove_part_using_name(self, part_name):
        """Return nothing.

        Find and remove a part using its name.
        Check to see if that part name is in store.
        Clear all stock of that part in store.
        """
        done = False
        for index, item in enumerate(self.items):
            if item.name == part_name:
                # Delete that item and its entry in the stock dictionary.
                del self.items[index]
                stock = self.stock.pop(part_name)
                done = True
        if not done:
            console.print(f'Could not find {part_name}!', style='red')
        else:
            console.print(f'Removed {part_name} (x{stock})', style='green')

    @icontract.require(lambda part_position: isinstance(part_position, int))
    def remove_part_using_position(self, part_position):
        """Return nothing.

        Find and access a part using its position.
        Check to see if the argument is less than the length of the list.
        Clear all stock of that part in store.
        """
        if part_position < len(self):
            removed_part = self.items.pop(part_position)
            stock = self.stock.pop(removed_part.name)
            console.print(f'Removed {removed_part.__str__()} (x{stock})',
                          style='green')
        else:
            print(f'{part_position} out of range 1 - {len(self)}')

    @icontract.require(
        lambda filename: isinstance(filename, str) & (filename != ''))
    @icontract.ensure(lambda result: result is None)
    def save_to_csv(self, filename='database'):
        """
        Save all parts to a csv file with an argument file name.
        Default to the file name database.csv
        """
        with open(file=f'database/{filename}.csv', mode='w',
                  encoding='UTF8', newline='') as outfile:
            for item in self.items:
                outfile.write(item.to_csv_string())
                # Check how many stock left.
                stock = self.stock[item.name]
                # Write that number to file if it is greater than 0.
                # Otherwise, write out of stock.
                if stock:
                    outfile.write(',x' + str(stock))
                else:
                    outfile.write(',OUT OF STOCK')
                outfile.write('\n')


class Wishlist(Partlist):
    """A subclass of the Partlist class."""

    __authenticator = Authenticator()

    def __init__(self):
        """Initialise Wishlist object."""
        super().__init__()
        self.__create_user()

    @icontract.ensure(lambda result: isinstance(result, str))
    def __str__(self):
        """
        Return a string that represents the Wishlist in the format:
        "---- Gary's Wishlist ----
        NVIDIA Quadro RTX: 48GB @ 1005.0MHz for $6300.00 (x1)
        AMD Ryzen 5: 4.0 cores @ 3.2GHz for $119.99 (x1)
        Corsair Vengeance LED: 16GB, DDR4 @ 3000MHz for $239.00 (x2)
        Seagate FireCuda: 1000GB SSHD for $105.00 (x1)
        Toshiba P300: 3000GB HDD for $115.00 (x1)
        --------------------
        $7117.99
        Valid computer"

        The last line is either "Valid computer" or "Not a valid computer".
        """
        result = f"\n---- {self.__username}'s Wishlist ----\n"

        if len(self):
            result += super().__str__()[20:-20]

        result += '--------------------\n'
        result += f'${self.__get_total_cost():.2f}\n'

        if self.__is_valid_computer():
            result += 'Valid computer'
        else:
            result += 'Not a valid computer'

        return result

    @classmethod
    def get_authenticator(cls):
        return cls.__authenticator

    @property
    def username(self):
        """Return the username attribute."""
        return self.__username

    @icontract.ensure(
        lambda self, result:
            isinstance(self.__username, str)
            & (result is None) & (self.__username != '')
    )
    def set_username(self):
        """Set the username attribute by keeping prompting the user."""
        username = None
        valid = False
        while username is None or not valid:
            try:
                username = input('Enter your username: ')
                if username == '':
                    raise ValueError(
                        'Cannot create a Wishlist with an empty name.')
                elif ' ' in username:
                    raise NameError(
                        'Username cannot contain any space character.')
            except Exception as e:
                print(e)
            else:
                valid = True
        self.__username = username

    @icontract.require(
        lambda username, email, password:
            isinstance(username, str) & isinstance(email, str)
            & isinstance(password, str))
    @icontract.ensure(lambda result: result is None)
    def __update_users(self, username, email, password):
        with open(file='database/users.csv', mode='a',
                  encoding='UTF8', newline='') as outfile:
            csv.writer(outfile).writerow(
                [self.username, email, password]
            )

    @icontract.ensure(lambda result: result is None)
    def __create_user(self):
        """Keep trying to add/validate new username/password."""
        valid = False
        while not valid:
            self.set_username()
            email = input('Enter your email: ')

            password = None
            verified = False
            while password is None or not verified:
                password = getpass.getpass(
                    prompt='Enter your password: '
                )
                password_verify = getpass.getpass(
                    prompt='Verify your password: '
                )
                try:
                    if password != password_verify:
                        raise InvalidPassword(password_verify)
                except InvalidPassword as e1:
                    print(e1)
                else:
                    verified = True

            try:
                Wishlist.__authenticator.add_user(self.__username,
                                                  email,
                                                  password)
            except UsernameAlreadyExists as e2:
                is_returned = input('Are you a returned customer? [Y/n] ')
                if is_returned in ('y'.lower(), ''):
                    try:
                        if email != self.get_authenticator().user_email[
                            self.__username
                        ]:
                            raise InvalidEmail(email)
                        self.get_authenticator().login(self.__username,
                                                       password)
                    except (InvalidPassword, InvalidEmail) as e3:
                        print(e3)
                    else:
                        valid = True
                        print()
                else:
                    print(e2)
            except Exception as e:
                print(e)
            else:
                valid = True
                print()
                self.__update_users(
                    self.__username,
                    Wishlist.__authenticator.users[self.username].email,
                    Wishlist.__authenticator.users[
                        self.username
                    ].password.password,
                )

    @icontract.ensure(lambda result: isinstance(result, float) or result >= 0)
    def __get_total_cost(self):
        """
        A private method used within this class only.
        Calculates and returns the total cost of all parts.
        """
        price = 0
        for item in self.items:
            number = self.stock[item.name]
            price += item.price * number
        return price

    @icontract.ensure(lambda result: isinstance(result, bool))
    def __is_valid_computer(self):
        """
        A private method used within this class only.
        Determines if the parts will make up a valid computer.
        A valid computer requires at least:
            - 1 CPU, 1 GraphicsCard, 1 Memory, and 1 Storage.
        """
        # A dictionary to check if one of these parts is in the Wishlist.
        is_in_wishlist = {
            'CPU': False,
            'GraphicsCard': False,
            'Memory': False,
            'Storage': False,
        }
        for item in self.items:
            if isinstance(item, CPU):
                is_in_wishlist['CPU'] = True
            elif isinstance(item, GraphicsCard):
                is_in_wishlist['GraphicsCard'] = True
            elif isinstance(item, Memory):
                is_in_wishlist['Memory'] = True
            elif isinstance(item, Storage):
                is_in_wishlist['Storage'] = True

        return (is_in_wishlist['CPU'] is True and
                is_in_wishlist['GraphicsCard'] is True and
                is_in_wishlist['Memory'] is True and
                is_in_wishlist['Storage'] is True)


# ------------------------------- User Interface ------------------------------
@icontract.invariant(
    lambda self:
        (isinstance(self.partlist, Partlist))
        & (
            (self.wishlist is None)
            | (isinstance(self.wishlist, Wishlist))
        )
)
class CommandPrompt:
    """The user interface of the system."""

    __menu = None

    def __init__(self):
        """Initialise CommandPrompt object."""
        self.__wishlist = None
        self.__read_from_csv()
        if CommandPrompt.__menu is None:
            CommandPrompt.__set_menu()

    @classmethod
    @icontract.require(
        lambda menu_type:
            (menu_type == 'Main Menu')
            | (menu_type == 'Wishlist')
            | (menu_type == 'Part Types')
    )
    @icontract.ensure(lambda result: result is None)
    def display_menu(cls, menu_type):
        """Display one of the three menus.

        Depending on the type of menu: Main Menu/Wishlist/Part Types,
        outputs the appropriate menu.
        """
        # Print Menu
        print(f'---- {menu_type} ----')
        for i, question in enumerate(cls.__menu[menu_type]):
            print(f'{i+1}. {question}')

    @classmethod
    def __set_menu(cls):
        """Set the menu class attribute."""
        @icontract.require(lambda obj: isinstance(obj, Question))
        @icontract.ensure(lambda result: isinstance(result, str))
        def convert_class_name(obj):
            """Convert a class name to a human-readable name.

            E.g. 'New Wishlist' is transformed into 'NewWishlist'.
            """
            obj_name = type(obj).__name__
            result = ''
            result += obj_name[0]
            for index, letter in enumerate(obj_name):
                if letter.islower():
                    result += letter
                else:
                    if index != 0:
                        result += ' ' + letter
            return result

        # A defaultdict type variable to store three types of menus.
        cls.__menu = collections.defaultdict(list)

        # Add four options for Main Menu.
        cls.__menu['Main Menu'].append(
            convert_class_name(NewWishlist(CommandPrompt(), False)),
        )
        cls.__menu['Main Menu'].append(
            convert_class_name(ListDatabase(CommandPrompt(), False)),
        )
        cls.__menu['Main Menu'].append(
            convert_class_name(AddPartToDatabase(CommandPrompt(), False)),
        )
        cls.__menu['Main Menu'].append(
            convert_class_name(Close(CommandPrompt(), execute=False)),
        )

        # Add five options for Wishlist Menu.
        cls.__menu['Wishlist'].append(
            convert_class_name(AddFromDatabase(CommandPrompt(), False)),
        )
        cls.__menu['Wishlist'].append(
            convert_class_name(RemoveFromWishlist(CommandPrompt(), False)),
        )
        cls.__menu['Wishlist'].append(
            convert_class_name(ShowWishlist(CommandPrompt(), False)),
        )
        cls.__menu['Wishlist'].append(
            convert_class_name(PurchaseAndClose(CommandPrompt(), False)),
        )
        cls.__menu['Wishlist'].append(
            convert_class_name(Close(CommandPrompt(), execute=False)),
        )

        # Add five options for Parts Types Menu.
        cls.__menu['Part Types'].append('CPU')
        cls.__menu['Part Types'].append('Graphics Card')
        cls.__menu['Part Types'].append('Memory')
        cls.__menu['Part Types'].append('Storage')
        cls.__menu['Part Types'].append('Back')

    @property
    def partlist(self):
        """Return the Partlist object."""
        return self.__partlist

    @property
    def wishlist(self):
        """Return the Wishlist object."""
        return self.__wishlist

    @wishlist.setter
    @icontract.require(lambda obj: (isinstance(obj, Wishlist)) | (obj is None))
    @icontract.ensure(lambda result: result is None)
    def wishlist(self, obj):
        """Set the wishlist attribute to the argument.

        1. A Wishlist object
        2. None (in which case is meant to reset the Wishlist after
           the user chose to Close (or Purchase and Close) the Wishlist)
        """
        self.__wishlist = obj

    @icontract.require(lambda limit: (limit == 5) | (limit == 6))
    def prompt_for_option(self, limit):
        """Return an int value representing user's choice.

        Prompt the user for a number as an option for the displayed menu.
        Option must be an integer number in range 1 - limit.
        """
        option = input(f'Enter an option (1-{limit-1}): ')
        # Handle the error if option is not a number.
        try:
            option = int(option)
        except ValueError as e:
            print(f'{type(e).__name__}: {repr(option)} is not a number.\n')
            option = None
        # Display ValueError if option is a number, but outside range.
        if option is not None and option not in range(1, limit):
            print(f'ValueError: {option} is outside range '
                  f'1 - {limit}.\n')
        return option

    @icontract.ensure(lambda result: result is None)
    def __read_from_csv(self):
        """Automatically invoked when a CommandPrompt object is constructed.

        By invoking this method, the CommandPrompt class should automatically
        construct a part list and fill it with items that it reads from the
        CSV file named "database.csv".
        """
        self.__partlist = Partlist()
        with open(file='database/database.csv', mode='r',
                  encoding='UTF8', newline='') as infile:
            csv_lists = list(csv.reader(infile, delimiter=',', quotechar='|'))

            for csv_list in csv_lists:
                if csv_list[0] == ('CPU'):
                    # Construct a CPU object.
                    self.partlist.add_to_partlist(
                        CPU.parse(csv_list)
                    )
                elif csv_list[0] == ('GraphicsCard'):
                    # Construct a GraphicsCard object.
                    self.partlist.add_to_partlist(
                        GraphicsCard.parse(csv_list)
                    )
                elif csv_list[0] == ('Memory'):
                    # Construct a Memory object.
                    self.partlist.add_to_partlist(
                        Memory.parse(csv_list)
                    )
                elif csv_list[0] == ('Storage'):
                    # Construct a Storage object.
                    self.partlist.add_to_partlist(
                        Storage.parse(csv_list)
                    )


@icontract.invariant(lambda self: isinstance(self.cmd, CommandPrompt))
class Question:
    """An abstract class.

    The superclass for other Question types.
    Questions are things the Command Prompt can ask.
    """

    def __init__(self, cmd):
        """Initialise Question object."""
        self.__cmd = cmd

    @property
    def cmd(self):
        """Return the cmd attribute."""
        return self.__cmd


class ListDatabase(Question):
    """Display the Partlist object."""

    def __init__(self, cmd, execute=True):
        """Only execute __init__ method when the 'execute' argument is True."""
        if execute:
            super().__init__(cmd)
            # The Partlist __str__() method is invoked.
            print(self.cmd.partlist)


class AddPartToDatabase(Question):
    """Display the Part Types menu.

    Take input for the user's choice. When the user selects a part type,
    call that type's input() method to create an object of that type. Add
    the part returned to the database. If the part is already in the
    database, increase its stock by 1 instead. Use exception handling to
    display any ValueErrors raised while taking input without crashing the
    program. The menu should repeat until the user enters 5.
    """

    def __init__(self, cmd, execute=True):
        """Only execute __init__ method when the 'execute' argument is True."""
        if execute:
            super().__init__(cmd)
            done = False
            while not done:
                # The Part Types menu is kept repeating until 5 is entered.
                option = None
                while option is None or option not in range(1, 6):
                    CommandPrompt.display_menu('Part Types')
                    option = self.cmd.prompt_for_option(limit=6)

                # Now we have a valid option between 1 and 5.
                if option == 5:
                    print()
                    done = True
                else:
                    """
                    Now we have a valid option between 1 and 5.
                    Depending on the number, constructs the appropriate part.
                    Also look that newly created part in the Partlist to see
                    if it is already in there.
                    """
                    try:
                        if option == 1:
                            new_part = CPU.input()
                        elif option == 2:
                            new_part = GraphicsCard.input()
                        elif option == 3:
                            new_part = Memory.input()
                        else:
                            new_part = Storage.input()

                        added = False
                        partlist = self.cmd.partlist
                        parts_of_new_part_type = (
                            item for item in partlist.items
                            if type(new_part).__name__ == type(item).__name__
                        )
                        for item in parts_of_new_part_type:
                            if item.name == new_part.name:
                                if not new_part.equals(item):
                                    console.print(
                                        'Invalid ' + type(item).__name__ + '!',
                                        'Try again with different arguments.',
                                        end='\n\n',
                                        style='red',
                                    )
                                else:
                                    partlist.add_to_partlist(
                                        new_part, print_status=True
                                    )
                                added = True

                        if not added:
                            partlist.add_to_partlist(
                                new_part, print_status=True
                            )
                    except Exception as e:
                        console.print(type(e).__name__ + ':', e, end='\n\n',
                                      style='red')


class Close(Question):
    """Called when user chooses 4 in Main Menu or 5 in Wishlist Menu.

    Before closing the main menu (and ending the program), the Partlist
    should be saved to a CSV file called "database.csv".
                                or
    Remove all the items from the Wishlist and add their stock back into
    the Partlist.
    """

    def __init__(self, cmd, current_menu='Main Menu', execute=True):
        """Only execute __init__ method when the 'execute' argument is True."""
        if execute:
            super().__init__(cmd)
            partlist = self.cmd.partlist
            wishlist = self.cmd.wishlist
            if current_menu == 'Main Menu':
                # Save Partlist to a csv file.
                partlist.save_to_csv()
                print('\nSee you again soon.')
            else:
                # Add stock back into Partlist.
                for item in wishlist.items:
                    partlist.stock[item.name] += wishlist.stock[item.name]
                # Remove all items from Wishlist. Deleter is called.
                del wishlist.items
                del wishlist.stock


class NewWishlist(Question):
    """Superclass of questions inside the Wishlist menu (except Close class).

    Take input for the user's name, then constructs a new Wishlist.
    """

    def __init__(self, cmd, execute=True):
        """Only execute __init__ method when the 'execute' argument is True."""
        if execute:
            super().__init__(cmd)
            if self.cmd.wishlist is None:
                self.cmd.wishlist = Wishlist()
                done = False
                while not done:
                    # The menu is kept repeating until the user enters 5.
                    option = None
                    while option is None or option not in range(1, 6):
                        CommandPrompt.display_menu('Wishlist')
                        option = cmd.prompt_for_option(limit=6)

                    # Now we have a valid option between 1 and 5.
                    if option in range(1, 6):
                        password = getpass.getpass(
                            prompt='Please enter your password: '
                        )
                        try:
                            self.cmd.wishlist.get_authenticator().login(
                                self.cmd.wishlist.username,
                                password,
                            )
                        except Exception as e:
                            print(e)
                        else:
                            if option == 1:
                                AddFromDatabase(cmd)
                            elif option == 2:
                                RemoveFromWishlist(cmd)
                            elif option == 3:
                                ShowWishlist(cmd)
                            elif option == 4:
                                PurchaseAndClose(cmd)
                                done = True
                            else:
                                Close(cmd, 'Wishlist')
                                done = True
                            print()
                            self.cmd.wishlist.get_authenticator().logout(
                                self.cmd.wishlist.username,
                                password,
                            )
                            if option in (4, 5):
                                self.cmd.wishlist = None

    @icontract.require(lambda part_name: isinstance(part_name, str))
    @icontract.ensure(lambda result: isinstance(result, bool))
    def look_up_partlist(self, part_name):
        """
        Search for a part with the name (parameter) to see if it exists in
        the part list and there is at least 1 stock remaining.
        """
        try:
            value = self.cmd.partlist.stock[part_name]
        except KeyError:
            console.print(f'Could not find {part_name}!', style='red')
            return False
        else:
            if value <= 0:
                console.print(f'Not enough of {part_name} in stock!',
                              style='red')
                return False
            return True

    @icontract.require(lambda part_name: isinstance(part_name, str))
    @icontract.ensure(lambda result: isinstance(result, bool))
    def look_up_wishlist(self, part_name):
        """
        Search for a part with the name (parameter) to see if it exists
        in the wish list.
        """
        try:
            value = self.cmd.wishlist.stock[part_name]
        except KeyError:
            console.print(f'Could not find {part_name}!', style='red')
            return False
        else:
            if value <= 0:
                console.print(f'Not enough of {part_name} in stock!',
                              style='red')
                return False
            return True


class AddFromDatabase(NewWishlist):
    """
    If the user selects to add a part, the application will display
    all the database items in a list and they will be asked to input
    the name of the part they want to add. The program will search
    for a part with that name and add it to the wish list if it
    exists and there is enough stock remaining.
    """

    def __init__(self, cmd, execute=True):
        """Only execute __init__ method when the 'execute' argument is True."""
        if execute:
            super().__init__(cmd)
            ListDatabase(cmd)
            part_name = input('Enter the name of the part to add: ')
            if self.look_up_partlist(part_name):
                partlist = self.cmd.partlist
                wishlist = self.cmd.wishlist
                # The part_name is available in stock.
                for partlist_item in partlist.items:
                    if partlist_item.name == part_name:
                        # Decrement that item in Partlist.
                        partlist.stock[part_name] -= 1
                        try:
                            wishlist.stock[part_name]
                        except KeyError:
                            # If the item is not in Wishlist:
                            # 1. Add that new item to Wishlist.
                            # 2. Set its number in Wishlist to 1.
                            wishlist.items.append(partlist_item)
                            wishlist.stock[part_name] = 1
                        else:
                            # Increment that item in Wishlist if it is there.
                            wishlist.stock[part_name] += 1
                        # Display result.
                        stock = wishlist.stock[part_name]
                        console.print(
                            f'Added {partlist_item.__str__()} (x{stock})',
                            style='green',
                        )


class RemoveFromWishlist(NewWishlist):
    """
    If the user selects to remove a part from the wish list they
    will be asked for the name of the part and that part will be
    removed if it exists and stock will return to the part list.
    """

    def __init__(self, cmd, execute=True):
        """Only execute __init__ method when the 'execute' argument is True."""
        if execute:
            super().__init__(cmd)
            part_name = input('Enter the name of the part to remove: ')
            if self.look_up_wishlist(part_name):
                self.cmd.wishlist.remove_part_using_name(
                    part_name
                )
                self.cmd.partlist.stock[part_name] += 1


class ShowWishlist(NewWishlist):
    """Display the Wishlist object."""

    def __init__(self, cmd, execute=True):
        """Only execute __init__ method when the 'execute' argument is True."""
        if execute:
            super().__init__(cmd)
            # The Wishlist __str__() method is invoked.
            print(self.cmd.wishlist)


class PurchaseAndClose(NewWishlist):
    """
    Save the Wishlist to a CSV file with the user's name as the filename,
    for example, if the username is "Gary", save it to a file called
    "Gary.csv".
    """

    def __init__(self, cmd, execute=True):
        """Only execute __init__ method when the 'execute' argument is True."""
        if execute:
            super().__init__(cmd)
            username = self.cmd.wishlist.username
            self.cmd.wishlist.save_to_csv(filename='receipts/'+username)
            console.print('Successful purchase!\n',
                          'Receipt in database/receipts/' + username + '.csv',
                          sep='',
                          style='green')


# ---------------------------------- Program ----------------------------------
if __name__ == '__main__':
    console.print(
        'Copyright (C) 2022 Tan Duc Mai '
        '(tan.duc.work@gmail.com, @tanducmai on LinkedIn)',
        'http://tanducmai.github.io/computer-shop-management/',
        sep='\n',
        end='\n\n' + '-'*30 + '\n\n',
        style='bold',
    )
    console.print('~~ [italic]Welcome to the Computer Store[/] ~~')
    print()
    cmd = CommandPrompt()

    done = False
    while not done:
        # Keep displaying Main Menu until the user enters 4.
        option = None
        while option is None or option not in range(1, 5):
            CommandPrompt.display_menu('Main Menu')
            option = cmd.prompt_for_option(limit=5)

        # Now we have a valid option between 1 and 4.
        if option != 4:
            if option == 1:
                NewWishlist(cmd)
            elif option == 2:
                print()
                ListDatabase(cmd)
                print()
            else:
                print()
                AddPartToDatabase(cmd)
        else:
            Close(cmd, 'Main Menu')
            done = True
