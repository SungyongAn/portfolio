import random


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
        str_list = map(str,output_range_zero)
        output_range.append(int("".join(str_list)))
    return output_range


def multiply(num_range, num_times):
    output_range = get_output_range(num_range)
    question_list = [random.randint(output_range[0], output_range[1]) for _ in range(num_times)]
    answer = question_list[0] * question_list[1]
    print(question_list)
    return question_list, answer

num_range = 3
num_times = 2
multiply(num_range, num_times)

