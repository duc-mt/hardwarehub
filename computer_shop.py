#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# |
# |        File:  computer_shop.py
# |      Author:  Tan Duc Mai
# |          Id:  517925
# | Description:  Creates a Computer shop which allows customers
# |               to select and purchase computer parts.
# | This is my own work as defined by the Academic Integrity policy.
# |
# ----------------------------------------------------------------------------


# ------------------------------- Module Import -------------------------------
import abc


# ------------------------------- Computer Part -------------------------------
class ComputerPart(metaclass=abc.ABCMeta):
    """
        An abstract class.
        The superclass for other ComputerPart types.
    """

    def __init__(self, name, price):
        """
            Initialises name and price.
            Called by subclasses using super().__init__()
        """
        self.__name = name
        self.__price = price

    @abc.abstractclassmethod
    def parse(cls):
        """
            An abstract class method.
            Splits the csv_string into separate values and parses them to the
            correct datatypes.
            Uses these values to construct and return a new ComputerPart.
        """
        pass

    @abc.abstractclassmethod
    def input(cls):
        """
            An abstract class method.
            Takes input for each of the necessary variables.
            Uses these input values to construct and return a new ComputerPart.
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
    def to_csv_string(self):
        """
            An abstract method.
            Returns the name of the class followed by each of the instance
            variables separated by commas.
        """
        pass

    @classmethod
    def input_name(cls):
        """
            Sets the name attribute to the argument
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
                print('ValueError: Name must not be empty.')
            else:
                valid = True
        return name

    @classmethod
    def input_price(cls):
        """
            Sets the price attribute to the argument
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
                print('ValueError: Price must not be negative.')
            else:
                valid = True
        return price

    @classmethod
    def display_menu(cls):
        menu_options = (
            'CPU', 'Graphics Card',
            'Memory', 'Storage', 'Back',
        )
        print(f'---- Part Types ----')
        for i, question in enumerate(menu_options):
            print(f'{i+1}. {question}')

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

    def equals(self, other):
        """
            Returns True if the calling object is equal to the other argument.
            Returns False otherwise.
            This method will be overridden in each subclass.
        """
        if isinstance(other, type(self)):
            if (self.get_name() == other.get_name() and
                self.get_price() == other.get_price()):
                return True
        return False


class CPU(ComputerPart):
    """
        A subclass of the ComputerPart class.
    """

    def __init__(self, name, price, cores, frequency_ghz):
        """
            Initialises cores and frequency_ghz.
        """
        super().__init__(name, price)
        self.__cores = cores
        self.__frequency_ghz = frequency_ghz

    def __str__(self):
        """
            Return the variables as a string.
            For example "Intel i7: 4 cores @ 3.2GHz for $990.00".
        """
        return f'{super().get_name()}: {self.get_cores()} cores @ ' + \
               f'{self.get_frequency_ghz()}GHz for ${super().get_price():.2f}'

    @classmethod
    def parse(cls, csv_string):
        """
            Calls the superclass's csv_string_to_list() method to get the
            values as a list.
            Parses these values to the correct datatypes.
            Uses these values to construct and return a new CPU.
        """
        csv_list = csv_string.split(',')[1:-1]
        csv_list[1] = float(csv_list[1])
        csv_list[2] = int(csv_list[2])
        csv_list[3] = float(csv_list[3])
        return CPU(
            csv_list[0],
            csv_list[1],
            csv_list[2],
            csv_list[3],
        )

    @classmethod
    def input(cls):
        """
            Takes input for the name, price, frequency, and number of cores.
            Uses these input values to construct and return a new CPU.
        """
        return cls(
            cls.input_name(),
            cls.input_price(),
            cls.input_cores(),
            cls.input_frequency_ghz(),
        )

    @classmethod
    def input_cores(cls):
        """
            Sets the cores attribute to the argument
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
                print('ValueError: Number of Cores must not be negative.')
            else:
                valid = True
        return cores

    @classmethod
    def input_frequency_ghz(cls):
        """
            Sets the frequency_ghz attribute to the argument
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
                print('ValueError: Frequency must not be negative.')
            else:
                valid = True
        return frequency_ghz

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

    def equals(self, other):
        """
            Returns True if the calling object and the other argument are both
            CPUs and the values of their variables are the same.
            Returns False otherwise.
        """
        if super().equals(other):
            if (self.get_cores() == other.get_cores() and
                self.get_frequency_ghz() == other.get_frequency_ghz()):
                return True
        return False

    def to_csv_string(self):
        """
            Return the name of the class followed by each of the class
            variables separated by commas.
            Format: "CPU,name,price,cores,frequency_ghz".
        """
        return f'CPU,{super().get_name()},{super().get_price()},' + \
               f'{self.get_cores()},{self.get_frequency_ghz()}'


class GraphicsCard(ComputerPart):
    """
        A subclass of the ComputerPart class.
    """

    def __init__(self, name, price, frequency_mhz, memory_gb):
        """
            Initialises frequency_mhz and memory_gb by calling theirs
            mutator methods.
        """
        super().__init__(name, price)
        self.__frequency_mhz = frequency_mhz
        self.__memory_gb = memory_gb

    def __str__(self):
        """
            Return the variables as a string.
            For example "NVIDIA GeForce 1080: 8GB @ 1607MHz for $925.00".
        """
        return f'{super().get_name()}: {self.get_memory_gb()}GB @ ' + \
               f'{self.get_frequency_mhz()}MHz for ${super().get_price():.2f}'

    @classmethod
    def parse(cls, csv_string):
        """
            Calls the superclass's csv_string_to_list() method to get the
            values as a list.
            Parses these values to the correct datatypes.
            Uses these values to construct and return a new GraphicsCard.
        """
        csv_list = csv_string.split(',')[1:-1]
        csv_list[1] = float(csv_list[1])
        csv_list[2] = int(csv_list[2])
        csv_list[3] = int(csv_list[3])
        return GraphicsCard(
            csv_list[0],
            csv_list[1],
            csv_list[2],
            csv_list[3],
        )

    @classmethod
    def input(cls):
        """
            Takes input for the name, price, memory, and frequency.
            Uses these input values to construct and return a new GraphicsCard.
        """
        return cls(
            cls.input_name(),
            cls.input_price(),
            cls.input_frequency_mhz(),
            cls.input_memory_gb(),
        )

    @classmethod
    def input_frequency_mhz(cls):
        """
            Sets the frequency_mhz attribute to the argument.
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
                print('ValueError: Frequency must not be negative.')
            else:
                valid = True
        return frequency_mhz

    @classmethod
    def input_memory_gb(cls):
        """
            Sets the memory_gb attribute to the argument.
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
                print('ValueError: Memory must not be negative.')
            else:
                valid = True
        return memory_gb

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

    def equals(self, other):
        """
            Returns True if the calling object and the other argument are both
            GraphicsCards and the values of their variables are the same.
            Returns False otherwise.
        """
        if super().equals(other):
            if (self.get_memory_gb() == other.get_memory_gb() and
                self.get_frequency_mhz() == other.get_frequency_mhz()):
                return True
        return False

    def to_csv_string(self):
        """
            Return the name of the class followed by each of the class
            variables separated by commas.
            Format: "GraphicsCard,name,price,frequency_mhz,memory_gb".
        """
        return f'GraphicsCard,{super().get_name()},{super().get_price()},' + \
               f'{self.get_frequency_mhz()},{self.get_memory_gb()}'


class Memory(ComputerPart):
    """
        A subclass of the ComputerPart class.
    """

    def __init__(self, name, price, capacity_gb, frequency_mhz, ddr):
        """
            Initialises capacity_gb and frequency_mhz by calling theirs
            mutator methods.
        """
        super().__init__(name, price)
        self.__capacity_gb = capacity_gb
        self.__frequency_mhz = frequency_mhz
        self.__ddr = ddr

    def __str__(self):
        """
            Return the variables as a string.
            For example "Corsair Vengeance: 16GB, DDR4 @ 3000MHz for $239.00".
        """
        return f'{super().get_name()}: {self.get_capacity_gb()}GB, ' + \
               f'{self.get_ddr()} @ {self.get_frequency_mhz()}MHZ ' + \
               f'for ${super().get_price():.2f}'

    @classmethod
    def parse(cls, csv_string):
        """
            Calls the superclass's csv_string_to_list() method to get the
            values as a list.
            Parses these values to the correct datatypes.
            Uses these values to construct and return a new Memory.
        """
        csv_list = csv_string.split(',')[1:-1]
        csv_list[1] = float(csv_list[1])
        csv_list[2] = int(csv_list[2])
        csv_list[3] = int(csv_list[3])
        return Memory(
            csv_list[0],
            csv_list[1],
            csv_list[2],
            csv_list[3],
            csv_list[4],
        )

    @classmethod
    def input(cls):
        """
            Takes input for the name, price, memory, and frequency.
            Uses these input values to construct and return a new Memory.
        """
        return cls(
            cls.input_name(),
            cls.input_price(),
            cls.input_capacity_gb(),
            cls.input_frequency_mhz(),
            cls.input_ddr(),
        )

    @classmethod
    def input_capacity_gb(cls):
        """
            Sets the capacity_gb attribute to the argument.
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
                print('ValueError: Capacity must not be negative.')
            else:
                valid = True
        return capacity_gb

    @classmethod
    def input_frequency_mhz(cls):
        """
            Sets the frequency_mhz attribute to the argument.
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
                print('ValueError: Frequency must not be negative.')
            else:
                valid = True
        return frequency_mhz

    @classmethod
    def input_ddr(cls):
        """
            Sets the ddr attribute to the argument
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
                print('ValueError: DDR must not be empty.')
            else:
                valid = True
        return ddr

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

    def equals(self, other):
        """
            Returns True if the calling object and the other argument are both
            Memory and the values of their variables are the same.
            Returns False otherwise.
        """
        if super().equals(other):
            if (self.get_frequency_mhz() == other.get_frequency_mhz() and
                self.get_capacity_gb() == other.get_capacity_gb() and
                self.get_ddr() == other.get_ddr()):
                return True
        return False

    def to_csv_string(self):
        """
            Return the name of the class followed by each of the class
            variables separated by commas.
            Format: "Memory,name,price,capacity_gb,frequency_mhz,ddr".
        """
        return f'Memory,{super().get_name()},{super().get_price()},' + \
               f'{self.get_capacity_gb()},{self.get_frequency_mhz()},' + \
               f'{self.get_ddr()}'


class Storage(ComputerPart):
    """
        A subclass of the ComputerPart class.
    """

    def __init__(self, name, price, capacity_gb, storage_type):
        """
            Initialises capacity_gb and frequency_mhz by calling theirs
            mutator methods.
        """
        super().__init__(name, price)
        self.__capacity_gb = capacity_gb
        self.__storage_type = storage_type

    def __str__(self):
        """
            Return the variables as a string.
            For example "Seagate Barracuda: 1000GB HDD for $60.00".
        """
        return f'{super().get_name()}: {self.get_capacity_gb()}GB, ' + \
               f'{self.get_storage_type()} for ${super().get_price():.2f}'

    @classmethod
    def parse(cls, csv_string):
        """
            Calls the superclass's csv_string_to_list() method to get the values
            as a list.
            Parses these values to the correct datatypes.
            Uses these values to construct and return a new Storage.
        """
        csv_list = csv_string.split(',')[1:-1]
        csv_list[1] = float(csv_list[1])
        csv_list[2] = int(csv_list[2])
        return Storage(
            csv_list[0],
            csv_list[1],
            csv_list[2],
            csv_list[3],
        )

    @classmethod
    def input(cls):
        """
            Takes input for the name, price, memory, and frequency.
            Uses these input values to construct and return a new Storage.
        """
        return cls(
            cls.input_name(),
            cls.input_price(),
            cls.input_capacity_gb(),
            cls.input_storage_type(),
        )

    @classmethod
    def input_capacity_gb(cls):
        """
            Sets the capacity_gb attribute to the argument.
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
                print('ValueError: Capacity must not be negative.')
            else:
                valid = True
        return capacity_gb

    @classmethod
    def input_storage_type(cls):
        """
            Sets the storage_type attribute to the argument.
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
                print(
                    'ValueError: Storage type must be one of HDD, SSD, or SSHD.'
                )
            else:
                valid = True
        return storage_type

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

    def equals(self, other):
        """
            Returns True if the calling object and the other argument are both
            Storage and the values of their variables are the same.
            Returns False otherwise.
        """
        if super().equals(other):
            if (self.get_capacity_gb() == other.get_capacity_gb() and
                self.get_storage_type() == other.get_storage_type()):
                return True
        return False

    def to_csv_string(self):
        """
            Return the name of the class followed by each of the class
            variables separated by commas.
            Format: "Storage,name,price,capacity_gb,storage_type".
        """
        return f'Storage,{super().get_name()},{super().get_price()},' + \
               f'{self.get_capacity_gb()},{self.get_storage_type()}'


# ------------------------------- Data Structure ------------------------------

class PartList():
    """
        A subclass of the WishList class.
        Stores the computer parts (instances of the ComputerPart class)
        available in stock.
    """
    def __init__(self):
        # A variable to store the items (ComputerParts) listed in the store.
        self.__items = list()
        """
            A dictionary
            1. Key is the computer part.
            2. Value is the number of stock that key has in stock.
        """
        self.__stock = dict()

    def __str__(self):
        """
            Return a string that represents the PartList in the format:
            "---- Part List ----
            NVIDIA Quadro RTX: 48GB @ 1005.0MHz for $6300.00 (x1)
            AMD Ryzen 3: 4.0 cores @ 3.7GHz for $97.99 (OUT OF STOCK)
            Corsair Vengeance LED: 16GB, DDR4 @ 3000MHz for $239.00 (x4)
            Seagate FireCuda: 1000GB SSHD for $105.00 (x45)
            --------------------"
        """
        result = ''
        result += '---- Part List ----\n'
        for item in self.get_items():
            result += item.__str__()
            # Check how many stock left.
            stock = self.get_stock()[item.get_name()]
                # Print that number if it is greater than 0.
                # Otherwise, write out of stock.
            if stock:
                result += ' (x' + str(stock) + ')'
            else:
                result += ' (OUT OF STOCK)'
            result += '\n'
        result += '--------------------'
        return result

    def __len__(self):
        """
            Get the length of the items attribute.
            Called within PartList class using len(self)
            Called outside PartList class using len(object)
                - Where object is an instance of the PartList class.
        """
        return len(self.get_items())

    def get_items(self):
        """
            Returns the items attribute.
        """
        return self.__items

    def get_stock(self):
        """
            Returns the stock attribute.
        """
        return self.__stock

    def add_to_part_list(self, new_part):
        """
            Add a new item to the store.
            If it is duplicate, the available stock must be incremented by 1.
        """
        name_of_new_part = new_part.get_name()
        if name_of_new_part not in self.get_items():
            self.get_items().append(new_part)
            self.get_stock()[name_of_new_part] = 1
        else:
            # Duplicate item, so increment available stock by 1.
            self.get_stock()[name_of_new_part] += 1

    def get_part_using_name(self, part_name):
        """
            Find and access a part using its name.
            Check to see if that part name is in store.
        """
        for item in self.get_items():
            if item.get_name() == part_name:
                return item

    def get_part_using_position(self, part_position):
        """
            Find and access a part using its position.
            Check to see if the argument is less than the length of the list.
        """
        if part_position < len(self):
            return self.get_items()[part_position]

    def remove_part_using_name(self, part_name):
        """
            Find and remove a part using its name.
            Check to see if that part name is in store.
            Clear all stock of that part in store.
        """
        for item in self.get_items():
            if item.get_name() == part_name:
                self.get_items().remove(part_name)
                del self.get_stock()[name_of_new_part]

    def remove_part_using_position(self, part_position):
        """
            Find and access a part using its position.
            Check to see if the argument is less than the length of the list.
            Clear all stock of that part in store.
        """
        if part_position < len(self):
            part_name = self.get_items().pop(part_position)
            self.get_stock().pop(part_name)

    def save_to_csv(self, filename='database'):
        """
            Save all parts to a csv file with an argument file name.
            Default to the file name database.csv
        """
        with open(filename + '.csv', mode='w') as outfile:
            for item in self.get_items():
                outfile.write(item.to_csv_string())
                # Check how many stock left.
                stock = self.get_stock()[item.get_name()]
                # Write that number to file if it is greater than 0.
                # Otherwise, write out of stock.
                if stock:
                    outfile.write(',x' + str(stock))
                else:
                    outfile.write(',OUT OF STOCK')
                outfile.write('\n')


class WishList(PartList):
    """
        A subclass of the PartList class.
    """
    def __init__(self):
        self.set_username()
        # A variable to store the items listed in the store.
        self.__items = list()
        """
            A dictionary
            1. Key is the computer part.
            2. Value is the number of stock that key has in Wish List.
        """
        self.__stock = dict()

    def __str__(self):
        """
            Returns a string that represents the WishList in the format:
            "---- Gary's Wish List ----
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
        result = ''
        result += f'\n---- {self.get_username()}\'s Wish List ----'

        if len(self):
            for item in self.get_items():
                result += '\n'
                result += item.__str__()
                # Check how many stock left.
                stock_in_part_list = self.get_stock()[item.get_name()]
                # Print that number if it is greater than 0.
                # Otherwise, write out of stock.
                if stock_in_part_list:
                    result += ' (x' + str(stock_in_part_list) + ')'
                else:
                    result += ' (OUT OF STOCK)'

        result += '\n--------------------\n'
        result += f'${self.__get_total_cost():.2f}\n'

        if self.__is_valid_computer():
            result += 'Valid computer'
        else:
            result += 'Not a valid computer'

        return result

    def __len__(self):
        """
            Get the length of the items attribute.
            Called within WishList class using len(self)
            Called outside WishList class using len(object)
                - Where object is an instance of the WishList class.
        """
        return len(self.get_items())

    def set_username(self):
        username = None
        while username is None or username == '':
            username = input('Enter your name: ')
            if username == '':
                print(
                  'ValueError: Cannot create a Wish List with an empty name.'
                )
        self.__username = username

    def get_username(self):
        return self.__username

    def get_items(self):
        """
            Returns the items attribute.
        """
        return self.__items

    def get_stock(self):
        """
            Returns the stock attribute.
        """
        return self.__stock

    def __get_total_cost(self):
        """
            A private method.
            Calculates and returns the total cost of all parts.
        """
        price = 0
        for item in self.get_items():
            number = self.get_stock()[item.get_name()]
            price += item.get_price() * number
        return price

    def __is_valid_computer(self):
        """
            A private method.
            Determines if the parts will make up a valid computer.
            A valid computer requires at least:
               - 1 CPU, 1 GraphicsCard, 1 Memory, and 1 Storage.
        """
        # A dictionary to check if one of these parts is in the WishList.
        is_in_wish_list = {
            'CPU': False,
            'GraphicsCard': False,
            'Memory': False,
            'Storage': False,
        }
        for item in self.get_items():
            if isinstance(item, CPU):
                is_in_wish_list['CPU'] = True
            elif isinstance(item, GraphicsCard):
                is_in_wish_list['GraphicsCard'] = True
            elif isinstance(item, Memory):
                is_in_wish_list['Memory'] = True
            elif isinstance(item, Storage):
                is_in_wish_list['Storage'] = True

        if (is_in_wish_list['CPU'] == True and
            is_in_wish_list['GraphicsCard'] == True and
            is_in_wish_list['Memory'] == True and
            is_in_wish_list['Storage'] == True):
            # Wish List currently has all of the parts -> a valid computer.
            return True
        else:
            return False


# ------------------------------- User Interface ------------------------------
class CommandPrompt:
    """
        The user interface of the system.
    """

    def __init__(self):
        self.__part_list = PartList()
        self.__wish_list = None
        self.__read_from_csv()
        self.__construct_menu()

    def get_part_list(self):
        """
            Returns the PartList object.
        """
        return self.__part_list

    def get_wish_list(self):
        """
            Returns the WishList object.
        """
        return self.__wish_list

    def set_wish_list(self, obj):
        """
            Sets the wish_list attribute to the argument (a WishList object).
        """
        if isinstance(obj, WishList):
            self.__wish_list = obj
        else:
            raise TypeError('WishListError')

    def get_menu_options(self):
        """
            Returns the menu_options attribute.
        """
        return self.__menu_options

    def display_menu(self, menu_type):
        """
            Depending on the type of menu: Main Menu/Wish List,
            outputs the appropriate menu.
        """
        print(f'\n---- {menu_type} ----')
        if menu_type == 'Main Menu':
            menu_options = self.get_menu_options()[0]
        elif menu_type == 'Wish List':
            menu_options = self.get_menu_options()[1]
        for i, question in enumerate(menu_options):
            print(f'{i+1}. {question}')

    def prompt_for_option(self, limit):
        """
            Prompts the user for a number as an option for the displayed menu.
            Option must be an integer number in range 1 - limit.
        """
        option = input(f'Enter an option (1-{limit-1}): ')
        # Handle the error if option is not a number.
        try:
            option = int(option)
        except ValueError as e:
            print(f'{type(e).__name__}: {repr(option)} is not a number.\n')
            option = None
        # Handle the error if option is a number, but outside range.
        if option is not None and option not in range(1, limit):
            try:
                raise ValueError(f'{repr} must be in range 1 - {limit}.')
            except ValueError as e:
                print(
                    f'{type(e).__name__}: {option} is outside range '
                    f'1 - {limit}.\n'
                )
                option = None
        return option

    def __read_from_csv(self):
        """
            This method is automatically invoked when an object of type
            CommandPrompt is constructed.
            By invoking this method, the CommandPrompt class should
            automatically construct a part list and fill it with items that
            it reads from the CSV file named "database.csv".
        """
        with open('database.csv') as infile:
            list_of_csv_strings = list()
            line = None
            while line is None or line != '':
                line = infile.readline().rstrip('\n')
                list_of_csv_strings.append(line)

            for csv_string in list_of_csv_strings:
                if 'CPU' in csv_string:
                    # Construct a CPU object.
                    self.get_part_list().add_to_part_list(
                        CPU.parse(csv_string)
                    )
                elif 'GraphicsCard' in csv_string:
                    # Construct a GraphicsCard object.
                    self.get_part_list().add_to_part_list(
                        GraphicsCard.parse(csv_string)
                    )
                elif 'Memory' in csv_string:
                    # Construct a Memory object.
                    self.get_part_list().add_to_part_list(
                        Memory.parse(csv_string)
                    )
                elif 'Storage' in csv_string:
                    # Construct a Storage object.
                    self.get_part_list().add_to_part_list(
                        Storage.parse(csv_string)
                    )

    def __construct_menu(self):
        """
            Appends each question from the list menu_options (parameter)
            to the menu_options attribute.
            Meanwhile, invokes the convert_class_name method to convert
            the name of each question to the proper format.
        """
        menu_options = []

        # Add four options for Main Menu.
        menu_options.append((
            self.__convert_class_name(NewWishList(self, execute=False)),
            self.__convert_class_name(ListDatabase(self, execute=False)),
            self.__convert_class_name(AddPartToDatabase(self, execute=False)),
            self.__convert_class_name(Close(self, execute=False)),
        ))

        # Add five options for Wish List Menu.
        menu_options.append((
            self.__convert_class_name(AddFromDatabase(self, execute=False)),
            self.__convert_class_name(RemoveFromWishList(self, execute=False)),
            self.__convert_class_name(ShowWishList(self, execute=False)),
            self.__convert_class_name(PurchaseAndClose(self, execute=False)),
            self.__convert_class_name(Close(self, execute=False)),
        ))

        self.__menu_options = menu_options

    def __convert_class_name(self, obj):
        """
            Convert a class name to a human-readable name.
            E.g. 'New Wish List' is transformed into 'NewWishList'.
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


class Question:
    """
        An abstract class.
        The superclass for other Question types.
        Questions are things the Command Prompt can ask.
    """

    def __init__(self, cmd):
        self.__cmd = cmd

    def get_cmd(self):
        return self.__cmd


class ListDatabase(Question):
    """
        Display the PartList object.
    """

    def __init__(self, cmd, execute=True):
        if execute:
            super().__init__(cmd)
            # The PartList __str__() method is invoked.
            print((super().get_cmd().get_part_list()))


class AddPartToDatabase(Question):
    """
        Display the Part Types menu.

        Take input for the user's choice. When the user selects a part type,
        call that type's input() method to create an object of that type. Add
        the part returned to the database. If the part is already in the
        database, increase its stock by 1 instead. Use exception handling to
        display any ValueErrors raised while taking input without crashing the
        program. The menu should repeat until the user enters 5.
    """

    def __init__(self, cmd, execute=True):
        if execute:
            super().__init__(cmd)
            # The Part Types menu is kept repeating until the user enters 5.
            option = None
            while option is None or option not in range(1, 6) or option != 5:
                ComputerPart.display_menu()
                option = super().get_cmd().prompt_for_option(limit=6)
                if option in range(1, 5):
                    """
                        Now we have a valid option between 1 and 5.
                        Depending on the number, constructs the appropriate part.
                        Also look that newly created part in the Part List to see
                        if it is already in there.
                    """
                    if option == 1:
                        new_part = CPU.input()
                    elif option == 2:
                        new_part = GraphicsCard.input()
                    elif option == 3:
                        new_part = Memory.input()
                    elif option == 4:
                        new_part = Storage.input()

                    if self.__look_up_part_list(new_part):
                        # If it exists in the Part List
                        # increments that part in stock by 1.
                        super().get_cmd().get_part_list().get_stock()[new_part.get_name()] += 1
                    else:
                        # Otherwise:
                        #     1. Adds that new part to the Part List
                        #     2. Sets its stock to 1.
                        super().get_cmd().get_part_list().get_items().append(new_part)
                        super().get_cmd().get_part_list().get_stock()[new_part.get_name()] = 1

                    print('Added', new_part.__str__(), end='')
                    # Check how many stock left.
                    print(
                        ' (x'
                        + str(super().get_cmd().get_part_list().get_stock()[new_part.get_name()])
                        + ')'
                    )
                    print()

    def __look_up_part_list(self, new_part):
        """
            Searchs for a part (parameter) which is a newly created part
            to see if it exists in the Part List.
            Returns True if it is, False otherwise.
        """
        try:
            value = super().get_cmd().get_part_list().get_stock()[new_part.get_name()]
        except KeyError:
            return False
        else:
            return True


class Close(Question):
    """
        Before closing the main menu (and ending the program), the Part List
        should be saved to a CSV file called "database.csv".
                                    or
        Remove all the items from the Wish List and add their stock back into
        the Part List.
    """

    def __init__(self, cmd, current_menu='Main Menu', execute=True):
        if execute:
            super().__init__(cmd)
            if current_menu == 'Main Menu':
                # Save PartList to a csv file.
                super().get_cmd().get_part_list().save_to_csv('test')
                print('\nSee you again soon.')
            else:
                # Add stock back into PartList.
                for item in super().get_cmd().get_wish_list().get_items():
                    super().get_cmd().get_part_list().get_stock()[item.get_name()] += 1
                # Remove all items from WishList.
                super().get_cmd().get_wish_list().get_items().clear()
                super().get_cmd().get_wish_list().get_stock().clear()


class NewWishList(Question):
    """
        Takes input for the user's name, then constructs a new WishList and
        displays the Wish List Menu in the format:
    """
    def __init__(self, cmd, execute=True):
        if execute:
            super().__init__(cmd)
            if super().get_cmd().get_wish_list() is None:
                super().get_cmd().set_wish_list(WishList())
                # The menu is kept repeating until the user enters 5.
                option = None
                while option is None or option not in range(1, 6) or option not in {4, 5}:
                    super().get_cmd().display_menu('Wish List')
                    option = cmd.prompt_for_option(limit=6)
                    if option in range(1, 6):
                        # Now we have a valid option between 1 and 5.
                        if option == 1:
                            AddFromDatabase(cmd)
                        elif option == 2:
                            RemoveFromWishList(cmd)
                        elif option == 3:
                            ShowWishList(cmd)
                        elif option == 4:
                            PurchaseAndClose(cmd)
                        else:
                            Close(cmd, 'Wish List')

    def look_up_part_list(self, part_name):
        """
            Search for a part with the name (parameter) to see if it exists in
            the part list and there is at least 1 stock remaining.
        """
        try:
            value = super().get_cmd().get_part_list().get_stock()[part_name]
        except KeyError:
            print(f'Could not find {part_name}!')
            return False
        else:
            if value > 0:
                return True
            else:
                print(f'Not enough of {part_name} in stock!')
                return False

    def look_up_wish_list(self, part_name):
        """
            Search for a part with the name (parameter) to see if it exists
            in the wish list.
        """
        try:
            value = super().get_cmd().get_wish_list().get_stock()[part_name]
        except KeyError:
            print(f'Could not find {part_name}!')
            return False
        else:
            if value > 0:
                return True
            else:
                print(f'Not enough of {part_name} in stock!')
                return False


class AddFromDatabase(NewWishList):
    """
        If the user selects to add a part, the application will display
        all the database items in a list and they will be asked to input
        the name of the part they want to add. The program will search
        for a part with that name and add it to the wish list if it
        exists and there is enough stock remaining.
    """

    def __init__(self, cmd, execute=True):
        if execute:
            super().__init__(cmd)
            ListDatabase(cmd)
            part_name = input(f'Enter the name of the part to add: ')
            if super().look_up_part_list(part_name):
                # The part_name is available in stock.
                for part_list_item in super().get_cmd().get_part_list().get_items():
                    if part_list_item.get_name() == part_name:
                        # Decrement that item in Part List.
                        super().get_cmd().get_part_list().get_stock()[part_name] -= 1
                        try:
                            value = super().get_cmd().get_wish_list().get_stock()[part_name]
                        except KeyError:
                            # If the item is not in Wish List:
                                # 1. Adds that new item to Wish List.
                                # 2. Sets its number in Wish List to 1.
                            super().get_cmd().get_wish_list().get_items().append(
                                part_list_item
                            )
                            super().get_cmd().get_wish_list().get_stock()[part_name] = 1
                        else:
                            # Increment that item in Wish List if it is there.
                            super().get_cmd().get_wish_list().get_stock()[part_name] += 1
                        # Display result.
                        print('Added', part_list_item.__str__(), end='')
                        # Check how many stock left.
                        print(
                            ' (x'
                            + str(super().get_cmd().get_wish_list().get_stock()[part_name])
                            + ')'
                        )


class RemoveFromWishList(NewWishList):
    """
        If the user selects to remove a part from the wish list they
        will be asked for the name of the part and that part will be
        removed if it exists and stock will return to the part list.
    """

    def __init__(self, cmd, execute=True):
        if execute:
            super().__init__(cmd)
            part_name = input(f'Enter the name of the part to remove: ')
            if super().look_up_wish_list(part_name):
                # The part_name is available in Wish List.
                for index, wish_list_item in enumerate(
                    super().get_cmd().get_wish_list().get_items()
                ):
                    if wish_list_item.get_name() == part_name:
                        # Deletes that item from Wish List.
                        del super().get_cmd().get_wish_list().get_items()[index]
                        # Returns the number of stock back to Part List.
                        super().get_cmd().get_part_list().get_stock()[part_name] += 1
                        # Display result.
                        print('Removed', wish_list_item.__str__(), end='')
                        # Check how many stock is in Wish List.
                        print(
                            ' (x'
                            + str(super().get_cmd().get_wish_list().get_stock()[part_name])
                            + ')'
                        )
                        # Delete the entry for the removed part.
                        del super().get_cmd().get_wish_list().get_stock()[part_name]


class ShowWishList(NewWishList):
    """
        Display the WishList object.
    """

    def __init__(self, cmd, execute=True):
        if execute:
            super().__init__(cmd)
            # The WishList __str__() method is invoked.
            print(super().get_cmd().get_wish_list())


class PurchaseAndClose(NewWishList):
    """
        Save the WishList to a CSV file with the user's name as the filename,
        for example, if the user name is "Gary", save it to a file called
        "Gary.csv".
    """

    def __init__(self, cmd, execute=True):
        if execute:
            super().__init__(cmd)
            username = super().get_cmd().get_wish_list().get_username()
            super().get_cmd().get_wish_list().save_to_csv(username)
            print(
                f'Successful purchase!',
                f'Receipt in {username}.csv',
                sep='\n',
            )


# ------------------------------- Computer Shop -------------------------------
class ComputerPartShop:
    """
        Manages the CommandPrompt object of the program.
    """
    def __init__(self, cmd):
        self.set_cmd(cmd)

    def get_cmd(self):
        return self.__cmd

    def set_cmd(self, cmd):
        if isinstance(cmd, CommandPrompt):
            self.__cmd = cmd
        else:
            raise TypeError('CommandPromptError')


# ------------------------------- Main Function -------------------------------
def main():
    print("~~ Welcome to the Computer Store ~~")
    shop = ComputerPartShop(CommandPrompt())  # Construct object
    cmd = shop.get_cmd()

    # Keep displaying Main Menu until the user enters 4.
    option = None
    while option is None or option not in range(1, 5) or option != 4:
        cmd.display_menu('Main Menu')
        option = cmd.prompt_for_option(limit=5)
        if option in range(1, 5):
            # Now we have a valid option between 1 and 4.
            if option == 1:
                NewWishList(cmd)
            elif option == 2:
                print()
                ListDatabase(cmd)
            elif option == 3:
                print()
                AddPartToDatabase(cmd)
            else:
                Close(cmd, 'Main Menu')


# --------------------------- Call the Main Function --------------------------
if __name__ == '__main__':
    main()
