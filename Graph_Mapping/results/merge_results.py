import os
import csv
import glob


def new_v(files_path, output_name):
    interesting_files = glob.glob(os.path.join(files_path, "*.csv"))
    result = None
    for filename in interesting_files:
        with open(filename) as fin:
            data = list(csv.reader(fin, delimiter=';'))
            if result is None:
                result = ([data[0]])
            result += data[1:]
    with open(output_name, 'w', newline='') as out:
        write = csv.writer(out, delimiter=';')
        write.writerows(result)


new_v('raw_results', 'raw_results.csv')
new_v('summary_results', 'summary_results.csv')
