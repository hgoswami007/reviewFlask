from flask import Flask,render_template,request
import requests
from flask_cors import cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)

@app.route('/',methods=['get'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            search_string =request.form['content'].replace(" ","")
            amazone_url ="https://www.flipkart.com/search?q=" + search_string
            uClient =uReq(amazone_url)
            amazonePage =uClient.read()
            uClient.close()
            amazone_html = bs(amazonePage,"html.parser")
            bigboxes =amazone_html.findAll("div",{"class":"_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLinl ="https://www.flipkart.com"+ box.div.div.div.a['href']
            productRes = requests.get(productLinl)
            productRes.encoding = 'utf-8'
            productHtml = bs(productRes.text,"html.parser")
            commentboxs = productHtml.findAll("div",{"class" : "_16PBlm"})
            # print("commentboxs=======>",commentboxs)


            filename = search_string +".csv"
            fw = open(filename,"w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            review = []
            for commentbox in commentboxs:
                try:
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                    # print('name===',name)
                except:
                    name ='No Name'

                try:
                    rating = commentbox.div.div.div.div.text
                except:
                    rating ='No Rating'

                try:
                    commHead = commentbox.div.div.div.p.text
                except:
                    commHead ='No Comment Heading'

                try:
                    comtag= commentbox.div.div.find_all('div', {'class': ''})
                    custComment = comtag[0].div.text

                except Exception as e:
                    print("Exception while creating dictionary: ", e)


                mydict = {"Product" : search_string,"Name":name,"Rating":rating,"CommentHead":commHead,"Comment":custComment}

                review.append(mydict)

            return render_template('results.html', reviews=review[0:(len(review)-1)])
            # return "good"

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'

    else:
        return render_template('index.html')


if (__name__) == '__main__':
    app.run()
