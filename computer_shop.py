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


# -------------------------------- Computer Part ------------------------------
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

    # def csv_string_to_list(cls, csv_string):
    #     """
    #         Splits the csv_string into separate values stored as a list.
    #         Called by subclasses using super().csv_string_to_list(csv_string)
    #     """
    #     result = []
    #     for letter in csv_string:
    #         item = ''
    #         if letter != ',':
    #             item += letter
    #         else:
    #             result.append(item)
    #     return result

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


class CPU(ComputerPart):
    """
        A subclass of the ComputerPart class.
    """

    def __init__(self, name, price, cores, frequency_ghz):
        """
            Initialises cores and frequency_ghz by calling theirs
            mutator methods.
        """
        super().__init__(name, price)
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
            f'CPU,{super().get_name()},{super().get_price()},'
            f'{self.get_cores()},{self.get_frequency_ghz()}'
        )

    def __str__(self):
        """
            Return the variables as a string.
            For example "Intel i7: 4 cores @ 3.2GHz for $990.00".
        """
        return (
            f'{super().get_name()}: {self.get_cores()} cores, @ '
            f'{self.get_frequency_ghz()}GHz for ${super().get_price():.2f}'
        )

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

        return CPU(csv_list[0], csv_list[1], csv_list[2], csv_list[3])

    @classmethod
    def input(cls):
        """
            Takes input for the name, price, frequency, and number of cores.
            Uses these input values to construct and return a new CPU.
        """
        name = input('Enter the name: ')
        price = float(input('Enter the price: '))
        cores = int(input('Enter the number of cores: '))
        frequency_ghz = float(input('Enter the frequency in GHz: '))

        return (CPU(name, price, cores, frequency_ghz))


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
            f'GraphicsCard,{super().get_name()},{super().get_price()},'
            f'{self.get_frequency_mhz()},{self.get_memory_gb()}'
        )

    def __str__(self):
        """
            Return the variables as a string.
            For example "NVIDIA GeForce 1080: 8GB @ 1607MHz for $925.00".
        """
        return (
            f'{super().get_name()}: {self.get_memory_gb()}GB @ '
            f'{self.get_frequency_mhz()}MHz for ${super().get_price():.2f}'
        )

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

        return GraphicsCard(csv_list[0], csv_list[1], csv_list[2], csv_list[3])

    @classmethod
    def input(cls):
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

    def __init__(self, name, price, capacity_gb, frequency_mhz, ddr):
        """
            Initialises capacity_gb and frequency_mhz by calling theirs
            mutator methods.
        """
        super().__init__(name, price)
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
            f'Memory,{super().get_name()},{super().get_price()},'
            f'{self.get_capacity_gb()},{self.get_frequency_mhz()},'
            f'{self.get_ddr()}'
        )

    def __str__(self):
        """
            Return the variables as a string.
            For example "Corsair Vengeance: 16GB, DDR4 @ 3000MHz for $239.00".
        """
        return (
            f'{super().get_name()}: {self.get_capacity_gb()}GB, '
            f'{self.get_ddr()} @ {self.get_frequency_mhz()}MHZ '
            f'for ${super().get_price():.2f}'
        )

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
            csv_list[0], csv_list[1], csv_list[2],csv_list[3], csv_list[4],
        )

    @classmethod
    def input(cls):
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

    def __init__(self, name, price, capacity_gb, storage_type):
        """
            Initialises capacity_gb and frequency_mhz by calling theirs
            mutator methods.
        """
        super().__init__(name, price)
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
            f'Storage,{super().get_name()},{super().get_price()},'
            f'{self.get_capacity_gb()},{self.get_storage_type()}'
        )

    def __str__(self):
        """
            Return the variables as a string.
            For example "Seagate Barracuda: 1000GB HDD for $60.00".
        """
        return (
            f'{super().get_name()}: {self.get_capacity_gb()}GB, '
            f'{self.get_storage_type()} for ${super().get_price():.2f}'
        )

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

        return Storage(csv_list[0], csv_list[1], csv_list[2], csv_list[3])

    @classmethod
    def input(cls):
        """
            Takes input for the name, price, memory, and frequency.
            Uses these input values to construct and return a new Storage.
        """
        name = input('Enter the name: ')
        price = float(input('Enter the price: '))
        capacity_gb = int(input('Enter the capacity in GB: '))
        storage_type = input('Enter the storage type (HDD/SSD/SSHD): ')

        return Storage(name, price, capacity_gb, frequency_mhz, storage_type)


# ------------------------------- Data Structure ------------------------------

class PartList():
    """
        A subclass of the WishList class.
        Stores the computer parts (instances of the ComputerPart class)
        available in stock.
    """
    def __init__(self):
        # A variable to store the items listed in the store.
        self.__items_in_store = []
        """
            A dictionary
            1. Key is the computer part.
            2. Value is the number of that key available in stock.
        """
        self.__stock_available = {}

    def get_length(self):
        """
            Get the length of the items_in_store attribute.
        """
        return len(self.get_items_in_store())

    def get_items_in_store(self):
        """
            Returns the items_in_store attribute.
        """
        return self.__items_in_store

    def get_stock_available(self):
        """
            Returns the stock_available attribute.
        """
        return self.__stock_available

    def add_part_to_store(self, new_part):
        """
            Add a new item to the store.
            If it is duplicate, the available stock must be incremented by 1.
        """
        name_of_new_part = new_part.get_name()
        if name_of_new_part not in self.get_items_in_store():
            self.get_items_in_store().append(new_part)
            self.get_stock_available().update({name_of_new_part: 1})
        else:
            # Duplicate item, so increment available stock by 1.
            self.get_stock_available()[name_of_new_part] += 1

    def get_part_using_name(self, part_name):
        """
            Find and access a part using its name.
            Check to see if that part name is in store.
        """
        for item in self.get_items_in_store():
            if item.get_name() == part_name:
                return item

    def get_part_using_position(self, part_position):
        """
            Find and access a part using its position.
            Check to see if the argument is less than the length of the list.
        """
        if part_position < self.get_length():
            return self.get_items_in_store()[part_position]

    def remove_part_using_name(self, part_name):
        """
            Find and remove a part using its name.
            Check to see if that part name is in store.
            Clear all stock of that part in store.
        """
        for item in self.get_items_in_store():
            if item.get_name() == part_name:
                self.get_items_in_store().remove(part_name)
                self.get_stock_available()[part_name] = 0

    def remove_part_using_position(self, part_position):
        """
            Find and access a part using its position.
            Check to see if the argument is less than the length of the list.
            Clear all stock of that part in store.
        """
        if part_position < self.get_length():
            part_name = self.get_items_in_store().pop(part_position)
            self.get_stock_available()[part_name] = 0

    def save_to_csv(self, filename):
        """
            Save all parts to a csv file with an argument file name.
        """
        with open(filename + '.csv', mode='w') as outfile:
            for item in self.get_items_in_store():
                outfile.write(item.to_csv_string())
                # Write how many stock left.
                stock_available = self.get_stock_available()[item.get_name()]
                if stock_available:
                    outfile.write(',x' + str(stock_available))
                else:
                    outfile.write(',OUT OF STOCK')
                outfile.write('\n')

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
        for item in self.get_items_in_store():
            result += item.__str__()
            result += '\n'
        result += '--------------------\n'
        return result


class WishList(PartList):
    """
        A subclass of the PartList class.
    """
    def __init__(self):
        self.__username = input('Enter your name: ')

    def get_username(self):
        return self.__username

    def get_total_cost(self):
        """
            Calculate and return the total cost of all parts.
        """
        price = 0
        return price

    def is_valid_computer(self):
        """
            Determine if the parts will make up a valid computer.
            A valid computer requires at least:
                - 1 CPU, 1 GraphicsCard, 1 Memory, and 1 Storage.
        """
        pass

    def __str__(self):
        """
            Return a string that represents the WishList in the format:
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
        result += f'---- {self.get_username()}\'s Wish List ----'
        # for item in

        if is_valid_computer():
            result += 'Valid computer'
        else:
            result += 'Not a valid computer'
        return result


# ------------------------------- User Interface ------------------------------
class CommandPrompt:
    """
        The user interface of the system.
    """

    def __init__(self):
        self.__part_list = PartList()
        self.read_from_csv()
        self.__wish_list = []
        self.__question_list = []

    def read_from_csv(self):
        """
            This method is automatically invoked when an object of type
            CommandPrompt is constructed.
            By invoking this method, the CommandPrompt class should
            automatically construct a part list and fill it with items that
            it reads from the CSV file named "database.csv".
        """
        with open('database.csv') as infile:
            list_of_csv_strings = []
            line = None
            while line is None or line != '':
                line = infile.readline().rstrip('\n')
                list_of_csv_strings.append(line)

            for csv_string in list_of_csv_strings:
                if 'CPU' in csv_string:
                    # Construct a CPU object.
                    self.get_part_list().add_part_to_store(
                        CPU.parse(csv_string)
                    )
                elif 'GraphicsCard' in csv_string:
                    # Construct a GraphicsCard object.
                    self.get_part_list().add_part_to_store(
                        GraphicsCard.parse(csv_string)
                    )
                elif 'Memory' in csv_string:
                    # Construct a Memory object.
                    self.get_part_list().add_part_to_store(
                        Memory.parse(csv_string)
                    )
                elif 'Storage' in csv_string:
                    # Construct a Storage object.
                    self.get_part_list().add_part_to_store(
                        Storage.parse(csv_string)
                    )

    # getter self.__part_list
    def get_part_list(self):
        return self.__part_list

    def get_items_in_store(self):
        return self.__part_list.get_items_in_store()

    # getter self.__wish_list
    def get_wish_list(self):
        return self.__wish_list

    # getter self.__question_list
    def get_question_list(self):
        return self.__question_list

    # setter self.__question_list
    def set_question_list(self, question_list):
        """
            Append each question to the self.__question_list.
            Convert the name of each question to proper format.
        """
        for question in question_list:
            if isinstance(question, Question):
                self.__question_list.append(self.convert_class_name(question))
            else:
                raise TypeError('QuestionError')

    def convert_class_name(self, class_type):
        """
            Convert a class name to a human-readable name.
            E.g. 'New Wish List' instead of 'NewWishList'.
        """
        obj_name = type(class_type).__name__
        result = ''
        result += obj_name[0]
        for index, letter in enumerate(obj_name):
            if letter.islower():
                result += letter
            else:
                if index != 0:
                    result += ' ' + letter
        return result

    # Provide user with a list of choices.
    def display_menu(self, menu_type, start=None, stop=None):
        """
            Depend on the type of menu: Main Menu/Wish List.
            Output the appropriate menu.
        """
        if menu_type != 'Part Types':
            target_list = self.get_question_list()[start:stop]
        else:
            target_list = [
                'CPU', 'Graphics Card',
                'Memory', 'Storage', 'Back',
            ]

        print(f'---- {menu_type} ----')
        for i, question in enumerate(target_list):
            print(f'{i+1}. {question}')

    def prompt_for_option(self, limit):
        """
            Prompt the user for a number as an option in the displayed menu.
        """
        option = None
        while option is None or option not in range(1, limit + 1):
            option = input(f'Enter an option (1-{limit}): ')
            valid = False
            if not valid:
                try:
                    option = int(option)
                    valid = True
                except ValueError:
                    print('ValueError:', repr(option), 'is not a number.')
            if valid and option not in range(1, limit + 1):
                print(
                    'ValueError:', option, 'is outside range 1 -', limit,
                    end='.\n',
                )
        return option


class Question:
    """
        A blueprint for all questions the Command Prompt can ask.
    """

    def __init__(self, cmd):
        super().__init__()
        self.__cmd = cmd

    # getter for self.__cmd
    def get_cmd(self):
        return self.__cmd

    def output_items(self, target_list, list_type):
        # if isinstance(target_list, WishList):
        # print(f'---- {prompt_for_username()}'s{list_type} ----')
        print(f'---- {list_type} ----')
        for index, item in enumerate(target_list, start=1):
            print(item)

    def prompt_for_part(self, command):
        part = None
        while part is None or part not in (
            'CPU', 'Graphics Card', 'Memory', 'Storage'
        ):
            part = input(f'Enter the name of the part to {command}? ')
            if part not in ('CPU', 'Graphics Card', 'Memory', 'Storage'):
                print(f'Could not find {part}')
        return part


class ListDatabase(Question):
    """
        Display the PartList object.
    """

    def __init__(self, cmd, execute=True):
        super().__init__(cmd)
        if execute:
            super().output_items(self.get_cmd().get_items_in_store(), 'Part List')


class AddPartToDatabase(Question):
    """

        Have not finished  XXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        Display the Part Types menu.

        Take input for the user's choice. When the user selects a part type,
        call that type's input() method to create an object of that type. Add
        the part returned to the database. If the part is already in the
        database, increase its stock by 1 instead. Use exception handling to
        display any ValueErrors raised while taking input without crashing the
        program. The menu should repeat until the user enters 5.
    """

    def __init__(self, cmd, execute=True):
        super().__init__(cmd)
        if execute:
            self.get_cmd().get_items_in_store().append(self.prompt_for_part('add'))


class NewWishList(Question):

    def __init__(self, cmd, execute=True):
        super().__init__(cmd)
        # if execute:
        #     self.get_cmd().display_menu(menu_type='Wish List', start=4, stop=9)

    def prompt_for_username(self):
        return input('Please input your name: ')

    def look_up_part_list(self, target_part):
        """
            Search for a part with the name (parameter) to see if it
            exists in the part list and there is at least 1 stock
            remaining.
        """
        part_list = self.get_cmd().get_items_in_store()
        for item in part_list:
            if item == target_part and part_list.count(item):
                return True
        return False

    def look_up_wish_list(self, target_part):
        """
            Search for a part with the name (parameter) to see if it
            exists in the wish list.
        """
        wish_list = self.get_cmd().get_wish_list()
        if target_part in wish_list:
            return True
        return False


class Close(NewWishList):
    """

        Have not finished  XXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        Before closing the menu (and ending the program), the part list
        should be saved to a csv file called "database.csv".

                                    or

        Remove all the items from the WishList and add their stock back into
        the PartList.
    """

    def __init__(self, cmd, target_menu, execute=True):
        super().__init__(cmd)
        if execute:
            if target_menu == 'WishList':
                self.close_wish_list_menu()
            else:
                self.close_main_menu()

    def close_wish_list_menu(self):
        # Add stock back into PartList.
        self.get_cmd().get_items_in_store().extend(self.get_cmd().get_wish_list())
        # Remove all items from WishList.
        del self.get_cmd().get_wish_list()[:]
        # Return to Main Menu.
        self.get_cmd().display_menu(menu_type='Main Menu', start=0, stop=4)

    def close_main_menu(self):
        # Save PartList to a csv file.
        # with open('database.csv', mode='w') as outfile:
        pass


class AddFromDatabase(NewWishList):
    """
        If the user selects to add a part, the application will display
        all the database items in a list and they will be asked to input
        the name of the part they want to add. The program will search
        for a part with that name and add it to the wish list if it
        exists and there is enough stock remaining.
    """

    def __init__(self, cmd, execute=True):
        super().__init__(cmd)
        if execute:
            ListDatabase(cmd)
            target_part = self.prompt_for_part('add')
            if self.look_up_part_list(target_part):
                self.get_cmd().get_wish_list().append(target_part)
                print(f'Added {target_part}')
            else:
                print('Not a valid part')


class RemoveFromWishList(NewWishList):
    """
        If the user selects to remove a part from the wish list they
        will be asked for the name of the part and that part will be
        removed if it exists and stock will return to the part list.
    """

    def __init__(self, cmd, execute=True):
        super().__init__(cmd)
        if execute:
            target_part = self.prompt_for_part('remove')
            if self.look_up_wish_list(target_part):
                wish_list = self.get_cmd().get_wish_list()
                count = 0
                for item in wish_list:
                    # Remove until all target_part is removed.
                    if item == target_part:
                        wish_list.remove(target_part)
                        count += 1
                print(f'Removed {target_part}')
                # The number of stock is returned back to part list.
                for _ in range(count):
                    self.get_cmd().get_items_in_store().append(target_part)
            else:
                print('Not a valid part')


class ShowWishList(NewWishList):
    """
        Display the WishList object.
    """

    def __init__(self, cmd, execute=True):
        super().__init__(cmd)
        if execute:
            super().output_items(self.get_cmd().get_wish_list(), 'Wish List')


class PurchaseAndClose(NewWishList):
    """
        Save the WishList to a CSV file with the user's name as the filename,
        for example, if the user name is "Gary", save it to a file called
        "Gary.csv".
    """

    def __init__(self, cmd, execute=True):
        super().__init__(cmd)
        if execute:
            with open(self.prompt_for_username() + '.csv', mode='w') as outfile:
                pass

# ------------------------------- Main Function -------------------------------
def main():
    # TODO Write your main program code here...
    print("~~ Welcome to the Computer Store ~~")
    print()
    # shop = ComputerPartShop()  # Construct object
    # shop.command_prompt()      # Call method to start the program

    cmd = CommandPrompt()

    cmd.set_question_list((
        NewWishList(cmd, False),
        ListDatabase(cmd, False),
        AddPartToDatabase(cmd, False),
        Close(cmd, False),
        AddFromDatabase(cmd, False),
        RemoveFromWishList(cmd, False),
        ShowWishList(cmd, False),
        PurchaseAndClose(cmd, False),
        Close(cmd, False),
    ))

    # Test display_menu() method
    # cmd.display_menu(menu_type='Main Menu', start=0, stop=4)
    # cmd.display_menu(menu_type='Wish List', start=4, stop=9)
    # cmd.display_menu(menu_type='Part Types')
    # print('-' * 40)

    # Test ShowWishList() class
    # ShowWishList(cmd)

    # Test ListDatabase() class
    # ListDatabase(cmd)

    # Test AddPartToDatabase() class
    # AddPartToDatabase(cmd)
    # ListDatabase(cmd)

    # Test AddFromDatabase() class
    # ShowWishList(cmd)
    # AddFromDatabase(cmd)
    # ShowWishList(cmd)

    # Test RemoveFromWishList() class
    # ListDatabase(cmd)
    # ShowWishList(cmd)
    # RemoveFromWishList(cmd)
    # ShowWishList(cmd)
    # ListDatabase(cmd)

    cmd.get_part_list().save_to_csv('henry')


# --------------------------- Call the Main Function --------------------------
if __name__ == '__main__':
    main()
