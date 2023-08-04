# pylint: disable-msg=too-many-locals
# pylint: disable=too-many-arguments

import io
import zipfile
import pandas as pd
import streamlit as st


def write_streamlit(stats, i, significant, it_num, filename, input_d, no_sets, absolute_features, categorical_features,
                    continuous_features):
    # output file
    out_file_name = filename + "_out_" + str(it_num) + ".csv"
    stat_file_name = filename + "_stats_" + str(it_num) + ".txt"
    heading_text = "Output: set division and statistics from run " + str(it_num + 1)
    st.subheader(heading_text)

    st.write("Input set amended with set allocation")
    st.write(input_d)
    output_csv = input_d.to_csv(index=False).encode('utf-8')
    key = "download-csv-run" + str(it_num)

    # save statistics to file if there was more than 1 set
    if no_sets > 1:
        txt_content = ""
        txt_content += f'Number of iterations: {i+1} \n \nResults for comparison between new sets:\n'
        st.write('Number of iterations ran:', i+1)
        st.write('**Results for comparison between new sets:**  \n')

        if significant:
            txt_content += "  \nIn 20 iterations no split could be found that results in p>.2 for all " \
                           "variables.  \n  \n"
            st.write("  \nIn 20 iterations no split could be found that results in p>.2 for all variables.  \n  \n")
        output = ""
        output_st = ""
        for testgroup in stats:
            for test in testgroup:
                if len(absolute_features) > 0:
                    output += f"'Absolute variable instance " \
                              f"'{stats[stats.index(testgroup)][testgroup.index(test)][0]}':" \
                              f"{stats[stats.index(testgroup)][testgroup.index(test)][1]} for " \
                              f"'{stats[stats.index(testgroup)][testgroup.index(test)][2]}': X2(" \
                              f"{stats[stats.index(testgroup)][testgroup.index(test)][4]}) = " \
                              f"{round(stats[stats.index(testgroup)][testgroup.index(test)][3], 3)}," \
                              f" p = {round(stats[stats.index(testgroup)][testgroup.index(test)][5], 3)};  \n"""

                    output_st += f"Absolute variable instance " \
                                 f"'{stats[stats.index(testgroup)][testgroup.index(test)][0]}': " \
                                 f"{stats[stats.index(testgroup)][testgroup.index(test)][1]} for " \
                                 f"'{stats[stats.index(testgroup)][testgroup.index(test)][2]}': _$\u03C7^2$_(" \
                                 f"{stats[stats.index(testgroup)][testgroup.index(test)][4]}) = " \
                                 f"{round(stats[stats.index(testgroup)][testgroup.index(test)][3], 3)}," \
                                 f" _p_ = {round(stats[stats.index(testgroup)][testgroup.index(test)][5], 3)};  \n"
                else:
                    output += f"'{stats[stats.index(testgroup)][testgroup.index(test)][1]} for " \
                               f"'{stats[stats.index(testgroup)][testgroup.index(test)][2]}': X2(" \
                               f"{stats[stats.index(testgroup)][testgroup.index(test)][4]}) = " \
                               f"{round(stats[stats.index(testgroup)][testgroup.index(test)][3], 3)}," \
                               f" p = {round(stats[stats.index(testgroup)][testgroup.index(test)][5], 3)};  \n"""
                    output_st += f"{stats[stats.index(testgroup)][testgroup.index(test)][1]} for " \
                                 f"'{stats[stats.index(testgroup)][testgroup.index(test)][2]}': _$\u03C7^2$_(" \
                                 f"{stats[stats.index(testgroup)][testgroup.index(test)][4]}) = " \
                                 f"{round(stats[stats.index(testgroup)][testgroup.index(test)][3], 3)}," \
                                 f" _p_ = {round(stats[stats.index(testgroup)][testgroup.index(test)][5], 3)};  \n"

        st.write(output_st)
        txt_content += output

        col_titles = []
        for subset in range(no_sets):
            col_titles.append(f"Set {subset+1}")
        col_titles.append("All")
        if len(categorical_features) > 0:
            txt_content += "  \nCross-tables for the distribution of categorical features:  \n  \n"
            st.write("  \n**Cross-tables for the distribution of categorical features:**  \n  \n")
            for feat in categorical_features:
                data_crosstab = pd.crosstab(input_d[feat], input_d['set_number'], margins=True)
                txt_content += (data_crosstab.to_string() + "\n\n")
                cross = data_crosstab.rename(columns=lambda x: 'Set ' + str(x), inplace=False)
                st.dataframe(cross, column_config={
                    "Set All": "All",
                })

        if len(absolute_features) > 0:
            txt_content += "  \nCross-table for the distribution of the absolute feature:  \n  \n"
            st.write("  \n**Cross-table for the distribution of the absolute feature:**  \n  \n")
            data_crosstab = pd.crosstab(input_d[absolute_features[0]],
                                        input_d['set_number'], margins=True)
            txt_content += (data_crosstab.to_string() + "\n\n")
            cross = data_crosstab.rename(columns=lambda x: 'Set ' + str(x), inplace=False)
            st.dataframe(cross, column_config={
                "Set All": "All",
            })

        if len(continuous_features) > 0:
            txt_content += "  \nAverage values per set:  \n  \n"
            st.write("  \n**Average values per set:**  \n  \n")
            output = ""
            for feat in continuous_features:
                for itemset in range(1, no_sets + 1):
                    mean = round(input_d.loc[input_d['set_number'] == itemset, feat].mean(), 3)
                    output += feat + " in set " + str(itemset) + ": " + str(mean) + "  \n"
            st.write(output)
            txt_content += output

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for file_name, data in [
                (stat_file_name, io.StringIO(txt_content)),
                (out_file_name, io.BytesIO(output_csv))
            ]:
                zip_file.writestr(file_name, data.getvalue())

        zip_file_name = filename + "_run_" + str(it_num) + ".zip"

        st.download_button("Download statistics only", data=txt_content, file_name=stat_file_name)
        st.download_button("Download set division as .csv file", output_csv, out_file_name, "text/csv", key=key)
        st.download_button("Download .zip file with set division and statistics", mime="application/zip",
                           data=zip_buffer, file_name=zip_file_name)
