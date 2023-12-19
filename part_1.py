from curses.ascii import isdigit
from functools import reduce
from typing import Dict, List, Literal


def add(a, b):
    return a + b


def issymbol(char: str) -> bool:
    return not char.isdigit() and char != "."


NameType = Literal["first", "last", "middle"]

data = open("data.txt", "r")

lines = data.readlines()

line_type: NameType = "first"

valid_numbers = []

for i in range(len(lines)):
    line = lines[i]

    # Some edge cases:
    # - first line - look only at the line below
    # - last line - look only at the line above

    # - scan the line for digits and form a number if there are couple digits in a row
    # - then check if there's a symbol:
    #   - left of the number, right of the number, above the number or below the number
    # - if on beginning of the line - can't look left, if on the end - can't look right

    if i == len(lines) - 1:
        line_type = "last"
    elif i > 0:
        line_type = "middle"

    if line_type != "first":
        print(f"Line above: {lines[i - 1]}")

    if i + 1 >= 100:
        print(f"Line   {i+1}: {line}")
    elif i + 1 >= 10:
        print(f"Line    {i+1}: {line}")
    else:
        print(f"Line     {i+1}: {line}")

    if line_type != "last":
        print(f"Line below: {lines[i + 1]}")

    numbers_in_line: List[int] = []
    # firstly, find the entire number
    j = 0
    index_number: Dict[int, int] = {}

    while j in range(len(line)):
        char = line[j]
        # print(f"Char: {char}")

        valid = False
        number_concat = ""
        if char.isdigit():
            number_concat = number_concat + char

            k = j + 1
            next_check = j + 3
            while True:
                if k >= len(line):
                    break

                if k == next_check and not valid:
                    next_check = k + 3

                next_char = line[k]
                if next_char.isdigit():
                    number_concat = number_concat + next_char
                    k = k + 1
                else:
                    j = k
                    break

            # check neighbouring symbols here:
            begin_index = j - len(number_concat)
            # print(f"Number {number_concat} begins at {begin_index} and ends at {j - 1}")

            iter_start = begin_index
            iter_end = j

            if begin_index > 0 and j < len(line) - 1:
                iter_start = begin_index - 1
                iter_end = j
            elif j == len(line) - 1:
                iter_start = begin_index - 1
                iter_end = j - 1
            # print(f"Number {number_concat} begins at {begin_index} and ends at {j - 1}")
            # print(iter_start, iter_end)
            for it in range(iter_start, iter_end + 1):
                # print(f"it={it}")
                if issymbol(line[iter_start]) or issymbol(line[iter_end]):
                    valid = True
                    break

                if i == 0:
                    # print(f"symbol={lines[i+1][it]}")
                    if issymbol(lines[i + 1][it]):
                        valid = True
                        break
                elif i == len(lines) - 1:
                    if issymbol(lines[i - 1][it]):
                        valid = True
                        break
                else:
                    if issymbol(lines[i - 1][it]):
                        valid = True
                        break
                    if issymbol(lines[i + 1][it]):
                        valid = True
                        break

            # print(f"is {number_concat} valid? {valid}")

            if valid:
                numbers_in_line.append(int(number_concat))
                valid_numbers.append(int(number_concat))

        if j <= len(line) - 1:
            j = j + 1

    print(f"Numbers for line: {numbers_in_line}\n")

final_sum = reduce(add, valid_numbers)
print(f"Final sum={final_sum}")

data.close()
