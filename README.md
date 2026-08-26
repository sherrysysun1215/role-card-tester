# 角色卡试炼场 · 分享版

静态单页应用，访客导入/使用预设角色卡与 AI 模型对话。API key 不进仓库：存于 GitHub Secrets，由 Actions 构建时注入。

## 目录

- `角色卡试炼场.html` — 源页面（功能/样式改这里）
- `cards/*.json` — 预设角色卡（人设/开场/关系阶段改这里）
- `build_share.py` — 构建脚本：预设卡 + 共享 API 配置 → `share/index.html`
- `write_shared_api.py` — CI 专用：从 Secrets 写 `shared_api.json`

## 更新流程

1. 改上面的源文件，push 到 `main`
2. Actions 自动构建并发布到 Pages（约 1 分钟）
3. 访客刷新即得更新（版本号机制：预设卡按名字合并更新，访客的聊天记录/立绘/模式保留）

## 共享 API 配置（Secrets）

仓库 Settings → Secrets and variables → Actions：

| Secret | 内容 |
|---|---|
| `SHARE_API_BASE` | API 地址，如 `https://api.moonshot.cn/v1` |
| `SHARE_API_KEY` | API key（请用单独、限额、可吊销的 key） |
| `SHARE_API_MODEL` | 模型名 |
| `SHARE_API_TEMP` | 温度，可选，默认 0.9 |

注意：Secrets 只保证仓库干净。key 仍会随页面下发到访客浏览器，公开页面上这是纯前端方案的固有限制——务必使用限额 key。
