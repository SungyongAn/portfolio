import random

math_dict = {4: ["A", "B"], 5: ["A", "B"], 6: ["A", "B"]}
board = [1, 2, 3, math_dict, 7, 8, 9, 10]
target_position = 0
branch_flag = False
road_to_pass = []
direct_select = ""
while target_position < board[-1]:
    input("Enterを押すとダイスを振ります")
    # ダイスを振る
    dice_roll = random.randint(1, 2)
    print("ダイスの目は" + str(dice_roll) + "です。")
    target_position += dice_roll
    if 3 <= target_position and branch_flag == False:
        target_position = 3
        # ルート選択の入力
        while True:
            direct_select = input("A or B: ")
            if direct_select == "A" or direct_select == "B":
                break
            else:
                print("AかBを入力してください。")
        branch_flag = True
        road_to_pass.append(target_position)
    elif target_position < 7:
        road_to_pass.append(str(target_position) + direct_select)
    elif target_position >= board[-1]:
        print("Goal")
        print(road_to_pass)
    else:
        road_to_pass.append(target_position)
