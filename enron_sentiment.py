from elasticsearch import Elasticsearch
import boto3
import re
import csv
es = Elasticsearch([{'host': 'archive.enron.email', 'port': 8080}])
client = boto3.client('comprehend')
emailRe = re.compile(r'\S*@\S*\s?')

def getSentiment(fromAddress,toAddress):
  if fromAddress.find('@')==-1:
    fromAddress=fromAddress+"@enron.com"
  if toAddress.find('@')==-1:
    toAddress=toAddress+"@enron.com"
  query1 = {
    "query": { 
      "bool": { 
        "must": [
          { "match": { "from_email": fromAddress }},
          { "match": { "to": toAddress }}
        ] 
      }
    },
     "size":500,
        "from": 0,
        "sort":[
          {
            "_score":"desc"
          }
        ]
  }
  results1 = es.search(index="enron", body=query1)
  mailBody1 = ""
  for mail in results1['hits']['hits']:
    mailBody1 = mail['_source']['body'].split("---")[0].split("___")[0].replace("\n", "")+mailBody1
  query2 = {
    "query": { 
      "bool": { 
        "must": [
          { "match": { "from_email": toAddress }},
          { "match": { "to": fromAddress }}
        ] 
      }
    },
     "size":500,
        "from": 0,
        "sort":[
          {
            "_score":"desc"
          }
        ]
  }
  results2 = es.search(index="enron", body=query2)
  mailBody2 = ""
  for mail in results2['hits']['hits']:
    mailBody2 = mail['_source']['body'].split("---")[0].split("___")[0].replace("\n", "")+mailBody2
  sentimentText = emailRe.sub('', mailBody1)[0:2499]+emailRe.sub('', mailBody2)[0:2499]
  response = dict()
  if len(sentimentText)>1:
    response = client.detect_sentiment(
      Text=sentimentText,
      LanguageCode='en'
  )
  response['count'] = len(results1['hits']['hits'])+len(results2['hits']['hits'])
  return response

sentimentText=[]
with open('/Users/qianshaoli/Documents/Academic/inst633/week7/enron-edge.csv') as adjacentList:
    adjacentList_reader = csv.reader(adjacentList, delimiter=',')
    line_count = 0
    for row in adjacentList_reader:
      if line_count == 0:
          print(f'Column names are {", ".join(row)}')
          line_count += 1
      else:
          print(row[0]+':'+row[1])
          response=getSentiment(row[0],row[1])
          print(response)
          print(line_count)
          if len(response)>1:
            sentimentText.append(row[0]+','+row[1]+','+str(response['count'])+','+response['Sentiment']+','+str(response['SentimentScore']['Positive'])+','+str(response['SentimentScore']['Negative'])+','+str(response['SentimentScore']['Neutral'])+','+str(response['SentimentScore']['Mixed']))
          line_count += 1
    print(f'processed {line_count} edges.')

with open('/Users/qianshaoli/Documents/Academic/inst633/week7/enron-edge-sentiment.csv','w') as adjacentList:
  adjacentList.write("Source,Target,Sentiment,PositiveScore,NegativeScore,NeutralScore,MixedScore\n")
  for row in sentimentText:
    adjacentList.write(row+'\n')
