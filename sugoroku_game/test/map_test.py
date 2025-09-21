import cv2 as cv
import streamlit as st
from PIL import Image

map_path = "sugoroku_map/background.png"

player_path = "sugoroku_map/pieces/playerA.png"

back_image = Image.open(map_path)

player_image = Image.open(player_path)

cv_player_image = cv.imread(player_image)

back_image.paste(player_image, (1, 1))

st.image(back_image)
