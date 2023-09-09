import json
import httpx

from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


class TikTokLive:

    @staticmethod
    # 输入直播间链接，获取直播间id和主播id
    def get_live_room_info(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0'
        }
        response = httpx.request("GET", url, headers=headers)
        html_content = response.text
        return html_content

    @staticmethod
    # 获取直播间id
    def get_live_room_id(html_content):
        # 解析html
        soup = BeautifulSoup(html_content, 'html.parser')

        # 获取直播间id
        # 找到具有特定属性的meta标签
        meta_tag = soup.find('meta', attrs={'data-rh': 'true', 'property': 'al:ios:url'})

        # 获取meta标签的content属性值
        if meta_tag:
            content_value = meta_tag['content']

            # 解析URL以获取room_id参数
            parsed_url = urlparse(content_value)
            room_id = parse_qs(parsed_url.query).get('room_id')

            if room_id:
                room_id = room_id[0]
                print(f"room_id: {room_id}")
                return room_id
            else:
                msg = 'room_id parameter not found'
                return msg
        else:
            msg = 'meta tag not found'
            return msg

    @staticmethod
    # 获取主播id
    def get_live_anchor_id(html_content):
        # 解析HTML内容
        soup = BeautifulSoup(html_content, 'html.parser')

        # 找到具有特定id和type属性的<script>标签
        script_tag = soup.find('script', attrs={'id': 'SIGI_STATE', 'type': 'application/json'})

        # 获取<script>标签的内容
        if script_tag:
            script_content = script_tag.string
            script_content = json.loads(script_content)
            anchor_id = script_content.get('LiveRoom').get('liveRoomUserInfo').get('user').get('id')
            print(f"anchor_id: {anchor_id}")
            return anchor_id
        else:
            print('script tag not found')

    @staticmethod
    # 获取直播间排行榜
    def get_live_room_ranking(anchor_id, room_id):
        domain = "https://webcast16-normal-useast8.us.tiktokv.com"
        path = "/webcast/ranklist/list/v2/"
        params = f"anchor_id={anchor_id}&room_id={room_id}&rank_type=8&region_type=1&gap_interval=0&use_simple_user=true&iid=7273961106314381102&device_id=7249641987414099499&ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=290204&version_name=29.2.4&device_platform=android&ab_version=29.2.4&ssmix=a&device_type=Pixel+6+Pro&device_brand=google&language=en&os_api=33&os_version=13&openudid=97c8d19399a5c330&manifest_version_code=2022902040&resolution=1440*2883&dpi=612&update_version_code=2022902040&_rticket=1694254730171&current_region=US&app_type=normal&sys_region=CN&mcc_mnc=310004&timezone_name=America%2FLos_Angeles&carrier_region_v2=310&residence=US&app_language=en&carrier_region=US&ac2=wifi5g&uoo=0&op_region=US&timezone_offset=-28800&build_number=29.2.4&host_abi=arm64-v8a&locale=en&region=CN&content_language=en%2C&ts=1694254635&cdid=f4e8fcb0-d9f6-4a55-92ae-d16cb01c32df&webcast_sdk_version=2830&webcast_language=en&webcast_locale=zh_CN_%23Hans&effect_sdk_version=13.9.0&current_network_quality_info=%7B%22tcp_rtt%22%3A63%2C%22quic_rtt%22%3A63%2C%22http_rtt%22%3A162%2C%22downstream_throughput_kbps%22%3A5656%2C%22quic_send_loss_rate%22%3A-1%2C%22quic_receive_loss_rate%22%3A-1%2C%22net_effective_connection_type%22%3A4%2C%22video_download_speed%22%3A2762%7D"
        url = f"{domain}{path}?{params}"
        headers = {
            'User-Agent': "com.zhiliaoapp.musically/2022902040 (Linux; U; Android 13; en; Pixel 6 Pro; Build/TQ2A.230305.008.E1; Cronet/TTNetVersion:ff9e1e59 2023-04-11 QuicVersion:d298137e 2023-02-13)",
            'Accept-Encoding': "gzip, deflate, br",
            # 'Cookie': "store-idc=useast5; store-country-code=us; install_id=7273961106314381102; ttreq=1$41a3f4497fd86dff31c7e77e9a3c75ed6bfe5442; passport_csrf_token=5246d657ad91addddbda460530f204c4; passport_csrf_token_default=5246d657ad91addddbda460530f204c4; tt-target-idc=useast5; d_ticket=bc046168ec742c25fb0efa1d39749c409d773; multi_sids=7151927120461038634%3A8a67d878b756dbe5810486ab9e38b383; cmpl_token=AgQQAPNSF-RPsLN-UXVaot0T_vp_yZ8MP6nZYM1G5A; odin_tt=a43eb4606585069f6b2883a44ab661ca6fd90e8f86acf3f7d8594034d9c0c8d383288533fde02c9aac831eb6529d53d4c1aae60437ff484ab4a617d2a4bfdceb8a43b7bd15d767bc572f4413bf2b362a; sid_guard=8a67d878b756dbe5810486ab9e38b383%7C1694239693%7C5184000%7CWed%2C+08-Nov-2023+06%3A08%3A13+GMT; uid_tt=af20bb5eba69cd529c2e024cefdfde36473234713ec14dbc155f12bb48eb2ef4; uid_tt_ss=af20bb5eba69cd529c2e024cefdfde36473234713ec14dbc155f12bb48eb2ef4; sid_tt=8a67d878b756dbe5810486ab9e38b383; sessionid=8a67d878b756dbe5810486ab9e38b383; sessionid_ss=8a67d878b756dbe5810486ab9e38b383; store-country-code-src=uid; tt-target-idc-sign=wG_NAMchJeziSRAj0QrPnYKIk7olkSIrSY0C7PVPgtAs82nT4qiNvihLwWxi9WXV2zZnhMBkX2vfaEF_KddGXqMLJ5SfRaUif7OjmutodpsuNFO1taZ1jLMuA9EiY998WIXDrqDwEEDub6aX88lkRLqznmdBg3VvGfyBUNghTfI8gqcDUA6UeiT1bt2ieD9cir2Ovz1rHrWSbc31bYeunK-dP0hbXXmNR_2FbI6MKyZ9raIY4rhzKOfuRLBI1LbOZ66gIrfxEmDCeQqS0vLNvEtfi7LMIVe0xbuohmTpaDHi_oBoC61Q2Ec-rJU-Pet2iN1vLXiA8pAxQdZ4ITOS_65zoPbcswvotryQ6Ay_ql9SRgBwlOI7ibu0PXFNtkmI3QlFp0q9gKgUeorQNn4bYcma6qyi9uJyCwdmrHEFQh7ZqtVaOMFmTDeSyU3Eidzk39JIBz8gaYKD6mkyBLq3_tPrY0Jn7pm3MfQ54vZb5KSJshqwalxMDJIUg-QTUPcd; msToken=kINphZRBvcW7GPWr9nkG8K0HvxMVKeSbC_-tr8MJK6-SlloKJ7906rV2RkN-mABkG-N6zwroF-XldKsviXEdiH0IiuNsyvd3sfnTHz4v6VjyCxtM98s0auNXlt46"
        }
        response = httpx.request("GET", url, headers=headers)
        data = response.json()
        print(data)
        return data


if __name__ == '__main__':
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
