
def check(app, input_str):
    """ Parse the input string and check the item given in it by ID.

        Example:
        (input_str = ":c 3") will check the item with ID 3.

        Keyword arguments:
        app -- The current app object that this was called from (self)
        input_str -- The input string given by the user. """
    input = input_str.split()
    if len(input) > 1:
        itemid = input[1]
        try:
            app.list.get_item(int(itemid)).check(app.cursor)
        except IndexError:
            app.error("Please enter a valid item id")
            return
        app.conn.commit()

def delete(app, input_str):
    """ Parse the input string and delete the item given in it by ID.

        Example:
        (input_str = ":c 3") will check the item with ID 3.

        Keyword arguments:
        app -- The current app object that this was called from (self)
        input_str -- The input string given by the user. """
    input = input_str.split()
    if len(input) > 1:
        itemid = input[1]
        try:
            app.list.remove_item(int(itemid), app.cursor)
        except IndexError:
            app.error("Please enter a valid item id")
            return
        app.conn.commit()

def clear(app, input_str):
    """ Clear the current list and database, waiting for the user
        to give either a "yes" or "no" input.

        Keyword arguments:
        app -- The current app object that this was called from (self)
        input_str -- Included just to make args same as other commands"""

    app.win.move(1, 0)
    message = "Are you sure you want to delete all items? "
    app.win.addstr(message)

    input = app.win.getstr().lower()
    while input != "yes":
        if input == "no":
            return
        # user didn't input a valid option (neither "yes" nor "no")
        app.win.move(2, 0)
        app.win.addstr("Please enter yes or no")
        # move cursor to end of line
        app.win.move(1, len(message))

        input = app.win.getstr().lower()

    app.list.clear(app.cursor)

