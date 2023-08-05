# pylint: disable-msg=too-many-locals
# pylint: disable=too-many-arguments

import pandas as pd
from .data import Average
from .data import Result
from .data import Run
from .data import Table


def to_dataclass(stats, i, significant, it_num, filename, input_d, no_sets, absolute_features, categorical_features,
                 continuous_features):
    res = []
    tab = []
    avgs = []
    stat_file_name = None

    # output file
    out_file_name = filename + "_out_" + str(it_num) + ".csv"

    # number of iterations
    iterations = i + 1

    # save statistics to file if there was more than 1 set
    if no_sets > 1:
        stat_file_name = filename + "_stats_" + str(it_num) + ".txt"
        for testgroup in stats:
            for test in testgroup:
                if len(absolute_features) > 0:
                    # TODO: order in a way that 'overall' comes first
                    test_results = Result(identifier=stats[stats.index(testgroup)][testgroup.index(test)][0],
                                          test=stats[stats.index(testgroup)][testgroup.index(test)][1],
                                          feature=stats[stats.index(testgroup)][testgroup.index(test)][2],
                                          df=stats[stats.index(testgroup)][testgroup.index(test)][4],
                                          x2=round(stats[stats.index(testgroup)][testgroup.index(test)][3], 3),
                                          p=round(stats[stats.index(testgroup)][testgroup.index(test)][5], 3))

                else:
                    test_results = Result(identifier="",
                                          test=stats[stats.index(testgroup)][testgroup.index(test)][1],
                                          feature=stats[stats.index(testgroup)][testgroup.index(test)][2],
                                          df=stats[stats.index(testgroup)][testgroup.index(test)][4],
                                          x2=round(stats[stats.index(testgroup)][testgroup.index(test)][3], 3),
                                          p=round(stats[stats.index(testgroup)][testgroup.index(test)][5], 3))
                res.append(test_results)

        if len(categorical_features) > 0:
            for feat in categorical_features:
                data_crosstab = pd.crosstab(input_d[feat], input_d['set_number'], margins=True)
                table = Table(feature=feat, crosstab=data_crosstab)
                tab.append(table)

        if len(absolute_features) > 0:
            data_crosstab = pd.crosstab(input_d[absolute_features[0]], input_d['set_number'], margins=True)
            table = Table(feature=absolute_features[0], crosstab=data_crosstab)
            tab.append(table)

        if len(continuous_features) > 0:
            for feat in continuous_features:
                for itemset in range(1, no_sets + 1):
                    mean = input_d.loc[input_d['set_number'] == itemset, feat].mean()
                    avg = Average(feature=feat, set_no=itemset, mean=mean)
                    avgs.append(avg)

    run = Run(csv_name=out_file_name, no_it=iterations, result=res, significant=significant, tables=tab,
              txt_name=stat_file_name, dataframe=input_d, averages=avgs, filename=filename)
    return run
