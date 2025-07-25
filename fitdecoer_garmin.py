import fitdecode
import csv

input_file = '19504776611_ACTIVITY.fit'
output_file = 'average_run.csv'

data_records = []
fieldnames_set = set()

with fitdecode.FitReader(input_file) as fit:
    for frame in fit:
        # Only keep time-series data frames
        if frame.frame_type == fitdecode.FIT_FRAME_DATA and frame.name == 'record':
            record = {}
            for field in frame.fields:
                record[field.name] = field.value
            data_records.append(record)
            fieldnames_set.update(record.keys())

# Convert the field set into a sorted list for CSV headers
fieldnames = sorted(fieldnames_set)

# Write out the cleaned CSV safely
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for row in data_records:
        writer.writerow(row)  # Missing fields = blank

print(f"CSV written to {output_file} with {len(data_records)} rows.")