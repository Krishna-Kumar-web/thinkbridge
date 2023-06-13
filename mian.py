from flask import Flask

app = Flask(__name__)

import requests,secrets

import pandas as pd
from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
import os
from werkzeug.utils import secure_filename
import csv

UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')

ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'secretkey'
client_id = "*************"
client_secret="*************"

'''
NOTE
development is paused on this task due the lack of credentials to fullfill the criteria 
to request the api
How ever the overall buisines logic the drown in the below code
'''

@app.route('/', methods=['GET', 'POST'])
def uploadFile():
  if request.method == 'POST':
    f = request.files.get('file')
    data_filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'],data_filename))
    session['uploaded_data_file_path'] =os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
    with open(os.path.join(app.config['UPLOAD_FOLDER'],data_filename),mode='r') as csv_file:
      content = csv_file.readlines()
    import pdb;pdb.set_trace()
    state=secrets.token_hex(8).upper()
    #url = requests.get("https://www.linkedin.com/oauth/v2/authorization",params={'response_type': 'code','client_id':'862k7t2jroe4bv','redirect_uri':'need to add redirect url here', 'state':state })
    x=requests.post("https://www.linkedin.com/oauth/v2/accessToken",\
                    params={'grant_type':'client_credentials','client_id':"862k7t2jroe4bv",\
                    'client_secret':"QT3iq1KNv4C0vxMS"})
    #get the access token


    company_names = content[1:]
    for company in company_names:
      company_name = company.replace("\n","")
      x = requests.get("https://api.linkedin.com/v2/search?q="+company_name, params={"access_token":acces_token})
      #response x will contain all the information related the company
      #from the json response get the employee data using  js path
      #update the csv
    return render_template('index2.html')
  return render_template("index.html")


@app.route('/show_data')
def showData():
	data_file_path = session.get('uploaded_data_file_path', None)
	uploaded_df = pd.read_csv(data_file_path,
							encoding='unicode_escape')
	# Converting to html Table
	uploaded_df_html = uploaded_df.to_html()
	return render_template('show_csv_data.html',
						data_var=uploaded_df_html)


if __name__ == '__main__':
	app.run(debug=True)