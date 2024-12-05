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


# 実数用）指定した桁数の最小値、最大値を作成
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


# 足し算
def addition(num_range, identification_code):
    if identification_code == 1: # 整数
        output_range = get_output_range(num_range)
        question_list = [random.randint(output_range[0], output_range[1]) for _ in range(2)]
        answer = sum(question_list)
    elif identification_code == 2: # 実数
        output_range = get_range_real_numbers(num_range)
        
        question_list_zero = [random.randint(output_range[0], output_range[1]) for _ in range(2)]
        idenominator = 10 ** num_range
        question_list = [question_list_zero[0] / idenominator, question_list_zero[1] / idenominator]
        answer = sum(question_list_zero) / idenominator
    return question_list, answer


# 引き算
def subtract(num_range, identification_code):
    if identification_code == 1:
        output_range = get_output_range(num_range)
        question_list = [random.randint(output_range[0], output_range[1]) for _ in range(2)]
        answer = 0
        for i in range(2):
            if i == 0:
                answer = question_list[i]
            else:
                answer -= question_list[i]
    elif identification_code == 2:
        output_range = get_range_real_numbers(num_range)
        question_list_zero = [random.randint(output_range[0], output_range[1]) for _ in range(2)]
        idenominator = 10 ** num_range
        question_list = [question_list_zero[0] / idenominator, question_list_zero[1] / idenominator]
        for i in range(2):
                if i == 0:
                    answer_zero = question_list_zero[i]
                else:
                    answer_zero -= question_list_zero[i]
        answer = answer_zero / idenominator
    return question_list, answer


# 掛け算
def multiply(num_range, identification_code):
    if identification_code == 1:
        output_range = get_output_range(num_range)
        question_list = [random.randint(output_range[0], output_range[1]) for _ in range(2)]
        answer = question_list[0] * question_list[1]
    elif identification_code == 2:
        output_range = get_range_real_numbers(num_range)
        question_list_zero = [random.randint(output_range[0], output_range[1]) for _ in range(2)]
        idenominator = 10 ** num_range
        question_list = [question_list_zero[0] / idenominator, question_list_zero[1] / idenominator]
        answer = question_list_zero[0] * question_list_zero[1] / (idenominator * idenominator)
    return question_list, answer


# 割り算で使用する最大値
def get_limit(num_range):
    limit_zero = []
    for _ in range(num_range):
        limit_zero.append(9)

    str_list = map(str, limit_zero)
    limit = (int("".join(str_list)))
    return limit


# 割り算（実数）
def divide(num_range):
    limit = get_limit(num_range)
    question_list = []
    for i in range(2):
        if i == 0:
            question_list.append(random.randint(limit//2, limit))
        else:
            question_list.append(random.randint(2, limit//2))
    answer = question_list[0] / question_list[1]
    return question_list, answer


# 割り算（余り表記）
def divide_residue(num_range):
    limit = get_limit(num_range)
    question_list = []
    for i in range(2):
        if i == 0:
            question_list.append(random.randint(limit//2, limit))
        else:
            question_list.append(random.randint(2, limit//2))
    answer = question_list[0] // question_list[1]
    residue = question_list[0] % question_list[1]
    return question_list, answer, residue
