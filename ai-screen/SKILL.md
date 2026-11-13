---
name: ai-screen
description: "AI 隐形工作台:在用户完全看不见的分层空间里干活(无头浏览器/隐藏窗口/虚拟屏)。任何 GUI 类任务(开浏览器、试 App、测 UI、跑带窗口的程序)都应先走本 skill 的分层路由,保证用户屏幕零打扰。"
---

# ai-screen — AI 隐形工作台

目的:**"AI 干活不吵用户"是默认状态**。你的窗口、测试、浏览器全部发生在用户看不见的层里,你照样能看见每一个工作对象的像素。

工具:`~/tools/ai-screen/bin/aiscreen`(下文简写 `$AIS`)。改动源码后 `make -C ~/tools/ai-screen build`。

## 分层路由(先判断,再动手)

| 判定 | 层 | 做法 |
|---|---|---|
| 活在浏览器/网页里? | **L1** | browser-use 的 headless 模式(`--browser-use=headless`,受管无头 Chromium)。不开任何可见窗口 |
| 活在一般 App 窗口里,只需要看**内容/做交互**? | **L2** | 窗口停 1px straddle(见下)+ `aiscreen hide --app`;`aiscreen capture --window <id>` 看内容;AX(osascript System Events / computer-use 插件)做交互。已验证:隐藏后仍持续渲染动画,截图照常 |
| 要验证**真实桌面合成效果**(透明、阴影、置顶覆盖、贴桌面的观感)? | **L3** | `aiscreen screen create` 造虚拟屏 → `aiscreen place --window <id> --display <id>` 安放 → `aiscreen capture --display <id>` 按屏截帧验收 → 用完 `aiscreen screen remove` |

L2 的"1px straddle"标准形态:窗口用 borderless、右下角只留 1 像素与屏幕相交(NS 坐标:`x=screen.maxX-1, y=-(h-1)`),视觉不可感知。**窗口必须落在这个形态,截图/渲染链路才活**(完全屏外=从未合成,截图只剩废弃 legacy API)。

## 纪律红线(硬性,违反=事故)

1. **严禁任何可见窗口出现在用户屏幕**;1px straddle 是唯一允许的"可见"(不可感知)
2. **严禁有头浏览器定位到屏外**——Chromium 会钳回屏上闪现(实测事故);浏览器一律 headless
3. **全透明窗口判死**:截图被 alpha 量化毁掉,看不见内容
4. **操作窗口后至少等 0.6–1.5s 再截图**(合成延迟,立即截=假失败)
5. `aiscreen screen remove`/BetterDisplay `discard` 必须带明确目标,裸删=删掉全部屏
6. 完全屏外窗口截图只能走 legacy `CGWindowListCreateImage`(SDK 已废弃,随时可能移除)——只作兜底,不作主力
7. 用户在办公时,不跑 `aiscreen doctor --full`(造屏会让菜单栏/调度中心闪变化);造屏类操作放在用户方便的时间
8. 截屏是被动读操作,可以放心;但**截到的内容是用户数据**,不得外传
9. **镜像窗(`aiscreen mirror`)仅限用户主动要求时开启**——它是"给用户看的观察窗",不是 AI 的工作需要;AI 不得自行 mirror 打扰用户

## 已知坑(踩过的,别再踩)

- **AX 树发布依赖完整 AppKit 生命周期**:裸 swiftc 程序没跑 `NSApplication.run()`(finishLaunching),它的窗口在 System Events/AX 里**根本不存在**(COUNT=0)。做测试窗口必须 `app.run()`。正常启动的第三方 App 无此问题
- 主线程堵死(信号量 wait)→ runloop 不跑 → 计时器不触发、窗口不合成、截图全败。探针/测试程序:主线程跑 `app.run()`,实验逻辑放后台线程
- offscreen 窗口的 CGWindowList 坐标可能被折叠(如报 0,0),**不要用 CG 窗口坐标判断屏外窗口真实位置**,以你自己设置的 frame 为准
- TCC 前提:屏幕录制 + 辅助功能两项授权(本机已授;`aiscreen doctor` 可查)。TCC 绑定签名身份——rebuild 后授权若失效,用固定签名身份重签
- `screencapture -D <N>` 的 N 是枚举序号,屏插拔会漂移;脚本里用 `aiscreen screen list` 现查 displayID

## 一分钟上手

```bash
AIS=~/tools/ai-screen/bin/aiscreen
$AIS doctor                    # 自检(TCC/类族/显示器)
$AIS screen create             # 造受管虚拟屏(L3;有可见变化,择时)
$AIS screen list               # 看 displayID
$AIS place --app Safari --display <id>   # 把某 App 主窗安到虚拟屏
$AIS capture --display <id> -o /tmp/x.png  # 我看这块屏
$AIS capture --window <id> -o /tmp/w.png   # 看单个窗口(隐藏窗口也行)
$AIS hide --app <pid|名>       # App 级隐形(进程活着,AX/截图照常)
$AIS unhide --app <pid|名>
$AIS screen remove             # 删屏(异步,1–2 秒后消失)
```

## 与 ai-deskpet 项目的关系

桌宠是本能力的**第一个客户**:它的自测(动画帧核对/聊天窗验证/48h 实测观察)全部在 L3 虚拟屏上进行,验收截屏走 `capture --display`。规格见 `~/.zcode/workspace/draft-2f29189c-a1e1-4228-bdda-49ec48d1c726/spec.md`;调研证据:该仓库 `research/05*-*.md`。
