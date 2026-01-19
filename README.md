# Mihoyo Auto Sign

> 自动签到，解放双手

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-Supported-green.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-Educational%20Only-red.svg)](LICENSE)

---

## 📋 简介

一个轻量级的米游社游戏自动签到工具，支持多游戏、多平台签到，无需复杂配置，开箱即用。

本项目基于 [tuotuooo/AutoLiver](https://github.com/tuotuooo/AutoLiver/) 开源项目优化实现。

### 支持的游戏

| 游戏 | 状态 |
|------|------|
| 原神 | ✅ |
| 星穹铁道 | ✅ |
| 崩坏3 | ✅ |
| 未定事件簿 | ✅ |
| 绝区零 | ✅ |

---

## 🚀 快速开始

### Docker 部署（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/MihoyoAutoSign.git
cd MihoyoAutoSign

# 2. 编辑配置文件
nano mys/config.toml

# 3. 启动服务
docker-compose up --build
```

### 本地运行

```bash
# 1. 安装依赖
pip install -r mys/requirements.txt

# 2. 编辑配置
nano mys/config.toml

# 3. 运行
python mys/run.py
```

---

## ⚙️ 配置

编辑 `mys/config.toml` 文件：

```toml
[mihoyo]
account = "your_phone_number"
password = "your_password"

[account]
mys_id = "your_mihoyo_uid"

[game]
ys_uid = "your_genshin_uid"
xqgd_uid = "your_hsr_uid"
bh3_uid = ""
wdsjb_uid = ""
zzz_uid = ""
```

**提示**：不需要签到的游戏 UID 留空即可。

---

## 📦 项目结构

```
MihoyoAutoSign/
├── mys/
│   ├── main_optimized.py    # 核心逻辑
│   ├── run.py              # 入口文件
│   ├── config.toml          # 配置文件
│   ├── requirements.txt      # 依赖列表
│   └── public_key.pem               # 加密密钥
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🛠️ 高级用法

### 指定签到游戏

```bash
# 只签到原神
python mys/run.py ys

# 签到多个游戏
python mys/run.py ys,xqgd,zzz
```

### 定时任务

**Docker 方式：**

```yaml
services:
  mihoyo-sign:
    build: .
    volumes:
      - ./mys/config.toml:/app/config.toml
    restart: always
    command: >
      sh -c "while true; do
        python run.py
        sleep 86400
      done"
```

**Cron 方式：**

```bash
# 每天早上 8 点执行
0 8 * * * cd /path/to/MihoyoAutoSign && python mys/run.py
```

---

## ⚠️ 注意事项

1. **设备验证**：首次使用可能需要关闭"新设备登录需短信验证"
   - 访问：https://user.mihoyo.com/#/login/captcha
   - 关闭相关选项

2. **账号安全**：
   - 请勿将配置文件上传到公开仓库
   - 定期更换密码
   - 本项目仅供学习使用

3. **使用限制**：
   - 严禁用于商业用途
   - 严禁用于违法违规活动
   - 使用后果由使用者自行承担

---

## 📝 开发

### 核心类

```python
from main_optimized import MihoyoSigner

signer = MihoyoSigner('config.toml')
token, mid, login_ticket = signer.login()
cookie_token, ltoken = signer.get_cookies(token, mid)
results = signer.sign_all(['ys', 'xqgd'])
```

### 技术栈

- Python 3.11+
- TOML 配置
- Docker & Docker Compose
- Requests
- Cryptography

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

本项目仅供学习交流使用。

---

<div align="center">

**Made with ❤️ for gamers**

</div>
