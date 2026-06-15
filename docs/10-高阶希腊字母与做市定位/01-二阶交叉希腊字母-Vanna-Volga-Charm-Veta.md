---
title: 二阶交叉希腊字母：Vanna / Volga / Charm / Veta
tags: [高阶希腊字母, Vanna, Volga, Charm, Veta, 做市, 推导]
level: 高级
prerequisites: [docs/02-希腊字母/06-组合希腊字母与关系.md, docs/03-定价模型/03-BSM模型.md, docs/04-波动率/02-波动率微笑与偏斜.md]
status: 完善中
updated: 2026-06-15
---

# 二阶交叉希腊字母：Vanna / Volga / Charm / Veta

> 一阶希腊字母（[Δ/Γ/Θ/𝒱/ρ](../02-希腊字母/)）只描述各风险的"一阶斜率"。专家/做市要管的是它们**怎么随别的变量漂移**——这就是二阶**交叉**希腊字母：Vanna（Δ 随 IV 漂）、Volga（Vega 随 IV 漂）、Charm（Δ 随时间漂）、Veta（Vega 随时间漂）。它们是 **skew 交易、vol-of-vol、隔夜/到期对冲漂移** 的语言。

## 前置知识
- [02/06 组合希腊字母](../02-希腊字母/06-组合希腊字母与关系.md) — 一阶全套与泰勒展开
- [03 BSM](../03-定价模型/03-BSM模型.md)、[04/02 微笑偏斜](../04-波动率/02-波动率微笑与偏斜.md)

---

## 1. 符号表（Notation）

| 符号 | 定义 | 含义 |
|---|---|---|
| $d_1,\ d_2$ | BSM 中间量 | $d_2=d_1-\sigma\sqrt{\tau}$ |
| $n(d_1)$ | 标准正态密度 | — |
| Vega | $S e^{-q\tau} n(d_1)\sqrt{\tau}$ | 一阶 IV 敏感度（per 1.0 vol） |
| Vanna | $\partial^2 V/\partial S\,\partial\sigma$ | = ∂Δ/∂σ = ∂Vega/∂S |
| Volga | $\partial^2 V/\partial\sigma^2$ | = ∂Vega/∂σ（又名 Vomma） |
| Charm | $\partial^2 V/\partial S\,\partial t$ | = ∂Δ/∂t（Delta 随时间漂移） |
| Veta | $\partial^2 V/\partial\sigma\,\partial t$ | = ∂Vega/∂t（Vega 随时间衰减） |

> 沿用 BSM 标杆：`S=K=60,000, τ=0.25, σ=80%, r=10%, q=0` → $d_1=0.2625,\ d_2=-0.1375,\ n(d_1)=0.38543$ ，Vega(1.0)=11,563。

---

## 2. Vanna：Delta 对 IV 的敏感度 `推导`

**结论（先给出）**：

$$ \boxed{\ \text{Vanna} = \frac{\partial \Delta}{\partial \sigma} = -\,e^{-q\tau}\,n(d_1)\,\frac{d_2}{\sigma}\ } $$

**直觉**：IV 一变，你的 **Delta 就跟着变**（等价地：现货一动，你的 **Vega 就变**）。

- **为什么做 skew 必须看 Vanna**：[风险逆转](../04-波动率/02-波动率微笑与偏斜.md)（买一侧虚值、卖另一侧）是**纯 Vanna 头寸**——它方向中性、Vega 也可中性，赚的就是"IV 与现货一起动"的相关性。
- 符号：ATM 略实值时 $d_2<0$ → Vanna>0（本例 +0.0662 per 1.0 vol，即每 +1% IV，Delta 约 +0.00066）。

---

## 3. Volga（Vomma）：Vega 对 IV 的敏感度 `推导`

$$ \boxed{\ \text{Volga} = \frac{\partial \text{Vega}}{\partial \sigma} = \text{Vega}\cdot\frac{d_1 d_2}{\sigma}\ } $$

**直觉**：期权价值对 IV 是否"凸"——即你的 **Vega 会不会随 IV 放大**。这是 **vol-of-vol（波动率的波动）** 敞口。

- **符号**：ATM 附近 $d_1>0>d_2$ → $d_1 d_2<0$ → **Volga<0**（本例 −521.7）；深虚/深实两翼 $d_1,d_2$ 同号 → **Volga>0**。
- **谁是多头 Volga**：买**两翼/宽跨**（OTM 期权）→ 正 Volga，赌"IV 自己会剧烈波动"。卖 ATM → 负 Volga。
- Vanna+Volga 是 **Bartlett / vanna-volga 定价法**的核心，业界用来把 ATM 报价 + RR + BF 拼出整条微笑。

---

## 4. Charm：Delta 的时间漂移（delta decay / bleed）`推导`

$$ \text{Charm}_{\text{call}} = \frac{\partial \Delta}{\partial t} = e^{-q\tau}\!\left[\,q\,N(d_1) - n(d_1)\,\frac{2(r-q)\tau - d_2\,\sigma\sqrt{\tau}}{2\tau\,\sigma\sqrt{\tau}}\,\right] $$

**直觉**：**就算现货一动不动**，光是时间流逝，你的 Delta 也会漂。本例 ≈ −0.2024/年 ≈ **−0.000554/天**。

- **实务杀伤**：一个隔夜/周末，Delta 中性的盘会"自己跑偏"，要补对冲——这叫 **delta bleed**。
- **临到期 + ATM 时 Charm 巨大**：到期日附近做市商为 charm 反复再对冲 → 产生 **charm flows**，是标的被"钉"在大行权价附近的成因之一（见 [03 做市定位](./03-做市商定位与gamma墙.md)）。

---

## 5. Veta：Vega 的时间衰减 `推导`

$$ \text{Veta} = \frac{\partial \text{Vega}}{\partial t} = S e^{-q\tau} n(d_1)\sqrt{\tau}\left[\,q + \frac{(r-q)d_1}{\sigma\sqrt{\tau}} - \frac{1+d_1 d_2}{2\tau}\,\right] $$

**直觉**：**Vega 也会随到期临近而缩水**（本例 ≈ −21,532/年）。长到期 Vega 大、临到期 Vega 塌——这正是 [日历价差](../06-组合策略/03-日历与对角价差.md) 押"近月 Vega 塌得比远月快"的来源。

---

## 6. 特例与检验

- **Vanna 在 ATM 远期**（ $d_2=0$ ）= 0：此时 Delta 对 IV 不敏感。✓
- **Volga 在 $d_1 d_2=0$ 处变号**：从 ATM（负）走向两翼（正），所以**宽跨/两翼是正 Volga**。✓
- **Charm/Veta 随 $\tau\to0$ 发散**：临到期 Delta/Vega 的时间漂移最猛（与 [Gamma/Theta 临到期爆大](../02-希腊字母/02-Gamma.md) 同源）。✓
- 数值校验：本篇全部闭式已用 [`tools/option_strategy.py`](../../tools/option_strategy.py) 的有限差分复核（误差 <2%）。

---

## 7. 算例（与 BSM 标杆自洽）

代入 $d_1=0.2625,\ d_2=-0.1375$ ：

| 高阶希腊字母 | 闭式代入 | 值 |
|---|---|---|
| Vanna | −0.38543 × (−0.1375) ÷ 0.80 | **+0.0662**（per 1.0 vol） |
| Volga | 11,563 × (0.2625 × (−0.1375)) ÷ 0.80 | **−521.7** |
| Charm（/年） | 见 §4 公式代入 | **−0.2024** → −0.000554/天 |
| Veta（/年） | 见 §5 公式代入 | **−21,532** |

读法：IV 升 1% → Delta 约 +0.00066（Vanna）；这张 ATM 期权是**负 Volga**（卖方对 vol-of-vol 不利）；每过一天 Delta 自己漂 −0.00055（Charm，需补对冲）。

---

## 8. 加密视角

- 加密 **skew 会翻转 + DVOL 剧烈波动** → Vanna/Volga 敞口经常比传统更大、更不稳定（[04/02](../04-波动率/02-波动率微笑与偏斜.md)、[09/04](../09-加密期权专题/04-DVOL与加密波动率特征.md)）。
- **7×24 没有周末间断**，但大额到期（季度）前后 Charm flows 依然明显（见 [03 做市定位](./03-做市商定位与gamma墙.md)）。
- 币本位下这些高阶量也有口径换算（思路同 [07 单位篇](../02-希腊字母/07-币本位希腊字母的单位与换算.md)）。

---

## 9. 常见误区

- ❌ 只对冲一阶（Δ/Vega）就以为中性 → skew 头寸的 Vanna、隔夜的 Charm 会让"中性"漂掉。
- ❌ 把 Volga 当 Vega → Vega 是斜率、Volga 是**对 IV 的凸性**；卖 ATM 看着 Vega 中性，仍是负 Volga，IV 暴动会亏。
- ❌ 忽略 Charm → 周末/临到期 Delta 自己跑偏，不补对冲会吃方向亏。
- ❌ 用股票 skew 先验套加密 → 加密 RR 会翻转，Vanna 符号随之变。

---

## 10. 关联
- [02/06 组合希腊字母](../02-希腊字母/06-组合希腊字母与关系.md)、[02/04 Vega](../02-希腊字母/04-Vega.md)
- 下一篇：[02-三阶希腊字母 Speed/Zomma/Color](./02-三阶希腊字母-Speed-Zomma-Color.md)
- [04/02 微笑偏斜](../04-波动率/02-波动率微笑与偏斜.md)（RR=Vanna、BF=Volga 的交易对象）、[03 做市定位](./03-做市商定位与gamma墙.md)
- 工具：[`tools/option_strategy.py`](../../tools/option_strategy.py)（有限差分可复算高阶希腊字母）。

## 11. 参考来源
- Vanna/Volga/Charm/Veta 定义与 BSM 闭式属 `公认结论`（Hull / Taleb《Dynamic Hedging》/ Castagna-Mercurio vanna-volga）。
- 本篇闭式与算例由 [`tools/option_strategy.py`](../../tools/option_strategy.py) 有限差分复核，与 [BSM 篇](../03-定价模型/03-BSM模型.md) 自洽 `推导`。
