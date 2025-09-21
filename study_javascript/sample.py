import random
import math
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

    num_one_zero = random.randint(start, end)
    num_two_zero = random.randint(start, end)

    num_one = num_one_zero / (10 ** digits)
    num_two = num_two_zero / (10 ** digits)

    return num_one, num_two


def create_qa_integer_not_division(num_one, num_two, arithmetic, questions, answers, question_num):

    if arithmetic == "addition":
        answer = num_one + num_two
        questions.append(f"問{question_num}） {num_one} + {num_two} =")
        answers.append(num_one + num_two)

    elif arithmetic == "subtraction":
        answer = num_one - num_two
        questions.append(f"問{question_num}） {num_one} - {num_two} = ")
        answers.append(answer)

    elif arithmetic == "multiplication":
        answer = num_one * num_two
        questions.append(f"問{question_num}） {num_one} × {num_two} = ")
        answers.append(answer)

    return questions, answers


def create_qa_real_not_division(num_one, num_two, digits, arithmetic, questions, answers, question_num):

    num_one_zero = num_one / 10 ** digits
    num_two_zero = num_two / 10 ** digits

    if arithmetic == "addition":
        answer = (num_one + num_two) / 10 ** digits
        questions.append(f"問{question_num}） {num_one_zero} + {num_two_zero} =")
        answers.append(answer)

    elif arithmetic == "subtraction":
        answer = (num_one - num_two) / 10 ** digits
        questions.append(f"問{question_num}） {num_one_zero} - {num_two_zero} = ")
        answers.append(answer)

    elif arithmetic == "multiplication":
        answer = (num_one * num_two) / ((10 ** digits) * (10 ** digits))
        questions.append(f"問{question_num}） {num_one_zero} × {num_two_zero} = ")
        answers.append(answer)

    return questions, answers


def create_qa_integer_division(question_num, questions, answers, num_one, num_two):

    questions.append(f"問{question_num}） {num_one} ÷ {num_two} = ")
    answers.append(num_one // num_two)
    answers.append(num_one % num_two)

    return questions, answers


def create_qa_real_division(question_num, questions, answers, num_one, num_two):

    questions.append(f"問{question_num}） {num_one} ÷ {num_two} = ")

    answer_zero = num_one / num_two
    answer = math.floor(answer_zero)  # 小数点以下の切り捨て
    answers.append(answer)

    if num_one % num_two == 0:
        answers.append(0)
    else:
        decimal_places = len(str(answer_zero - answer)) - 2  # 小数点以下の桁数の確認

        if decimal_places > max():
            factor_zero = max()
            if factor_zero == 1:
                factor = "0.1"
            elif factor_zero == 2:
                factor = "0.01"
            elif factor_zero == 3:
                factor = "0.001"

            answer_zero = Decimal(str(answer)).quantize(Decimal(factor), ROUND_HALF_UP)
            answers.append(answer_zero)

    return questions, answers


def create_questions(type, arithmetic, digits, numquestions):
    questions = []
    answers = []

    # 整数問題の値をランダム作成
    if type == "integer":
        for i in range(numquestions):
            question_num = i + 1
            num_one, num_two = get_num_integer(digits)

            if arithmetic != "division":
                questions, answers = create_qa_integer_not_division(num_one, num_two, arithmetic, questions, answers, question_num)

            else:
                questions, answers = create_qa_integer_division(questions, numquestions, answers, num_one, num_two)

    # 実数の値をランダム作成
    elif type == "real":
        for i in range(numquestions):
            question_num = i + 1
            # num_one, num_two = get_num_real(digits)
            num_one, num_two = get_num_integer(digits)

            if arithmetic != "division":
                questions, answers = create_qa_real_not_division(num_one, num_two, digits, arithmetic, questions, answers, question_num)

            else:
                questions, answers = create_qa_real_division(question_num, questions, answers, num_one, num_two)

    return questions, answers


if __name__ == "__main__":
    type = "real"
    arithmetic = "multiplication"
    digits = 1
    numquestions = 2

    questions= create_questions(type, arithmetic, digits, numquestions)
    print(questions)
