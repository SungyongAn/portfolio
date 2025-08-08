import random

# 全10マスで3マス目で必ず止まりルート選択、選択したルートを通って7マス目から合流してゴールを目指す。

# 選択可能ルートの一覧
math_dict = {4: ["A", "B"], 5: ["A", "B"], 6: ["A", "B"]}
# すごろくの全体図
board = [1, 2, 3, math_dict, 7, 8, 9, 10]

# プレイヤーの位置
target_position = 0
# 分岐ルート選択判定
branch_flag = False
# 選択したルート情報の保管
direct_select = ""
# プレイヤーが止まったマスの情報
road_to_pass = []

# すごろくの全体動作
while target_position < board[-1]:
    input("Enterを押すとダイスを振ります")
    # ダイスを振る
    dice_roll = random.randint(1, 2)
    print("ダイスの目は" + str(dice_roll) + "です。")
    # ダイスを振った後のプレイヤーの位置情報
    target_position += dice_roll
    # 3マス目
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
