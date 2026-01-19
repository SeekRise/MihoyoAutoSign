#!/usr/bin/env python3
import sys
import os
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / 'config.toml'

sys.path.insert(0, str(SCRIPT_DIR))

from main_optimized import MihoyoSigner


def main():
    print("米游社自动签到工具")
    print("=" * 50)

    if not CONFIG_PATH.exists():
        print(f"配置文件不存在，请先创建 {CONFIG_PATH}")
        return 1

    games = None
    if len(sys.argv) > 1:
        games = sys.argv[1].split(',')

    try:
        signer = MihoyoSigner(str(CONFIG_PATH))

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
        results = signer.sign_all(games, cookies)

        print("=" * 50)
        print("签到完成！")
        return 0

    except Exception as e:
        print(f"签到失败: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
