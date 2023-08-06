'''
Package to check sanity of dynamic bike datasets
'''


def dup_timestamps(dataframe):
    """
    Checks for duplicate timestamps. Returns a dataframe of results.
    """
    num_dups = dataframe.groupby("datetime").count()["cadence"]
    result = num_dups[num_dups > 1]

    result_df = pd.DataFrame()

    if len(result) != 0:
        for dup_date in result.index:
            num = result[dup_date]  # number of dups
            # get start of the dup
            dup_index = dataframe[dataframe["datetime"] == dup_date].index[0]
            result_df = result_df.append(
                pd.DataFrame(
                    {
                        "duplicate_stamp": [dup_date],
                        "num_dups": [num],
                        "location": [dup_index],
                    }
                )
            )
        return result_df
    else:
        return pd.DataFrame()


def mylist(myseries):
    """
    Checks whether a series of integers is sequential. Returns EMPTY if list is empty.

    input
    -----
    mylist : series, int
    """
    if myseries.empty == False:
        it = (x for x in myseries)
        first = next(it)
        return all(a == b for a, b in enumerate(it, first + 1))
    else:
        return "**LIST IS EMPTY**"


def sanity(new_df, num_part, num_sess):
    """
    Checks that dataframe contains num_part participants, and that each participant has num_sess sessions, sends print statement.

    Requires id and session columns

    input
    -----
    new_df: pd.DataFrame
        Dataframe to check
    num_part: int
        Number of participants
    num_sess: int
        Number of sessions per participant

    output
    ------
    result: pd.DataFrame
        Dataframe that includes the participant id, number of sessions, and expected number of sessions
    """
    import pandas as pd

    part = list(new_df["id"].unique())
    sesh = list(new_df["session"].unique())
    part_size = len(new_df["id"].unique())
    if num_part == part_size:
        print(f"There are still {num_part} participants")
    else:
        print(f"Missing {num_part-part_size} participants")

    print(
        f"""-------------------
Checking whether {num_sess} sessions still exist
-------------------"""
    )
    result = pd.DataFrame()
    for p in part:
        ses_size = len(new_df[new_df["id"] == p].loc[:, "session"].unique())
        if num_sess == ses_size:
            pass
        else:
            print(f"{p}: Missing {num_sess-ses_size} sessions")

        result = result.append(
            pd.DataFrame({"id": p, "num_sessions": [ses_size], "expected": [num_sess]})
        )
    return result.reset_index(drop=True)


def in_there(my_list, my_series):
    """
    Sorts each element into 'there' or 'not_there' lists, depending on whether
    or not they appear in my_series. Returned as a dictionary.

    input
    -----
    my_list: list
        List of elements to check
    my_series: pd.Series
        Series that the elements should (or should not) be in

    output
    ------
    result: dict
        Dictionary of lists 'there' and 'not_there'
    """
    there = []
    not_there = []
    mylist = list(my_series.unique())
    for x in my_list:
        if x in mylist:
            there.append(x)
        else:
            not_there.append(x)
    result = {"there": there, "not_there": not_there}
    return result
