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
    
    question_list_two = [Decimal(question_list_zero[i]) for i in range(len(question_list_zero))]

    idenominator = [10 ** num_range[i] for i in range(len(num_range))]

    question_list = [question_list_two[i] / idenominator[i] for i in range(len(num_range))]

    answer = question_list[0] / question_list[1]

    num_decimal_places = math.floor(answer) #小数点以下の切り捨て
    
    digits = len(str(answer - num_decimal_places)) - 2 # 小数点以下の桁数の確認

    if digits > max(num_range):
        factor_zero = max(num_range)
        if factor_zero == 1:
            factor = "0.1"
        elif factor_zero == 2:
            factor = "0.01"
        elif factor_zero == 3:
            factor = "0.001"
        
        answer = Decimal(str(answer)).quantize(Decimal(factor), ROUND_HALF_UP)

    # answer = 0
    # for i in range(len(num_range)):
    #     if len(str(question_list[i])) < num_range[i] + 2:
    #         answer += question_list[i] * (num_range[i] + 2)
    #     else:
    #         answer += question_list[i]

    # if len(str(answer)) > sum(num_range) + 1:
    #     factor = 10 ** sum(num_range)
    #     answer = math.floor(answer * factor) / factor

    return question_list, answer


# def truncate(number, digits):
#     factor = 10 ** digits
#     return math.floor(number * factor) / factor

num_range = [2, 1]
question_list, answer = addition(num_range)

print(answer)

print(question_list, answer)
print(answer)

# question_list, answer, residue = divide_residue(num_range)
# print(question_list, answer, residue)
