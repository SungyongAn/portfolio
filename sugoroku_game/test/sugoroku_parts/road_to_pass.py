

def create_road_to_pass():
    math_dict = {4: ["A", "B"], 5: ["A", "B"], 6: ["A", "B"]}
    board = [1, 2, 3, math_dict, 7, 8, 9, 10]

    # ルート選択の入力
    direct_select = input("A or B")

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
