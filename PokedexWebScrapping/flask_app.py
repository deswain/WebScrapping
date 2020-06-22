import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/review', methods=['POST', 'GET'])  # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'] #.replace(" ", "")
            pokedesk_url = "https://www.pokemon.com/us/pokedex/" + searchString
            uClient = uReq(pokedesk_url)
            pokedeskPage = uClient.read()
            uClient.close()
            pokedesk_html = bs(pokedeskPage, "html.parser")
            #bigboxes = pokedesk_html.findAll("div", {"class": "container pokedex"})
            #del bigboxes[0:3]
            #box = bigboxes[0]
            #pokeLink = "https://www.pokemon.com/us/pokedex/" + box.div.div.div.a['href']
            prodRes = requests.get(pokedesk_url)
            prodRes.encoding = 'utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html)
            #commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})

            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Number, Name, Type, Weakness,Description \n"
            fw.write(headers)
            reviews = []
            #for commentbox in prod_html:
            try:
                pokemonNumber = pokedesk_html.find(class_ = "pokedex-pokemon-pagination-title").find(class_="pokemon-number").text.lstrip().lstrip('#')
                pokemonNumber
            except:
                pokemonNumber = 'NA'

            try:
                title = pokedesk_html.find('div', class_="pokedex-pokemon-pagination-title").text.strip('\n').lstrip().split('\n')[0]
                title
            except:
                title = 'No Name'

            try:
                description = pokedesk_html.find(class_="version-y active").text.replace('\n', '').lstrip().rstrip()
                description
            except:
                description = "No description"
            try:
                pokemonType = pokedesk_html.find(class_="dtm-type").find('li').find('a').text
                pokemonType
            except:
                pokemonType = 'No Data'
            try:
                pokemonWeakness = pokedesk_html.find(class_="dtm-weaknesses").find('span').text.rstrip('\n').split('\n')[0]
                pokemonWeakness
            except:
                pokemonWeakness = 'NA'

            reviews = {"Pokemon Number": pokemonNumber, "Name": title, "Type": pokemonType,"Weakness": pokemonWeakness,
                       "Description": description}
                #reviews.append(mydict)
            print(reviews)
            return render_template('results.html', reviews=reviews)
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

port = int(os.getenv("PORT"))
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=port)
    #app.run(host='127.0.0.1', port=8001, debug=True)
