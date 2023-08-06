def z_score_calc(dataframe, col, overall=True, group="id"):
    """
    Calculates the z score of each value in a series.

    input:
    ------
    dataframe: pd.DataFrame
    col: str
        Column in dataframe to analyze
    overall: bool
        True: analyzes series without regard to group
        False: analyzes each group independently, then returns a df containing one ID and one z-score column.
    group: str
        Column where identifiers or participants are
    """
    if overall == True:
        my_series = dataframe[col]
        z_col = ((my_series) - my_series.mean()) / my_series.std()
        dataframe[f"{col}_overall_z_score"] = z_col
        return z_col
    else:
        z_df = pd.DataFrame(columns=[group, f"{col}_z_score"])
        my_groups = list(dataframe[group].unique())
        for g in my_groups:
            my_series = dataframe[dataframe[group] == g][col]
            z_score = ((my_series) - my_series.mean()) / my_series.std()
            temp_z_df = pd.DataFrame()
            temp_z_df[f"{col}_z_score"] = z_score
            temp_z_df[group] = g
            z_df = z_df.append(temp_z_df)
        return z_df


def bartlett(args):
    """
    Modified version of scipy stat's bartlett function to accept a list of arrays. Modification: turn args into a list

    Source code: https://github.com/scipy/scipy/blob/v1.5.3/scipy/stats/morestats.py#L2177-L2273
    """
    import numpy as np
    from collections import namedtuple
    import scipy.stats as stats

    # Handle empty input and input that is not 1d
    for a in args:
        if np.asanyarray(a).size == 0:
            return BartlettResult(np.nan, np.nan)
        if np.asanyarray(a).ndim > 1:
            raise ValueError("Samples must be one-dimensional.")

    k = len(args)
    if k < 2:
        raise ValueError("Must enter at least two input sample vectors.")
    Ni = np.zeros(k)
    ssq = np.zeros(k, "d")
    for j in range(k):
        Ni[j] = len(args[j])
        ssq[j] = np.var(args[j], ddof=1)
    Ntot = np.sum(Ni, axis=0)
    spsq = np.sum((Ni - 1) * ssq, axis=0) / (1.0 * (Ntot - k))
    numer = (Ntot * 1.0 - k) * np.log(spsq) - np.sum((Ni - 1.0) * np.log(ssq), axis=0)
    denom = 1.0 + 1.0 / (3 * (k - 1)) * (
        (np.sum(1.0 / (Ni - 1.0), axis=0)) - 1.0 / (Ntot - k)
    )
    T = numer / denom
    pval = stats.distributions.chi2.sf(T, k - 1)  # 1 - cdf

    BartlettResult = namedtuple("BartlettResult", ("statistic", "pvalue"))

    return BartlettResult(T, pval)
