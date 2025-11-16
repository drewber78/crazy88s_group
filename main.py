"""Project entrypoint.

Running `python main.py` will launch the interactive UI in `user_menu.py`.
"""

from user_menu import welcome_menu, main_menu


def main():
    """Run the welcome screen then the main menu loop from `user_menu.py`."""
    welcome_menu()

    menu_call = True
    while menu_call is not False:
        menu_call = main_menu()


if __name__ == '__main__':
    main()
