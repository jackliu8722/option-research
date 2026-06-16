---
title: 随机波动率：Heston 与 SABR
tags: [高级定价, 随机波动率, Heston, SABR, 微笑, 校准]
level: 高级
prerequisites: [docs/11-高级定价模型/01-局部波动率与Dupire方程.md, docs/10-高阶希腊字母与做市定位/01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md]
status: 完善中
updated: 2026-06-16
---

# 随机波动率：Heston 与 SABR

> [局部波动率](./01-局部波动率与Dupire方程.md) 静态完美但动态错。**随机波动率（stochastic vol, SV）让波动率自己成为一个随机过程**——这样微笑能"自然生成"、且动态更合理。两大主力：**Heston**（有半闭式解，学术/风控常用）与 **SABR**（有微笑近似公式，做市/插值标配）。关键直觉：**相关性 ρ 造偏斜（接 [Vanna](../10-高阶希腊字母与做市定位/01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md)），vol-of-vol 造凸性（接 Volga）**。

## 前置知识
- [11/01 局部波动率](./01-局部波动率与Dupire方程.md)
- [10/01 Vanna/Volga](../10-高阶希腊字母与做市定位/01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md)、[04/02 微笑偏斜](../04-波动率/02-波动率微笑与偏斜.md)

---

## 1. 符号表（Notation）

| 符号 | 含义 |
|---|---|
| $v_t$ | 瞬时方差（ $\sqrt{v}$ = 瞬时波动率） |
| $\kappa,\ \theta$ | 方差均值回归速度 / 长期方差（Heston） |
| $\xi$ | vol-of-vol（Heston，方差的波动） |
| $\rho$ | 价格与波动率的相关性 |
| $\alpha,\ \beta,\ \nu$ | SABR：水平 / backbone 指数 / vol-of-vol |
| $F$ | 远期价 |

---

## 2. Heston 模型 `公认结论`

**SDE**（风险中性测度）：

$$ dS = (r-q)\,S\,dt + \sqrt{v}\,S\,dW_1 $$

$$ dv = \kappa(\theta - v)\,dt + \xi\sqrt{v}\,dW_2,\qquad dW_1\,dW_2 = \rho\,dt $$

- 方差 $v$ 服从 **CIR 过程**：均值回归到 $\theta$ 、速度 $\kappa$ 、波动 $\xi$ 。
- **半闭式定价**：通过**特征函数 + 傅里叶反演**（Heston 1993）可半解析地算欧式价——比蒙特卡洛快得多，是校准的常用目标。
- **Feller 条件** $\xi^2 \le 2\kappa\theta$ 保证方差不触 0。

**参数 → 微笑形状**（务必记）：

| 参数 | 控制 | 对应希腊字母 |
|---|---|---|
| $\rho$ | **偏斜方向/陡度**（ρ<0 → put skew） | [Vanna / RR](../10-高阶希腊字母与做市定位/01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md) |
| $\xi$ (vol-of-vol) | **微笑凸性/尾部** | [Volga / BF](../10-高阶希腊字母与做市定位/01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md) |
| $\kappa,\ \theta$ | 水平 + 期限结构 | term/level |

---

## 3. SABR 模型 `公认结论`

**SDE**（对远期 $F$ ）：

$$ dF = \alpha\,F^{\beta}\,dW_1,\qquad d\alpha = \nu\,\alpha\,dW_2,\qquad dW_1\,dW_2 = \rho\,dt $$

- $\beta$ = **backbone**（CEV 指数）：β=1 近似对数正态（vol 报价稳定），β=0 正态。
- **Hagan 近似**：SABR 最大价值是有一条**隐含波动率的近似公式**（Hagan 2002），直接把 $(\alpha,\beta,\rho,\nu)$ 映成整条微笑——做市插值、报价标配。ATM（ $K=F$ ）简化为：

$$ \sigma_{\text{ATM}} \approx \frac{\alpha}{F^{1-\beta}}\left[\,1 + \Big(\tfrac{(1-\beta)^2}{24}\tfrac{\alpha^2}{F^{2-2\beta}} + \tfrac{\rho\beta\nu\alpha}{4F^{1-\beta}} + \tfrac{2-3\rho^2}{24}\nu^2\Big)T\,\right] $$

**参数 → 形状**：α 定 ATM 水平；**ρ 定偏斜**（ρ<0 → 左高右低）；**ν 定凸性**（vol-of-vol 越大微笑越弯）；β 影响 backbone（ATM vol 随 F 移动的方式）。

---

## 4. 算例：SABR 生成一条 put skew（已数值复算）

取 $F=60{,}000,\ T=0.25,\ \beta=1,\ \alpha=0.80,\ \rho=-0.5,\ \nu=1.0$ ，Hagan 公式算出：

| 行权价 K | SABR 隐含 IV |
|---|---|
| 48,000 | 0.851 |
| 54,000 | 0.818 |
| 60,000 (ATM) | 0.790 |
| 66,000 | 0.768 |
| 72,000 | 0.750 |

- **左高右低 = put skew**，正是 $\rho=-0.5<0$ 的效果；把 $\rho$ 翻成正会得到 call skew（加密牛市常态）。
- $\nu=1.0$ 给两翼相对中间的上翘（凸性）；调大 $\nu$ 微笑更弯。
- 这张表用 [`tools/option_strategy.py`](../../tools/option_strategy.py) 配合 Hagan 公式复算。

---

## 5. Heston vs SABR vs 局部波动率

| | 局部波动率 | Heston | SABR |
|---|---|---|---|
| vol 是 | 确定函数 | 随机（CIR） | 随机（CEV+lognormal vol） |
| 定价 | 复现曲面 | 特征函数半闭式 | Hagan 近似公式 |
| 强项 | 静态完美拟合 | 期限结构、风控 | 单到期微笑插值、做市 |
| 弱项 | 动态错（[01](./01-局部波动率与Dupire方程.md)） | 校准较重、短到期偏斜不足 | 单到期、远翼近似失真 |

> **共同短板**：纯扩散 SV 的**短到期偏斜会过快衰减**，配不出加密这种"短到期也很陡"的偏斜——要补 [跳跃（Bates）](./03-跳跃扩散Merton与Bates.md)。

---

## 6. 加密视角

- **ρ 会翻号**：股票常 ρ<0（put skew），加密牛市常 ρ>0（call skew）→ 校准时不能固定符号（[04/02](../04-波动率/02-波动率微笑与偏斜.md)）。
- **ν 很大**：加密 vol-of-vol 高（DVOL 自己剧烈波动）→ 微笑更弯、Volga 敞口大（[10/01](../10-高阶希腊字母与做市定位/01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md)）。
- 行权价稀疏 + 短到期陡偏斜 → 实务常用 **SABR 配单到期 + 跳跃补短端**。

---

## 7. 常见误区

- ❌ 以为 SV 能完美复现曲面 → 它是参数模型，只能近似；完美静态拟合用局部波动率。
- ❌ 把 ρ 与 ν 混 → ρ 管偏斜（一阶不对称），ν 管凸性（二阶弯曲）。
- ❌ 用纯 SV 配加密短到期陡偏斜 → 短端要靠跳跃。
- ❌ 固定 ρ<0 套加密 → 加密会翻成 call skew。

---

## 8. 关联
- [11/01 局部波动率](./01-局部波动率与Dupire方程.md)
- 下一篇：[03-跳跃扩散 Merton 与 Bates](./03-跳跃扩散Merton与Bates.md)
- [10/01 Vanna/Volga](../10-高阶希腊字母与做市定位/01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md)（ρ↔skew、vol-of-vol↔凸性）、[04/02 微笑偏斜](../04-波动率/02-波动率微笑与偏斜.md)

## 9. 参考来源
- Heston 1993（特征函数解）、SABR / Hagan 2002（隐含波动率近似）、ρ↔skew、vol-of-vol↔凸性属 `公认结论`（Heston / Hagan-Kumar-Lesniewski-Woodward / Gatheral）。
- §4 SABR 微笑由 [`tools/option_strategy.py`](../../tools/option_strategy.py) + Hagan 公式数值复算 `推导`。
