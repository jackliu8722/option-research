---
title: 波动率交易与 Delta 对冲下的 PnL（含推导）
tags: [进阶, 量化, 波动率交易, Delta对冲, PnL, 推导]
level: 高级
prerequisites: [docs/02-希腊字母/03-Theta.md, docs/03-定价模型/03-BSM模型.md]
status: 完善中
updated: 2026-06-11
---

# 波动率交易与 Delta 对冲下的 PnL（含推导）

> 把期权 Delta 对冲后，剩下的盈亏几乎只取决于一件事：**已实现波动 vs 隐含波动谁高**。本篇**推导**这条核心结论——Delta 对冲组合每天的盈亏 $\approx \tfrac{1}{2}\,\Gamma S^2(\sigma_{\text{real}}^2-\sigma_{\text{imp}}^2)\,dt$ ——它把 [Theta](../02-希腊字母/03-Theta.md)、[Gamma](../02-希腊字母/02-Gamma.md)、[波动率](../04-波动率/) 串成一条主线。

## 前置知识
- [03-Theta](../02-希腊字母/03-Theta.md)、[03-BSM 模型](../03-定价模型/03-BSM模型.md)

---

## 1. 设定：持有期权 + 连续 Delta 对冲

持有一张期权 $V$ ，用 $-\Delta$ 单位标的对冲方向。组合 $\Pi = V - \Delta S$ 。考察一个小时段 $dt$ 内的盈亏（暂略利率/carry，聚焦核心）。

---

## 2. 推导：用 Itô 展开 `推导`

由 [Itô 引理](../03-定价模型/03-BSM模型.md)，期权价值变化：

$$ dV = \Theta\,dt + \Delta\,dS + \tfrac{1}{2}\Gamma\,(dS)^2 $$

Delta 对冲组合（持 $-\Delta$ 标的）的盈亏，方向项 $\Delta\,dS$ 被抵消：

$$ d\Pi = dV - \Delta\,dS = \Theta\,dt + \tfrac{1}{2}\Gamma\,(dS)^2 $$

在 BSM 下，Theta 与 Gamma 由 [BSM 方程](../03-定价模型/03-BSM模型.md) 绑定（略 carry）：

$$ \Theta \approx -\tfrac{1}{2}\,\sigma_{\text{imp}}^2\,S^2\,\Gamma $$

代入：

$$ d\Pi \approx \tfrac{1}{2}\Gamma\,(dS)^2 - \tfrac{1}{2}\sigma_{\text{imp}}^2 S^2\Gamma\,dt = \tfrac{1}{2}\Gamma S^2\!\left[\left(\frac{dS}{S}\right)^2 - \sigma_{\text{imp}}^2\,dt\right] $$

由于 $\mathbb{E}\!\left[(dS/S)^2\right]=\sigma_{\text{real}}^2\,dt$ ，取期望得**核心公式**：

$$ \boxed{\;\mathbb{E}[d\Pi] \approx \tfrac{1}{2}\,\Gamma S^2\left(\sigma_{\text{real}}^2 - \sigma_{\text{imp}}^2\right)dt\;} $$

---

## 3. 结论的含义

- **多头期权（ $\Gamma>0$ ）**：当 $\sigma_{\text{real}}>\sigma_{\text{imp}}$ → Delta 对冲后**净赚**；反之被 Theta 吃。
- **空头期权（ $\Gamma<0$ ）**：当 $\sigma_{\text{real}}<\sigma_{\text{imp}}$ → 净赚（卖贵的 IV，实际没那么波动）。
- 权重是**美元 Gamma** $\Gamma S^2$ ：ATM、临到期最大（[Gamma 篇](../02-希腊字母/02-Gamma.md)）。
- 这就是 [Theta 篇"波动率对决"](../02-希腊字母/03-Theta.md) 的精确版，也是 [跨式](../06-组合策略/01-跨式与宽跨式.md) 等波动率策略的盈亏来源。

---

## 4. 路径依赖与"对冲误差"

- 实际是离散对冲（非连续），每步盈亏 $\tfrac{1}{2}\Gamma_t(\Delta S_t^2 - \sigma_{\text{imp}}^2 S_t^2\,dt)$ 沿路径累加 → **结果依赖路径**（你在高 Gamma 时段是否抓住了波动）。
- **对冲误差**：对冲不够频繁 → 偏离理论；太频繁 → 手续费/滑点（[09/02 funding](../09-加密期权专题/02-永续合约与资金费率对冲.md)）。
- 因此"买对了波动率"也可能因**路径不利 + 对冲成本**而没赚到。

---

## 5. 加密视角

- 用**永续**做 Delta 对冲（[09/02](../09-加密期权专题/02-永续合约与资金费率对冲.md)），**资金费率/滑点**计入对冲成本，吃掉部分 Gamma 收益。
- $\sigma_{\text{imp}}$ 用 [DVOL/IV](../09-加密期权专题/04-DVOL与加密波动率特征.md)， $\sigma_{\text{real}}$ 用 [已实现波动](../04-波动率/01-历史波动率与已实现波动率.md)，注意同口径（年化 $\sqrt{365}$ ）。
- 加密的**跳跃**让"已实现方差"出现尖峰 → 多头 Gamma 偶尔大赚、空头大亏（厚尾）。

---

## 6. 常见误区

- ❌ 以为"买对方向"就赚 → Delta 对冲后赚的是**波动率差**，不是方向。
- ❌ 忽略路径与对冲成本 → 理论赚、实盘没赚。
- ❌ $\sigma_{\text{real}}$ 与 $\sigma_{\text{imp}}$ 用不同年化口径比较。
- ❌ 空头 Gamma 只看 Theta 收入、不看跳跃尾部。

---

## 7. 关联
- [02-Gamma](../02-希腊字母/02-Gamma.md)、[03-Theta](../02-希腊字母/03-Theta.md)、[04 波动率](../04-波动率/)
- 下一篇：[02-已实现与隐含波动率价差交易](./02-已实现与隐含波动率价差.md)
- [09/02 永续对冲](../09-加密期权专题/02-永续合约与资金费率对冲.md)

## 8. 参考来源
- Delta 对冲组合 PnL $=\tfrac{1}{2}\Gamma S^2(\sigma_{\text{real}}^2-\sigma_{\text{imp}}^2)dt$ 、路径依赖、对冲误差属 `公认结论`（Hull 第 19 章 / Natenberg / Carr）。
- 推导为标准 `推导`（略 carry 项）。
