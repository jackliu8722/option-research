---
title: 三阶希腊字母：Speed / Zomma / Color
tags: [高阶希腊字母, Speed, Zomma, Color, Gamma]
level: 高级
prerequisites: [docs/02-希腊字母/02-Gamma.md, docs/10-高阶希腊字母与做市定位/01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md]
status: 完善中
updated: 2026-06-15
---

# 三阶希腊字母：Speed / Zomma / Color

> 二阶希腊字母管"Delta/Vega 怎么漂"，三阶则管 **Gamma 怎么漂**——Speed（Γ 随现货）、Zomma（Γ 随 IV）、Color（Γ 随时间）。它们对**大头寸/做市/临到期的高 Gamma 仓位**才显著，平时小，但在尾部和到期日会突然要命。

## 前置知识
- [02/02 Gamma](../02-希腊字母/02-Gamma.md)
- [10/01 二阶交叉希腊字母](./01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md)

---

## 1. 符号表（Notation）

| 符号 | 定义 | 含义 |
|---|---|---|
| Gamma | $e^{-q\tau} n(d_1)/(S\sigma\sqrt{\tau})$ | 二阶（见 [02/02](../02-希腊字母/02-Gamma.md)） |
| Speed | $\partial^3 V/\partial S^3=\partial\Gamma/\partial S$ | Gamma 随现货变化 |
| Zomma | $\partial\Gamma/\partial\sigma$ | Gamma 随 IV 变化 |
| Color | $\partial\Gamma/\partial t$ | Gamma 随时间变化 |

> 沿用 BSM 标杆：`S=K=60,000, τ=0.25, σ=80%, r=10%, q=0` → $d_1=0.2625,\ d_2=-0.1375$ ，Gamma $\approx 1.606\times10^{-5}$ 。

---

## 2. Speed：Gamma 随现货的变化 `推导`

$$ \boxed{\ \text{Speed} = \frac{\partial\Gamma}{\partial S} = -\frac{\Gamma}{S}\left(1+\frac{d_1}{\sigma\sqrt{\tau}}\right)\ } $$

**直觉**：现货一动，**Gamma 本身也变**（Gamma 不是常数）。

- 用处：大头寸/做市做 Delta 对冲时，Speed 决定"对冲比率随现货的二阶修正"——现货大幅跳时，光用 Gamma 线性外推 Delta 会有误差，Speed 是补偿项。
- 本例 ≈ **−4.43×10⁻¹⁰**（很小，但乘以大名义/大跳就显著）。

---

## 3. Zomma：Gamma 随 IV 的变化 `推导`

$$ \boxed{\ \text{Zomma} = \frac{\partial\Gamma}{\partial\sigma} = \Gamma\,\frac{d_1 d_2 - 1}{\sigma}\ } $$

**直觉**：IV 一变，**Gamma 也变**——衡量你的 Gamma 敞口在 IV 冲击下稳不稳。

- 本例 ≈ **−2.08×10⁻⁵**：IV 升时这张 ATM 期权的 Gamma 略降（ $d_1 d_2-1<0$ ）。
- 用处：高波动事件中，多头 Gamma 头寸的"Gamma 含金量"会随 IV 变化——Zomma 告诉你 Gamma scalping 的引擎是否被 IV 改变。

---

## 4. Color：Gamma 随时间的衰减 `推导`

$$ \text{Color} = \frac{\partial\Gamma}{\partial t} = e^{-q\tau}\frac{n(d_1)}{2S\tau\sigma\sqrt{\tau}}\left[\,2q\tau+1+\frac{2(r-q)\tau - d_2\sigma\sqrt{\tau}}{\sigma\sqrt{\tau}}\,d_1\,\right] $$

**直觉**：**Gamma 随到期临近怎么变**。ATM 临到期 Gamma 暴涨（[02/02](../02-希腊字母/02-Gamma.md)）——Color 就是这个"暴涨速度"（本例 ≈ **+3.4×10⁻⁵/年**，为正：时间流逝 Gamma 升），对**到期日附近的做市/0DTE**至关重要：你的 Gamma 一夜之间可能翻倍，对冲节奏要随之改。

---

## 5. 特例与检验

- **深虚/深实**（ $n(d_1)\to0$ ）：Speed/Zomma/Color 全 →0（Gamma 本身趋 0）。✓
- **ATM 临到期**（ $\tau\to0$ ）：Color/Speed 发散——Gamma 又高又快变，最难对冲。✓
- Zomma 在 $d_1 d_2=1$ 处变号。✓
- 数值校验：Speed、Zomma、Color 均已用 [`tools/option_strategy.py`](../../tools/option_strategy.py) 有限差分（含 Richardson 外推）复核，闭式与数值吻合。

---

## 6. 什么时候真要管这些

- **平时**：三阶希腊字母数值很小，散户单腿可忽略。
- **要命的时候**：① **大名义/做市簿**（小系数 × 大头寸 = 大风险）；② **临到期/0DTE**（Color/Speed 发散）；③ **加密尾部大跳**（[09/04 清算级联](../09-加密期权专题/04-DVOL与加密波动率特征.md)，现货瞬间大移使 Gamma 线性外推失效，Speed 补偿）。

---

## 7. 常见误区

- ❌ 以为 Gamma 是常数 → Speed/Color 说明它随现货和时间都在变。
- ❌ 用 Δ+Γ 线性外推应对大跳 → 大 $\Delta S$ 时需 Speed 的三阶修正。
- ❌ 临到期沿用平时对冲频率 → Color 让 Gamma 暴涨，必须加密对冲。

---

## 8. 关联
- [02/02 Gamma](../02-希腊字母/02-Gamma.md)、[10/01 二阶交叉希腊字母](./01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md)
- 下一篇：[03-做市商定位与 gamma 墙](./03-做市商定位与gamma墙.md)
- 工具：[`tools/option_strategy.py`](../../tools/option_strategy.py)（有限差分可复算）。

## 9. 参考来源
- Speed/Zomma/Color 定义与 BSM 闭式属 `公认结论`（Hull / Taleb《Dynamic Hedging》/ Haug《Option Pricing Formulas》）。
- Speed、Zomma、Color 闭式均由 [`tools/option_strategy.py`](../../tools/option_strategy.py) 有限差分复核（与数值吻合）`推导`。
