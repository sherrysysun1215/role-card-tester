#!/usr/bin/env python3
"""CI 专用：从环境变量写 shared_api.json（key 只存在于 Secrets，不进仓库）。"""
import json, os, sys

cfg = {
    "baseUrl": os.environ.get("API_BASE", "").strip(),
    "apiKey": os.environ.get("API_KEY", "").strip(),
    "model": os.environ.get("API_MODEL", "").strip(),
    "temperature": float(os.environ.get("API_TEMP") or 0.9),
}
if not cfg["baseUrl"] or not cfg["apiKey"] or not cfg["model"]:
    sys.exit("缺少 Secrets：SHARE_API_BASE / SHARE_API_KEY / SHARE_API_MODEL")
json.dump(cfg, open("shared_api.json", "w"), ensure_ascii=False)
print("shared_api.json 已生成（key 长度 %d）" % len(cfg["apiKey"]))
