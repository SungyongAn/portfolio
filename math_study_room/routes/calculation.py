import random


# 出題される数字の最小値、最大値を作成
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


# 足し算
def add(num_times, num_range):
    output_range = get_output_range(num_range)
    question_list = [random.randint(output_range[0], output_range[1]) for _ in range(num_times)]
    answer = sum(question_list)
    return question_list, answer


# 引き算
def subtract(num_range, num_times):
    output_range = get_output_range(num_range)
    question_list = [random.randint(output_range[0], output_range[1]) for _ in range(num_times)]
    answer = 0
    for i in range(num_times):
        if i == 0:
            answer = question_list[i]
        else:
            answer -= question_list[i]
    return question_list, answer


# 割り算で使用する最大値
def get_limit(num_range):
    limit_zero = []
    for _ in range(num_range):
        limit_zero.append(9)

    str_list = map(str, limit_zero)
    limit = (int("".join(str_list)))
    return limit


# 割り算
# def divide(num_range, num_times):
#     limit = get_limit(num_range)
#     question_list = []
#     answer = []
#     for i in range(num_times):
#         if i == 0:
#             question_list.append(random.randint(limit//2, limit))
#         else:
#             question_list.append(random.randint(2, limit//2))

#     if question_list[0] % question_list[1] == 0:
#         answer = question_list[0] // question_list[1]
#     else:
#         answer = str(question_list[0] // question_list[1]) + "と余り" + str(question_list[0] % question_list[1])
#         for _ in range(2):
#             answer.append(question_list[0] // question_list[1])
#     return question_list, answer


def divide(num_range):
    output_range = get_output_range(num_range)
    question_list = []
    question_list.append(random.randint(output_range[0], output_range[1]))
    question_list.append(random.randint(output_range[0], question_list[0]))
    answer = question_list[0] / question_list[1]
    return question_list, answer


# 掛け算
def multiply(num_range, num_times):
    output_range = get_output_range(num_range)
    question_list = [random.randint(output_range[0], output_range[1]) for _ in range(num_times)]
    answer = question_list[0] * question_list[1]
    return question_list, answer
