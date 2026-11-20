# Orca 编排层：非侵入平行技能族 + review 外置 + 全面板

在已验证的 matt 技能链之上加 Orca 编排层时，我们决定**新增平行技能族**（`pgrill-with-docs` 统一入口兼协调者 + `pimplement` tdd-only 变体，源仅 `~/.agents/skills`、不软链），**原 ship/implement/implement-spec 一字不改**；code-review 从 implement 内部**外置成独立缝**（standard 全票落地后一次 integration review，light 单次 implement 后一次），工人一律**结构化聊天面板**而非终端 TUI。因为原链在日常使用、改它会污染已验证资产；review 外置才能让该缝独立换底座/模型；面板走 structured chat 不依赖 headless CLI（绕开 zcode 无 headless 的坑）。

## Considered Options

- 改原 ship/implement 加 Orca 模式：否——污染日常在用的已验证链。
- n8n / Dify 作编排层：否——n8n 运行中人机对话弱 + 2.0 默认禁 shell 节点；Dify 沙箱禁宿主 shell（见 `research/orchestrator-platform-selection-2026-11.md`）。
- 终端 TUI 工人：否——依赖 headless CLI（zcode 缺）且 UI 不如面板；面板 structured chat 已用 env 端点跑通、无官方登录墙。
- review 内置于 implement：否——该缝无法独立换底座/模型。

## Consequences

- 新族只读组合原技能（grill/to-spec/to-tickets/code-review/accept/tdd/retro），原链零改动。
- 协调者 = Orca 内 agent 面板会话（wake 自动推进）；外部脚本协调（--from + 只读 poll）仅 fallback。
- 缝位配置 `docs/agents/orca-seams` 用户可编辑；模型路由起步 Orca agent profiles，聚合网关后置。
- 新技能源仅 `~/.agents/skills`；**claude 侧补相对软链**（`~/.claude/skills`，既有拓扑，使 claude/Orca 可 invoke；2026-11-20 修订：原"不软链"本意仅指 zcode 侧）；**zcode 侧不软链**、不补 zcode 缺失链。