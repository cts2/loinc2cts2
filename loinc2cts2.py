from reader.loinc_csv_reader import LoincReader

def rowCallback(row):
    print row


reader = LoincReader("tests/loinc.csv")

reader.read(rowCallback)
