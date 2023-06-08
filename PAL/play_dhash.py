import time
import numpy
import pyautogui
from PIL import Image
import imagehash

end_emb = imagehash.dhash(Image.open('1.png'))
start_emb = imagehash.dhash(Image.open('0.png'))
move_emb = imagehash.dhash(Image.open('2.png'))
mov2_emb = imagehash.dhash(Image.open('22.png'))
tran_emb = imagehash.dhash(Image.open('3.png'))
fight_emb = imagehash.dhash(Image.open('4.png'))
hit_emb = imagehash.dhash(Image.open('44.png'))
memory = [end_emb, start_emb,
          move_emb, mov2_emb,
          tran_emb, fight_emb, hit_emb]

c1, c2 = pyautogui.size()
region=(c1/2-321, c2/2-227, 642, 452)

def sim(a, b):
    return [a - i for i in b]

key = 'up'
pre = 0
im = imagehash.dhash(pyautogui.screenshot(region=region))
while True:
    cos_scores = sim(im, memory)
    # print(cos_scores)
    case = cos_scores.index(min(cos_scores))
    # print(case)
    if (case < 4
        and (numpy.asarray(cos_scores) - numpy.asarray(pre)).sum() == 0):
        if key == 'up':
            key = 'down'
        else:
            key = 'up'
    if (case == 1):
        key = 'up'
        with pyautogui.hold(key):  # Press the Up key down and hold it.
            time.sleep(0.1)
            im = imagehash.dhash(pyautogui.screenshot(region=region))
    elif (case == 2 or case == 3):
        if key == 'up':
            pyautogui.keyDown('left')
        with pyautogui.hold(key):
            time.sleep(0.1)
            im = imagehash.dhash(pyautogui.screenshot(region=region))
            pyautogui.keyUp('left')
    elif (case == 0):
        key = 'down'
        with pyautogui.hold(key):
            time.sleep(0.1)
            im = imagehash.dhash(pyautogui.screenshot(region=region))
    else:
        with pyautogui.hold('a'):
            time.sleep(0.1)
            im = imagehash.dhash(pyautogui.screenshot(region=region))
    pre = cos_scores
