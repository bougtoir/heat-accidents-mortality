#!/usr/bin/env python3
"""Shared quasi-Poisson distributed-lag machinery for the US and Japan analyses."""
import numpy as np
import pandas as pd
import scipy.linalg as sla
from dlnm import DistLagBins, lag_matrix

BINS = [(0, 0), (1, 3), (4, 10)]     # lag windows (days)
VAR_DF = 4                            # exposure spline df per window (constant-free -> 3 eff.)
SEED = 20260722


def fit_poisson_irls(X, y, maxiter=100, tol=1e-9):
    """Memory-light Poisson (log link) IRLS via normal equations."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    beta = np.zeros(X.shape[1]); beta[0] = np.log(max(y.mean(), 1e-3))
    for _ in range(maxiter):
        eta = np.clip(X @ beta, -30, 30); mu = np.exp(eta)
        z = eta + (y - mu) / mu
        WX = mu[:, None] * X
        A = X.T @ WX
        try:
            new = np.linalg.solve(A, WX.T @ z)
        except np.linalg.LinAlgError:
            new = np.linalg.lstsq(A, WX.T @ z, rcond=None)[0]
        if np.max(np.abs(new - beta)) < tol:
            beta = new; break
        beta = new
    mu = np.exp(np.clip(X @ beta, -30, 30))
    XtWX = X.T @ (mu[:, None] * X)
    try:
        cov = np.linalg.inv(XtWX)
    except np.linalg.LinAlgError:
        cov = np.linalg.pinv(XtWX)
    pearson = np.sum((y - mu) ** 2 / mu)
    return beta, cov, mu, pearson


def _full_rank(X, protect):
    """Drop linearly dependent columns (empty dummy categories etc.) via pivoted
    QR so the normal equations are non-singular. Exposure-basis columns in
    `protect` are always retained (they are well-conditioned and informative)."""
    cols = list(X.columns)
    Q, R, piv = sla.qr(X.values, mode="economic", pivoting=True)
    d = np.abs(np.diag(R))
    tol = (d.max() * 1e-9) if d.size else 0.0
    rank = int((d > tol).sum())
    keep = set(cols[i] for i in piv[:rank]) | set(protect)
    kept = [c for c in cols if c in keep]
    dropped = len(cols) - len(kept)
    if dropped:
        print(f"    dropped {dropped} rank-deficient design column(s)")
    return X[kept]


def fit_model(df, exposure, confounder_fn, extra=None, var_df=VAR_DF, group="unit"):
    cb = DistLagBins(df[exposure].values, BINS, var_df)
    idx, lagged = lag_matrix(df, group, "date", exposure, cb.maxlag)
    lagged = lagged[np.argsort(idx)]
    full = ~np.isnan(lagged).any(axis=1)
    cbdf = pd.DataFrame(cb.transform(lagged), columns=cb.colnames(), index=df.index)
    blocks = [cbdf, confounder_fn(df)]
    if extra is not None:
        blocks.append(extra.loc[df.index])
    X = pd.concat(blocks, axis=1)
    X = X.loc[X.index[full]].dropna(); d = df.loc[X.index]
    X = _full_rank(X, protect=cb.colnames())
    beta, cov, mu, pear = fit_poisson_irls(X.values, d.deaths.values)
    phi = pear / (len(d) - X.shape[1])
    cov = cov * phi
    cols = list(X.columns); ci = [cols.index(c) for c in cb.colnames()]
    return dict(cb=cb, beta=beta[ci], cov=cov[np.ix_(ci, ci)], d=d, phi=phi,
                cbX=X[cb.colnames()].values, npar=X.shape[1])


def _ci(b, beta, cov):
    lr = float(b @ beta); se = float(np.sqrt(max(b @ cov @ b, 0)))
    return np.exp(lr), np.exp(lr - 1.96 * se), np.exp(lr + 1.96 * se)


def cumulative_curve(m, xgrid, ref):
    ref_b = m["cb"].cumulative_basis([ref])[0]
    rows = [(x, *_ci(m["cb"].cumulative_basis([x])[0] - ref_b, m["beta"], m["cov"]))
            for x in xgrid]
    return pd.DataFrame(rows, columns=["x", "rr", "lo", "hi"])


def bin_response(m, xhi, xref=0.0):
    rows = []
    for bi, (lo, hi) in enumerate(m["cb"].bins):
        b = (m["cb"].bin_basis([xhi], bi) - m["cb"].bin_basis([xref], bi))[0]
        rows.append((f"lag{lo}-{hi}", *_ci(b, m["beta"], m["cov"])))
    return pd.DataFrame(rows, columns=["window", "rr", "lo", "hi"])


def attributable(m, expname, ref=0.0, only="hot", nsim=1000):
    rng = np.random.default_rng(SEED)
    y = m["d"].deaths.values
    ref_b = m["cb"].cumulative_basis([ref])[0]
    L = m["cbX"] - ref_b
    x = m["d"][expname].values
    sel = (x > ref) if only == "hot" else (x < ref) if only == "cold" else np.ones(len(y), bool)
    an = np.where(sel, (1 - np.exp(-np.clip(L @ m["beta"], -10, 10))) * y, 0.0)
    draws = rng.multivariate_normal(m["beta"], m["cov"], size=nsim)
    sims = np.array([np.where(sel, (1 - np.exp(-np.clip(L @ b, -10, 10))) * y, 0.0).sum()
                     for b in draws])
    return an, sims
