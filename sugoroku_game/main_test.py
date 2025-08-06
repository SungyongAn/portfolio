import random

# 対象のコマを動かす
def move_the_target_piece(target_position, dice_roll):
    target_position += dice_roll
    return target_position


# ゴール条件を満たしているかの判定
def check_goal_condition(goal_condition, tatget_position):
    if goal_condition == False:
        tatget_position = 1
    else:
        tatget_position = "Goal"
    return tatget_position


def create_sugoroku_board():
    math_dict = {4: ["A", "B"], 5: ["A", "B"], 6: ["A", "B"]}
    board= [1, 2, 3, math_dict, 7, 8, 9, 10]
    
    
    
    road_to_pass = []
    j = 0
    for i in range(10):
        if 2 < i < 6:
            road_to_pass.append(str(list(math_dict)[j]) + direct_select)
            j += 1
        elif 6 <= i:
            indx = i - (len(math_dict) - 1)
            print(i, indx)
            road_to_pass.append(board[indx])
        else:
            road_to_pass.append(board[i])
            
    return board, road_to_pass


if __name__ == "__main__":
    target_position = 0
    bord, road_to_pass = create_sugoroku_board()
    
    while target_position < bord[-1]:
        input("Enterを押すとダイスを振ります")
        # ダイスを振る
        dice_roll = random.randint(1, 6)
        target_position += dice_roll
        if target_position > 3:
            # ルート選択の入力
            direct_select = input("A or B")
