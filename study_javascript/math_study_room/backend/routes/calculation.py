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


def create_qa_not_division(arithmetic, questions, numquestions, answers, num_one, num_two):
    for i in range(numquestions):
        question_num = i + 1

        if arithmetic == "addition":
            questions.append(f"問{question_num}） {num_one} + {num_two} =")
            answers.append(num_one + num_two)

        elif arithmetic == "subtraction":
            questions.append(f"問{question_num}） {num_one} - {num_two} = ")
            answers.append(num_one - num_two)

        elif arithmetic == "multiplication":
            questions.append(f"問{question_num}） {num_one} × {num_two} = ")
            answers.append(num_one * num_two)

    return questions, answers


def create_qa_integer_division(questions, numquestions, answers, num_one, num_two):

    for i in range(numquestions):
        question_num = i + 1
        questions.append(f"問{question_num}） {num_one} ÷ {num_two} = ")
        answers.append(num_one // num_two)
        answers.append(num_one % num_two)

    return questions, answers


def create_qa_real_division(questions, numquestions, answers, num_one, num_two):

    for i in range(numquestions):
        question_num = i + 1

        questions.append(f"問{question_num}） {num_one} ÷ {num_two} = ")

        answer_zero = num_one / num_two
        answer = math.floor(answer_zero)  # 小数点以下の切り捨て
        answers.append(answer)
        answers.append(num_one % num_two)

        decimal_places = len(str(answer_zero - answer)) - 2  # 小数点以下の桁数の確認

        if decimal_places > max():
            factor_zero = max()
            if factor_zero == 1:
                factor = "0.1"
            elif factor_zero == 2:
                factor = "0.01"
            elif factor_zero == 3:
                factor = "0.001"

            answer = Decimal(str(answer)).quantize(Decimal(factor), ROUND_HALF_UP)


def create_questions(type, arithmetic, digits, numquestions):
    questions = []
    answers = []

    # 整数問題の値をランダム作成
    if type == "integer":
        num_one, num_two = get_num_integer(digits)

        if arithmetic != "division":
            questions, answers = create_qa_not_division(arithmetic, questions, numquestions, answers, num_one, num_two)

        else:
            questions, answers = create_qa_integer_division(questions, numquestions, answers, num_one, num_two)

    # 実数の値をランダム作成
    elif type == "real":
        num_one, num_two = get_num_real(digits)

        if arithmetic != "division":
            questions, answers = create_qa_not_division(arithmetic, questions, numquestions, answers, num_one, num_two)

        else:
            questions, answers = create_qa_real_division(questions, numquestions, answers, num_one, num_two)

    return questions, answers
