import random
import math
from decimal import ROUND_HALF_UP, Decimal


# 実数用)指定した桁数の最小値、最大値を作成
def get_range_real_numbers(num_range):
    output_range = []
    for i in range(len(num_range)):
        if num_range[i] == 1:
            output_range.append([1, 19])
        elif num_range[i] == 2:
            output_range.append([1, 199])
        elif num_range[i] == 3:
            output_range.append([1, 1999])
    return output_range


def addition(num_range):
    output_range = get_range_real_numbers(num_range)

    question_list_zero = [random.randint(output_range[i][0], output_range[i][1]) for i in range(2)]

    idenominator = [10 ** num_range[i] for i in range(len(num_range))]

    question_list_tow = [question_list_zero[i] / idenominator[i] for i in range(len(num_range))]
    
    question_list = ["{:.num_range[i]f}".format for i in range(len(question_list_tow))]

    answer_zero = 0
    for i in range(len(question_list_zero)):
        if num_range[i] < max(num_range):
            increase_num_digits = 10 ** (max(num_range) - num_range[i])
            answer_zero += question_list_zero[i] * increase_num_digits
        else:
            answer_zero += question_list_zero[i]

    answer = answer_zero / max(idenominator)

    return question_list, answer


# def truncate(number, digits):
#     factor = 10 ** digits
#     return math.floor(number * factor) / factor

num_range = [3, 3]
question_list, answer = addition(num_range)

print(question_list, answer)
print(answer)
a = format(question_list[0], f'.{num_range[0]}f')
b = format(question_list[1], f'.{num_range[1]}f')
print(a)
print(b)

# if len(str(question_list[0])) != num_range[0] + 2:
#     question_list[0] = list(str(question_list[0])).extend["0"]

# if len(str(question_list[1])) != num_range[1] + 2:
#     question_list[1] = list(str(question_list[1])).extend["0"]
# question_list, answer, residue = divide_residue(num_range)
# print(question_list, answer, residue)
