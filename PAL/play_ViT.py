import time
import pyautogui
from sentence_transformers import SentenceTransformer, util
from PIL import Image

model = SentenceTransformer('clip-ViT-B-32')
end_emb = model.encode(Image.open('1.png'))
start_emb = model.encode(Image.open('0.png'))
move_emb = model.encode(Image.open('2.png'))
mov2_emb = model.encode(Image.open('22.png'))
tran_emb = model.encode(Image.open('3.png'))
fight_emb = model.encode(Image.open('4.png'))
hit_emb = model.encode(Image.open('44.png'))
memory = [end_emb, start_emb,
          move_emb, mov2_emb,
          tran_emb, fight_emb, hit_emb]

c1, c2 = pyautogui.size()
region=(c1/2-320, c2/2-222, 640, 444)

key = 'down'
pre = 0
speed = 4
im = pyautogui.screenshot(region=region)
img_emb = model.encode(im)
while True:
    cos_scores = util.cos_sim(img_emb, memory)
    # print(cos_scores)
    case = cos_scores.argmax().item()
    case = -1 if cos_scores[0][case] - 0.9 < 0 else case
    # print(case)
    if (case < 4
        and (cos_scores - pre).sum() == 0):
        if key == 'up':
            key = 'down'
        else:
            key = 'up'
    if (case == 1):
        key = 'up'
        with pyautogui.hold(key):  # Press the Up key down and hold it.
            time.sleep(2/speed)
        with pyautogui.hold('left'):
            img_emb = model.encode(im)
            im = pyautogui.screenshot(region=region)
    elif (case == 2 or case == 3):
        with pyautogui.hold(key):
            img_emb = model.encode(im)
            im = pyautogui.screenshot(region=region)
    elif (case == 0):
        key = 'down'
        with pyautogui.hold(key):
            img_emb = model.encode(im)
            im = pyautogui.screenshot(region=region)
    else:
        with pyautogui.hold('space'):
            img_emb = model.encode(im)
            im = pyautogui.screenshot(region=region)
    pre = cos_scores
