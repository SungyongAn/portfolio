import random


# 整数）出題される数字の最小値、最大値を作成
def get_output_range(num_range):
    output_range = []
    for i in range(2):
        output_range_zero = []
        if i == 0:
            for j in range(num_range):
                if j == 0:
                    output_range_zero.append(1)
                else:
                    output_range_zero.append(0)
        else:
            for j in range(num_range):
                output_range_zero.append(9)
        str_list = map(str, output_range_zero)
        output_range.append(int("".join(str_list)))
    return output_range


def get_range_real_numbers(num_range):
    output_range = []
    for i in range(2):
        if i == 0:
            output_range.append(1)
        else:
            output_range_zero = []
            for j in range(num_range + 1):
                if j == 0:
                    output_range_zero.append(1)
                else:
                    output_range_zero.append(9)
            str_list = map(str, output_range_zero)
            output_range.append(int("".join(str_list)))
    return output_range


# 掛け算
def multiply(num_times, num_range, type):
    if type == 1:
        output_range = get_output_range(num_range)
        question_list = [random.randint(output_range[0], output_range[1]) for _ in range(num_times)]
        answer = question_list[0] * question_list[1]
    elif type == 2:
        output_range = get_range_real_numbers(num_range)
        question_list_zero = [random.randint(output_range[0], output_range[1]) for _ in range(num_times)]
        idenominator = 10 ** (num_range)
        question_list = [question_list_zero[0] / idenominator, question_list_zero[1] / idenominator]
        answer = question_list_zero[0] * question_list_zero[1] / (idenominator * idenominator)
    return question_list, answer

multiply(2, 3, 2)
