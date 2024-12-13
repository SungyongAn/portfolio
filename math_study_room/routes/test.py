import random
from decimal import ROUND_HALF_UP, Decimal


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


def divide(num_range):
    output_range = get_range_real_numbers(num_range)
    question_list_zero = [random.randint(output_range[0], output_range[1]) for _ in range(2)]
    idenominator = 10 ** num_range
    question_list = [question_list_zero[0] / idenominator, question_list_zero[1] / idenominator]
    answer_zero = str(question_list_zero[0] / question_list_zero[1])
    print(answer_zero) # noqa: T201
    answer = Decimal(str(answer_zero)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    print(answer) # noqa: T201
    return question_list, answer

divide(2)
