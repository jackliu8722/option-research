# 10 · 高阶希腊字母与做市定位

从"交易者"到"专家/做市级"的分水岭：一阶希腊字母只给斜率，本章讲它们**怎么随别的变量漂移**（二阶/三阶），以及**做市商对冲流如何反过来推动市场**。

> 公式型 A 档：每篇含符号表 → 闭式（已用 [`tools/option_strategy.py`](../../tools/option_strategy.py) 有限差分复核）→ 直觉 → 与 [BSM 标杆](../03-定价模型/03-BSM模型.md) 自洽的算例 → 特例 → 误区。

## 已完成
- [01 · 二阶交叉希腊字母 Vanna / Volga / Charm / Veta](./01-二阶交叉希腊字母-Vanna-Volga-Charm-Veta.md) — Δ/Vega 随 IV、时间的漂移；skew(RR)=Vanna、BF=Volga、delta bleed=Charm、Vega 衰减=Veta（含闭式与算例）
- [02 · 三阶希腊字母 Speed / Zomma / Color](./02-三阶希腊字母-Speed-Zomma-Color.md) — Gamma 随现货/IV/时间的变化；大头寸、临到期/0DTE、尾部大跳才显著
- [03 · 做市商定位与 Gamma 墙](./03-做市商定位与gamma墙.md) — dealer gamma、GEX 与 gamma 翻转点、pinning/钉价、vanna/charm flows、加密 put wall 与清算级联反身性

## 前置
- [02 希腊字母](../02-希腊字母/)（一阶全套）、[03 BSM](../03-定价模型/)、[04 波动率](../04-波动率/)

## 关联
- [04/02 微笑偏斜](../04-波动率/02-波动率微笑与偏斜.md)（RR/BF 就是 Vanna/Volga 的交易对象）
- [09/04 加密波动率与清算](../09-加密期权专题/04-DVOL与加密波动率特征.md)、[research/market-notes](../../research/market-notes/)
