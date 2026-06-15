---
title: Gamma：Delta 的变化率与凸性
tags: [希腊字母, Gamma, 凸性, 对冲]
level: 进阶
prerequisites: [docs/02-希腊字母/01-Delta.md]
status: 完善中
updated: 2026-06-15
---

# Gamma：Delta 的变化率与凸性

> Delta 会变，**Gamma 量化它变多快**。它是 [Delta 的 S 形曲线](./01-Delta.md) 的斜率，也是期权"凸性（convexity）"的来源——多头期权天生有利的弯曲，但这份好处要用 [Theta](./03-Theta.md) 来买单。核心结论： $\Gamma = e^{-q\tau}\,n(d_1)/(S\sigma\sqrt{\tau})$ 。

## 前置知识
- [01-Delta](./01-Delta.md) — Delta 与 Delta 中性
- [03-BSM 模型](../03-定价模型/03-BSM模型.md) — $d_1$ 与正态密度 $n(\cdot)$

---

## 1. 符号表（Notation）

| 符号 | 含义 | 单位/口径 |
|---|---|---|
| $S,\ K,\ \tau,\ \sigma$ | 现价/行权价/期限/IV | 见 [01-Delta](./01-Delta.md) |
| $n(d_1)$ | 标准正态密度在 $d_1$ 处的值 | — |
| $\Gamma$ | $\partial\Delta/\partial S=\partial^2 V/\partial S^2$ | 每 \$1（量纲 1/USD） |
| $\Gamma S^2$ | 美元 Gamma（dollar gamma） | USD |

## 2. 直觉：Delta 的"加速度"

**Gamma（Γ）= 标的变动 1 个单位时，Delta 的变动量。**

$$ \Gamma = \frac{\partial \Delta}{\partial S} = \frac{\partial^2 V}{\partial S^2} $$

- Delta 是"速度"（一阶），Gamma 是"加速度"（二阶）。
- Call/Put 的 Γ **相同且对多头恒正**（见 §5）。

---

## 3. 符号与分布

- **买入期权（long call 或 long put）→ Γ 恒为正**；**卖出期权 → Γ 为负**。
- **ATM 附近 Γ 最大**；深实值/深虚值 Γ→0（Δ 已贴近 ±1 或 0，不再怎么变）。
- **越临近到期，ATM 的 Γ 越尖**（Delta 在 $K$ 附近近乎跳变）→ 到期前平值仓位最"不稳定"。

---

## 4. 凸性：多头 Gamma 的好处与代价

Delta 只是局部线性近似，**Gamma 衡量这条近似偏离实际的弯曲**。对一段标的变动 $\Delta S$ ，Gamma 带来的额外损益：

$$ \text{Gamma PnL} \approx \tfrac{1}{2}\,\Gamma\,(\Delta S)^2 $$

- 这一项**与方向无关**（ $(\Delta S)^2$ 恒正）：**多头 Gamma 不管涨跌都赚这块弯曲**；空头 Gamma 不管涨跌都亏。
- 代价：多头 Gamma 必然**付 Theta**（时间衰减），空头 Gamma 必然**收 Theta**。**Gamma 与 Theta 是一对反向兄弟**（见 [03-Theta](./03-Theta.md)）。

> 一句话：**多头 Gamma = 买"波动"（涨跌都好）+ 付时间租金；空头 Gamma = 卖"波动"（怕大动）+ 收时间租金。**

---

## 5. 公式与推导

**结论（先给出）**：

$$ \boxed{\ \Gamma = \frac{e^{-q\tau}\,n(d_1)}{S\,\sigma\,\sqrt{\tau}}\ } $$

（Call/Put 的 Γ 相同。）

**逐步推导** `推导`：

1. 由 [Delta 篇](./01-Delta.md)： $\Delta_{\text{call}} = e^{-q\tau} N(d_1)$ 。

2. 对 $S$ 求导（ $N'=n$ ，链式法则）： $\Gamma = e^{-q\tau}\,n(d_1)\,\frac{\partial d_1}{\partial S}$ 。

3. 代入 $\dfrac{\partial d_1}{\partial S} = \dfrac{1}{S\sigma\sqrt{\tau}}$ ，即得结论。

4. Put 与 Call 的 Δ 仅差一个常数 $e^{-q\tau}$ （对 $S$ 求导为 0），故 **Γ 两者相同**。

**各项含义**： $n(d_1)$ 在 ATM 最大（标的最可能"翻边"处弯曲最强）；分母 $S\sigma\sqrt{\tau}$ 说明 **高价、高波动、长到期 → Γ 越小**（标的本来就动得多，多动一点不改变 Δ 多少）。

> **Gamma–Theta 对偶**：Delta 中性下 $\Theta \approx -\tfrac{1}{2}\sigma^2 S^2 \Gamma$ （见 [03-Theta](./03-Theta.md)）——同一份凸性，Γ 收、Θ 付。

## 6. 特例与极限检验

- **深实值/深虚值**（ $|d_1|\to\infty$ ）： $n(d_1)\to0$ ， $\Gamma\to0$ 。✓
- **ATM 临到期**（ $S=K,\ \tau\to0$ ）：分母 $\to0$ ， $\Gamma\to\infty$ ——Δ 在 $K$ 处跳变。✓
- **长到期**（ $\tau$ 大）： $\Gamma$ 小且沿 $S$ 平缓（凸性摊薄到很宽的价格区间）。✓

## 7. 敏感度 / 比较静态

| 输入 ↑ | $\Gamma$ 变化（ATM 附近） | 直觉 |
|---|---|---|
| $\tau$ | ↓ | 长到期凸性摊平 |
| $\sigma$ | ↓ | 高 IV 把分布摊宽 |
| $S$ 偏离 $K$ | ↓ | 离 ATM 越远越小 |

---

## 8. Gamma 与动态对冲（Gamma Scalping）

Delta 中性不能一劳永逸，正是因为 Gamma：

- 标的一动 → Δ 变（变多少由 Γ 决定）→ 净 Δ 漂移 → 需**再对冲**。
- **多头 Gamma 的再对冲是"高抛低吸"**：涨了 Δ 变大→卖出对冲，跌了 Δ 变小→买入对冲，每次再平衡锁住一点凸性收益，这叫 **Gamma scalping**；只要实际波动 > 隐含波动（你付的 Theta），就净赚。
- **空头 Gamma 的再对冲是"追涨杀跌"**：越对冲越亏，大行情下尤其痛。

---

## 9. 算例（与 BSM 篇自洽）

沿用 [BSM 算例](../03-定价模型/03-BSM模型.md)：`S=60,000`、`K=60,000`、`τ=0.25`、`σ=80%`、`r=10%`、`q=0`， $n(d_1)=0.38543$ 。代入：

$$ \Gamma = \frac{0.38543}{60{,}000 \times 0.80 \times \sqrt{0.25}} = \frac{0.38543}{24{,}000} \approx 1.606\times10^{-5} $$

（单位：每 \$1。）含义：BTC 涨 \$100，这张 Call 的 Δ 约增 1.606e−5 × 100 ≈ 0.0016。

**凸性收益**：标的净位移 $\Delta S=\pm3{,}000$ 时

$$ \text{Gamma PnL} \approx \tfrac{1}{2}\times 1.606\times10^{-5}\times 3{,}000^2 \approx \tfrac{1}{2}\times1.606\times10^{-5}\times9{,}000{,}000 \approx 72 $$

- 不管涨跌都 +\$72（多头 Gamma）；若当天 Theta 损耗 > \$72 → 净亏，< \$72 → 净赚。**这就是"已实现 vs 隐含波动"的对决**（[03-Theta](./03-Theta.md)）。
- **币口径**： $\Gamma$ 不能简单除以 $S$ （含 inverse 修正，见 [07 单位篇](./07-币本位希腊字母的单位与换算.md)）。

---

## 10. 加密视角：Gamma 风险被放大

- 加密**已实现波动高、且有[清算级联](../09-加密期权专题/04-DVOL与加密波动率特征.md)**（瞬间大跳）→ 对**空头 Gamma**（卖方）杀伤极大：一次跳空就能吞掉很久收的 Theta。
- 多头 Gamma 在高波动环境里 scalping 机会多，但**付的 Theta 也贵**（高 IV）。
- 对冲腿是永续（[09/02](../09-加密期权专题/02-永续合约与资金费率对冲.md)），再对冲越频繁、手续费/资金费率越高 → Gamma 收益要先盖过摩擦。

---

## 11. 常见误区

- ❌ 以为 Delta 中性就安全 → 忽略了 Γ 带来的 Δ 漂移和空头 Gamma 的尾部风险。
- ❌ 只看 Theta 收入卖期权 → 空头 Gamma 的"收租"在大行情里会被一次性吐回。
- ❌ 以为 Gamma 收益要靠看对方向 → $(\Delta S)^2$ 与方向无关，多头 Gamma 涨跌都赚弯曲。
- ❌ 忽略再对冲成本 → 高频 scalping 的手续费/资金费率可能盖过凸性收益。
- ❌ 把 Γ 像 Theta 一样"除以 S"换币口径 → Δ/Γ 有 inverse 修正（[07 单位篇](./07-币本位希腊字母的单位与换算.md)）。

---

## 12. 关联
- [01-Delta](./01-Delta.md) — Γ 是 Δ 的变化率
- 下一篇：[03-Theta](./03-Theta.md) — Gamma 的反向兄弟
- [07 币本位单位](./07-币本位希腊字母的单位与换算.md)、[09/02 永续对冲](../09-加密期权专题/02-永续合约与资金费率对冲.md)、[09/04 DVOL](../09-加密期权专题/04-DVOL与加密波动率特征.md)
- 工具：[`tools/option_strategy.py`](../../tools/option_strategy.py) 的 `bsm_greeks`。

## 13. 参考来源
- Gamma 定义、符号、ATM 最大、 $\tfrac12\Gamma(\Delta S)^2$ 凸性、Gamma–Theta 对偶、Gamma scalping、闭式 $\Gamma=e^{-q\tau}n(d_1)/(S\sigma\sqrt\tau)$ 属 `公认结论`（Hull 第 19 章 / Natenberg）。
- 算例由 [`tools/option_strategy.py`](../../tools/option_strategy.py) 复算，与 [BSM 篇](../03-定价模型/03-BSM模型.md) 自洽 `推导`。
