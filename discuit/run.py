# pylint: disable-msg=too-many-locals
# pylint: disable=too-many-arguments

import sys
from .calculations import do_statistics
from .clustering import clustering
from .clustering import divide_in_sets
from .clustering import prepare_data
from .clustering import split
from .write import write_out


def run_all(i, it_num, no_sets, input_d, continuous_features, categorical_features, label, disregard,
            absolute_features, filename):
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
    stats = do_statistics(input_d, absolute_features, continuous_features, categorical_features)

    # This checks for looping but is inside the loop
    all_ns = True

    for var_type in stats:
        for var in var_type:
            if var[5] < 0.2:
                all_ns = False

    # write to files
    if all_ns:
        write_out(stats, i, False, it_num, filename, input_d, no_sets, absolute_features, categorical_features,
                  continuous_features)
    elif i < 19:
        i = i + 1
        run_all(i, it_num, no_sets, input_d, continuous_features, categorical_features, label, disregard,
                absolute_features, filename)
    else:
        print("\nCouldn't split into sets as expected. The output might be less than optimal, please run again for "
              "better results")
        write_out(stats, i, True, it_num, filename, input_d, no_sets, absolute_features, categorical_features,
                  continuous_features)
