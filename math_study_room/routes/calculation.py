import random
import math
from decimal import ROUND_HALF_UP, Decimal


# 整数)出題される数字の最小値、最大値を作成
def get_output_range(num_range):
    output_range = []
    for i in range(len(num_range)):
        if num_range[i] == 1:
            output_range.append([1, 9])
        elif num_range[i] == 2:
            output_range.append([10, 99])
        elif num_range[i] == 3:
            output_range.append([100, 999])
    return output_range


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


# 足し算
def addition(num_range, identification_code):
    if identification_code == 1: # 整数
        output_range = get_output_range(num_range)
        question_list = [random.randint(output_range[i][0], output_range[i][1]) for i in range(2)]
        answer = sum(question_list)

    elif identification_code == 2: # 実数
        output_range = get_range_real_numbers(num_range)

        question_list_zero = [random.randint(output_range[i][0], output_range[i][1]) for i in range(2)]

        idenominator = [10 ** num_range[i] for i in range(len(num_range))]

        question_list = [question_list_zero[i] / idenominator[i] for i in range(len(num_range))]

        answer_zero = 0
        for i in range(len(question_list_zero)):
            if num_range[i] < max(num_range):
                increase_num_digits = 10 ** (max(num_range) - num_range[i])
                answer_zero += question_list_zero[i] * increase_num_digits
            else:
                answer_zero += question_list_zero[i]

        answer = answer_zero / max(idenominator)

    return question_list, answer


# 引き算
def subtract(num_range, identification_code):
    if identification_code == 1: # 整数
        output_range = get_output_range(num_range)
        question_list = [random.randint(output_range[i][0], output_range[i][1]) for i in range(2)]
        answer = 0
        for i in range(2):
            if i == 0:
                answer = question_list[i]
            else:
                answer -= question_list[i]

    elif identification_code == 2: # 実数
        output_range = get_range_real_numbers(num_range)

        question_list_zero = [random.randint(output_range[i][0], output_range[i][1]) for i in range(2)]

        idenominator = [10 ** num_range[i] for i in range(len(num_range))]

        question_list = [question_list_zero[i] / idenominator[i] for i in range(len(num_range))]

        answer_zero = 0
        for i in range(len(question_list_zero)):
            if i == 0:
                if num_range[i] < max(num_range):
                    increase_num_digits = 10 ** (max(num_range) - num_range[i])
                    answer_zero += question_list_zero[i] * increase_num_digits
                else:
                    answer_zero += question_list_zero[i]
            else:
                if num_range[i] < max(num_range):
                    increase_num_digits = 10 ** (max(num_range) - num_range[i])
                    answer_zero -= question_list_zero[i] * increase_num_digits
                else:
                    answer_zero -= question_list_zero[i]

        answer = answer_zero / max(idenominator)
    return question_list, answer


# 掛け算
def multiply(num_range, identification_code):
    if identification_code == 1: # 整数
        output_range = get_output_range(num_range)
        question_list = [random.randint(output_range[i][0], output_range[i][1]) for i in range(2)]
        answer = question_list[0] * question_list[1]

    elif identification_code == 2: # 実数
        output_range = get_range_real_numbers(num_range)
        question_list_zero = [random.randint(output_range[0], output_range[1]) for _ in range(2)]
        idenominator = 10 ** num_range
        question_list = [question_list_zero[0] / idenominator, question_list_zero[1] / idenominator]
        answer = question_list_zero[0] * question_list_zero[1] / (idenominator * idenominator)
    return question_list, answer


# 割り算(余り、分数表記)
def divide_residue(num_range):
    output_range = get_output_range(num_range)
    question_list = []
    for i in range(len(output_range)):
        question_list.append(random.randint(output_range[i][0], output_range[i][1]))
    answer = question_list[0] // question_list[1]
    residue = question_list[0] % question_list[1]
    return question_list, answer, residue


# 割り算)実数
def divide(num_range):
    output_range = get_range_real_numbers(num_range)
    question_list_zero = [random.randint(output_range[0], output_range[1]) for _ in range(2)]
    idenominator = 10 ** num_range
    question_list = [question_list_zero[0] / idenominator, question_list_zero[1] / idenominator]
    answer_zero = str(question_list_zero[0] / question_list_zero[1])
    answer = Decimal(str(answer_zero)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
    return question_list, answer
