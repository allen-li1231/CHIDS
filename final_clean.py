import numpy as np
import pandas as pd
import re
import seaborn as sns
from libTools import numInterval


# translate words into numeric
d_word_num = {"nil": '0',
              "sober": '0',
              "every ": '1 ',
              "once": '1',
              "one": '1',
              "twice ": '2',
              "two": '2',
              "three": '3',
              "four": '4',
              "five": '5',
              "six": '6',
              "seven": '7',
              "eight": '8',
              "nine": '9',
              "ten": '10',
              "few": ">1",
              "several": ">2",
              "couple time": ">1",
              " lot": " >5",
              "heavy": ">5"
              # more to add
              }

# read files
doclist = pd.read_csv("./data/finalcombineddoc.csv", sep=',', encoding='latin1', index_col=None, header=0)
obsdata = pd.read_csv("./data/obsdata.csv", encoding='latin1', index_col=None, header=0)
labs = pd.read_csv("./data/labs.csv", encoding='latin1', index_col=None, header=0)

doclist.PID.unique().shape
# Out[15]: (16011,)
obsdata.OBSID.unique().shape
# Out[38]: (20765894,)

# grasp hdid summaries with count
hdid_smy = obsdata.groupby(['HDID', "DESCRIPTION"])['SDID'].count()
hdid_smy = hdid_smy.reset_index()
# columns we need to examine
examine_cols = ["OBSID", "SDID", "HDID", "DESCRIPTION", "OBSDATE", "OBSVALUE"]

# first go for family history
hdid_smy.loc[hdid_smy['DESCRIPTION'].str.lower().str.contains("history")]
# 1057, 4705
hdid_smy.loc[hdid_smy['DESCRIPTION'].str.lower().str.contains("diabete")]
# 2303
family_hx = obsdata[obsdata['HDID'].isin([2303, 4705])][examine_cols]
family_hx.sort_values(["OBSID", "OBSDATE"], inplace=True)

family_hx.SDID.unique().shape[0] / doclist.SDID.unique().shape[0]
# approximate proportion: 24%-25%

df_family_hx = family_hx.groupby(["HDID", "DESCRIPTION", "OBSVALUE"])["OBSID"].count()

# next, find diet and physical exercise
hdid_smy.loc[hdid_smy['DESCRIPTION'].str.lower().str.contains("diet|exercise", regex=True)]
# exercise: freq: 128, time: 2664, comment: 8768
# diet: 2487, 1167, 77728
exercise_hx = obsdata[obsdata['HDID'].isin([128, 2664, 8768])][examine_cols]
exercise_hx.OBSVALUE = exercise_hx.OBSVALUE.str.lower()
df_exercise_hx = exercise_hx.groupby(["HDID", "DESCRIPTION", "OBSVALUE"])["OBSID"].count()
diet_hx = obsdata[obsdata['HDID'].isin([2487, 1167, 77728])][examine_cols]
diet_hx.OBSVALUE = diet_hx.OBSVALUE.str.lower()
df_diet_hx = diet_hx.groupby(["HDID", "DESCRIPTION", "OBSVALUE"])["OBSID"].count()

# now alcohol and caffeine
hdid_smy.loc[hdid_smy['DESCRIPTION'].str.lower().str.contains("alcohol|caffeine", regex=True)]
# alcohol: 2313, 10102, 7591
# caffeine: 2738, 30515
alcohol_hx = obsdata[obsdata['HDID'].isin([2313, 10102, 7591])][examine_cols]
alcohol_hx.OBSVALUE = alcohol_hx.OBSVALUE.str.lower()
df_alcohol_hx = alcohol_hx.groupby(["HDID", "DESCRIPTION", "OBSVALUE"])["OBSID"].count()
caffeine_hx = obsdata[obsdata['HDID'].isin([2738, 30515])][examine_cols]
caffeine_hx.OBSVALUE = caffeine_hx.OBSVALUE.str.lower()
df_caffeine_hx = caffeine_hx.groupby(["HDID", "DESCRIPTION", "OBSVALUE"])["OBSID"].count()

# output files
df_family_hx.to_csv("./final_dump/family_hx.csv")
# df_exercise_hx.to_csv("./final_dump/exercise_hx.csv")
# df_diet_hx.to_csv("./final_dump/diet_hx.csv")
df_alcohol_hx.to_csv("./final_dump/alcohol_hx.csv")
df_caffeine_hx.to_csv("./final_dump/caffeine_hx.csv")

family_hx = family_hx[family_hx.HDID == 2303]
family_hx["dmy_has_family_hx"] = np.where(family_hx.OBSVALUE == 'no', 'NO', "YES")
family_hx["dmy_count_family_hx"] = np.where(family_hx.OBSVALUE == 'no', 0, family_hx.OBSVALUE.str.count(',')+1)

PID_SDID = doclist[['PID', 'SDID']]
patient_family_hx = pd.merge(PID_SDID, family_hx, 'right', "SDID")
patient_family_hx.to_csv("./family_hx_dmy.csv", index=False)


# rule of making dummies for alcohol
def alcohol_freq(s_val: str):
    s_val = s_val.lower()
    for k, v in d_word_num.items():
        s_val = s_val.replace(k, v)

    # find comparable numbers in the string
    lst_matched = re.findall(r"([<>]? ?=? ?[+-]?\.?\d+\.?\d*) ?-? ?(\.?\d*\.?\d*)", s_val)
    # check if any matches
    if len(lst_matched) != 0:
        n_l, n_r = lst_matched[0]
        n_l = numInterval(n_l)
        n_r = float(n_r) if n_r else n_l
        n_mean = (n_r+n_l) / 2.

        if "wk" in s_val or "week" in s_val:
            n_mean = n_mean / 7.

        if "mon" in s_val:
            n_mean = n_mean / 30.

        if "weekend" in s_val or "social" in s_val or s_val == "soc":
            n_mean = n_mean * 3 / 7.

        if "yr" in s_val or "year" in s_val:
            n_mean = n_mean / 365

        # dont do anything right now to matched numbers that makes no sense
        if not (n_mean >= 50 or n_mean < 0):
            if "pint" in s_val or n_mean >= 5:
                return "alcoholic"
            elif n_mean > 1:
                return "daily"
            else:
                return "infrequent"

    if "alcoholic" in s_val or "pint" in s_val:
        return "alcoholic"

    if any(["mod" in s_val,
            "yes" in s_val,
            "qd" in s_val,
            "qod" in s_val,
            "qhs" in s_val,
            "wine" in s_val,
            "vine" in s_val,
            "sacramental" in s_val,
            "beer" in s_val,
            "budweiser" in s_val,
            "coolers" in s_val,
            "chanpagne" in s_val,
            "champange" in s_val,
            "peach snapps" in s_val,
            "all" in s_val,
            "daily" in s_val,
            "current" in s_val,
            "most days" in s_val,
            "everyday" in s_val,
            "periodic" in s_val,
            "on" == s_val,
            "oz per day" in s_val]):
        return "daily"

    if any(["sometimes" in s_val,
            "infrequent" in s_val,
            "social" in s_val,
            s_val == "soc",
            "couple" in s_val,
            "off and on" in s_val,
            "decrease" in s_val]):
        return "infrequent"

    if "weekend" in s_val or "social" in s_val or s_val == "soc" or "sicial" in s_val or "socail" in s_val:
        return "infrequent"

    if "weekly" in s_val:
        return "infrequent"

    if "monthly" == s_val or "qom" == s_val:
        return "infrequent"

    if any(["occ" in s_val,
            "oacc" in s_val,
            "rar" in s_val,
            "ocas" in s_val,
            "seldom" in s_val,
            "mild" in s_val,
            "limit" in s_val,
            "minimal" in s_val,
            "little" in s_val,
            "r very are" == s_val,
            "raer" == s_val]):
        return "infrequent"

    if "former" in s_val or "previous" in s_val or "history" in s_val or "stop" in s_val or "used to" in s_val:
        return "denies"

    if any(["fruit drink" in s_val,
            "denies" in s_val,
            "denis" in s_val,
            "denied" in s_val,
            "disable" in s_val,
            "no" in s_val,
            "non" in s_val,
            "never" in s_val,
            "quit" in s_val]):
        return "denies"

    if any(["liquor" in s_val,
            "liqour" in s_val,
            "liquior" in s_val,
            "spirits" in s_val,
            "rum" in s_val,
            "vodka" in s_val,
            "whisky" in s_val,
            "whiskey" in s_val,
            "gin" in s_val,
            "brandy" in s_val,
            "pina colada" in s_val,
            "vermouth" in s_val,
            "cocktail" in s_val,
            "abstinant" in s_val,
            "long island ice tea" in s_val,
            "bud light lime" in s_val,
            "mix" in s_val,
            "margaritas" in s_val,
            "martini" in s_val,
            "scotch" in s_val,
            "scoth" in s_val,
            "bourbon" in s_val,
            "martini" in s_val,
            "hennessy" in s_val,
            "henessy" in s_val,
            "jack dan" in s_val,
            "burbon" in s_val,
            "white russian" in s_val,
            "cognac" in s_val,
            "cognnac" in s_val,
            "bourbon" in s_val,
            "alcohol" in s_val,
            "shots" in s_val]):
        return "alcoholic"

    if s_val == 'o':
        return "denies"

    return "unknown"


alcohol_hx["dmy_OBSVALUE"] = alcohol_hx["OBSVALUE"].apply(alcohol_freq, convert_dtype=False)
alcohol_freq = alcohol_hx.groupby("dmy_OBSVALUE")["SDID"].count()
alcohol_freq = alcohol_freq[['alcoholic', 'daily', 'infrequent', 'denies', 'unknown']]

ax1_title = f"Proportion across categories in Medstar's final data"
sns.set_style("whitegrid")
ax1 = sns.barplot(x=alcohol_freq.index, y=alcohol_freq, palette="BuGn_r")
ax1.set_title(ax1_title)
ax1.set(xlabel="Category", ylabel="Frequency")
ax1.set_ylim(top=max(alcohol_freq) * 1.2)
for bar, f in zip(ax1.patches, alcohol_freq):
    text_x = bar.get_x() + bar.get_width() / 2
    text_y = bar.get_height()
    text = f"{f:,}\n{f/sum(alcohol_freq):.2%}"
    ax1.text(text_x, text_y, text,
             fontsize=10, ha='center', va='bottom')

