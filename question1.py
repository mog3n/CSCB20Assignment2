from flask import Flask, render_template
app = Flask(__name__)

def remove_numbers(name):
    """Removes numbers from a string

    Args:
        name (str): A name

    Returns:
        str: A string without numbers

    """
    # Create string to store the new name
    name_without_numbers = ""
    for letter in name:
        # If the letter is NOT a number, then add it to the name
        if letter not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            name_without_numbers += letter
    return name_without_numbers


def update_name(name):
    """Modifies the name to a lower or upper string, or removes numbers

    Args:
        name (str): Any name

    Returns:
        str: The modified string
    """
    # Set name as string
    name = str(name)

    # Remove numbers from name
    name_num_removed = remove_numbers(name)

    # check if any numbers were removed
    if name_num_removed != name:
        return name_num_removed

    # Otherwise, change to lower or upper case
    if name == str.lower(name):
        # name is lowercased. Upper case it
        print("to upper")
        return str.upper(name)
    elif name == str.upper(name):
        # name is uppercased. Lower case it
        print("to lower")
        return str.lower(name)
    else:
        # name is neither
        return name


@app.route('/<name>')
def generateResponse(name):
    """Greets the user by name at /name

    Args:
        name (str): A name

    Returns:
        str: HTML greeting with the updated name

    """
    name = update_name(name)
    return "Welcome, {0}, to my CSCB20 website!".format(name)


if __name__ == '__main__':
    app.run()