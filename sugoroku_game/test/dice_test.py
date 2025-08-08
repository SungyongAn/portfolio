import streamlit as st
import time
import random


def load_dice_image(number):
    # サイコロ画像のパスを構築
    dice_img = f"ImageMaterial/saikoro-illust{number}.png"
    return dice_img


# サイコロを出目の決定
def backend_dice_roll():
    return random.randint(1, 6)


st.title("サイコロアニメーションテスト")

# セッション状態の初期化
if 'dice_result' not in st.session_state:
    st.session_state.dice_result = None
if 'is_rolling' not in st.session_state:
    st.session_state.is_rolling = False

# サイコロを振るボタン
if st.button("🎲 サイコロを振る", disabled=st.session_state.is_rolling):
    # バックエンドで結果を決定
    final_result = backend_dice_roll()
    st.session_state.dice_result = final_result
    st.session_state.is_rolling = True
    
    # プレースホルダーを作成
    dice_placeholder = st.empty()
    status_placeholder = st.empty()
    
    status_placeholder.write("🎲 サイコロを振っています...")
    
    # 2秒間サイコロが転がっているような表示を出力する
    animation_duration = 2.0  # 秒
    frames_per_second = 10
    total_frames = int(animation_duration * frames_per_second)
    
    for frame in range(total_frames):
        # 1-6を順番に表示
        current_number = (frame % 6) + 1
        dice_img = load_dice_image(current_number)
        
        # 画像が正常に読み込まれた場合のみ表示
        if dice_img is not None:
            dice_placeholder.image(dice_img, width=200, caption=f"サイコロの目: {current_number}")
        
        # 順番に表示されるサイコロ画像の表示時間を調整
        time.sleep(1.0 / frames_per_second)
    
    # 最終結果を表示
    final_dice_img = load_dice_image(final_result)
    if final_dice_img is not None:
        dice_placeholder.image(final_dice_img, width=200, caption=f"結果: {final_result}")
        status_placeholder.success(f"🎉 サイコロの結果は {final_result} です！")
    
    st.session_state.is_rolling = False

# 結果の履歴表示
# if st.session_state.dice_result is not None and not st.session_state.is_rolling:
#     st.write("**前回の結果:**")
#     result_img = load_dice_image(st.session_state.dice_result)
#     if result_img is not None:
#         st.image(result_img, width=150, caption=f"前回の結果: {st.session_state.dice_result}")
