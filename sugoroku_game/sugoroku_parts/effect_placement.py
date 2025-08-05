import random


# 双六のボード上にランダムで効果を配置したボードの作成
def get_effect_positions(effects, available_positions):
    effect_positions = []
    i = 0

    while len(effect_positions) < len(effects):
        effect_positions_zero = random.choice(available_positions)
        # 効果によってコマがスタート地点を超えないように確認
        if effect_positions_zero + effects[i] < 0:
            continue
        # 効果によってコマがゴール地点を超えないように確認
        elif effect_positions_zero + effects[i] > 10:
            continue
        else:
            effect_positions.append(effect_positions_zero)
            # 同じ数字が重複されないようにリストから削除
            available_positions.remove(effect_positions_zero)
            i += 1

    return effect_positions
