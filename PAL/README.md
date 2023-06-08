# 仙靈島智能除草方案
這邊是在用 DOSBox-X 在玩，基於[中文 DOS 游戏合集](https://github.com/rwv/chinese-dos-games)

開啟遊戲後抵達山谷可以使用本方案開始除草

## ViT 除草機
用 CMD/Shell 運行：
```bash
# 首先安裝依賴
pip install -r requirements_ViT.txt
# 然後運行
python play_ViT.py
```
程序開啟後需點擊遊戲窗口確保鍵盤操作輸入到遊戲

> ⚠️ 你可能發覺效率並沒有比人手操作更快，不要緊，我也是依靠 CPU 進行圖像處理，每秒處理2.3幀（`batch_size=1`）

> 💰 如果你有配置高級顯卡的話，可以編輯 Python 腳本，在 `model.encode(...)` 當中加入 `device='cuda'` 的參數用 GPU 加速

## dHash 除草劑
用 CMD/Shell 運行：
```bash
# 首先安裝依賴
pip install -r requirements_dhash.txt
# 然後運行
python play_dhash.py
```
程序開啟後需點擊遊戲窗口確保鍵盤操作輸入到遊戲

> :octocat: 可以將 DOSBox-X 的 CPU 週期設置到 1500 左右然後按加速到最快，之後再開啟本方案，我這邊是試到的最高效率

# Credits
[中文 DOS 游戏合集](https://github.com/rwv/chinese-dos-games)
