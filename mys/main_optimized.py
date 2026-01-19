import requests
import tomllib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64
from pathlib import Path


class MihoyoSigner:
    def __init__(self, config_path='config.toml'):
        self.config_path = Path(config_path)
        self.script_dir = self.config_path.parent
        with open(self.config_path, 'rb') as f:
            self.config = tomllib.load(f)

    def encrypt_credentials(self, account, password):
        key_path = self.script_dir / 'public_key.pem'
        with open(key_path, "rb") as key_file:
            pem_public_key = key_file.read()
        public_key = serialization.load_pem_public_key(pem_public_key)

        account_cipher = public_key.encrypt(
            account.encode('utf-8'),
            padding.PKCS1v15()
        )
        password_cipher = public_key.encrypt(
            password.encode('utf-8'),
            padding.PKCS1v15()
        )

        return base64.b64encode(account_cipher).decode(), base64.b64encode(password_cipher).decode()

    def login(self):
        account = self.config['mihoyo']['account']
        password = self.config['mihoyo']['password']

        encrypted_account, encrypted_password = self.encrypt_credentials(account, password)

        url = "https://passport-api.mihoyo.com/account/ma-cn-passport/app/loginByPassword"
        headers = {
            'Accept': 'application/json',
            'x-rpc-app_id': 'bll8iq97cem8',
            'x-rpc-client_type': '2',
            'x-rpc-device_id': '2892ab834db5dafc',
            'x-rpc-device_fp': '38d7f86f2c07e',
            'x-rpc-device_name': 'NX627J',
            'x-rpc-device_model': 'NX627J',
            'x-rpc-sys_version': '9',
            'x-rpc-game_biz': 'bbs_cn',
            'x-rpc-app_version': '2.69.1',
            'x-rpc-sdk_version': '2.20.2',
            'x-rpc-lifecycle_id': '829012ac-f4f1-4e3a-8309-456922e9252a',
            'x-rpc-account_version': '2.20.2',
            'Host': 'passport-api.mihoyo.com',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/4.9.3'
        }
        json_data = {"account": encrypted_account, "password": encrypted_password}

        response = requests.post(url, headers=headers, json=json_data)
        data = response.json()

        if data.get('data') is None:
            print(f"登录失败，响应内容: {data}")
            raise Exception(f"登录失败: {data.get('message', '未知错误')}")

        token = data['data']['token']['token']
        mid = data['data']['user_info']['mid']
        login_ticket = data['data']['login_ticket']

        return token, mid, login_ticket

    def get_cookies(self, token, mid):
        url = 'https://passport-api.mihoyo.com/account/auth/api/getCookieAccountInfoBySToken'
        url1 = 'https://passport-api.mihoyo.com/account/auth/api/getLTokenBySToken'
        headers = {
            'Accept': 'application/json',
            'x-rpc-app_id': 'bll8iq97cem8',
            'x-rpc-client_type': '2',
            'x-rpc-device_id': '2892ab834db5dafc',
            'x-rpc-device_fp': '38d7f86f2c07e',
            'x-rpc-device_name': 'NX627J',
            'x-rpc-device_model': 'NX627J',
            'x-rpc-sys_version': '9',
            'x-rpc-game_biz': 'bbs_cn',
            'x-rpc-app_version': '2.69.1',
            'x-rpc-sdk_version': '2.20.2',
            'x-rpc-lifecycle_id': '944d2d5e-a3f8-4bf3-ac39-53acac38b4ee',
            'x-rpc-account_version': '2.20.2',
            'Cookie': f'stoken={token};mid={mid}',
            'Content-Type': 'application/json',
            'Host': 'passport-api.mihoyo.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/4.9.3'
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        if data.get('data') is None:
            print(f"获取Cookie失败，响应内容: {data}")
            raise Exception(f"获取Cookie失败: {data.get('message', '未知错误')}")

        cookie_token = data['data']['cookie_token']

        response = requests.get(url1, headers=headers)
        data = response.json()

        if data.get('data') is None:
            print(f"获取LToken失败，响应内容: {data}")
            raise Exception(f"获取LToken失败: {data.get('message', '未知错误')}")

        ltoken = data['data']['ltoken']

        return cookie_token, ltoken

    def sign_game(self, game_name, uid, hdid, region, sign_game, url, login_ticket, ltoken, cookie_token, mys_id):
        headers = {
            'x-rpc-signgame': sign_game,
            'Cookie': f'login_ticket={login_ticket};account_id={mys_id};ltoken={ltoken};cookie_token={cookie_token};'
        }

        data = {
            "act_id": hdid,
            "region": region,
            "uid": uid,
            "lang": "zh-cn"
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        try:
            if result["data"]["gt"] != "":
                challenge = result['data']['challenge']
                headers['x-rpc-challenge'] = challenge
                response = requests.post(url, headers=headers, json=data)
                result = response.json()
        except:
            pass

        return result

    def sign_all(self, games=None, cookies=None):
        if games is None:
            games = ['ys', 'xqgd']

        game_configs = {
            'ys': {
                'uid': self.config['game']['ys_uid'],
                'hdid': 'e202311201442471',
                'region': 'cn_gf01',
                'sign_game': 'hk4e',
                'url': self.config['api']['url'],
                'name': '原神'
            },
            'xqgd': {
                'uid': self.config['game']['xqgd_uid'],
                'hdid': 'e202304121516551',
                'region': 'prod_gf_cn',
                'sign_game': '',
                'url': self.config['api']['url'],
                'name': '星穹轨道'
            },
            'bh3': {
                'uid': self.config['game']['bh3_uid'],
                'hdid': 'e202306201626331',
                'region': 'pc01',
                'sign_game': '',
                'url': self.config['api']['url'],
                'name': '崩坏3'
            },
            'wdsjb': {
                'uid': self.config['game']['wdsjb_uid'],
                'hdid': 'e202202251749321',
                'region': 'cn_prod_gf01',
                'sign_game': '',
                'url': self.config['api']['url'],
                'name': '未定事件薄'
            },
            'zzz': {
                'uid': self.config['game']['zzz_uid'],
                'hdid': 'e202406242138391',
                'region': 'prod_gf_cn',
                'sign_game': 'zzz',
                'url': self.config['api']['url_zzz'],
                'name': '绝区零'
            }
        }

        results = {}

        for game in games:
            if game not in game_configs:
                continue

            config = game_configs[game]
            uid = config['uid']

            if not uid:
                continue

            print(f"{config['name']}签到中")

            result = self.sign_game(
                game_name=game,
                uid=uid,
                hdid=config['hdid'],
                region=config['region'],
                sign_game=config['sign_game'],
                url=config['url'],
                login_ticket=cookies['login_ticket'],
                ltoken=cookies['ltoken'],
                cookie_token=cookies['cookie_token'],
                mys_id=self.config['account']['mys_id']
            )

            results[game] = result
            print(f"{config['name']}签到结果: {result}")

        return results


def main():
    signer = MihoyoSigner()

    print("登录中...")
    token, mid, login_ticket = signer.login()
    print("登录成功")

    print("获取Cookie中...")
    cookie_token, ltoken = signer.get_cookies(token, mid)
    print("Cookie获取成功")

    cookies = {
        'login_ticket': login_ticket,
        'ltoken': ltoken,
        'cookie_token': cookie_token
    }

    print("开始签到...")
    results = signer.sign_all(cookies=cookies)

    return results


if __name__ == "__main__":
    main()
