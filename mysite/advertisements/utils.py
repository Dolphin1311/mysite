import random
import string
import os
import hashlib


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    """Create random string only with lowercase letters and digits with selected size"""
    return "".join(random.choice(chars) for _ in range(size))


def path_and_rename(instance, filename_base: str, deep_level=3):
    """
    Create whole filepath string to the storing image based on changed filename
    :param instance: instance of class
    :param filename_base: filename before editing
    :param deep_level: number of levels of nesting of folders
    :return: string of the whole path to the storing image
    """
    file_name, file_extension = os.path.splitext(filename_base)
    path = "images/"
    count_letters = 2
    filename = get_md5_file(file_name)

    for i in range(deep_level):
        path += filename[count_letters - 2 : count_letters] + "/"
        count_letters += 2

    filename += file_extension
    return os.path.join(path, filename)


def get_md5_file(filename):
    """
    Create md5 hash string based on filename
    :param filename: filename
    :return: string of md5 hash
    """
    result = hashlib.md5(filename.encode()).hexdigest()

    return result
