#!/usr/bin/env python3
"""多平台文生图脚本。

支持平台与模型：
  aihubmix : AiHubMix 聚合平台（OpenAI 兼容接口）
             - gpt-image-2.5-flare 等  → /images/generations
             - gemini 系（nano banana）→ /chat/completions + modalities（Google 原生路由）
  bigmodel : 智谱开放平台（cogview-3-flash 免费 / cogview-4）

API Key 的读取顺序（绝不打印、不写入日志）：
  1. 环境变量 AIHUBMIX_API_KEY（或 OPENAI_API_KEY）/ ZHIPUAI_API_KEY（或 ZAI_API_KEY）
  2. 文件 ~/.config/zcode-image/<provider>.key（权限 600）
     bigmodel 另兼容旧版单 Key 文件 ~/.config/zcode-image/key
"""
import argparse
import base64
import datetime
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

KEY_DIR = pathlib.Path.home() / ".config/zcode-image"
DEFAULT_OUT_DIR = pathlib.Path.home() / "Pictures/zcode-images"

PROVIDERS = {
    "aihubmix": {
        "base_url": "https://aihubmix.com/v1",
        # 主域名在国内部分网络被 DNS 污染，官方备用域名（见 docs.aihubmix.com 快速开始）
        "fallback_base_url": "https://api.inferera.com/v1",
        "default_model": "gpt-image-2.5-flare",
        "env": ("AIHUBMIX_API_KEY", "OPENAI_API_KEY"),
        "quality": True,
        "timeout": 180,
    },
    "bigmodel": {
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "default_model": "cogview-3-flash",
        "env": ("ZHIPUAI_API_KEY", "ZAI_API_KEY"),
        "quality": False,
        "timeout": 120,
    },
}


def load_key(provider):
    for env in PROVIDERS[provider]["env"]:
        value = os.environ.get(env)
        if value:
            return value.strip()
    key_file = KEY_DIR / f"{provider}.key"
    if key_file.exists():
        return key_file.read_text().strip()
    if provider == "bigmodel":
        legacy = KEY_DIR / "key"
        if legacy.exists():
            return legacy.read_text().strip()
    return None


def pick_provider(want):
    if want != "auto":
        return want
    return "aihubmix" if load_key("aihubmix") else "bigmodel"


def api_request(conf, path, payload, provider):
    """带备用域名回退的 POST。HTTP 层错误直接退出（换域名无用）。"""
    urls = [conf["base_url"]]
    if conf.get("fallback_base_url"):
        urls.append(conf["fallback_base_url"])
    key = load_key(provider)
    last_err = None
    for base in urls:
        request = urllib.request.Request(
            base + path,
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=conf["timeout"]) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            # 只输出错误正文，避免把请求头（含 Key）带进日志
            detail = e.read().decode(errors="replace")[:500]
            sys.exit(f"[{provider}] API 返回错误 {e.code}: {detail}")
        except urllib.error.URLError as e:
            last_err = e
            continue
    sys.exit(f"[{provider}] 网络错误: {last_err.reason}（主域名与备用域名均连接失败）")


def extract_chat_image(result, provider):
    """从 chat/completions 返回里提取图片 base64。
    AiHubMix 的 gemini 路由放在 message.multi_mod_content[].inline_data.data；
    其他网关（OpenRouter 风格）放在 message.images[].image_url.url 或 content 内嵌 data URL。
    """
    try:
        message = result["choices"][0]["message"]
    except (KeyError, IndexError):
        sys.exit(f"[{provider}] 返回格式异常: {json.dumps(result, ensure_ascii=False)[:300]}")
    for part in message.get("multi_mod_content") or []:
        if isinstance(part, dict):
            data = (part.get("inline_data") or {}).get("data")
            if data:
                return data
    for im in message.get("images") or []:
        url = im.get("image_url", {}).get("url", "") if isinstance(im, dict) else str(im)
        if url.startswith("data:"):
            return url.split(",", 1)[1]
    content = message.get("content") or ""
    match = re.search(r"data:image/[^;\s\"')]+;base64,([A-Za-z0-9+/=]+)", content)
    if match:
        return match.group(1)
    sys.exit(f"[{provider}] 返回中没有图片: {json.dumps(result, ensure_ascii=False)[:300]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="图片描述，中英文均可")
    parser.add_argument("--provider", default="auto",
                        choices=["auto", "aihubmix", "bigmodel"])
    parser.add_argument("--model", default=None, help="不填用平台默认模型")
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--quality", default="medium",
                        choices=["low", "medium", "high", "xhigh", "max", "auto"],
                        help="仅 aihubmix(gpt-image) 支持")
    parser.add_argument("--out", default=None, help="输出文件路径")
    args = parser.parse_args()

    provider = pick_provider(args.provider)
    conf = PROVIDERS[provider]
    if not load_key(provider):
        sys.exit(
            f"未找到 {provider} 的 API Key。请把 Key 存入 {KEY_DIR / (provider + '.key')}"
            f"（权限 600）或环境变量 {conf['env'][0]}"
        )

    model = args.model or conf["default_model"]
    # AiHubMix 对 gemini 系（nano banana）走 chat 接口 + modalities，其余走 images 接口
    chat_style = provider == "aihubmix" and model.startswith("gemini")

    if chat_style:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": args.prompt}],
            "modalities": ["image", "text"],
        }
        result = api_request(conf, "/chat/completions", payload, provider)
        image_b64 = extract_chat_image(result, provider)
        quality_note = "-"
    else:
        payload = {"model": model, "prompt": args.prompt, "size": args.size}
        if conf["quality"]:
            payload["quality"] = args.quality
        result = api_request(conf, "/images/generations", payload, provider)
        item = result["data"][0]
        if item.get("b64_json"):
            image_b64 = item["b64_json"]
        elif item.get("url"):
            with urllib.request.urlopen(item["url"], timeout=120) as img:
                image_b64 = base64.b64encode(img.read()).decode()
        else:
            sys.exit(f"返回内容中没有图片: {json.dumps(result, ensure_ascii=False)[:300]}")
        quality_note = payload.get("quality", "-")

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = args.out or str(DEFAULT_OUT_DIR / f"{provider}-{stamp}.png")
    out_path = pathlib.Path(out).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(base64.b64decode(image_b64))

    print(f"{out_path}  (provider={provider}, model={model}, quality={quality_note})")


if __name__ == "__main__":
    main()
