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

### 口径与免责
- **USD 口径**（标准 BSM）。Deribit 为**币本位/反向**，盈亏对美元有非线性残留，需另做换算（[09/01 币本位与反向合约](../docs/09-加密期权专题/01-币本位与反向合约.md)）。
- 未计手续费/滑点（[08/04 回测](../docs/08-进阶与量化/04-回测方法论.md)）；IV 为输入假设。
- 仅供学习与研究，**不构成投资建议**。

## 依赖
- Python 3（标准库）。无第三方依赖。
