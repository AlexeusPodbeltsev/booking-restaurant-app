import streamlit as st
import re
from restaurant_classes import Table, Booking, Restaurant, TableDuplicateException, TableOperateException

# Create instance of restaurant at session
if 'restaurant' not in st.session_state:
    st.session_state['restaurant'] = Restaurant()

restaurant = st.session_state['restaurant']


class WrongInputFormatException(Exception):
    """
    This Exception is raised if string doesn't match the format
    """
    pass


def parse_name_of_table(choice):
    """
    parses choice to get table name
    :param choice:
    :return: name of the table
    """
    name = re.search("(\\w+\\s?\\d+)", choice).group(0)
    return name


def check_table_name_or_phone_num(name="Table 1", phone_num="+79991112233"):
    """
    Matches name of table and guest phone number with pattern using regex
    :param name: name of table
    :param phone_num: guest phone number
    :raises WrongInputFormatException: if string doesn't match the pattern
    :return: None
    """
    name_pattern = re.compile("^\\w+\\s?\\d+$")
    if not name_pattern.match(name):
        raise WrongInputFormatException("Wrong table name format. Right format example: 'Table 1'")

    phone_num_pattern = re.compile("^\\+\\d{11}$")
    if not phone_num_pattern.match(phone_num):
        raise WrongInputFormatException("Wrong phone number format. Right format example: '+79991112233'")


def display_tables_page():
    """
    Displays table management page
    First form displays list of tables in restaurant and let user take, release and delete the table
    Second form let user create a new entry of table
    It also checks whether input name is duplicate or match the pattern
    If no exceptions were raised then new entry added to the restaurant
    :return: None
    """
    st.title("Tables")
    with st.form(key="Operate with tables"):
        choice = st.selectbox("Table",
                              [f"{table.name} - {table.num_of_seats} - {'Booked' if table.is_reserved else 'Free'}"
                               for table in restaurant.tables])
        col1, col2, col3, col4 = st.columns(4)
        take = col1.form_submit_button("Take the table")
        if take:
            name = parse_name_of_table(choice)
            try:
                restaurant.take_table_by_name(name)
            except TableOperateException as ex:
                st.error(ex)

        release = col2.form_submit_button("Release the table")
        if release:
            name = parse_name_of_table(choice)
            try:
                restaurant.release_table_by_name(name)
            except TableOperateException as ex:
                st.warning(ex)
        delete = col4.form_submit_button("Delete")
        if delete:
            name = parse_name_of_table(choice)
            restaurant.delete_table(name)

    #    add new table
    with st.form(key="Add table"):
        name = st.text_input("Name of the table")
        num_of_seats = st.number_input("Number of seats", 1)
        add = st.form_submit_button("Add")
    if add:
        try:
            check_table_name_or_phone_num(name=name)
            restaurant.add_table(Table(name, num_of_seats))
        except (TableDuplicateException, WrongInputFormatException) as ex:
            st.error(str(ex))


def display_booking_page():
    """
    Displays and manipulates with Booking entries
    Form 'add booking' creates new Booking entry
    This form collect required information about the guest and booking
    If 'submit' button is clicked, then new Booking entry will be created
    After that the function checks is list of booking empty
    if not it displays active booking records with checkbox
    if checkbox was chosen then corresponding booking entry will be added to the list_to_delete
    When 'submit' button is clicked then every booking entry from the list will be deleted
    :return: None
    """
    with st.form(key="add booking"):
        st.title("Booking")
        guest_name = st.text_input("Input name")
        guest_phone_num = st.text_input("Input phone")
        col1, col2 = st.columns(2)
        b_from = col1.time_input("From")
        b_to = col2.number_input("Period", 1)
        choice = st.selectbox("Select table",
                              [f"{table.name} - {table.num_of_seats} seats" for table in restaurant.tables if
                               not table.is_reserved])
        submit = st.form_submit_button("Submit")
        if submit:
            try:
                check_table_name_or_phone_num(phone_num=guest_phone_num)
                table = [table for table in restaurant.tables if table.name == parse_name_of_table(choice)]
                restaurant.add_booking(Booking(guest_name, guest_phone_num, b_from, b_to, table[0]))
            except WrongInputFormatException as ex:
                st.error(str(ex))

    if restaurant.bookings:
        inner_col1, inner_col2, inner_col3, inner_col4, inner_col5, inner_col6 = st.columns(6)
        inner_col1.text("Guest name")
        inner_col2.text("Phone num")
        inner_col3.text("From")
        inner_col4.text("To")
        inner_col5.text("Table")
        inner_col6.text("Release")
        list_to_delete = []

        for booking in restaurant.bookings:
            inner_col1.text(booking.guest_name)
            inner_col2.text(booking.phone_num)
            inner_col3.text(booking.b_from)
            inner_col4.text(booking.b_to)
            inner_col5.text(booking.table.name)
            release_booking = inner_col6.checkbox("Release", key=booking.table.name)
            if release_booking:
                list_to_delete.append(booking)
        submit = st.button("Submit")
        if submit:
            restaurant.delete_booking(list_to_delete)


def display_status_page():
    """
    displays status of tables page with number of free tables and free seats
    :return: None
    """
    st.title("Status")

    for table in restaurant.tables:
        inner_col1, inner_col2 = st.columns(2)
        inner_col1.text(f"{table.name} - {table.num_of_seats} seats")
        inner_col2.text("Free" if not table.is_reserved else "Booked")

    st.write(f"Number of free tables {restaurant.get_num_of_free_tables()}")
    st.write(f"Number of free seats {restaurant.get_num_of_free_seats()}")


# display application sidebar
page = st.sidebar.radio("Page", ["Booking", "Tables", "Status"])
if page == "Booking":
    display_booking_page()
elif page == "Tables":
    display_tables_page()
elif page == "Status":
    display_status_page()
