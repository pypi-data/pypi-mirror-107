# -*- coding: utf-8 -*-
import os
import sys

import click
import numpy as np
from pandas import DataFrame, read_csv
from scipy.stats import norm


@click.command()
@click.option("-y", help="The outcome variable of interest", required=True)
#@click.option("-g", help="Grouping column")
def main(y):
    df = read_csv(sys.stdin)
    data = np.array(df[y])
    s = np.sort(data)
    n = len(data)
    k = np.floor(np.log2(n)) - 3
    alpha = 0.05
    k = int(np.floor(np.log2(n) - np.log2(2 * (norm.ppf(q=1 - (alpha / 2)) ** 2))))
    lvl = (k - 1) * 2
    nq = lvl - 1
    qs = np.zeros(nq)  # initialize array of quantiles

    def f(n):
        return (1 + np.floor(n)) / 2

    for i in range(1, k):
        # print("---------")
        # print(i)
        if i == 1:
            """
            median calculation
            """
            d = f(n)
            qs[i - 1] = 0.5
        else:
            d = f(d)
            if np.ceil(d) != np.floor(d):
                l_idx1 = int(np.floor(d))
                l_idx2 = int(np.ceil(d))
                u_idx1 = int(np.floor(n - d + 1))
                u_idx2 = int(np.ceil(n - d + 1))
                l = np.average([s[l_idx1], s[l_idx2]])
                u = np.average([s[u_idx1], s[u_idx2]])
                ql = np.average([l_idx1 / n, l_idx2 / n])
                qu = np.average([u_idx1 / n, u_idx2 / n])
            else:
                l = s[int(d)]
                u = s[int(np.floor(n - d + 1))]
                ql = int(d) / n
                qu = int(np.floor(n - d + 1)) / n
            qs[((i - 1) * 2) - 1] = ql
            qs[(i - 1) * 2] = qu

    vf = np.quantile(data, qs)
    qlower = qs[1::2]
    qupper = qs[2::2]
    lower = vf[1::2]
    upper = vf[2::2]
    tail_area = 2 ** np.arange(2, k)

    df = d = {
        "tail_area_odds": tail_area,
        "lower_quantile": qlower,
        "upper_quantile": qupper,
        "lower_value": lower,
        "upper_value": upper,
    }

    df = DataFrame(d).round(decimals=5)
    df.to_csv("/tmp/lvplot.csv", index=False)
    os.system("cat /tmp/lvplot.csv")


if __name__ == "__main__":
    main()
