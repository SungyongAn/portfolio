import random
from decimal import ROUND_HALF_UP, Decimal


# 整数問題の値をランダム作成
def get_num_integer(digits):
    start = 10**(digits - 1)
    end = (10**digits) - 1

    num_one = random.randint(start, end)
    num_two = random.randint(start, end)

    return num_one, num_two


def get_num_real(digits):
    start = 10**(digits - 1)
    end = (10**digits) - 1
    print(start, end)

    num_one_zero = random.randint(start, end)
    num_two_zero = random.randint(start, end)
    print(num_one_zero, num_two_zero)
    print(10 ** digits)

    num_one = num_one_zero / (10 ** digits)
    num_two = num_two_zero / (10 ** digits)

    return num_one, num_two


def create_questions(type, arithmetic, digits, numquestions):
    questions = []
    answers = []

    for i in range(numquestions):
        question_num = i + 1

        # 整数問題の値をランダム作成
        if type == "integer":
            num_one, num_two = get_num_integer(digits)

        # 実数の値をランダム作成
        elif type == "real":
            num_one, num_two = get_num_integer(digits)

        # 四則演算
        if arithmetic == "addition":
            questions.append(f"問{question_num} {num_one} + {num_two} =")
            answers.append(num_one + num_two)

        elif arithmetic == "subtraction":
            questions.append(f"問{question_num} {num_one} - {num_two} = ")
            answers.append(num_one - num_two)

        elif arithmetic == "multiplication":
            questions.append(f"問{question_num} {num_one} × {num_two} = ")
            answers.append(num_one * num_two)

        elif arithmetic == "division":
            questions.append(f"問{question_num} {num_one} ÷ {num_two} = ")

            if num_one % num_two == 0:
                answers.append(num_one // num_two)

            # elif num_one % num_two != 0:
                # answer.append(num_one // num_two)
                # answer.append(num_one % num_two)
                # print(answer)

    return questions, answers
