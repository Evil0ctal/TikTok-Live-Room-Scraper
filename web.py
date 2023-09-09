# PyWebIO support
from pywebio import *
from pywebio.input import *
from pywebio.output import *

# Flask support
from flask import Flask, render_template, request
from pywebio.platform.flask import webio_view

# TikTokLive
from TikTokLive import TikTokLive

# 初始化TikTokLive
TikTokLive = TikTokLive()

# Flask app
app = Flask(__name__)

title = "TikTok直播间排名采集器"
version = "V1.0.0"
description = "TikTok直播间排名采集器在线版，可以采集任意直播间的排名。"

config(theme='minty',
       title=title,
       description=description
       )


def main():
    tiktok_live_url = input('请输入TikTok直播间链接：', type=TEXT, required=True)

    # 获取直播间信息
    live_room_info = TikTokLive.get_live_room_info(tiktok_live_url)

    # 获取直播间ID
    room_id = TikTokLive.get_live_room_id(live_room_info)

    # 获取主播ID
    anchor_id = TikTokLive.get_live_anchor_id(live_room_info)

    room_ranking = TikTokLive.get_live_room_ranking(anchor_id, room_id)

    room_ranking = room_ranking.get('data').get('rank_view')

    print(f"数据采集完成，直播间ID：{room_id}，主播ID：{anchor_id}，排名：{room_ranking}")
    put_markdown(f"## 解析结果：")
    put_markdown(f"- 直播间ID：{room_id}")
    put_markdown(f"- 主播ID：{anchor_id}")
    # $.data.rank_view.owner_rank.rank_str
    put_markdown(f"- 直播间所有者排名：{room_ranking.get('owner_rank').get('rank_str')}")

    # $.data.rank_view.owner_rank.rank_user.nickname
    put_markdown(f"- 直播间所有者昵称：{room_ranking.get('owner_rank').get('rank_user').get('nickname')}")

    # $.data.rank_view.ranks
    for rank in room_ranking.get('ranks'):
        # $.data.rank_view.ranks.[0].rank
        put_markdown(f"- 排名：{rank.get('rank')}")
        # $.data.rank_view.ranks.[0].rank_user.display_id
        put_markdown(f"- 用户ID：{rank.get('rank_user').get('display_id')}")
        # $.data.rank_view.ranks.[0].rank_user.nickname
        put_markdown(f"- 用户昵称：{rank.get('rank_user').get('nickname')}")
        # $.data.rank_view.ranks.[0].score
        put_markdown(f"- 亲密度(钻石)：{rank.get('score')}")
        # $.data.rank_view.ranks.[0].score_description
        put_markdown(f"- 亲密度描述(钻石)：{rank.get('score_description')}")
        put_markdown(f"---")


# Routes
app.add_url_rule('/', 'main', webio_view(main), methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
