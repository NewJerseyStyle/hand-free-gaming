# 十里坡智能驅蟲方案

這邊是在用 PAL-SDL2 在玩，因為之前的中文 DOS 游戏合集沒有課金 🙈

開啟遊戲後抵達長坡可以使用本方案開始驅蟲

# DQN 除草機
用 CMD/Shell 運行：
```bash
# 首先安裝依賴
pip install -r requirements_ViT.txt
# 然後運行
python play_ViT.py
```
程序開啟後需點擊遊戲窗口確保鍵盤操作輸入到遊戲，之後它會慢慢學會如何有效地增加經驗值，但……

> ⚠️ 你可能發覺效率並沒有比人手操作更快，不要緊，我也是依靠 CPU 在磨嘰

> 💰 如果你有配置高級顯卡的話，可以編輯 Python 腳本，在 `model.encode(...)` 當中加入 `device='cuda'` 的參數用 GPU 加速  
> 如果不順利的話，可能是因為需要手動安裝 GPU 版本的 PyTorch，可以在[官網](https://pytorch.org/get-started/locally/)選擇操作系統版本和顯卡等資訊後往 CMD 複製貼上安裝指令

> 🤬🤡🐱對世界充滿好奇的 AI 有一定機率會離開十里坡 ~~閒逛摸魚~~ 去探索地圖的每一個角落；為了避免它亂用道具或者沉迷於跟路人聊天，已經禁止它按 [space](https://zh.wikipedia.org/zh-hk/%E7%A9%BA%E6%A0%BC%E9%94%AE) 和 [enter](https://zh.wikipedia.org/wiki/%E5%9B%9E%E8%BB%8A%E9%8D%B5) 鍵

> ⌨️ :octocat: 🖱️ 還是嫌棄這個實現太慢？沒問題，魔改一下換成 CNN 的 DQN 就會快些了，默認用的 ViT 特徵提取是比較殺雞用牛刀了

## dHash 迷之走位
用 CMD/Shell 運行：
```bash
# 首先安裝依賴
pip install -r requirements_dhash.txt
# 然後運行
python play_dhash.py
```
程序開啟後需點擊遊戲窗口確保鍵盤操作輸入到遊戲

> ⚠️ 你可能發覺這個選項很不靠譜，這並不是錯覺
