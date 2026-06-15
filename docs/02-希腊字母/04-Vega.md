---
title: Vega：对隐含波动率的敏感度
tags: [希腊字母, Vega, 波动率, IV]
level: 进阶
prerequisites: [docs/02-希腊字母/03-Theta.md, docs/00-基础概念/04-期权价格的直觉.md]
status: 完善中
updated: 2026-06-15
---

# Vega：对隐含波动率的敏感度

> [00/04 比较静态表](../00-基础概念/04-期权价格的直觉.md) 说"σ 升、Call 和 Put 都变贵"。**Vega 就是这条的数字版——你对隐含波动率（IV）的敞口。** 在加密这种 IV 又高又跳的市场，Vega 往往是仓位里最大的隐藏风险（想想事件后的 vol crush）。核心结论： $\mathcal{V} = S e^{-q\tau} n(d_1)\sqrt{\tau}$ ，Call/Put 相同且恒正。

## 前置知识
- [03-Theta](./03-Theta.md)、[04-期权价格的直觉](../00-基础概念/04-期权价格的直觉.md)
- [03-BSM 模型](../03-定价模型/03-BSM模型.md)、[09/04 DVOL](../09-加密期权专题/04-DVOL与加密波动率特征.md)

---

## 1. 符号表（Notation）

| 符号 | 含义 | 单位/口径 |
|---|---|---|
| $S,\ K,\ \tau,\ \sigma,\ q$ | 见 [01-Delta](./01-Delta.md) | — |
| $\mathcal{V}$ | $\partial V/\partial\sigma$ | USD / 1.0 vol（÷100 = 每 1%） |
| $n(d_1)$ | 正态密度在 $d_1$ | — |

## 2. 直觉：IV 动 1 个点，期权动多少

**Vega（𝒱）= 隐含波动率变动 1 个百分点时，期权价格的变动量。**

$$ \mathcal{V} = \frac{\partial V}{\partial \sigma}\quad(\text{per 1\% vol}) $$

- **买入期权（long call / long put）→ Vega 为正**：IV 升值钱、IV 跌亏钱（Call/Put 同号）。
- **卖出期权 → Vega 为负**。

---

## 3. 分布：哪里 Vega 最大

- **ATM 附近 Vega 最大**（与 Gamma、Theta 同样在 ATM 最大）。
- **到期越远，Vega 越大**：长到期对 IV 更敏感（ $\sqrt{\tau}$ 因子，时间越长波动率假设的累积影响越大）。
- 深实值/深虚值 Vega 小。

---

## 4. 公式与推导

**结论（先给出）**：

$$ \boxed{\ \mathcal{V} = S e^{-q\tau} n(d_1)\sqrt{\tau}\ } $$

（Call/Put 相同且恒正；这是 per 1.0 vol，实务每 1% 用 $\mathcal{V}/100$ 。）

**逐步推导** `推导`：

1. 对 Call 闭式求 $\partial/\partial\sigma$ ： $\mathcal{V} = S e^{-q\tau} n(d_1)\dfrac{\partial d_1}{\partial\sigma} - K e^{-r\tau} n(d_2)\dfrac{\partial d_2}{\partial\sigma}$ 。
2. 同 [Delta 篇](./01-Delta.md) 的恒等式 $S e^{-q\tau} n(d_1) = K e^{-r\tau} n(d_2)$ ，两项合并为 $S e^{-q\tau} n(d_1)\Big(\dfrac{\partial d_1}{\partial\sigma}-\dfrac{\partial d_2}{\partial\sigma}\Big)$ 。
3. 由 $d_2 = d_1 - \sigma\sqrt{\tau}$ 得 $\dfrac{\partial d_1}{\partial\sigma}-\dfrac{\partial d_2}{\partial\sigma} = \sqrt{\tau}$ ，即得结论。
4. 因 $C-P$ 与 $\sigma$ 无关（[平价](../03-定价模型/01-平价公式.md)），**Vega 两者相同**；又 $n>0$ → **恒正**（IV 是单调的，[这保证 IV 反解唯一](../03-定价模型/04-隐含波动率与模型校准.md)）。

**各项含义**： $n(d_1)$ 在 ATM 最大； $\sqrt{\tau}$ 让长到期 Vega 大——所以**选长到期就是选 Vega 敞口**。

## 5. 特例与极限检验

- **临到期**（ $\tau\to0$ ）： $\sqrt{\tau}\to0$ ， $\mathcal{V}\to0$ 。✓
- **深实值/深虚值**（ $|d_1|\to\infty$ ）： $n(d_1)\to0$ ， $\mathcal{V}\to0$ 。✓
- **ATM**： $n(d_1)$ 接近峰值 $\approx0.399$ ， $\mathcal{V}$ 最大。✓

## 6. 敏感度 / 比较静态

| 输入 ↑ | $\mathcal{V}$ 变化（ATM） | 直觉 |
|---|---|---|
| $\tau$ | ↑ | 长到期更吃 IV |
| $S$ 偏离 $K$ | ↓ | 离 ATM 越远越小 |
| $\sigma$ | 缓变 | ATM Vega 对 σ 本身较稳 |

---

## 7. Vega vs Gamma：都关乎波动，但不是一回事 `公认结论`

| | Gamma | Vega |
|---|---|---|
| 关注 | **已实现**波动（标的真的动） | **隐含**波动（IV 报价变） |
| 触发 | 标的 $S$ 变动 | 市场 IV 变动 |
| 期限偏好 | **短到期最大** | **长到期最大** |
| 你赚/亏自 | 实际大幅波动（scalping） | IV 涨跌 |

- 短到期：高 Gamma、低 Vega → 玩"真波动"；长到期：低 Gamma、高 Vega → 玩"IV 水平"。**选到期 = 选你要 Gamma 还是 Vega。**

---

## 8. Vega 与"vol crush"（加密尤其要命）

事件（ETF 裁决、减半、FOMC、大额解锁）前 IV 常被推高；**事件落地后 IV 骤降，叫 vol crush**。

- 事件前**买期权（多头 Vega）赌方向**：哪怕方向对，事件后 IV 暴跌也可能让期权亏钱——**方向赢了，Vega 输了**。
- 反过来，事件前**卖 IV（空头 Vega）**赚的就是这波 crush，但要扛事件当天的 Gamma 跳动风险。
- 加密 IV 量级与波动远超股票（[DVOL 篇](../09-加密期权专题/04-DVOL与加密波动率特征.md)），**Vega 盈亏经常盖过 Delta 盈亏**。

**组合 Vega 与曲面**：组合 Vega 可加，但不同到期/行权价的 IV 不齐步走（[波动率曲面](../04-波动率/)）——"净 Vega=0"不代表对波动免疫，还有**期限结构风险、skew 风险**（日历价差就是押期限结构的 Vega 交易）。

---

## 9. 算例（与 BSM 篇自洽）

沿用 [BSM 算例](../03-定价模型/03-BSM模型.md)：`S=60,000`、`K=60,000`、`τ=0.25`、`σ=80%`、`q=0`， $n(d_1)=0.38543$ 。

$$ \mathcal{V} = 60{,}000 \times 0.38543 \times \sqrt{0.25} \approx 11{,}563\ (\text{per }1.0) \;\Rightarrow\; \mathbf{115.6}\ \text{USD/1\%} $$

- IV 从 80% 升到 90%（+10 点）：这张 Call 约 +\$1,156；DVOL crush −20 点：约 −\$2,313。
- **组合 vol crush**：净 𝒱 = +\$300/1%，DVOL 从 85% 跌到 65%（−20）→ Vega PnL ≈ 300 × (−20) = −\$6,000：即便方向没错、标的没动，单 IV 回落就亏 \$6,000。
- **币口径**： $\mathcal{V}_{\text{btc}}=\mathcal{V}_{\text{usd}}/S$ （Vega 可简单除 $S$ ，见 [07 单位篇](./07-币本位希腊字母的单位与换算.md)）。

---

## 10. 常见误区

- ❌ 把 Vega 和 Gamma 混为一谈 → 一个隐含、一个已实现；期限偏好相反。
- ❌ 买期权只赌方向、不看 IV 高低 → 高 IV 买入容易吃 vol crush。
- ❌ 以为净 Vega=0 就对波动免疫 → 还有期限结构 / skew 的曲面风险。
- ❌ 忽略加密 Vega 的量级 → DVOL 动辄十几二十点，Vega 盈亏常是主导项。

---

## 11. 关联
- [02-Gamma](./02-Gamma.md)（对照）、[03-Theta](./03-Theta.md)
- 下一篇：[05-Rho](./05-Rho.md) — 利率敏感度
- [03-BSM 模型](../03-定价模型/03-BSM模型.md)、[04-波动率](../04-波动率/)、[09/04 DVOL](../09-加密期权专题/04-DVOL与加密波动率特征.md)、[07 币本位单位](./07-币本位希腊字母的单位与换算.md)
- 工具：[`tools/option_strategy.py`](../../tools/option_strategy.py) 的 `bsm_greeks`。

## 12. 参考来源
- Vega 定义、ATM/长到期最大、Vega 与 Gamma 的期限对比、vol crush、闭式 $\mathcal{V}=Se^{-q\tau}n(d_1)\sqrt\tau$ 属 `公认结论`（Hull 第 19 章 / Natenberg）。
- 算例由 [`tools/option_strategy.py`](../../tools/option_strategy.py) 复算，与 [BSM 篇](../03-定价模型/03-BSM模型.md) 自洽 `推导`。
