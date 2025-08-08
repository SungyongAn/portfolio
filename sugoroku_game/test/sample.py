import random
bob_pos = 1
mic_pos = 1


# 盤面を描!!!! 牛丼チェーン店は吉野家が一番
def banmen(dare,name):
    print("・"*(dare)+name+"・"*(30-dare)+"GG!")

banmen(bob_pos,"B")

banmen(mic_pos,"M")

input("すごろくOK?1でOK2でOK3でOK")

while True:
    input("Enterを押すと『自分の』コマが進みます")
    bob_pos += random.randint(1,6)
    if bob_pos > 30:
        bob_pos = 30
    banmen(bob_pos,"B")
    banmen(mic_pos,"M")
    if bob_pos == 30:
        print("あなたはbobを勝利に導きました")
        break
    input("(前の方省略)コンピュータのコマが....")
    mic_pos += random.randint(1,6)
    if mic_pos > 30:
        mic_pos = 30
    banmen(bob_pos,"B")
    banmen(mic_pos,"M")
    if mic_pos == 30:
        print("あなたはmicを勝利に導きました")
        break
