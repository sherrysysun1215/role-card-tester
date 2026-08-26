#!/usr/bin/env python3
"""构建分享版 share/index.html：
- 源页面：角色卡试炼场.html
- 内置预设角色卡：cards/ 下所有 *.json（新访客只继承卡与开场预设，不带聊天记录）
- 共享 API 配置：shared_api.json（可选，本地保存，不要提交进任何仓库）
  格式：{"baseUrl": "...", "apiKey": "sk-...", "model": "...", "temperature": 0.9}
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

def main():
    src = open(os.path.join(ROOT, '角色卡试炼场.html'), encoding='utf-8').read()

    cards = []
    for p in sorted(glob.glob(os.path.join(ROOT, 'cards', '*.json'))):
        with open(p, encoding='utf-8') as f:
            cards.append(json.load(f))          # 校验 + 规范化
    if not cards:
        sys.exit('cards/ 目录下没有可用的角色卡 JSON')

    presets = json.dumps(cards, ensure_ascii=False, indent=None)
    marker = 'const PRESETS = []; /* __PRESETS__ */'
    assert marker in src, '源页面缺少 PRESETS 注入位'
    out = src.replace(marker, f'const PRESETS = {presets};')

    import time
    ver_marker = "const PRESET_VERSION = 'dev'; /* __PRESET_VERSION__ */"
    assert ver_marker in src, '源页面缺少 PRESET_VERSION 注入位'
    ver = time.strftime('%Y%m%d-%H%M%S')
    out = out.replace(ver_marker, f"const PRESET_VERSION = '{ver}';")
    print(f'预设版本：{ver}')

    api_marker = 'const SHARED_API = null; /* __SHARED_API__ */'
    assert api_marker in src, '源页面缺少 SHARED_API 注入位'
    api_path = os.path.join(ROOT, 'shared_api.json')
    if os.path.exists(api_path):
        shared = json.load(open(api_path, encoding='utf-8'))
        out = out.replace(api_marker, f'const SHARED_API = {json.dumps(shared, ensure_ascii=False)};')
        print(f'已注入共享 API：{shared.get("baseUrl")} / {shared.get("model")}')
    else:
        print('未找到 shared_api.json，访客需自行配置 API')

    out = out.replace('<title>角色卡试炼场 · 对话测试</title>', '<title>角色卡试炼场 · 分享体验版</title>')
    os.makedirs(os.path.join(ROOT, 'share'), exist_ok=True)
    dst = os.path.join(ROOT, 'share', 'index.html')
    open(dst, 'w', encoding='utf-8').write(out)
    print(f'完成：{dst}（{os.path.getsize(dst)} bytes，{len(cards)} 张预设卡）')

if __name__ == '__main__':
    main()
