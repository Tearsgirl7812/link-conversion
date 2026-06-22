# 🔗 Link Conversion - 連結轉換工具

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Status](https://img.shields.io/badge/status-Active-brightgreen)

**Link Conversion** 是一個專門轉換國外主流社交平台連結的工具，透過轉換連結以減少不必要參數和防止社交平台追蹤用戶。

## ✨ 功能

轉換以下平台的連結為潔淨連結：
- 🔵 **Facebook** - 移除分享參數
- 📷 **Instagram** - 移除追蹤參數
- 🎥 **YouTube** - 統一為標準格式
- 💬 **Threads** - 移除追蹤參數
- 𝕏 **X (Twitter)** - 移除追蹤參數

## 📱 平台

- **Web 應用** - 直接使用，無需安裝
- **桌面應用** - Windows, macOS, Linux
- **行動應用** - 作為 PWA 安裝在手機/平板
- **社交機器人**：
  - Telegram Bot
  - Discord Bot
  - WhatsApp Bot

## 🚀 快速開始

### Web 版本

1. 打開 `web/index.html` 在瀏覽器中
2. 貼上連結
3. 點擊「轉換」
4. 複製潔淨連結

### Python API

```python
from core.converter import LinkConverter

converter = LinkConverter()
result = converter.convert('https://www.instagram.com/p/DZQ_TWrlCRS/?utm_source=ig_web_copy_link')
print(result['converted'])
# 輸出: https://www.instagram.com/p/DZQ_TWrlCRS
```

### Docker 部署

```bash
docker-compose up
```

## 📁 項目結構

```
link-conversion/
├── core/                      # 核心轉換邏輯
│   ├── __init__.py
│   ├── converter.py           # 主轉換器
│   ├── platforms/             # 平台轉換器
│   │   ├── __init__.py
│   │   ├── facebook.py
│   │   ├── instagram.py
│   │   ├── youtube.py
│   │   ├── threads.py
│   │   └── x.py
│   └── detector.py            # 平台偵測
├── web/                       # Web 應用
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── manifest.json          # PWA 配置
├── api/                       # API 伺服器
│   ├── app.py                 # Flask 應用
│   ├── requirements.txt
│   └── __init__.py
├── bots/                      # 社交機器人
│   ├── __init__.py
│   ├── telegram_bot.py
│   ├── discord_bot.py
│   └── whatsapp_bot.py
├── desktop/                   # 桌面應用 (Electron)
│   ├── main.js
│   ├── preload.js
│   └── package.json
├── tests/                     # 測試
│   ├── __init__.py
│   └── test_converters.py
├── docs/                      # 文檔
│   ├── API.md
│   ├── INSTALLATION.md
│   ├── BOT_SETUP.md
│   └── CONTRIBUTING.md
├── .github/workflows/         # CI/CD
│   └── deploy.yml
├── requirements.txt           # Python 依賴
├── package.json               # Node 依賴
├── Dockerfile
├── docker-compose.yml
└── config.example.env
```

## 🔄 轉換示例

| 平台 | 原始 | 轉換後 |
|------|------|--------|
| Facebook | `https://www.facebook.com/share/p/14hd6A5N7Bk/` | `https://www.facebook.com/akina.na.741785/posts/...` |
| Instagram | `https://www.instagram.com/p/DZQ_TWrlCRS/?utm_source=ig_web_copy_link&igsh=...` | `https://www.instagram.com/p/DZQ_TWrlCRS` |
| YouTube | `https://youtu.be/iRSu_af96q8?si=UpTOo8--4Ca-h8P6` | `https://www.youtube.com/watch?v=iRSu_af96q8` |
| X | `https://x.com/user/status/123?s=20` | `https://x.com/user/status/123` |

## 🛠️ 安裝

### 要求
- Python 3.8+
- Node.js 14+（用於 Electron）
- Docker（可選）

### 本地開發

```bash
# 克隆倉庫
git clone https://github.com/Tearsgirl7812/link-conversion.git
cd link-conversion

# 安裝 Python 依賴
pip install -r requirements.txt

# 啟動 API 伺服器
python api/app.py

# 在另一個終端啟動 Web 應用
python -m http.server 8000 -d web
```

訪問 http://localhost:8000

## 🤖 機器人設置

### Telegram Bot

```bash
TELEGRAM_TOKEN=your_token python bots/telegram_bot.py
```

### Discord Bot

```bash
DISCORD_TOKEN=your_token python bots/discord_bot.py
```

詳見 [BOT_SETUP.md](docs/BOT_SETUP.md)

## 🎯 目標

✅ 程式碼簡單易維護  
✅ 所有人都能快速上手  
✅ 介面簡單直接  
✅ 部署流程簡單  
✅ 兼容手機、平板電腦和電腦  
✅ 不用任何金錢預算維護  

## 📄 許可

MIT License - 詳見 [LICENSE](LICENSE)

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

詳見 [CONTRIBUTING.md](docs/CONTRIBUTING.md)

## 📧 聯絡

如有問題或建議，請開啟 GitHub Issue。

---

⭐ 如果覺得有用，請給我們一個星星！
