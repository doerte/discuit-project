# pylint: disable-msg=too-many-locals

import sys
from typing import List
from kmodes.kmodes import KModes
from kmodes.kprototypes import KPrototypes
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


def prepare_data(data, continuous, categorical, label, disregard):
    # remove label column & disregarded columns
    if len(label) != 0:
        data = data.drop([label[0]], axis=1)
    if len(disregard) != 0:
        data = data.drop(disregard, axis=1)
    # transform continuous data
    if len(continuous) != 0:
        # replace md with average
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
                    i = i + 1
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
