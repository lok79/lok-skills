#!/usr/bin/env python3
"""把已生成的图片打包成 ZCode 对话内可渲染的 Gen UI 片段。

用法：
  python3 show.py --dir <会话可视化目录> 图1.png [图2.png ...]

输出一个 <时间戳>-gallery.html。把打印出的绝对路径按以下格式放在回复末尾
（单独一行，不加反引号/代码块）：
  ::visualize{"path":"<输出的绝对路径>"}

图片用 macOS 自带 sips 压成 JPEG 并以 base64 内嵌——片段自包含，
不依赖本地路径（沙箱 CSP 禁止加载外部/本地资源）。总量超限时自动降低分辨率。
"""
import argparse
import base64
import datetime
import pathlib
import subprocess
import sys
import tempfile

MAX_TOTAL_BYTES = 900_000  # 官方建议片段 < 1MB，留余量


def to_jpeg_bytes(png: pathlib.Path, max_px: int, quality: int) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        out = tmp.name
    try:
        subprocess.run(
            ["sips", "-Z", str(max_px), "-s", "format", "jpeg",
             "-s", "formatOptions", str(quality), str(png), "--out", out],
            check=True, capture_output=True,
        )
        return pathlib.Path(out).read_bytes()
    finally:
        pathlib.Path(out).unlink(missing_ok=True)


def build_fragment(items, root_id):
    figures = []
    for path, b64 in items:
        figures.append(
            '<figure style="margin:0">'
            f'<img src="data:image/jpeg;base64,{b64}" alt="{path.stem}" '
            'style="width:100%;height:auto;display:block;border-radius:8px" />'
            '<figcaption style="font-size:12px;color:var(--muted-foreground);'
            f'margin-top:4px">{path.stem}</figcaption>'
            "</figure>"
        )
    grid = (
        '<div style="display:grid;gap:12px;'
        'grid-template-columns:repeat(auto-fit,minmax(260px,1fr));'
        f'align-items:start">{"".join(figures)}</div>'
    )
    return f'<div id="{root_id}">{grid}</div>'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="+", help="要展示的图片路径（1 张或多张）")
    parser.add_argument("--dir", required=True,
                        help="当前会话的可视化目录（取自系统提示）")
    parser.add_argument("--max-px", type=int, default=640)
    parser.add_argument("--quality", type=int, default=75)
    args = parser.parse_args()

    out_dir = pathlib.Path(args.dir).expanduser()
    if not out_dir.is_dir():
        sys.exit(f"可视化目录不存在: {out_dir}")

    max_px, quality = args.max_px, args.quality
    while True:
        items = []
        for raw in args.images:
            path = pathlib.Path(raw).expanduser()
            if not path.exists():
                sys.exit(f"图片不存在: {path}")
            raw_bytes = to_jpeg_bytes(path, max_px, quality)
            items.append((path, base64.b64encode(raw_bytes).decode("ascii")))
        total_b64 = sum(len(b) for _, b in items)
        if total_b64 <= MAX_TOTAL_BYTES or max_px <= 360:
            break
        max_px, quality = int(max_px * 0.8), max(60, quality - 5)

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = out_dir / f"{stamp}-gallery.html"
    out.write_text(build_fragment(items, f"img-gallery-{stamp}"), encoding="utf-8")
    print(out.resolve())


if __name__ == "__main__":
    main()
