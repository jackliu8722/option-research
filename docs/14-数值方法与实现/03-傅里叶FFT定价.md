---
title: 傅里叶 / FFT 定价（Characteristic Function & Carr-Madan）
tags: [数值方法, 傅里叶, FFT, 特征函数, Carr-Madan, Heston]
level: 高级
prerequisites: [docs/14-数值方法与实现/02-有限差分PDE.md, docs/11-高级定价模型/02-随机波动率Heston与SABR.md]
status: 完善中
updated: 2026-06-16
---

# 傅里叶 / FFT 定价（Characteristic Function & Carr-Madan）

> 这是**实务给 [Heston / Merton / Bates](../11-高级定价模型/) 定价的标准武器**。诀窍：很多模型**没有价格的解析式，却有"特征函数"的解析式**（终端对数价的傅里叶变换）。一旦有特征函数，就能用傅里叶反演**快速**算出期权价——而且 FFT 一次出**整条行权价曲线**，校准微笑神器。

## 前置知识
- [14/02 有限差分](./02-有限差分PDE.md)、[11/02 Heston/SABR](../11-高级定价模型/02-随机波动率Heston与SABR.md)（特征函数从哪来）

---

## 1. 核心思想：有特征函数就能定价 `公认结论`

**特征函数** = 终端对数价 $\ln S_T$ 的傅里叶变换：

$$ \varphi(u) = \mathbb{E}^{Q}\!\big[e^{iu\ln S_T}\big] $$

- BSM、**Heston、Merton、Bates、Lévy** 等都有**闭式特征函数**（即便价格没有闭式）。
- 有了 $\varphi$ ，期权价是它的一个**傅里叶积分**——这把"难定价"变成"算一个积分"。

---

## 2. Gil–Pelaez：从特征函数取出概率 `公认结论`

Call = $S e^{-q\tau}\Pi_1 - K e^{-r\tau}\Pi_2$ ，两个"概率"由特征函数反演：

$$ \Pi_j = \frac{1}{2} + \frac{1}{\pi}\int_0^{\infty}\text{Re}\!\left[\frac{e^{-iu\ln K}\,\varphi_j(u)}{iu}\right]du $$

- $\varphi_2=\varphi$ （风险中性）， $\varphi_1(u)=\varphi(u-i)/\varphi(-i)$ （股票测度）。
- 数值上就是把这个积分离散求和——[`tools/option_strategy.py`](../../tools/option_strategy.py) 的 `fourier_call` 就这么做。

---

## 3. Carr–Madan：FFT 一次出所有行权价 `公认结论`

直接对 Call 价做傅里叶变换会发散（赔付不可积），**Carr–Madan（1999）加一个阻尼因子** $e^{\alpha k}$ （ $k=\ln K$ ）让它可积，得到干净的变换：

$$ \psi(v) = \frac{e^{-r\tau}\,\varphi\big(v-(\alpha+1)i\big)}{\alpha^2+\alpha - v^2 + i(2\alpha+1)v} $$

- 对 $\psi$ 做一次 **FFT**，就同时得到**一整排行权价**的期权价——这是校准微笑时的速度关键（成百上千个报价点一次算完）。

---

## 4. 算例：傅里叶价复现 BSM（已验证）

`S=K=60,000, τ=0.25, σ=80%, r=10%`，用 BSM 特征函数 + Gil–Pelaez（`fourier_call`）：

| 方法 | ATM Call 价 |
|---|---|
| BSM 解析 | \$10,152.55 |
| 傅里叶（Gil–Pelaez） | **\$10,152.55**（误差 ≈ 0） |

- **关键**：把上面的特征函数换成 [Heston](../11-高级定价模型/02-随机波动率Heston与SABR.md) 或 [Merton](../11-高级定价模型/03-跳跃扩散Merton与Bates.md) 的，同一套代码就给 SV/跳跃模型定价了——这正是 Bates 校准的做法。

---

## 5. 强项与弱项

- **强项**：**快**（FFT 全行权价一次出）、对**仿射模型（Heston/Lévy）几乎精确**、是 SV/跳跃模型校准的标准管线。
- **弱项**：**需要特征函数**（不是所有模型/赔付都有）；主要给**欧式**用，**路径依赖**仍靠 [MC](./01-蒙特卡洛.md)；阻尼参数 $\alpha$ 要调好。

---

## 6. 三种数值方法怎么选

| 需求 | 首选 |
|---|---|
| 欧式 + 有特征函数（Heston/Bates 校准） | **傅里叶/FFT** |
| 美式 / 障碍 / 低维 | **[有限差分](./02-有限差分PDE.md)** |
| 路径依赖 / 高维 / 任意赔付 | **[蒙特卡洛](./01-蒙特卡洛.md)** |

---

## 7. 加密视角

- 加密做市/风控给 **Heston/Bates 校准 [DVOL 曲面](../09-加密期权专题/04-DVOL与加密波动率特征.md)** 时，几乎都用 FFT（速度撑得起实时重校准）。
- 加密**跳跃**（[Merton/Bates](../11-高级定价模型/03-跳跃扩散Merton与Bates.md)）的特征函数也是闭式 → 傅里叶法天然适配厚尾模型。
- 校准目标：用 FFT 算出整张模型微笑，与市场 [RR/BF](../04-波动率/02-波动率微笑与偏斜.md) 对齐，反解参数 $(\kappa,\theta,\xi,\rho,\lambda,\dots)$ 。

---

## 8. 常见误区

- ❌ 以为傅里叶法万能 → 它要特征函数、主攻欧式，路径依赖还得 MC。
- ❌ 阻尼参数 $\alpha$ 乱设 → 取太大/太小数值不稳。
- ❌ 把 Gil–Pelaez 积分上限取太小 → 截断误差；高 IV/短到期要积分更远。
- ❌ 用它算美式 → 该上有限差分。

---

## 9. 关联
- [14/01 蒙特卡洛](./01-蒙特卡洛.md)、[14/02 有限差分](./02-有限差分PDE.md)
- [11/02 Heston/SABR](../11-高级定价模型/02-随机波动率Heston与SABR.md)、[11/03 Merton/Bates](../11-高级定价模型/03-跳跃扩散Merton与Bates.md)（特征函数来源）、[04/02 微笑校准](../04-波动率/02-波动率微笑与偏斜.md)
- 工具：[`tools/option_strategy.py`](../../tools/option_strategy.py) 的 `fourier_call`

## 10. 参考来源
- 特征函数定价、Gil–Pelaez 反演、Carr–Madan FFT、仿射模型应用属 `公认结论`（Carr-Madan 1999 / Heston 1993 / Gil-Pelaez 1951 / Gatheral）。
- §4 由 [`tools/option_strategy.py`](../../tools/option_strategy.py) 的 `fourier_call` 复算，与 [BSM 篇](../03-定价模型/03-BSM模型.md) 精确一致 `推导`。
