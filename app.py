from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests
from csv import writer

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/collectData',methods=['POST'])
def collectData():
    productPath = [request.form.get("productPath")][0]
    getData(productPath)
    return render_template('index.html', alert_message=productPath)


def getData(productPath):
    with open('dataset.csv', 'a', newline='') as fObject:  
        writerObject = writer(fObject)
        for status in range(2):
            filter = "1,2"
            if status == 1:
                filter = "4,5"
            for pageSize in range(1, getPageSize(productPath, filter) + 1):
                soup = getPageSoup(productPath, pageSize, filter)
                for item in soup.find_all('span', itemprop='description'):
                    writerObject.writerow([item.getText().strip().replace('\n', '').replace(",", ""),status])  
        fObject.close()


def getPageSize(productPath, filter):
    soup = getPageSoup(productPath, 1, filter)
    liElements = soup.find_all('span', class_='hermes-PageHolder-module-1QoWq')
    if len(liElements) == 0:
        return 1
    else:
        return int(liElements[-1].getText())

def getPageSoup(productPath, commentPage, filter):
    url = 'https://www.hepsiburada.com/' + f'{productPath}-yorumlari?sayfa={commentPage}&filtre={filter}'

    headers = {
        'User-Agent':
            (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
            )
    }
    response = (requests.get(url=url, headers=headers)).content
    return BeautifulSoup(response, 'html.parser')
    
if __name__  == '__main__':
    app.run(debug=True, port=5001)