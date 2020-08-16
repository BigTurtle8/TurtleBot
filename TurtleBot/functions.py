num_to_str = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


# Python program to convert a list
# to string using list comprehension
def list_to_str(lst, sep=''):
    # using list comprehension
    new = sep.join([str(elem) for elem in lst])

    return new


def number_comma(num):
    cycle = 0
    new_string = []
    for char in reversed(str(num)):
        cycle += 1
        if cycle == 4:
            cycle = 0
            cycle += 1
            new_string.insert(0, ',')
        new_string.insert(0, char)
    return list_to_str(new_string, '')


# Python Program to Convert seconds
# into hours, minutes and seconds

def convert(seconds):
    minu, sec = divmod(seconds, 60)
    hour, minu = divmod(minu, 60)
    return hour, minu, sec
