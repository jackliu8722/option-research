# 期权知识库与策略研究

从 0 构建的**期权知识库 + 策略研究工作区**。主要研究**加密货币期权**（BTC/ETH，以 Deribit 为主），以**通用理论为骨架**、加密市场为主要落地场景，传统市场（美股/A股）作为对照。

- 协作约定与内容规范见 [CLAUDE.md](./CLAUDE.md)
- AI 助手的角色与工作流见 [AGENT.md](./AGENT.md)

> **进度**：docs 教学章 00–09 已完成初稿；strategies/ 已建 19 张策略卡片。涉及平台具体规则/数字处标注 `待核实`，待对官方文档核实。

## 学习路线（docs/）

| 章节 | 主题 | 状态 |
|------|------|------|
| [00-基础概念](./docs/00-基础概念/) | 期权是什么、买/卖方、看涨/看跌、行权、到期、内在/时间价值 | ✅ |
| [01-合约与机制](./docs/01-合约与机制/) | 合约规格、乘数、保证金、行权交割、各市场规则对照 | ✅ |
| [02-希腊字母](./docs/02-希腊字母/) | Delta / Gamma / Theta / Vega / Rho 及其关系、币本位单位 | ✅ |
| [03-定价模型](./docs/03-定价模型/) | 平价公式(PCP)、二叉树、Black-Scholes-Merton、隐含波动率（含推导）| ✅ |
| [04-波动率](./docs/04-波动率/) | HV / IV、波动率微笑/曲面、期限结构、VIX / DVOL | ✅ |
| [05-基础策略](./docs/05-基础策略/) | 单腿、备兑、保护、垂直价差 | ✅ |
| [06-组合策略](./docs/06-组合策略/) | 跨式/宽跨、蝶式、铁鹰、日历/对角、比率、选择框架 | ✅ |
| [07-风险管理](./docs/07-风险管理/) | 仓位、组合希腊字母、压力测试、平台风险、纪律复盘 | ✅ |
| [08-进阶与量化](./docs/08-进阶与量化/) | 波动率交易(对冲PnL推导)、VRP、曲面建模、回测、数据 | ✅ |
| [09-加密期权专题](./docs/09-加密期权专题/) | 币本位/反向、资金费率对冲、r、DVOL、交易所、链上、特有风险 | ✅ |

## 策略卡片库（strategies/）

- **单腿**：[买入看涨](./strategies/买入看涨-long-call.md) · [买入看跌](./strategies/买入看跌-long-put.md) · [卖出看涨](./strategies/卖出看涨-short-call.md) · [卖出看跌](./strategies/卖出看跌-short-put.md)
- **持仓+期权**：[备兑开仓](./strategies/备兑开仓-covered-call.md) · [保护性看跌](./strategies/保护性看跌-protective-put.md)
- **垂直价差**：[牛市看涨](./strategies/牛市看涨价差-bull-call-spread.md) · [熊市看跌](./strategies/熊市看跌价差-bear-put-spread.md) · [牛市看跌](./strategies/牛市看跌价差-bull-put-spread.md) · [熊市看涨](./strategies/熊市看涨价差-bear-call-spread.md)
- **波动率/中性**：[多头跨式](./strategies/多头跨式-long-straddle.md) · [空头跨式](./strategies/空头跨式-short-straddle.md) · [多头宽跨式](./strategies/多头宽跨式-long-strangle.md) · [空头宽跨式](./strategies/空头宽跨式-short-strangle.md) · [铁鹰](./strategies/铁鹰-iron-condor.md) · [多头蝶式](./strategies/多头蝶式-long-butterfly.md)
- **期限/比率**：[多头日历](./strategies/多头日历价差-long-calendar.md) · [对角](./strategies/对角价差-diagonal-spread.md) · [看涨比率价差](./strategies/看涨比率价差-call-ratio-spread.md)

## 其它目录

- [strategies/](./strategies/) — 策略卡片库（每个策略一份结构化文档）
- [research/](./research/) — 研究笔记：`market-notes/` 市场观察、`journal/` 实盘复盘
- [references/](./references/) — [术语表](./references/术语表.md)、[书单与资源](./references/书单与资源.md)
- [tools/](./tools/) — 量化分析工具（`option_strategy.py`：BSM/希腊字母/组合盈亏/压力测试，纯标准库）
- [templates/](./templates/) — 写作模板

## 免责声明

本仓库仅供期权学习与研究，**不构成投资建议**。期权交易高风险，可能损失全部本金甚至更多。
