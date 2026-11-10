---
name: gen-image
description: 当用户要求生成图片、画图、文生图（"生成一张…的图"、"画一个…"、"生图"）时使用。双平台：AiHubMix（GPT Image 2.5 / Nano Banana，第一梯队）与智谱 bigmodel（cogview-3-flash 免费）。
---

# 文生图（gen-image）

```bash
python3 ~/.zcode/skills/gen-image/generate.py "<描述>" [--provider aihubmix|bigmodel] [--model X] [--size WxH] [--quality low|medium|high|xhigh|max|auto] [--out 路径]
```

图片保存到 `~/Pictures/zcode-images/<provider>-<时间戳>.png`，脚本会打印路径和所用模型。

## 平台/模型选择

- **高质量、正式用图、"Codex 同档"** → `--provider aihubmix`（默认 `gpt-image-2.5-flare` + quality medium，1024x1024 约 $0.053/张）
- **精细交付图** → aihubmix + `--quality high`（约 $0.21/张，用户明确要求才用）
- **免费测试、草稿、构图确认** → `--provider bigmodel`（`cogview-3-flash`，免费）
- **想要 Nano Banana 风格** → aihubmix + `--model gemini-nano-banana-2.1`；上一代 `gpt-image-2`
- `--provider` 省略时自动选：有 aihubmix Key 用 aihubmix，否则 bigmodel

## 尺寸

- gpt-image：`1024x1024` / `1024x1536`（竖）/ `1536x1024`（横）
- cogview：`1024x1024` / `1440x720`（横）/ `720x1440`（竖）

## prompt 写法

把用户需求扩写成具体描述（主体、风格、光线、构图、文字内容）。图里要出现文字时，明确引号标注文字内容——这是 GPT Image 系的强项。

## 流程

1. 运行脚本，拿到打印出的图片路径
2. **在对话里展示图片（默认要做）**：
   ```bash
   python3 ~/.zcode/skills/gen-image/show.py --dir "<会话可视化目录>" <图片路径> [更多图片...]
   ```
   `<会话可视化目录>` 取自系统提示中 "Writable, durable visualization directory for this session" 的路径（每次会话不同，找不到该字段说明当前端不支持内联渲染）。
   命令会打印片段的绝对路径，在**最终回复里单独一行**按此格式引用（不加反引号、不加代码块、不写成 Markdown 链接）：
   `::visualize{"path":"<打印出的绝对路径>"}`
   多张图自动排成网格；片段超 1MB 会自动降分辨率。生成的原图（PNG 全尺寸）仍以 Markdown 链接附上，方便用户取原图。
3. 若当前端没有可视化目录：退回用 Read 查看图片确认效果，并以 Markdown 链接给出路径
4. 不满意时调整 prompt/质量/平台重出；报错原样转述（脚本不输出 Key）

## Key 管理

- 位置：`~/.config/zcode-image/aihubmix.key` 和 `~/.config/zcode-image/bigmodel.key`（权限 600）
- 也可用环境变量 `AIHUBMIX_API_KEY` / `ZHIPUAI_API_KEY`
- 任何情况下不把 Key 内容打印到对话或日志
- 用户未存 Key 时，让用户自己在终端运行：

```bash
bash -c 'mkdir -p ~/.config/zcode-image && chmod 700 ~/.config/zcode-image; read -s -p "粘贴 AiHubMix Key: " A; echo; [ -n "$A" ] && printf "%s" "$A" > ~/.config/zcode-image/aihubmix.key; read -s -p "粘贴 bigmodel Key: " B; echo; [ -n "$B" ] && printf "%s" "$B" > ~/.config/zcode-image/bigmodel.key; chmod 600 ~/.config/zcode-image/*.key 2>/dev/null; ls -l ~/.config/zcode-image/; echo 完成'
```
