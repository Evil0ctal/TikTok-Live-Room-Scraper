# TikTok-Live-Rank

## 1-安装依赖
`pip install -r requirements.txt`

## 2-运行

- 如果要运行Web程序: `python3 web.py`

## 3-调用已封装的类

```python
TikTokLive = TikTokLive()

url = input("请输入TikTok直播间分享链接：")

# 获取直播间信息
live_room_info = TikTokLive.get_live_room_info(url)

# 获取直播间ID
room_id = TikTokLive.get_live_room_id(live_room_info)

# 获取主播ID
anchor_id = TikTokLive.get_live_anchor_id(live_room_info)

room_ranking = TikTokLive.get_live_room_ranking(anchor_id, room_id)

print(room_ranking)

```
