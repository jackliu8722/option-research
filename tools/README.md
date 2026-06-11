# tools/ — 量化分析工具

研究主线的轻量 Python 工具。**纯标准库**（只用 `math`，无需 numpy/scipy），随处可跑。

## option_strategy.py — 期权策略分析

BSM 定价 + 希腊字母 + 多腿组合盈亏/平衡/最大盈亏 + 压力测试。

### 运行（自带验证）
```bash
python3 tools/option_strategy.py
```
直接复现 [2026-06-11 三结构算例](../research/market-notes/2026-06-11-三结构对照-BTC.md)（牛市看跌价差 / 限险看涨风险逆转 / 铁鹰），用于校验手算。

### 自定义组合
```python
from tools.option_strategy import Leg, Position

# 例：牛市看跌价差（卖 58K put / 买 53K put），S0=61672，28 天
pos = Position(
    [Leg(-1, "put", 58000, 0.62), Leg(+1, "put", 53000, 0.68)],
    S0=61672, tau=28/365, r=0.0, q=0.0,
)
print(pos.summary())        # 净权利金、最大盈亏、盈亏平衡
print(pos.net_greeks())     # 净 Delta/Gamma/Vega/Theta/Rho
print(pos.stress([-0.3,-0.1,0,0.1,0.3], [0,0.1,0.2]))  # 价格×IV 压力网格
```

- `Leg(qty, kind, K, sigma)`：`qty` 正=多/负=空；`kind`='call'/'put'；`sigma`=该腿 IV（小数）。
- `Position(legs, S0, tau, r, q)`：入场即记录净权利金。

### 隐含波动率反解
```python
from tools.option_strategy import bsm_price, implied_vol
px = bsm_price(61672, 60000, 28/365, 0.60, kind="call")
implied_vol(px, 61672, 60000, 28/365, kind="call")   # → ≈0.60（二分法，稳健）
```

### 币本位 / 反向(inverse) 口径（Deribit）
```python
pos.entry_premium_coin()      # 入场净权利金（BTC）
pos.expiry_pnl_coin(ST)       # 反向到期盈亏（BTC）= USD内在/ST − 入场币权利金
pos.summary_coin()            # 币口径最大盈亏/平衡
```
> ⚠️ **inverse 洞察**：USD 封顶的亏损在**币口径下不封顶**——固定美元亏损 ÷ 越低的结算价 = 越多币。例：牛市看跌价差 USD 最大亏损 −\$3,764，但 BTC 跌 50% 时币口径达 −0.14 BTC 且随跌幅继续放大（[09/01](../docs/09-加密期权专题/01-币本位与反向合约.md)）。

### ASCII 盈亏图（无需 matplotlib）
```python
print(ascii_payoff(pos, lo=0.7, hi=1.3, coin=False))   # 纯文本到期盈亏图
```

### 口径与免责
- **USD 口径**（标准 BSM）。Deribit 为**币本位/反向**，盈亏对美元有非线性残留，需另做换算（[09/01 币本位与反向合约](../docs/09-加密期权专题/01-币本位与反向合约.md)）。
- 未计手续费/滑点（[08/04 回测](../docs/08-进阶与量化/04-回测方法论.md)）；IV 为输入假设。
- 仅供学习与研究，**不构成投资建议**。

## scan_strategies.py — 给定观点批量扫描

把研究从"手挑行权价"升级为"在你的观点下搜索最优结构"。

```bash
python3 tools/scan_strategies.py
```
- 遍历牛市看跌价差与铁鹰的参数，按**期望盈亏 EV** 排序，同时给 POP（胜率）、R:R、净贷方、最大亏损。
- **EV 在"你的观点分布"下计算**：改文件顶部 `VIEW_MU`（漂移）、`VIEW_SIGMA`（你认为的实际波动）即可看排序如何变。
- 偏斜 IV 由 `skew_iv(K)` 给（可调 `ATM/PUT_SLOPE/CALL_SLOPE`）。

> ⚠️ **两条铁律**：① 风险中性下（σ_real=隐含）任何仓位 EV≈0——**正 EV 完全来自你与市场不同的看法**，输入错则全错。② **对数正态低估加密跳跃/清算尾部**→短波动率结构的真实尾部比 EV 显示的更差（[07/03 压力测试](../docs/07-风险管理/03-尾部风险与压力测试.md)、[08/02 VRP](../docs/08-进阶与量化/02-已实现与隐含波动率价差.md)）。**"高 EV/高 POP" ≠ "安全"**。

## 依赖
- Python 3（标准库）。无第三方依赖。
