"""
Some functions to help plot more complicated graphs.
"""


def plot_before_after(id_sess, before, after, mark=None):
    """
    Plots two dataframes side by side.
    `mark` can be a dictionary of list [x,y] that should be colored in the before plot

    example:
        cut_us = {
            'first':(213,80),
            'second':(321,72)
        }

        plot_before_after(id_sess, before_df, after_df, mark=cut_us)
    """
    fig, ax = plt.subplots(ncols=2, figsize=(10, 4))

    sns.scatterplot(x="elapsed_sec", y="cadence", data=before, ax=ax[0])
    ax[0].set_title(f"{id_sess} | Before | {calc_sess_time(before)} minutes")
    if mark:
        for key in mark.keys():
            point = mark[key]
            ax[0].scatter(x=point[0], y=point[1], c="red")

    sns.scatterplot(x="elapsed_sec", y="cadence", data=after, ax=ax[1])
    ax[1].set_title(f"After | {calc_sess_time(after)} minutes")


def plot_one(id_sess, dataframe):
    """
    Quickly plots a single dataframe
    """
    sns.scatterplot(x="elapsed_sec", y="cadence", data=dataframe)
    plt.title(f"{id_sess}: cadence over time")


def plot_corr_triangle(df, output=None, annot=True, figsize=(11, 9), **kwargs):
    """
    Gets the lower half of a correlation dataframe, plots it.

    input
    -----
    df: pd.DataFrame
        Dataframe previously run through the pd.DataFrame.corr() functions
    output: str
        Saves the figure as that filename
    annot: bool
        Whether to show correlations in the heatmap
    **kwargs:
        All keywords are passed to sns.heatmap()

    Source: https://stackoverflow.com/a/59173863
    """
    import seaborn as sns
    import matplotlib.pyplot as plt

    mask = np.zeros_like(df, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Want diagonal elements as well
    mask[np.diag_indices_from(mask)] = False

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=figsize)

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns_plot = sns.heatmap(
        df,
        mask=mask,
        cmap=cmap,
        annot=annot,
        vmin=-1,
        vmax=1,
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5},
        **kwargs,
    )
    plt.yticks(rotation=0)
    # save to file
    if type(output) == str:
        fig = sns_plot.get_figure()
        fig.savefig(output)
