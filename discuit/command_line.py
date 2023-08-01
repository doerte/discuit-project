# TODO: maybe include more than 1 absolute variable? maybe all categorical variables can be absolute?
# TODO: consider stopping if silhouette score is too low. Exit with error message.
# TODO: guess variable type

import argparse
import pathlib
import sys
import pandas as pd
from .run import run_all


# set defaults
iterations = 1
no_sets = 2
filename = "placeholder"
input_d = pd.DataFrame()


# The following info must come from user. In GUI this should be selected in the GUI after opening a file!
categorical_features = []
continuous_features = []
absolute_features = []
label = []
disregard = []

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


def main():  # noqa: MC0001
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
    # number of runs provided as an argument. If nothing is provided it's 1. Also needs to come from GUI!
    iterations = args.runs

    # Check all the columns and ask about status. Label and absolute can only be chosen once.
    if args.columns is None or len(args.columns) != len(input_d.columns):  # noqa: MC0001
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
                "More than one 'absolute' variable was specified. Please use -h to get help in "
                "providing suitable arguments")
            sys.exit(1)  # abort
    # actually run the program

    for it_num in range(iterations):
        # progress bar
        perc = 20 // iterations
        progress = '=' * it_num * perc
        percdone = round(it_num / iterations * 100, None)
        sys.stdout.write('\r')
        sys.stdout.write(f"[{progress:20}] {percdone}%")
        sys.stdout.flush()

        # initiate loop-tracking
        i = 0
        # start first loop
        run_all(i, it_num, no_sets, input_d, continuous_features, categorical_features, label, disregard,
                absolute_features, filename)

    # final progress bar
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * 20:20}] 100%\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
