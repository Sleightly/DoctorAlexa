import csv

list_of_info = []
with open('meds.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count+=1
            continue
        list_of_info.append(row)

print(list_of_info)
#print(list(med_df))
#print(med_df['Medication'])
#print(med_df['Strength'])
#print(med_df['Units'])
#print(med_df['Dosage Form'])
#print(med_df['8:00 AM'])
#print(med_df['8:00 PM'])
#print(med_df['Link'])






