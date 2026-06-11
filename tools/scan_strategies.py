#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_strategies.py — 给定"观点"批量扫描结构，按期望盈亏(EV)排序

思路：
  - 把研究从"手挑行权价"升级为"在你的观点下搜索"。
  - **EV 完全取决于你输入的观点分布**（漂移 mu、实际波动 sigma_real）。
    风险中性下任何仓位 EV≈0，必须用你与市场不同的看法才有意义。
  - 这是评估/排序工具，**不是预测、不构成建议**。

用法：python3 tools/scan_strategies.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from option_strategy import Leg, Position  # noqa: E402

# ===== 市场快照（2026-06-11，示意）=====
S0 = 61672.0
TAU = 28 / 365

# ===== 偏斜 IV 模型（put skew：下方更陡）=====
ATM, PUT_SLOPE, CALL_SLOPE = 0.58, 0.60, 0.30


def skew_iv(K):
    m = (S0 - K) / S0                      # OTM put: m>0；OTM call: m<0
    return ATM + (PUT_SLOPE if m > 0 else CALL_SLOPE) * m


# ===== 你的观点（核心输入！改这里）=====
VIEW_MU = 0.00        # 年化漂移：0=认为不涨不跌（中性）
VIEW_SIGMA = 0.50     # 你认为的"实际波动"：0.50 < ATM隐含0.58 → 你认为市场高估了波动


def bull_put(Ks, Kl):
    return Position([Leg(-1, "put", Ks, skew_iv(Ks)), Leg(+1, "put", Kl, skew_iv(Kl))], S0, TAU)


def iron_condor(Kp_s, Kp_l, Kc_s, Kc_l):
    return Position([Leg(-1, "put", Kp_s, skew_iv(Kp_s)), Leg(+1, "put", Kp_l, skew_iv(Kp_l)),
                     Leg(-1, "call", Kc_s, skew_iv(Kc_s)), Leg(+1, "call", Kc_l, skew_iv(Kc_l))],
                    S0, TAU)


def metrics(pos):
    s = pos.summary()
    e = pos.expected_pnl(VIEW_MU, VIEW_SIGMA)
    credit = -pos.entry_premium                      # >0=净贷方收
    maxp, maxl = s["max_profit"][1], s["max_loss"][1]
    rr = (maxp / abs(maxl)) if maxl < 0 else float("inf")
    return {"credit": credit, "maxp": maxp, "maxl": maxl,
            "rr": rr, "pop": e["POP"], "ev": e["EV"]}


def scan_bull_puts():
    rows = []
    for Ks in (54000, 56000, 58000, 60000, 62000):
        for w in (3000, 5000, 7000):
            Kl = Ks - w
            m = metrics(bull_put(Ks, Kl))
            rows.append((f"{Ks:,.0f}/{Kl:,.0f}", w, m))
    rows.sort(key=lambda r: r[2]["ev"], reverse=True)
    print("\n【牛市看跌价差扫描】（按 EV 排序）")
    print(f"  观点: μ={VIEW_MU:.0%}/年, σ_real={VIEW_SIGMA:.0%}（ATM隐含≈{ATM:.0%}）")
    print(f"  {'卖/买':>14} {'宽':>6} {'净贷$':>8} {'最大亏$':>9} {'R:R':>6} {'POP':>6} {'EV$':>8}")
    for name, w, m in rows:
        print(f"  {name:>14} {w:>6,} {m['credit']:>8,.0f} {m['maxl']:>9,.0f} "
              f"{m['rr']:>6.2f} {m['pop']:>6.1%} {m['ev']:>+8,.0f}")


def scan_iron_condors():
    rows = []
    for half in (4000, 6000, 8000):          # 短腿离现价的距离
        for w in (4000, 6000):               # 每侧宽度
            Kp_s, Kc_s = round(S0 - half, -3), round(S0 + half, -3)
            ic = iron_condor(Kp_s, Kp_s - w, Kc_s, Kc_s + w)
            m = metrics(ic)
            rows.append((f"{Kp_s:,.0f}-{Kc_s:,.0f}", w, m))
    rows.sort(key=lambda r: r[2]["ev"], reverse=True)
    print("\n【铁鹰扫描】（按 EV 排序）")
    print(f"  {'区间':>16} {'宽':>6} {'净贷$':>8} {'最大亏$':>9} {'R:R':>6} {'POP':>6} {'EV$':>8}")
    for name, w, m in rows:
        print(f"  {name:>16} {w:>6,} {m['credit']:>8,.0f} {m['maxl']:>9,.0f} "
              f"{m['rr']:>6.2f} {m['pop']:>6.1%} {m['ev']:>+8,.0f}")


if __name__ == "__main__":
    print("=" * 70)
    print("注：EV/POP 基于你的观点分布(μ, σ_real)，非预测；USD 口径；")
    print("    未计手续费/滑点；币本位另算(docs/09/01)。不构成投资建议。")
    print("=" * 70)
    scan_bull_puts()
    scan_iron_condors()
    print("\n解读：EV 越高=在你的观点下越划算；但同时看 POP(胜率)、R:R、最大亏损，")
    print("并据风险预算定仓(docs/07/01)。换 VIEW_MU/VIEW_SIGMA 看排序如何变。")
