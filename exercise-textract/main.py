import glob
import boto3
import json
import csv
import sys

csv_array = []
client = boto3.client('textract')
for filename in glob.glob('raw_images/*.jpg'):
    csv_row = {}
    print(f"Processing: {filename}")
    with open(filename, 'rb') as fd:
        file_bytes = fd.read()

    response = client.analyze_document(
        Document={'Bytes': file_bytes},
        FeatureTypes=["QUERIES"],
        QueriesConfig={
            'Queries': [
                {'Text': 'What is the response id', 'Alias': 'ResponseId'},
                {'Text': 'What are the notes?', 'Alias': 'Notes'},
            ]
        }
    )

    # uncomment this to see the format of the reponse
    # print(json.dumps(response, indent=2))

    #####
    # Replace this code with a solution to populate a dictionary with the results from textract
    #####
    for index in range(len(response["Blocks"])):
        block = response["Blocks"][index]
        if block["BlockType"] == "QUERY" and block["Query"]["Alias"] == "ResponseId":
            csv_row["ResponseId"] = response["Blocks"][index+1]["Text"]
        if block["BlockType"] == "QUERY" and block["Query"]["Alias"] == "Notes":    
            csv_row["Notes"] = response["Blocks"][index+1]["Text"]
    csv_array.append(csv_row)

writer = csv.DictWriter(sys.stdout, fieldnames=["ResponseId", "Notes"], dialect='excel')
writer.writeheader()
for row in csv_array:
    writer.writerow(row)

