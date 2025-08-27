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
    answer = []

    for _ in range(numquestions):

        # 整数問題の値をランダム作成
        if type == "integer":
            num_one, num_two = get_num_integer(digits)

        # 実数の値をランダム作成
        elif type == "real":
            num_one, num_two = get_num_integer(digits)

        # 四則演算
        if arithmetic == "addition":
            question = f"{num_one} + {num_two} ="
            answer.append(num_one + num_two)

        elif arithmetic == "subtraction":
            question = f"{num_one} - {num_two} = "
            answer.append(num_one - num_two)

        elif arithmetic == "multiplication":
            question = f"{num_one} × {num_two} = "
            answer.append(num_one * num_two)

        elif arithmetic == "division":
            question = f"{num_one} ÷ {num_two} = "

            if num_one % num_two == 0:
                answer.append(num_one // num_two)

            elif num_one % num_two != 0:
                answer = []
                answer.append(num_one // num_two)
                answer.append(num_one % num_two)
                print(answer)

        questions.append({"question": question, "answer": answer})

    return questions


if __name__ == "__main__":
    type = "real"
    arithmetic = "division"
    digits = 2
    numquestions = 2

    questions = create_questions(type, arithmetic, digits, numquestions)
    print(questions)

