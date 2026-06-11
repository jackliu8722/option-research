#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
option_strategy.py — 期权策略分析工具（纯标准库，无需 numpy/scipy）

功能：
  - BSM 定价 + 希腊字母（Delta/Gamma/Vega/Theta/Rho）
  - 多腿组合：净权利金、到期盈亏、盈亏平衡、最大盈亏、净希腊字母
  - 压力测试：价格 × IV 冲击网格下的盯市盈亏

口径说明（重要）：
  - 计算为 **USD 口径**（标准 BSM，USD 计价/结算）。
  - Deribit 为**币本位/反向（inverse）**，盈亏对美元有非线性残留，
    需在此基础上做币口径换算（见 docs/09-加密期权专题/01-币本位与反向合约.md）。
  - 本工具用于教学/研究算例，不构成投资建议。

用法：
  python3 tools/option_strategy.py          # 复现 2026-06-11 三结构算例（自带验证）
  或 import 后用 Position/Leg 自定义组合。
"""
from __future__ import annotations
import math
from dataclasses import dataclass

SQRT2PI = math.sqrt(2 * math.pi)


def _N(x: float) -> float:
    "标准正态 CDF"
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _n(x: float) -> float:
    "标准正态密度"
    return math.exp(-0.5 * x * x) / SQRT2PI


def d1d2(S, K, tau, sigma, r=0.0, q=0.0):
    if tau <= 0 or sigma <= 0:
        raise ValueError("tau 和 sigma 必须 > 0")
    v = sigma * math.sqrt(tau)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma * sigma) * tau) / v
    return d1, d1 - v


def bsm_price(S, K, tau, sigma, r=0.0, q=0.0, kind="call"):
    d1, d2 = d1d2(S, K, tau, sigma, r, q)
    df_r, df_q = math.exp(-r * tau), math.exp(-q * tau)
    if kind == "call":
        return S * df_q * _N(d1) - K * df_r * _N(d2)
    return K * df_r * _N(-d2) - S * df_q * _N(-d1)


def bsm_greeks(S, K, tau, sigma, r=0.0, q=0.0, kind="call"):
    "返回 dict：delta, gamma, vega(每1%), theta(每天), rho(每1%)"
    d1, d2 = d1d2(S, K, tau, sigma, r, q)
    df_r, df_q = math.exp(-r * tau), math.exp(-q * tau)
    nd1 = _n(d1)
    gamma = df_q * nd1 / (S * sigma * math.sqrt(tau))
    vega = S * df_q * nd1 * math.sqrt(tau)          # 每 1.00 vol
    if kind == "call":
        delta = df_q * _N(d1)
        theta = (-S * df_q * nd1 * sigma / (2 * math.sqrt(tau))
                 - r * K * df_r * _N(d2) + q * S * df_q * _N(d1))
        rho = K * tau * df_r * _N(d2)
    else:
        delta = -df_q * _N(-d1)
        theta = (-S * df_q * nd1 * sigma / (2 * math.sqrt(tau))
                 + r * K * df_r * _N(-d2) - q * S * df_q * _N(-d1))
        rho = -K * tau * df_r * _N(-d2)
    return {"delta": delta, "gamma": gamma,
            "vega": vega / 100.0, "theta": theta / 365.0, "rho": rho / 100.0}


@dataclass
class Leg:
    qty: int          # +多 / -空
    kind: str         # 'call' / 'put'
    K: float
    sigma: float      # 该腿 IV（小数，如 0.62）


class Position:
    def __init__(self, legs, S0, tau, r=0.0, q=0.0):
        self.legs, self.S0, self.tau, self.r, self.q = legs, S0, tau, r, q
        self.entry_premium = self.price(S0, tau)   # 净权利金（>0=净借方/你付）

    def price(self, S, tau, dsigma=0.0):
        return sum(l.qty * bsm_price(S, l.K, tau, max(l.sigma + dsigma, 1e-6),
                                     self.r, self.q, l.kind) for l in self.legs)

    def net_greeks(self, S=None, tau=None):
        S = self.S0 if S is None else S
        tau = self.tau if tau is None else tau
        out = {"delta": 0, "gamma": 0, "vega": 0, "theta": 0, "rho": 0}
        for l in self.legs:
            g = bsm_greeks(S, l.K, tau, l.sigma, self.r, self.q, l.kind)
            for k in out:
                out[k] += l.qty * g[k]
        return out

    def expiry_payoff(self, ST):
        "到期内在价值之和（不含入场权利金）"
        v = 0.0
        for l in self.legs:
            intr = max(ST - l.K, 0.0) if l.kind == "call" else max(l.K - ST, 0.0)
            v += l.qty * intr
        return v

    def expiry_pnl(self, ST):
        "到期总盈亏 = 到期内在价值 − 入场净权利金"
        return self.expiry_payoff(ST) - self.entry_premium

    def summary(self, lo=0.5, hi=1.8, step=0.001):
        "扫描 [lo*S0, hi*S0] 求最大盈亏与盈亏平衡"
        S0 = self.S0
        grid = [S0 * (lo + i * step) for i in range(int((hi - lo) / step) + 1)]
        pnls = [(s, self.expiry_pnl(s)) for s in grid]
        max_p = max(pnls, key=lambda t: t[1])
        min_p = min(pnls, key=lambda t: t[1])
        # 盈亏平衡：符号变化点（线性插值）
        bes = []
        for (s0, p0), (s1, p1) in zip(pnls, pnls[1:]):
            if (p0 <= 0 < p1) or (p0 >= 0 > p1):
                bes.append(s0 + (s1 - s0) * (-p0) / (p1 - p0))
        # 边缘是否发散（判断"不封顶"）
        up_unbounded = pnls[-1][1] > pnls[-2][1] + 1e-6 and pnls[-1][1] == max_p[1]
        dn_unbounded = pnls[0][1] > pnls[1][1] + 1e-6 and pnls[0][1] == max_p[1]
        return {"net_premium": self.entry_premium, "max_profit": max_p,
                "max_loss": min_p, "breakevens": bes,
                "up_unbounded": up_unbounded, "dn_unbounded": dn_unbounded}

    def stress(self, price_shocks, iv_shocks):
        "返回 {(dp,div): 盯市盈亏}，盯市=冲击后重定价 − 入场价（同到期 tau）"
        out = {}
        for dp in price_shocks:
            for dv in iv_shocks:
                mtm = self.price(self.S0 * (1 + dp), self.tau, dsigma=dv)
                out[(dp, dv)] = mtm - self.entry_premium
        return out


def _fmt_usd(x):
    return f"{'+' if x >= 0 else '-'}${abs(x):,.0f}"


def demo():
    "复现 2026-06-11 三结构算例（验证手算）"
    S0, tau = 61672.0, 28 / 365
    structures = {
        "A 牛市看跌价差": [Leg(-1, "put", 58000, 0.62), Leg(+1, "put", 53000, 0.68)],
        "B 限险看涨风险逆转": [Leg(-1, "put", 58000, 0.62), Leg(+1, "put", 53000, 0.68),
                              Leg(+1, "call", 66000, 0.54)],
        "C 铁鹰": [Leg(-1, "put", 58000, 0.62), Leg(+1, "put", 53000, 0.68),
                  Leg(-1, "call", 66000, 0.54), Leg(+1, "call", 71000, 0.52)],
    }
    print(f"参数：S0={S0:,.0f}  tau={tau:.4f}({28}天)  r=0  q=0\n" + "=" * 66)
    for name, legs in structures.items():
        pos = Position(legs, S0, tau)
        s = pos.summary()
        g = pos.net_greeks()
        prem = pos.entry_premium  # >0=净借方
        prem_btc = prem / S0
        kind = "净借方(付)" if prem > 0 else "净贷方(收)"
        print(f"\n【{name}】")
        print(f"  净权利金: {_fmt_usd(prem)} = {prem_btc:+.4f} BTC  [{kind}]")
        print(f"  最大盈利: {_fmt_usd(s['max_profit'][1])} @ S_T≈{s['max_profit'][0]:,.0f}"
              + ("（上行不封顶）" if s["up_unbounded"] else ""))
        print(f"  最大亏损: {_fmt_usd(s['max_loss'][1])} @ S_T≈{s['max_loss'][0]:,.0f}")
        print(f"  盈亏平衡: " + ", ".join(f"{b:,.0f}" for b in s["breakevens"]))
        print(f"  净希腊字母: Δ={g['delta']:+.3f}  Γ={g['gamma']:+.6f}"
              f"  Vega={_fmt_usd(g['vega'])}/1%  Θ={_fmt_usd(g['theta'])}/天")
    print("\n" + "=" * 66)
    print("注：USD 口径；Deribit 币本位需另做反向换算（docs/09/01）。不构成建议。")


if __name__ == "__main__":
    demo()
