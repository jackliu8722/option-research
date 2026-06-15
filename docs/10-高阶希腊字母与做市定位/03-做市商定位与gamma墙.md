---
title: 做市商定位与 Gamma 墙（Dealer Positioning / GEX / Pinning）
tags: [做市, dealer gamma, GEX, gamma墙, 钉价, vanna flows, charm flows, 反身性]
level: 高级
prerequisites: [docs/02-希腊字母/02-Gamma.md, docs/10-高阶希腊字母与做市定位/01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md]
status: 完善中
updated: 2026-06-15
---

# 做市商定位与 Gamma 墙（Dealer Positioning / GEX / Pinning）

> 期权不是单向工具——**有人买就有做市商在对侧卖**。做市商为保持自己 Delta 中性而做的对冲，会**反过来推动标的**。理解"做市商净 Gamma 在哪边、被迫怎么对冲"，就能解释**钉价（pinning）、gamma 墙、vol-crush 后的 vanna 反弹、加密的 \$60K put wall**这类现象。这是从"交易者"到"专家"的分水岭。

## 前置知识
- [02/02 Gamma](../02-希腊字母/02-Gamma.md)（多/空 Gamma 的再对冲方向）
- [10/01 Vanna/Charm](./01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md)

---

## 1. 核心机制：做市商对冲方向 `公认结论`

做市商持有期权后做 Delta 对冲。**净 Gamma 的符号决定他们的对冲行为是"抑波"还是"助涨助跌"**：

| 做市商净 Gamma | 现货上涨时 | 现货下跌时 | 对市场的效果 |
|---|---|---|---|
| **多头 Gamma（long）** | Δ 变大 → **卖现货** | Δ 变小 → **买现货** | **高抛低吸 → 抑制波动**（均值回归、钉住） |
| **空头 Gamma（short）** | Δ 变更负 → **买现货** | Δ 变更正 → **卖现货** | **追涨杀跌 → 放大波动**（趋势、踩踏） |

- 这是 [02/02 Gamma scalping](../02-希腊字母/02-Gamma.md) 的"市场层"投影：你的再对冲就是别人看到的买卖盘。
- **关键问题**：整个市场的做市商**净 Gamma 在多头还是空头**？以及**在哪个价位翻转**？

---

## 2. GEX：把做市商 Gamma 按行权价加总 `推导`/`观点`

**Gamma Exposure（GEX）** 估计做市商在各行权价的净 Gamma 敞口（美元 Gamma × 未平仓量），常用假设"做市商**卖出 Call、买入 Put**"（传统股票经验）：

$$ \text{GEX} \approx \sum_i \Gamma_i \cdot S^2 \cdot 0.01 \cdot \text{OI}_i \cdot (\pm 1) $$

- $\pm1$ 按假设的做市商持仓方向（Call 一种符号、Put 另一种）。
- **Gamma 翻转点（zero-gamma / flip level）**：GEX 由正转负的价位。**在此之上多头 Gamma（抑波），之下空头 Gamma（放大）**——常被当作"波动率开关"。`观点·待核实`
- ⚠️ **GEX 是估计**：做市商真实持仓不可直接观测，靠"谁卖谁买"的假设；**加密的假设与股票未必相同**（见 §5）。

---

## 3. Gamma 墙与钉价（Pinning）`公认结论`（机制）/`观点`（强度）

- **Gamma 墙（gamma wall）**：某行权价 OI 极大 → 做市商在该价位 Gamma 极集中。若做市商**多头 Gamma**，临到期现货被"高抛低吸"**吸附到该行权价** = **钉价（pinning）**。
- **Charm flows 加剧钉价**：临到期 [Charm](./01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md)（Delta 时间漂移）大 → 做市商每天为 charm 再对冲，把现货往大 OI 行权价推。
- **Max pain**：到期时令期权买方总价值最小的行权价，常与钉价区域重合（相关而非因果）`观点`。
- 反过来，做市商**空头 Gamma** + 大墙被击穿 → 对冲变成追涨杀跌 → **加速突破**。

---

## 4. Vanna flows：vol-crush 驱动的"无量反弹" `推导`/`观点`

由 [Vanna](./01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md)（Δ 随 IV 漂移）：**IV 一降，做市商的 Delta 自动变化 → 被迫买/卖现货**。

- 经典：事件落地、[vol crush](../02-希腊字母/04-Vega.md) → 做市商（常空 put、随 IV 下降 Delta 上移）**买入现货** → **"利空出尽"式 vanna 反弹**，常无明显基本面消息。
- Vanna + Charm flows 是"OPEX（到期周）前后行情"的主流解释之一 `观点`。

---

## 5. 加密视角：put wall、清算级联与反身性

- **\$60K put wall（示例 `观点·待核实`）**：大量 BTC put 集中在某整数关口 → 做市商在该位 Gamma 集中。市场常把它当"支撑/磁吸"。
- **与清算级联叠加（加密特有，危险）**：若做市商在关口下方**空头 Gamma**，跌破后对冲转为**卖出**，又叠加 [永续清算级联](../09-加密期权专题/04-DVOL与加密波动率特征.md) → **下跌自我强化（反身性）**，比传统股票更猛、更快。
- **数据来源差异**：股票有 OCC/SqueezeMetrics 类 GEX 数据；**加密靠 Deribit 公开 OI + 第三方（Laevitas/Amberdata/Greeks.live）估算**，做市商方向假设更不确定 `待核实`。
- 加密做市商也可能**两边都做**（不一定"卖 Call 买 Put"），所以照搬股票 GEX 符号约定要谨慎。

---

## 6. 实操：把"做市商在做什么"纳入决策

- **判 regime**：估计 Gamma 翻转点——上方多头 Gamma（预期窄幅震荡，适合卖波动）、下方空头 Gamma（预期放大波动，慎卖、防踩踏）。`观点`
- **关注大到期 + 大墙**：季度到期、整数关口大 OI → 临到期留意钉价/突破。
- **事件后想 vanna**：vol crush 后的反弹常是结构性对冲流，不是基本面。
- **加密叠加清算图**：把 put wall / gamma 翻转点和清算热力图一起看，下方空 Gamma + 密集清算 = 高踩踏风险。

---

## 7. 常见误区

- ❌ 把 GEX/翻转点当精确真值 → 它建立在**做市商持仓假设**上，加密尤其不确定（`待核实`）。
- ❌ 以为"墙=铁支撑" → 多头 Gamma 才吸附；做市商空 Gamma 时墙被击穿会**加速**而非支撑。
- ❌ 把 max pain 当因果 → 它是相关现象，不是"庄家把价砸到 max pain"。
- ❌ 用股票 GEX 符号约定照搬加密 → 做市商方向假设不同。
- ❌ 忽视加密反身性 → 空 Gamma + 清算级联会让"支撑位"变"加速带"。

---

## 8. 关联
- [02/02 Gamma](../02-希腊字母/02-Gamma.md)、[10/01 Vanna/Charm](./01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md)
- [09/04 DVOL 与清算级联](../09-加密期权专题/04-DVOL与加密波动率特征.md)、[07 风险管理](../07-风险管理/)
- 市场观察落地：[research/market-notes](../../research/market-notes/)

## 9. 参考来源
- 做市商多/空 Gamma 的对冲方向与抑波/放大效应属 `公认结论`（Hull / 做市文献）。
- GEX、gamma 翻转点、pinning、vanna/charm flows 的**机制**为业界广泛使用，但**幅度与可预测性有争议**，标 `观点`；具体行权价/持仓方向 `待核实`（依赖第三方估算）。
- 加密 put wall、反身性叠加清算为市场观察 `观点·待核实`。
