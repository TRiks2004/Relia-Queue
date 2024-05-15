import math
import random

def round_value(value, decimals=4):
    return round(value, decimals)

def interval_between_apps(alpha, random_value):
    return round_value(-1 / alpha * math.log(random_value))

def max_row(lst):
    return max(lst)

def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    transposed_matrix = []

    for col in range(cols):
        new_row = []
        for row in range(rows):
            new_row.append(matrix[row][col])
        transposed_matrix.append(new_row)

    return transposed_matrix

def max_columns(lst):
    return [max_row(row) for row in transpose(lst)]

def generate_random_number():
    number = round_value(random.uniform(0, 1))
    if number == 0:
        return generate_random_number()
    else:
        return number

def sum_expected_values(lst):
    return sum([answer.expected_value for answer in lst])
