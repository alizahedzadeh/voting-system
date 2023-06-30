from Manager import Manager
from Student import Student
from Parents import Parents

from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *


def register_manager():
    obj = Manager()
    obj.register()
    print("\n")
    Screen().input('Press [Enter] to continue')


def Show_All_Polls(obj):
    obj.show_all_polls()
    print("\n")
    Screen().input('Press [Enter] to continue')


def Create_Poll(obj):
    obj.create_poll()
    print("\n")
    Screen.input('Press [Enter] to continue')


def Show_Polls_Result(obj):
    obj.show_polls_result()
    print("\n")
    Screen.input('Press [Enter] to continue')


def Show_Students_Poll(obj):
    obj.polls_for_students()
    print("\n")
    Screen.input('Press [Enter] to continue')


def Answer_Poll_Students(obj):
    obj.answer_poll()
    print("\n")
    Screen.input('Press [Enter] to continue')


def Answer_Poll_Parents(obj):
    obj.answer_poll()
    print("\n")
    Screen.input('Press [Enter] to continue')


def Show_Parents_Poll(obj):
    obj.polls_for_parents()
    print("\n")
    Screen.input('Press [Enter] to continue')


def login_manager():
    obj = Manager()
    obj.login()
    print("\n")
    Screen().input('Press [Enter] to continue')

    if obj.logged_in:
        submenu_formatter = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.ASCII_BORDER)
        submenu = ConsoleMenu("Manager Pannel", "This is for Managers",
                              formatter=submenu_formatter,
                              exit_option_text="Logout")

        function_item_1 = FunctionItem("Create Poll", Create_Poll, args=[obj])
        function_item_2 = FunctionItem("Show All Polls", Show_All_Polls, args=[obj])
        function_item_3 = FunctionItem("Show Polls Results", Show_Polls_Result, args=[obj])

        submenu.append_item(function_item_1)
        submenu.append_item(function_item_2)
        submenu.append_item(function_item_3)

        submenu.start()
        submenu.join()


def login_student():
    obj = Student()
    obj.login()
    print("\n")
    Screen().input('Press [Enter] to continue')

    if obj.logged_in:
        submenu_formatter = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.ASCII_BORDER)
        submenu = ConsoleMenu("Student Pannel", "This is for Students",
                              formatter=submenu_formatter,
                              exit_option_text="Logout",)

        function_item_1 = FunctionItem("Answer Poll", Answer_Poll_Students, args=[obj])
        function_item_2 = FunctionItem("Show Students Poll", Show_Students_Poll, args=[obj])

        submenu.append_item(function_item_1)
        submenu.append_item(function_item_2)

        submenu.start()
        submenu.join()


def login_parents():
    obj = Parents()
    obj.login()
    print("\n")
    Screen().input('Press [Enter] to continue')

    if obj.logged_in:
        submenu_formatter = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.ASCII_BORDER)
        submenu = ConsoleMenu("Student Pannel", "This is for Students",
                              formatter=submenu_formatter,
                              exit_option_text="Logout")

        function_item_1 = FunctionItem("Answer Poll", Answer_Poll_Parents, args=[obj])
        function_item_2 = FunctionItem("Show Parents Poll", Show_Parents_Poll, args=[obj])

        submenu.append_item(function_item_1)
        submenu.append_item(function_item_2)

        submenu.start()
        submenu.join()


def main():
    # Change some menu formatting
    menu_format = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.HEAVY_BORDER) \
        .set_prompt("SELECT>") \
        .set_title_align('center') \
        .set_subtitle_align('center') \
        .set_left_margin(4) \
        .set_right_margin(4) \
        .show_header_bottom_border(True)

    menu = ConsoleMenu("Vote System Menu", "This is the Root Menu", formatter=menu_format)
    submenu_formatter = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.ASCII_BORDER)

    register_item = FunctionItem("Register (just for Managers)", register_manager)

    # Create a second submenu, but this time use a standard ConsoleMenu instance, and use the submenu_formatter.
    submenu_2 = ConsoleMenu("Login Menu", "This is for users login", formatter=submenu_formatter)

    function_item_1 = FunctionItem("Manager", login_manager)
    function_item_2 = FunctionItem("Student", login_student)
    function_item_3 = FunctionItem("Parent", login_parents)

    submenu_2.append_item(function_item_1)
    submenu_2.append_item(function_item_2)
    submenu_2.append_item(function_item_3)

    # Menu item for opening submenu 2
    submenu_item_2 = SubmenuItem("Login", submenu=submenu_2)
    submenu_item_2.set_menu(menu)

    # Add all the items to the root menu
    menu.append_item(register_item)
    menu.append_item(submenu_item_2)

    # Show the menu
    menu.start()
    menu.join()


if __name__ == "__main__":
    main()
