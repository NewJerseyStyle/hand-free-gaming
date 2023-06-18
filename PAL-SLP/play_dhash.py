import time
import numpy
import pyautogui
from PIL import Image
import imagehash

end_emb = imagehash.dhash(Image.open('1.png'))
start_emb = imagehash.dhash(Image.open('0.png'))
tran_emb = imagehash.dhash(Image.open('3.png'))
fight_emb = imagehash.dhash(Image.open('4.png'))
hit_emb = imagehash.dhash(Image.open('44.png'))
memory = [end_emb, start_emb,
          tran_emb, fight_emb, hit_emb]

c1, c2 = pyautogui.size()
region=(c1/2-321, c2/2-216, 642, 432)

def sim(a, b):
    return [a - i for i in b]

# hold key until screen nothing move
def hold():
    i = 1
    while i:
        p = imagehash.dhash(pyautogui.screenshot(region=region))
        time.sleep(0.5)
        i = sum(sim(p,
                    [imagehash.dhash(
                        pyautogui.screenshot(region=region))]))

key_dict = {
    0: 'up',
    1: 'down',
    2: 'left',
    3: 'right'}
pre = 0
pressed = []
while True:
    im = imagehash.dhash(pyautogui.screenshot(region=region))
    cos_scores = sim(im, memory)
    # print(min(cos_scores))
    case = cos_scores.index(min(cos_scores))
    case = case if min(cos_scores) < 20 else -1
    # print(case)
    if (case == 1):
        with pyautogui.hold('right'):
            hold()
    elif (case == 0):
        with pyautogui.hold('left'):
            hold()
    elif (case > 0):
        with pyautogui.hold('a'):
            time.sleep(0.1)
    else:
        key = key_dict[numpy.random.randint(0, 4)]
        if ((numpy.asarray(cos_scores) - numpy.asarray(pre)).sum() == 0):
            while key in pressed:
                key = key_dict[numpy.random.randint(0, 4)]
            pressed.append(key)
        else:
            pressed = [key]
        with pyautogui.hold(key):
            hold()
    pre = cos_scores
