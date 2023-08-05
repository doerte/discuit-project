def write_to_file(output):
    for r in output.runs:
        # save .csv
        r.dataframe.to_csv(r.csv_name, index=False)

        # save stats output
        stat_file_name = r.txt_name

        with open(stat_file_name, "w", encoding="utf8") as f:
            stat_string = f'Number of iterations: {r.no_it} \n \nResults for comparison between ' \
                          f'new sets:\n'

            if r.significant:
                stat_string += "\nIn 20 iterations no split could be found that results in p>.2 for all variables.\n\n"

            for test in r.result:
                # TODO: find a way to only include the first part if there is an absolute variable
                stat_string += f"Absolute variable instance '{test.identifier}': {test.test} for '{test.feature}': " \
                               f"X2({test.df}) = {test.x2}, p = {test.p}\n"

            if r.tables[0].crosstab is not None:
                stat_string += "\nCross-tables:\n\n"
                for table in r.tables:
                    stat_string += (table.crosstab.to_string() + "\n\n")

            if r.averages is not None:
                stat_string += "\nAverage values per set:\n\n"
                for average in r.averages:
                    stat_string += (average.feature + " in set " + str(average.set_no) + ": " + str(average.mean)
                                    + "\n")

            f.write(stat_string)
            f.close()
