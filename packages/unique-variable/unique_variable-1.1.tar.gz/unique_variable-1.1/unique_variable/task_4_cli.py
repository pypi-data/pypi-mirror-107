from collections import Counter
from functools import lru_cache
import argparse


@lru_cache()
def count_letter(word):

    my_counter = Counter(word)
    once_symbol = 0

    for character, count in my_counter.items():
        if count == 1 and character != ' ':
            once_symbol += 1
    return once_symbol


def count_letter_in_file(file):
    try:
        text = file.read()
    except IOError:
        print("Can't read the file")
        return
    return count_letter(text)


def run_function(args):

    if args.file:
        return count_letter_in_file(args.file)
    return count_letter(args.word)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--word', help='Enter the string')
    parser.add_argument('--file', type=argparse.FileType('r'))

    arguments = parser.parse_args()
    run_function(arguments)
