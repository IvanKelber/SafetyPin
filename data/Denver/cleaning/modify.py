import csv

def modifydenver():
    distinct = []
    with open("../offense_table.csv") as crime:
        reader = csv.DictReader(crime)
        for data in reader:
            if data['Offense'] not in distinct:
                distinct.append(data['Offense'])                
                
            
    print distinct   
    with open("../offense_table1.csv","wb") as crime:
        fields = ['Offense_ID','Offense']
        writer = csv.DictWriter(crime, fields)

        writer.writeheader()
        for index in range(0,len(distinct)):
            writer.writerow({'Offense_ID': index, 'Offense': distinct[index]})
    
modifydenver()
