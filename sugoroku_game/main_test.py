import random


# ダイスを振る
def roll_the_dice():
    dice_roll = random.randint(1, 6)
    return dice_roll


# 対象のコマを動かす
def move_the_target_piece(target_position, dice_roll):
    target_position += dice_roll
    return target_position


# ゴール条件を満たしているかの判定
def check_goal_condition(goal_condition, tatget_position)
    if goal_condition == False:
        tatget_position = 1
    else:
        tatget_position = "Goal"
    return tatget_position


# 双六のボード上にランダムで効果を配置したボードの作成
def get_effect_positions(effects, available_positions):
    effect_positions = []
    i = 0
    while len(effect_positions) < len(effects):
        effect_positions_zero = random.choice(available_positions)
        if effect_positions_zero + effects[i] < 0:
            continue
        elif effect_positions_zero + effects[i] > 10:
            continue
        else:
            effect_positions.append(effect_positions_zero)
            # 同じ数字が重複されないようにリストから削除
            available_positions.remove(effect_positions_zero)
            i += 1
    return effect_positions


def create_sugoroku_board():
    # 10マスの盤面を初期化（すべて効果なし=0）
    board = [0] * 10

    # 効果リスト
    effects = [-1, +1, -2, +2]

    # マス2-9（インデックス1-8）からランダムに4つ選んで効果を配置
    available_positions = list(range(2, 9)) 
    print(available_positions)

    # 効果がスタートとゴールを超えないようにランダムで配置
    effect_positions = get_effect_positions(effects, available_positions)
    print(effect_positions)

    for i, pos in enumerate(effect_positions):
        board[pos] = effects[i]

    return board

if __name__ == "__main__":
    goal_condition = False

    
    bord = create_sugoroku_board()
    print(bord)
