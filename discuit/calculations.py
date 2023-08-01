import pandas as pd
from scipy.stats import chi2_contingency
from scipy.stats import kruskal


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


def do_statistics(data, absolute_features, continuous_features, categorical_features):
    stats_out = []
    subsets = []
    if len(absolute_features) > 0:
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
