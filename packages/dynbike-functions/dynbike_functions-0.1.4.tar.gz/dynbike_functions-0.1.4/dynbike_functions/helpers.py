"""
A package with frequently used helper functions to process, clean, analyze dynamic bike files.
"""
import sqlalchemy as sq
import pandas as pd
import datetime as dt
import numpy as np

# Prevent the following warning
## SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame.
## Try using .loc[row_index,col_indexer] = value instead
pd.options.mode.chained_assignment = None  # default='warn'


def append_new_df(big_df, small_df, check_elapsed_sec=True):
    """
    Appends small_df to big_df and does some sanity checks along the way.
    Required columns: id_sess, elapsed_sec
    id_sess is the first unique id_sess of small_df

    check_elapsed_sec: bool
        Checks sanity of elapsed_sec, and if True then
        checks whether the first digit of elapsed_sec is 0. If it is not,
        then makes it 0. If sanity is False moves on without doing anything.
    """
    expected_num_cols = len(big_df.columns)
    small_cols = len(small_df.columns)
    try:
        id_sess = small_df["id_sess"].unique()[0]
    except:
        print(
            "id_sess column not found, don't forget to run dataset through processor!"
        )
    if small_cols == expected_num_cols:  # same amount of columns
        if all(small_df.columns == big_df.columns):  # same name columns
            all_ids = list(big_df["id_sess"].unique())
            if id_sess in all_ids:
                print(f"Not appending, {id_sess} already exists in big_df")
                return big_df
            else:  # if not in df already, continue
                if check_elapsed_sec:
                    elapsed_sec = small_df.sort_values("elapsed_sec").reset_index(
                        drop=True
                    )["elapsed_sec"]
                    first_sec = elapsed_sec[0]
                    sane = c.mylist(small_df["elapsed_sec"])
                    if (first_sec != 0) & (sane):
                        small_df["elapsed_sec"] = [i for i in range(len(small_df))]
                        print(
                            "NOTE: elapsed_sec reset to start from 0. It was and is sane."
                        )
                    else:
                        if first_sec != 0:
                            # elapsed_sec is not sane, so no action is taken
                            print(
                                "NOTE: elapsed_sec does not start from 0 and is not sane. No action taken to correct this."
                            )
                        else:
                            print(
                                "NOTE: elapsed_sec is not sane but it does start from 0."
                            )
                print(f"{id_sess} appended")
                return big_df.append(small_df)
        else:
            not_in_big = []
            not_in_small = []
            for small_col in small_df.columns:
                if small_col not in big_df.columns:
                    not_in_big.append(small_col)

            for big_col in big_df.columns:
                if big_col not in small_df.columns:
                    not_in_small.append(big_col)

            if not_in_big:
                print(f"{not_in_big} are not in the big_df")
            if not_in_small:
                print(f"{not_in_small} are not in the small_df")
            return big_df
    else:
        print("small_df and big_df do not have the same number of columns")
        return big_df


class dbConnect:
    def __init__(self, sqlite_db):
        """
        Class to connect to sqlite, then load and list tables

        input
        -----
        sqlite_db: str
            Location of database
        """
        engine = sq.create_engine(sqlite_db)
        cnx = engine.connect()
        meta = sq.MetaData()
        meta.reflect(engine)

        self.cnx = cnx
        self.meta = meta
        self.engine = engine

    def list_tables(self):
        "Lists all tables in db"
        return list(self.meta.tables.keys())

    def load_table(self, table_name):
        "Loads a table from db"

        table = self.meta.tables[table_name]
        resultset = self.cnx.execute(sq.select([table])).fetchall()
        df = pd.DataFrame(resultset)
        df.columns = table.columns.keys()
        return df

    def drop_table(self, table_name):
        """
        Drops give table from database
        """
        table = self.meta.tables[table_name]  # get metadata for table
        table.drop(bind=self.engine)
        print(f"{table_name} dropped from database")

    def save_table(
        self, dataframe, table_name, if_exists="replace", index=False, add_modified=True
    ):
        "Saves dataframe into db, adds 'last_modified' column"
        dt_date = dt.datetime.now()

        if add_modified:
            dataframe["last_modified"] = dt_date

        dataframe.to_sql(table_name, self.cnx, if_exists=if_exists, index=index)

        today = f"{dt_date.month}/{dt_date.day}/{dt_date.year}"
        print(f"Saved as {table_name} on {today}")

    def save_files_to_db(self, recursive_loc="data"):
        """
        Saves csv files to db. Saved for posterity

        input
        -----
        recursive_loc: str
            Location of parent folder where files are. Recursively includes all csv files within child folders of parent folder.
        """
        files = os.listdir(recursive_loc)
        try:
            for file in files:
                if ".csv" in file:
                    df = pd.read_csv(f"data/{file}")
                    new_name = file.replace(".csv", "")
                    df.to_sql(new_name, self.cnx, if_exists="replace", index=False)
            print("All files saved to db")
        except e as Exception:
            print(e)


def calc_sess_time(dataframe):
    "Returns a datetime object indicating how long the dataframe is"
    return dataframe["datetime"].max() - dataframe["datetime"].min()


class cleanOldDf:
    """
    Cleans up an unprocessed bike DF made up of several dynamic bike outputs (that was made with dynamic biking script).
    Must have columns: date, time, hr, cadence, power, id, session in that order.

    count_row true:
        Adds integers for each row, starting over at each session for each participant. Represents seconds.
    date_time true:
        Combines date and time columns in one date column.
    In both cases:
        Converts date to datetime; id and session to category.
    """

    def __init__(self, df):

        # Format the columns
        df.columns = list(pd.Series(df.columns).str.lower())
        df["id"] = df["id"].astype("category")  # format column
        df["hr"] = pd.to_numeric(df["hr"])  # format column
        df["session"] = df["session"].astype("category")  # format column
        self.df = df

    def datetime_maker(self, count_row=False):
        """
        Combines the date and time columns into one datetime column.

        input
        -----
        count_row: bool
            True: runs row_counter() function first, then combines the date and time columns
            False: just combines the date and time columns

        return
        ------
        df: Dataframe
            The dataframe with date and time combined, columns formatted, rows counted (if count_row=True)
        """
        # only call row_counter function if count_row = True, then reorder the columns
        if count_row == True:
            df = self.row_counter(maker=True)
            df[["id", "session", "date", "time", "seconds", "hr", "cadence", "power"]]
        else:
            df = self.df.copy()
            df = df[["id", "session", "date", "time", "hr", "cadence", "power"]]
        # Create date column
        df["date"] = df["date"] + " " + df["time"]
        del df["time"]  # remove time column
        df["date"] = pd.to_datetime(df["date"])
        return df

    def row_counter(self, maker=False):
        """
        Adds a new seconds column that restarts from 0 for each participant + session combination

        input
        ------
        maker: bool
            If True, assumes the dataframe will be processed through self.datetime_maker next. Will not format date col to datetime.
        return
        ------
        df: Dataframe
            the input df, but with a new column of seconds and all colulmns formatted
        """
        old_df = self.df.copy()
        # Prepare to separate old_df into dictionary of dfs
        part = list(old_df["id"].unique())  # list of participants
        sesh = list(old_df["session"].unique())  # list of sessions
        sep_dfs = {}
        # Add in time component (each row is 1 second) to each df for each participant + session combination
        for p in part:
            for s in sesh:
                dfx = old_df[
                    (old_df["id"] == p) & (old_df["session"] == s)
                ]  # select certain participant + session
                dfx = dfx.reset_index(drop=True)  # get rid of the old index
                dfx = dfx.reset_index(
                    drop=False
                )  # create index column with new numbers
                dfx["seconds"] = dfx["index"]  # rename column
                del dfx["index"]  # remove index column
                sep_dfs[f"{p}_{s}"] = dfx  # save into dictionary

        # Turn dictionary into a new df
        keys = sep_dfs.keys()
        example = list(keys)[0]
        all_columns = list(sep_dfs[example].columns)  # grab the columns names
        df = pd.DataFrame(columns=all_columns)  # make a new blank df with column names
        for key in keys:
            df = pd.concat((df, sep_dfs[key]))  # concatenate the dfs into one big one
        df = df[["id", "session", "date", "time", "seconds", "hr", "cadence", "power"]]
        # Format columns
        df["date"] = pd.to_datetime(df["date"]) if not maker else df["date"]
        df["id"] = df["id"].astype("category")
        df["session"] = df["session"].astype("category")
        df["hr"] = pd.to_numeric(df["hr"])
        df["seconds"] = pd.to_numeric(df["seconds"])
        df = df.reset_index(drop=True)  # new index
        return df


class dateAnalysis:
    def __init__(self, dataframe, session="session", date="date"):
        """
        Includes two functions that will extract the date from each participant, and then finds the elapsed time between sessions.

        input
        -----
        dataframe: pd.DataFrame
            Dataframe with at least 'id','date' variables
        session: str
            String with name of variable that contains session numbers
        date: datetime
            Column with all dates
        participant: str
            Column with ids of participants

        self.var
        self.date_df: pd.DataFrame
            Dataframe of id, session, and date only
        """
        self.dataframe = dataframe
        self.session = session
        self.date = date

        dataframe["datetime"] = dataframe[date]
        try:
            dataframe["date"] = dataframe["datetime"].apply(lambda x: x.date())
        except:
            print("Looks like date column is already just dates without time")
        dataframe = dataframe.astype({"id": str, session: str})

        date_df = (
            dataframe.groupby(["id", session, "date"])
            .mean()
            .reset_index()[["id", session, "date"]]
        )
        date_df = date_df.sort_values(["id", "date"])
        date_df = date_df.reset_index(drop=True)

        self.date_df = date_df
        print(
            "Now you can use dateAnalysis.date_diff() to find the difference in dates"
        )

    def date_diff(
        self, dataframe=None, session="session", date="date", participant="id"
    ):
        """
        For use after date_finder function

        Returns a new dataframe with sessions as columns and date of occurrance as datapoint for each participant
        Two new columns are included: elapsed (days between first and last sessions, datetime) and
        elap_int (days between first and last sessions, int)

        input
        -----
        dataframe: pd.DataFrame
            Dataframe created by dateAnalysis.date_finder(). If none given, uses self.date_df
        """
        if not dataframe:
            dataframe = self.date_df

        list_date = list(dataframe[session].unique())  # date col for each session
        list_date.append("elapsed")
        new_date = pd.DataFrame(
            columns=list_date, index=dataframe[participant].unique()
        )  # new df of NaNs to fill in
        # extract the start, mid, end dates for each session

        for part in dataframe[participant].unique():
            temp_df = dataframe[dataframe[participant] == part].reset_index(drop=True)
            date_sr = temp_df[date].sort_values()

            for i in range(len(date_sr)):
                new_date.loc[part, list_date[i]] = date_sr[i]

        new_date["elapsed"] = new_date[list_date[-2]] - new_date[list_date[0]]
        new_date["elap_int"] = (
            new_date["elapsed"].apply(lambda x: str(x)).str.extract("(\d\d?) days")
        )
        self.new_date = new_date
        return new_date

    def date_consistent_checker(self, clean_df=None):
        """
        Checks the number of days elapsed between datetime columns, where the columns are in sequential order

        input
        -----
        clean_df: pd.DataFrame
            Usually created with dateAnalysis.date_diff()
            Sessions must be in own col, each col consisting of datetime.date objects.
        """
        if type(clean_df) == pd.DataFrame:
            dataframe = clean_df.copy()
        else:
            dataframe = self.new_date.copy()

        for num in range(len(dataframe.columns) - 2):
            try:
                dataframe[f"elap{num+2}-{num+1}"] = (
                    dataframe[f"session{num+2}"] - dataframe[f"session{num + 1}"]
                )
                dataframe[f"elap_int{num+2}-{num+1}"] = (
                    dataframe[f"elap{num+2}-{num+1}"]
                    .apply(lambda x: str(x))
                    .str.extract("(\d\d?) days")
                )
                print(f"Finished session{num+1}")

            except Exception as e:
                if "session" in str(e):
                    print(f"Reached end, no session called {e}")
                else:
                    print("Something bad occurred.")
                    print(e)

        return dataframe
    
    
def elapsed_time(dataframe, part, sess, timer="date"):
    """
    Calculates the time that elapsed during each participant's session.

    input
    -----
    part: list
        List of participants to filter by
    sesh: list
        List of sessions that all participants went through
    timer: str
        Column that contains the time variable.
    """
    delta_time = {}
    for p in part:
        for s in sess:
            my_df = dataframe[(dataframe["id"] == p) & (dataframe["session"] == s)]

            delta = my_df[timer].max() - my_df[timer].min()
            delta_time[f"{p}_{s}"] = delta
    return delta_time


def back_to_raw(dataframe, raw_idsess):
    """
    When loading raw bike files, column names are standardized by load_people function. This function
    formats them back to raw, so the dataset can be run through dfBikes() and processed properly.
    """
    raw_cols = ["Date", "Time", "Millitm", "HR", "Cadence", "Power", "ID"]
    dataframe = dataframe.drop(["datetime", "elapsed_sec"], axis=1)
    dataframe.columns = raw_cols

    dataframe["ID"] = raw_idsess

    return dataframe


def perc_time_in_col(dataframe, col, threshold=0, perc="greater", id_col="id_sess"):
    """
    OG purpose: Calculates the percent occurrance of positive `col` values per `id_col`.
    NOT whether the mean is neg or pos.

    input
    -----
    dataframe: pd.DataFrame
    col: str
        Variable of interest to count
    threshold: int
        Number (noninclusive) to consider as threshold
    perc: string
        One of "greater", "lesser", or "equal"
        Determines how to compare all values to the threshold
    id_col: str
        Column participants are identified by

    return
    ------
    df_merged: pd.DataFrame
        Each row represents one `id_col`
        Columns are counts of `col` < 0 and perc in negative for each `id_col`
    """
    try:
        all_count = dataframe.groupby([id_col]).count()[
            [col]
        ]  # count number of lines per id_col

        if perc == "greater":
            val_ = dataframe[dataframe[col] > threshold]  # filter to > threshold
            compare = "pos"
        elif perc == "lesser":
            val_ = dataframe[dataframe[col] < threshold]  # filter to < threshold
            compare = "neg"
        else:
            val_ = dataframe[dataframe[col] == threshold]  # filter to equal threshold
            compare = f"_{threshold}"

        val_count = val_.groupby([id_col]).count()[
            [col]
        ]  # count number of positive lines per id_col

        df1 = all_count.reset_index()  # reset indexes so dataframes can be merged
        df2 = val_count.reset_index()
        df_merged = df2.merge(
            df1, on=[id_col], suffixes=[f"_{compare}", "_all"], how="right"
        )
        # NAs represent id_sess that were in df1 but not in df2
        # if they're not in df2, there were no positive powers
        df_merged = df_merged.fillna(0)
        # calculate and round percent
        df_merged[f"perc_time_in_{compare}"] = round(
            100 * (df_merged[f"{col}_{compare}"] / df_merged[f"{col}_all"]), 2
        )
        df_merged = df_merged.sort_values(f"perc_time_in_{compare}", ascending=False)
        return df_merged
    except Exception as e:
        print(
            "REMINDER: make sure participant ID and session labels are one variable (ex: id_sess)"
        )
        return e


def df_to_dic(dataframe, col1, col2):
    """
    Takes a dataframe and two columns. Returns a dictionary. Assumes col1 and col2 have a 1:1 ratio of key:value

    input
    -----
    col1: str
        The column to use as key
    col2: str
        The column to use as value
    """
    temp_dic = {}

    for i, row in dataframe.iterrows():
        if row[col1] in temp_dic.keys():
            continue
        else:
            temp_dic[row[col1]] = row[col2]
    return temp_dic


def dic_to_df(my_dic):
    """
    Takes a dictionary of dfs, extracts the first df. Appends all other dfs to the first df.

    input:
    -----
    my_dic: dic
        Dictionary of dataframes

    output:
    ------
    new_df: dataframe
    """
    new_df = pd.DataFrame(columns=list(my_dic[list(my_dic.keys())[0]].columns))
    for p in list(my_dic.keys()):
        temp_df = my_dic[p]
        new_df = pd.concat([new_df, temp_df])
        new_df = new_df.reset_index(drop=True)

    return new_df


def label_bmi(score):
    """
    Labels BMI scores based on CDC definitions.

    https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html#InterpretedAdults
    """
    if score < 18.5:
        return "underweight"
    elif score > 30:
        return "obese"
    elif (score >= 18.5) & (score <= 24.9):
        return "normal"
    else:
        return "overweight"


def label_effort(score):
    """
    Labels effort scores based on findings from robert dataset
    """
    if score > 65:
        return "high"
    elif score < 35:
        return "low"
    else:
        return "medium"


def load_people(my_id, dataframe, raw=False):
    """
    Loads id_sess from given dataset
    """
    if raw:
        my_id = my_id.replace("SMB", "SMB_")
        temp_df = dataframe[dataframe["ID"].str.contains(my_id)]
        temp_df.columns = [col.lower() for col in temp_df.columns]
        # format the raw_df columns for plotting
        temp_df["datetime"] = temp_df["date"] + " " + temp_df["time"]
        temp_df["datetime"] = pd.to_datetime(temp_df["datetime"])
        temp_df["elapsed_sec"] = [i for i in range(len(temp_df))]
        return temp_df
    else:
        ptemp_df = dataframe[dataframe["id_sess"] == my_id]
        return ptemp_df


def num_scriptor(phrase, script):
    """
    Turns all numbers into subscripts or superscripts

    input
    -----
    phrase: str
        Any string with digits in it
    script: str
        'sub': creates subscripts
        'sup': creates superscripts

    return
    ------
    phrase: str
        String with the digits sub/superscripted

    Source: https://stackoverflow.com/a/24392215/
    """
    if script == "sub":
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return phrase.translate(SUB)
    elif script == "sup":
        SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        return phrase.translate(SUP)
    else:
        return "script must be sub or sup"


def remove_idsess(id_sess, dataframe):
    """
    Removes the id_sess from dataframe. Created to avoid repetitive mistakes.
    """
    return dataframe[dataframe["id_sess"] != id_sess]


def save_to_excel(dataframe, save_loc="output/", force=False):
    """
    Saves each id_sess into a separate xlsx file at the given location, to be used with MatLab
    entropy script.

    Columns: [Date, HR, Cadence, Power, ID]
    Filename: id_sess.xlsx
    """
    from tqdm.notebook import tqdm as prog_bar

    all_ids = list(dataframe["id_sess"].unique())
    for id_sess in prog_bar(all_ids, ascii=True):
        name = f"{save_loc + id_sess}.xlsx"
        temp = dataframe[dataframe["id_sess"] == id_sess].reset_index(drop=True)

        if not c.mylist(temp["elapsed_sec"]):
            # Did not pass sanity check
            if force:
                # if user wants to save it regardless, notify and save
                print(
                    f"WARNING: Saved as xlsx, but {id_sess} did not pass sequential check."
                )
            else:
                # otherwise notify user and pass
                print(
                    f"WARNING: {id_sess} did not pass sequential check. Not saved as xlsx file."
                )
                continue
        temp = temp[["datetime", "hr", "cadence", "power", "id_sess"]]
        temp.columns = ["Date", "HR", "Cadence", "Power", "ID"]
        temp.to_excel(name, index=False)
    print("Saved!")


def session_extractor(dataframe, head_dic, tail_dic):
    """
    Extract the sessions from each participant

    input
    -----
    dataframe
    head_dic: dic
        Dictionary in format of dic{id = [loc, mean, std]} where id represents participant/session combo,
        and loc represents the row index where the cutting will start
    tail_dic: dic
        Dictionary in format of dic{id = [loc, mean, std]} where id represents participant/session combo,
        and loc represents the row index where the cutting will end

    return
    ------
    new_df: dataframe
        Original dataframe but with each participant/session combo shortened according to given dictionaries.
    """
    # cut out subdataframes
    temp_dic = {}
    for key, value_h in head_dic.items():
        value_t = tail_dic[key]
        temp_df = dataframe[dataframe["id_sess"] == key]
        temp_df = temp_df.reset_index(drop=True)
        temp_df = temp_df.iloc[value_h[0] : value_t[0], :]
        temp_df = temp_df.reset_index(drop=True)
        temp_dic[key] = temp_df

    # recreate dataframe
    new_df = pd.DataFrame(columns=list(dataframe.columns))
    for key, value in temp_dic.items():
        new_df = pd.concat([new_df, value])
    new_df = new_df.reset_index(drop=True)

    return new_df


########################
# DEPRECATED FUNCTIONS #
########################


def balancer(dataframe):
    """
    Deprecated.

    Removes participants 2,6,7 so dataset can be analyzed with RM ANOVA. Only useful for Robert dataset.
    """
    new_df = dataframe[
        (dataframe["id"] != "pdsmart002")
        & (dataframe["id"] != "pdsmart006")
        & (dataframe["id"] != "pdsmart007")
    ]
    return new_df


def get_raw_idsess(id_sess, raw_dataframe):
    """
    Deprecated. Used for NIH dataset only.

    Locates the original id from raw_df
    """
    id_sess = id_sess.replace("SMB", "SMB_")
    temp = raw_dataframe[raw_dataframe["ID"].str.contains(id_sess)].reset_index(
        drop=True
    )

    raw_idsess = temp.loc[0, "ID"]

    return raw_idsess
