# 11 · 高级定价模型

BSM 用一个常数 σ 配不出微笑。本章是"超越 BSM"的三条主线：让 σ 随**时空**变（局部波动率）、让 σ 自己**随机**（Heston/SABR）、在扩散上叠加**跳跃**（Merton/Bates）。每个模型解释一种现实：偏斜、凸性、厚尾。

> A 档：可数值验证的公式（Merton 泊松加权 BSM、SABR Hagan 近似）已用 [`tools/option_strategy.py`](../../tools/option_strategy.py)（`merton_call` / `sabr_iv`）复算。

## 已完成
- [01 · 局部波动率与 Dupire 方程](./01-局部波动率与Dupire方程.md) — $\sigma_{\text{loc}}(S,t)$ 复现整张曲面、Dupire 公式、局部vs隐含偏斜、"静态完美动态错"的局限
- [02 · 随机波动率 Heston 与 SABR](./02-随机波动率Heston与SABR.md) — Heston(CIR+特征函数)、SABR(Hagan 近似)、**ρ↔偏斜/Vanna、vol-of-vol↔凸性/Volga**（含 SABR 微笑算例）
- [03 · 跳跃扩散 Merton 与 Bates](./03-跳跃扩散Merton与Bates.md) — Merton 泊松加权 BSM 闭式、跳跃生成厚尾/短端偏斜、Bates=Heston+跳跃（加密首选，含算例）

## 主线
局部波动率（静态拟合）→ 随机波动率（动态微笑/期限）→ 跳跃（厚尾/短端偏斜）→ Bates（全家桶，贴合加密）。

## 关联
- [10 高阶希腊字母](../10-高阶希腊字母与做市定位/)（ρ/vol-of-vol 对应 Vanna/Volga）、[04 波动率](../04-波动率/)、[08 进阶量化](../08-进阶与量化/)
