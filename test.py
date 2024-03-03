import csv

def compare_csv(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2, open(output_file, 'w') as output:
        csv1 = csv.reader(f1)
        csv2 = csv.reader(f2)
        writer = csv.writer(output)

        set1 = set(tuple(row) for row in csv1)
        set2 = set(tuple(row) for row in csv2)

        diff = set1.symmetric_difference(set2)

        writer.writerows(diff)

# Usage example
compare_csv('file1.csv', 'file2.csv', 'output.csv')