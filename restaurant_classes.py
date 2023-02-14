class Table:
    """
    Class Table represents object of real world table
    It has next fields: name, num_of_seats and is_reserved
    When instance of table is created is_reserved = False
    """

    def __init__(self, name, num_of_seats):
        """
        Constructor of object Table
        :param name: name of the table
        :param num_of_seats: number of seats
        By default, field is_reserved = False
        """
        self.__name = name
        self.__num_of_seats = num_of_seats
        self.__is_reserved = False

    @property
    def name(self):
        return self.__name

    @property
    def num_of_seats(self):
        return self.__num_of_seats

    @property
    def is_reserved(self):
        return self.__is_reserved

    def book(self):
        """
        Changes state of table to booked
        :return: None
        """
        self.__is_reserved = True

    def release(self):
        """
        Changes state of table to released
        :return: None
        """
        self.__is_reserved = False

    def __eq__(self, other):
        return self.__name == other.name


class Booking:
    """
    Class Booking represents object of real world - booking
    It has next fields: guest_name, phone_num b_from, b_to, table
    """

    def __init__(self, guest_name, phone_num, b_from, b_to, table):
        """
        Constructor of object Booking
        :param guest_name: guest name
        :param phone_num: guest phone number
        :param b_from: booking from
        :param b_to: booking to
        :param table: booking table
        """
        self.__guest_name = guest_name
        self.__phone_num = phone_num
        self.__b_from = b_from
        self.__b_to = b_to
        self.__table = table

    @property
    def guest_name(self):
        return self.__guest_name

    @property
    def phone_num(self):
        return self.__phone_num

    @property
    def b_from(self):
        return self.__b_from

    @property
    def b_to(self):
        return self.__b_to

    @property
    def table(self):
        return self.__table

    def __eq__(self, other):
        return self.__guest_name == other.guest_name and self.__phone_num == other.phone_num \
               and self.__b_from == other.b_from and self.__b_to == other.b_to and self.__table.name == other.table.name


class TableDuplicateException(Exception):
    """
    Raises if table is already in the restaurant
    """
    pass


class TableOperateException(Exception):
    """
    Raises if user tries to take already booked table or release free table
    """
    pass


class Restaurant:
    """
    Main object of application. It stores list of tables and list of bookings in restaurant
    """

    def __init__(self):
        """
        Constructor of Restaurant.
        It creates two empty lists:
        1)tables
        2)bookings
        """
        self.__tables = []
        self.__bookings = []

    @property
    def tables(self):
        return self.__tables

    @property
    def bookings(self):
        return self.__bookings

    def add_table(self, table):
        """
        Add a new table to the list of tables
        :param table: added table
        :raises TableDuplicateException: if table is already exist
        :return: None
        """
        if table not in self.__tables:
            self.__tables.append(table)
        else:
            raise TableDuplicateException(f"Table with name '{table.name}' already exists")

    def add_booking(self, booking):
        """
        Add new Booking to the list of bookings
        :param booking:
        :return: None
        """
        if booking not in self.__bookings:
            [table for table in self.__tables if table.name == booking.table.name][0].book()
            self.__bookings.append(booking)

    def delete_table(self, name):
        """
        Firstly, it will delete booking if booking with this table name exist.
        After that it deletes table from the list of tables
        :param name:
        :return:
        """
        self.__bookings = [booking for booking in self.__bookings if booking.table.name != name]
        self.__tables = [table for table in self.__tables if table.name != name]

    def take_table_by_name(self, name):
        """
        Firstly, it will find table in the list of tables by its name.
        Secondly, it will check whether the table is booked
        If no exception is raised, then it will book the table
        :param name: name of the table
        :raises TableOperateException: if table is already booked
        :return: None
        """
        table = [table for table in self.__tables if table.name == name][0]
        if table.is_reserved:
            raise TableOperateException(
                f"{table.name} is already booked, please release it first or choose another one")
        else:
            table.book()

    def release_table_by_name(self, name):
        """
        Firstly, it will find table in the list of tables by its name.
        Secondly, it will check whether the table is free
        If no exception is raised, then it will delete corresponding entry in booking list and release the table
        :param name: name of the table
        :raises TableOperateException: if table is free
        :return: None
        """
        table = [table for table in self.__tables if table.name == name][0]
        if not table.is_reserved:
            raise TableOperateException(f"{table.name} is free")
        else:
            self.__bookings = [booking for booking in self.__bookings if booking.table.name != name]
            table.release()

    def delete_booking(self, bookings):
        """
        Firstly, it will delete entry of booking in the list of booking
        Then, it will find the entry of corresponding table and release it
        :param bookings: list of bookings to delete
        :return: None
        """
        for booking in bookings:
            self.__bookings = [b for b in self.__bookings if not booking.__eq__(b)]
            table = [table for table in self.__tables if table.name == booking.table.name]
            table[0].release()

    def get_num_of_free_tables(self):
        """
        Calculates length of list of free tables
        :return: number of free tables
        """
        return len([table for table in self.__tables if not table.is_reserved])

    def get_num_of_free_seats(self):
        """
        Calculates sum of seats of free tables
        :return: number of free seats
        """
        free_tables = [table for table in self.__tables if not table.is_reserved]
        return sum([table.num_of_seats for table in free_tables])
