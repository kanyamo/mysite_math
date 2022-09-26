def strtobool(string):
    string = string.lower()
    if string in ('true', 't', 'yes', 'y', '1', 'on'):
        return True
    else:
        return False
