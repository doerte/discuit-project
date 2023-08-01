# pylint: disable-msg=too-many-locals
#pylint: disable=too-many-arguments

import pandas as pd


def write_out(stats, i, significant, it_num, filename, input_d, no_sets, absolute_features, categorical_features,
              continuous_features):

    # output file
    out_file_name = filename + "_out" + str(it_num) + ".csv"
    input_d.to_csv(out_file_name, index=False)
    # save statistics to file if there was more than 1 set
    if no_sets > 1:
        stat_file_name = filename + "_stats" + str(it_num) + ".txt"
        with open(stat_file_name, "w", encoding="utf8") as f:
            iterations = i + 1
            stat_string = f'Number of iterations: {iterations} \n \nResults for the following tests:\n'

            if significant:
                stat_string += "\nIn 20 iterations no split could be found that results in p>.2 for all variables.\n\n"

            for testgroup in stats:
                for test in testgroup:
                    results = (f"{stats[stats.index(testgroup)][testgroup.index(test)][1]} for "
                               + stats[stats.index(testgroup)][testgroup.index(test)][2]
                               + f": X2({stats[stats.index(testgroup)][testgroup.index(test)][4]}) = "
                                 f"{round(stats[stats.index(testgroup)][testgroup.index(test)][3],3)},"
                                 f"p = {round(stats[stats.index(testgroup)][testgroup.index(test)][5], 3)};\n")
                    if len(absolute_features) > 0:
                        stat_string += (f"Absolute variable instance "
                                        f"'{stats[stats.index(testgroup)][testgroup.index(test)][0]}' :")
                        stat_string += results

                    else:
                        stat_string += results

            if len(categorical_features) > 0:
                stat_string += "\nCross-tables for the distribution of categorical features:\n\n"
                for feat in categorical_features:
                    data_crosstab = pd.crosstab(input_d[feat], input_d['set_number'], margins=True)
                    stat_string += (data_crosstab.to_string() + "\n\n")

            if len(absolute_features) > 0:
                stat_string += "\nCross-table for the distribution of the absolute feature:\n\n"
                data_crosstab = pd.crosstab(input_d[absolute_features[0]],
                                            input_d['set_number'], margins=True)
                stat_string += (data_crosstab.to_string() + "\n\n")

            if len(continuous_features) > 0:
                stat_string += "\nAverage values per set:\n\n"
                for feat in continuous_features:
                    for itemset in range(1, no_sets + 1):
                        mean = input_d.loc[input_d['set_number'] == itemset, feat].mean()
                        stat_string += (feat + " in set " + str(itemset) + ": " + str(mean) + "\n")

            f.write(stat_string)
            f.close()
