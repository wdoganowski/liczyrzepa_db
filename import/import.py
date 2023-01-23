import json, csv

input_file = 'import/liczyrzepa.csv'
db_header = ['PK', 'SK', 'GSI1PK', 'GSI1SK', 'GSI2PK', 'GSI2SK', 'GSI3PK', 'GSI3SK']

sys.

with open(input_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            db_header.extend(row)
            print(db_header)
            line_count += 1
        else:
            # print(f'{row}.')
            line_count += 1
    print(f'Processed {line_count} lines.')