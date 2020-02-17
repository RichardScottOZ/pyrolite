"""
Compositional Data Imputation
-----------------------------

pyrolite includes the :func:`~pyrolite.comp.impute.EMCOMP` compositional missing data
imputation algorithm of Palarea-Albaladejo and Martín-Fernández (2008).
This algorithm imputes 'below-detection' data based on specified proportion thresholds.

.. note:: This example and features in this module are currently incomplete and a work in progress.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyrolite.comp.impute import EMCOMP
from pyrolite.util.synthetic import random_composition, random_cov_matrix
from pyrolite.plot import pyroplot

np.random.seed(41)
########################################################################################

sample_data = random_composition(
    size=1000,
    D=4,
    cov=random_cov_matrix(3, sigmas=[0.1, 0.3, 0.15]),
    propnan=0.1,
    missing="MNAR",
    missingcols=3,
)
########################################################################################
imputed_data, p0, niter = EMCOMP(
    sample_data, threshold=np.nanpercentile(sample_data, 10, axis=0), tol=0.01
)
imputed_data = pd.DataFrame(imputed_data, columns=["A", "B", "C", "D"])
########################################################################################
fig, ax = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(12, 5))

ax[0].set_title("Original Data")
ax[1].set_title("New Imputed Data")
ax[2].set_title("Imputed Dataset")
fltr = (np.isfinite(sample_data).sum(axis=1)) == sample_data.shape[1]
imputed_data.loc[fltr, ["A", "B", "C"]].pyroplot.scatter(
    marker="D", color="0.5", alpha=0.1, ax=ax[0], no_ticks=True
)
imputed_data.loc[~fltr, ["A", "B", "C"]].pyroplot.scatter(
    marker="D", color="r", alpha=0.1, ax=ax[1], no_ticks=True
)
imputed_data.loc[:, ["A", "B", "C"]].pyroplot.scatter(
    marker="D", color="k", alpha=0.1, ax=ax[2], no_ticks=True
)
########################################################################################
import scipy.stats

fig, ax = plt.subplots(1)
sigma = 0.1
dif = np.random.randn(15)
SD = np.sort(dif / sigma)
ϕ = scipy.stats.norm.pdf(SD, loc=0, scale=1)
Φ = scipy.stats.norm.cdf(SD, loc=0, scale=1)
ax.plot(SD, ϕ, color="0.5", ls="-.", label="PDF")
ax.plot(SD, Φ, color="0.5", label="CDF")
ax2 = ax.twinx()
ax2.plot(SD, ϕ / Φ, color="k", label="PDF/CDF")  # pdf / cdf
ax2.scatter(SD, sigma * ϕ / Φ, color="k", label="D")
ax.legend(frameon=False, facecolor=None)
ax2.legend(frameon=False, facecolor=None)
ax.set_yscale("log")
plt.show()