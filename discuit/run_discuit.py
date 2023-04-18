# TODO: maybe include more than 1 absolute variable? maybe all categorical variables can be absolute?
# TODO: consider stopping if silhouette score is too low. Exit with error message.
# pylint: disable-msg=too-many-locals

import argparse
import pathlib
import sys
from typing import List
import pandas as pd
from kmodes.kmodes import KModes
from kmodes.kprototypes import KPrototypes
from scipy.stats import chi2_contingency
from scipy.stats import kruskal
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


# check whether path and number of sets arguments were provided
parser = argparse.ArgumentParser()
parser.add_argument('datapath', type=pathlib.Path, help='path to input data file (csv)')
parser.add_argument('sets', type=int, help='provide number of desired sets')
parser.add_argument('--columns', nargs='*',
                    choices=['l', 'c', 'n', 'a', 'd'],
                    help='provide the data type for each column (l(abel)/c(ategorical)'
                         '/n(umerical)/a(bsolute)/d(isregard).'
                         'The number of labels needs to match the number of columns'
                         ' in your input file. If this is not the case you can provide '
                         'them later on and your input will be ignored.'
                         '"Label" and "absolute" can only be specified once.',
                    default=None)
parser.add_argument('--runs', type=int,
                         help='indicate how many different output options you want to generate',
                    default=1)
args = parser.parse_args()
no_sets = int(sys.argv[2])

# read file and check if it's suitable
# noinspection PyBroadException
try:
    input_d = pd.read_csv(sys.argv[1])
    filename = pathlib.Path(sys.argv[1]).with_suffix('').name
except FileNotFoundError:
    print("File not found.")
    sys.exit(1)  # abort
except pd.errors.EmptyDataError:
    print("No data")
    sys.exit(1)  # abort
except pd.errors.ParserError:
    print("Parse error")
    sys.exit(1)  # abort
except Exception:
    print("Something else went wrong. \n "
          "Make sure your input looks as follows: \n"
          "'model.py [path to csv file] [number of sets].'")
    sys.exit(1)  # abort

# The following info must come from user. In GUI this should be selected in the GUI after opening a file!
categorical_features = []
continuous_features = []
absolute_features = []
label = []
disregard = []
# number of runs provided as an argument. If nothing is provided it's 1. Also needs to come from GUI!
iterations = args.runs


# Check all the columns and ask about status. Label and absolute can only be chosen once.
if args.columns is None or len(args.columns) != len(input_d.columns): # noqa: MC0001
    print("You didn't provide valid data type indications when running the program. Please specify them now")
    for column in input_d.columns:
        feature = None
        while feature is None:
            input_value = input("Is '" + column + "' the label (can only be assigned once), a categorical, "
                                                  "numerical or absolute (can be assigned once) variable "
                                                  "or should it be disregarded in splitting? l/c/n/a/d ")
            if input_value not in ('l', 'c', 'n', 'a', 'd'):
                print("Please choose either l, c, n, a or d ")
            else:
                feature = input_value
                if feature == "c":
                    categorical_features.append(column)
                elif feature == "n":
                    continuous_features.append(column)
                elif feature == "a":
                    if len(absolute_features) > 0:
                        print('You already have an absolute feature. Please choose something else.')
                        feature = None
                    else:
                        absolute_features.append(column)
                elif feature == "l":
                    if len(label) > 0:
                        print('You already have a label. Please choose something else.')
                        feature = None
                    else:
                        label.append(column)
                elif feature == "d":
                    disregard.append(column)
# if specified when running program, take them from there
else:
    for column in input_d.columns:
        feature = args.columns[input_d.columns.get_loc(column)]
        if feature == "c":
            categorical_features.append(column)
        elif feature == "n":
            continuous_features.append(column)
        elif feature == "a":
            absolute_features.append(column)
        elif feature == "l":
            label.append(column)
        elif feature == "d":
            disregard.append(column)
    if len(label) > 1:
        print("More than one 'label' was specified. Please use -h to get help in providing suitable arguments")
        sys.exit(1)  # abort
    if len(absolute_features) > 1:
        print(
            "More than one 'absolute' variable was specified. Please use -h to get help in providing suitable arguments")
        sys.exit(1)  # abort


def prepare_data(data, continuous, categorical, label, disregard):
    # remove label column & disregarded columns
    if len(label) != 0:
        data = data.drop([label[0]], axis=1)
    if len(disregard) != 0:
        data = data.drop(disregard, axis=1)
    # transform continuous data
    if len(continuous) != 0:
        #replace md with average
        for feat in continuous:
            data[feat].fillna(data[feat].mean(), inplace=True)
        mms = MinMaxScaler()
        data[continuous] = mms.fit_transform(data[continuous])
    # make sure categorical data uses numbers (for silhouette score)
    if len(categorical) != 0:
        for feat in categorical:
            # replace missing data with dummy category
            data[feat].fillna("missingData", inplace=True)
            if data[feat].dtype not in ("float64", "int64"):
                # find unique values
                values = data[feat].unique()
                i = 0
                # replace values
                for value in values:
                    data[feat].replace(value, i, inplace=True)
                    i=i+1
    return data


def clustering(transformed_data, categorical_features, continuous_features):
    # determine max number of clusters...
    max_clus = int(len(transformed_data) * .5)
    max_clus = min(max_clus, 10)
    cl_range = range(2, max_clus)  # changed to max 10 clusters to keep speed, check which max is appropriate
    # kmodes prototype for mixed numerical and categorical data
    largest_sil = (0, -1)

    # this needs to be adjusted depending on input
    categorical_features_idx = [transformed_data.columns.get_loc(col) for col in categorical_features]
    mark_array = transformed_data.values

    # choose algorithm depending on input
    if (len(categorical_features) != 0) and (len(continuous_features) != 0):
        for k in cl_range:
            kproto = KPrototypes(n_clusters=k, max_iter=20)
            kproto.fit_predict(mark_array, categorical=categorical_features_idx)
            sil = metrics.silhouette_score(transformed_data, kproto.labels_, sample_size=1000)
            if sil > largest_sil[1]:
                largest_sil = (k, sil)
        kproto_final = KPrototypes(n_clusters=largest_sil[0], max_iter=20)

        pred_cluster = kproto_final.fit_predict(mark_array, categorical=categorical_features_idx)

    elif (len(categorical_features) != 0) and (len(continuous_features) == 0):
        for k in cl_range:
            kmode = KModes(n_clusters=k, init="random", n_init=5)
            kmode.fit_predict(transformed_data)
            sil = metrics.silhouette_score(transformed_data, kmode.labels_, sample_size=1000)
            if sil > largest_sil[1]:
                largest_sil = (k, sil)
        kmode_final = KModes(n_clusters=largest_sil[0], init="random", n_init=5)
        pred_cluster = kmode_final.fit_predict(transformed_data)
    else:
        for k in cl_range:
            km = KMeans(n_clusters=k, n_init=1, init='k-means++')
            km.fit_predict(transformed_data)
            sil = metrics.silhouette_score(transformed_data, km.labels_, sample_size=1000)
            if sil > largest_sil[1]:
                largest_sil = (k, sil)
        km_final = KMeans(n_clusters=largest_sil[0], init='k-means++', n_init=1)
        pred_cluster = km_final.fit_predict(transformed_data)

    clusters: List[List[int]] = [[] for _ in range(largest_sil[0])]

    for i, cluster in enumerate(pred_cluster):
        clusters[cluster].append(i)

    final_clusters = []

    for cluster in clusters:
        cluster_new = []
        for item in cluster:
            cluster_new.append(transformed_data.iloc[item].name)
        final_clusters.append(cluster_new)

    return final_clusters

def divide_in_sets(clusters, output_sets):
    # divide clusters evenly amongst desired sets
    for cluster in clusters:
        for item in cluster:
            output_sets[output_sets.index(min(output_sets, key=len))].append(item)


def split(absolute, data):
    try:
        grouped = data.groupby(absolute)
    except KeyError:
        print('You listed an absolute variable that cannot be found in the input file')
        sys.exit(1)  # abort

    data_splitted = []
    for _, group in grouped:
        # drop absolute columns from further analysis
        data_x = group.drop(columns=absolute)
        data_splitted.append(data_x)

    return data_splitted


def kwtest(label, features, sets, data):
    stats = []
    df = len(sets) - 1
    for feat in features:
        kw_input = []
        for s_set in sets:
            itemlist = data.loc[data.set_number == s_set, feat].tolist()
            kw_input.append(itemlist)
        stat, p = kruskal(*kw_input)
        stats.append([label, "Kruskal-Wallis test", feat, stat, df, p])
    return stats


def chi(label, features, data):
    stats = []
    for feat in features:
        data_crosstab = pd.crosstab(data[feat],
                                    data['set_number'])

        # check expected values and only use yates correction if any exp value < 5
        _, _, _, exp = chi2_contingency(data_crosstab)
        yates = False
        test = "Chi2-Test"

        for exp_list in exp:
            if any(x < 5 for x in exp_list):
                yates = True
                test = "Chi2-Test with Yates correction"

        stat, p, dof, _ = chi2_contingency(data_crosstab, correction=yates)

        stats.append([label, test, feat, stat, dof, p])

    return stats


def statistics(data):
    stats_out = []
    subsets = data[absolute_features[0]].unique()
    sets = data.set_number.unique()

    for subset in subsets:
        stats_frame = data.loc[data[absolute_features[0]] == subset]
        stats_out.append(kwtest(subset, continuous_features, sets, stats_frame))
        stats_out.append(chi(subset, categorical_features, stats_frame))

    # overall stats
    stats_out.append(kwtest("overall", continuous_features, sets, data))
    stats_out.append(chi("overall", categorical_features, data))
    stats_out.append(chi("overall", absolute_features, data))
    return stats_out


def write_out(stats, i, significant, it_num):
    # output file
    out_file_name = filename + "_out" + str(it_num) + ".csv"
    input_d.to_csv(out_file_name, index=False)
    # save statistics to file if there was more than 1 set
    if no_sets > 1:
        stat_file_name = filename + "_stats" + str(it_num) + ".txt"
        with open(stat_file_name, "w",encoding="utf8") as f:
            iterations = i + 1
            stat_string = f'Number of iterations: {iterations} \n \nResults for the following tests:\n'

            if significant:
                stat_string += ("\nIn 20 iterations no split could be found that results in p>.2 for all variables.\n\n")

            for testgroup in stats:
                for test in testgroup:
                    stat_string += (f"Absolute variable instance '{stats[stats.index(testgroup)][testgroup.index(test)][0]}'"
                                f": {stats[stats.index(testgroup)][testgroup.index(test)][1]} for "
                                + stats[stats.index(testgroup)][testgroup.index(test)][2]
                                + f": X2({stats[stats.index(testgroup)][testgroup.index(test)][4]}) = "
                                  f"{round(stats[stats.index(testgroup)][testgroup.index(test)][3],3)},"
                                  f"p = {round(stats[stats.index(testgroup)][testgroup.index(test)][5], 3)};\n")


            if len(categorical_features) > 0:
                stat_string += ("\nCross-tables for the distribution of categorical features:\n\n")
                for feat in categorical_features:
                    data_crosstab = pd.crosstab(input_d[feat],
                                            input_d['set_number'], margins=True)
                    stat_string += (data_crosstab.to_string() + "\n\n")

            if len(absolute_features) > 0:
                stat_string += ("\nCross-table for the distribution of the absolute feature:\n\n")
                data_crosstab = pd.crosstab(input_d[absolute_features[0]],
                                            input_d['set_number'], margins=True)
                stat_string += (data_crosstab.to_string() + "\n\n")

            if len(continuous_features) > 0:
                stat_string += ("\nAverage values per set:\n\n")
                for feat in continuous_features:
                    for itemset in range(1, no_sets + 1):
                        mean = input_d.loc[input_d['set_number'] == itemset , feat].mean()
                        stat_string += (feat + " in set " + str(itemset) + ": " + str(mean) + "\n")

            f.write(stat_string)
            f.close()

def run_all(i, it_num):
    output_sets = []
    for _ in range(0, no_sets):
        output_sets.append([])

    if no_sets > 1:
        # prepare data
        dat = prepare_data(input_d, continuous_features, categorical_features, label, disregard)

        # split by "absolute" feature and remove absolute features from clustering
        if len(absolute_features) == 1:
            datasets = split(absolute_features[0], dat)
        else:
            datasets = [dat]
    else:
        print("Please use more than 1 set for this tool to be meaningful!")
        sys.exit(1)  # abort

    # for each part of the absolute splitting make sets
    for data in datasets:
        # form clusters
        clusters = clustering(data, categorical_features, continuous_features)

        # divide in sets
        divide_in_sets(clusters, output_sets)

    set_numbers = []
    for item in input_d.index:
        for j, _ in enumerate(output_sets):
            if item in output_sets[j]:
                set_numbers.append(j + 1)

    # add new column
    input_d['set_number'] = set_numbers

    # do statistics
    stats = statistics(input_d)

    # This checks for looping but is inside the loop
    all_ns = True

    for var_type in stats:
        for var in var_type:
            if var[5] < 0.2:
                all_ns = False

    # write to files
    if all_ns:
        write_out(stats, i, False, it_num)
    elif i < 19:
        i = i + 1
        run_all(i, it_num)
    else:
        print("\nCouldn't split into sets as expected. The output might be less than optimal, please run again for "
              "better results")
        write_out(stats, i, True, it_num)


### actually run the program ###

for it_num in range(iterations):
    # progress bar
    perc = 20//iterations
    progress = '=' * it_num * perc
    percdone = round(it_num / iterations * 100, None)
    sys.stdout.write('\r')
    sys.stdout.write(f"[{progress:20}] {percdone}%")
    sys.stdout.flush()

    # initiate loop-tracking
    i = 0
    # start first loop
    run_all(i, it_num)

# final progress bar
sys.stdout.write('\r')
sys.stdout.write(f"[{'='*20:20}] 100%\n")
sys.stdout.flush()
