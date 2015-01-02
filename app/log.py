
f = open('log', 'a')

def log(message):
    """ Log the message to the file with name log """
    f.write(str(message) + '\n')
