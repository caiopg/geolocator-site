import pandas
import geopy
import os
from flask import Flask, render_template, request, send_file
from werkzeug import secure_filename
from geopy.geocoders import Nominatim

new_name = "default.csv"

def create_csv(df, column, file_name):
    nom = Nominatim()
    df["Latitude"] = df[column].apply(lambda x : nom.geocode(x, timeout=10)).apply(lambda x: x.latitude if x != None else "NaN")
    df["Longitude"] = df[column].apply(lambda x : nom.geocode(x, timeout=10)).apply(lambda x: x.longitude if x != None else "NaN")
    df.to_csv(file_name)

    return df

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/success-table", methods=['POST'])
def success():
    if(request.method == 'POST'):
        file = request.files["file_name"]
        global new_name
        new_name = secure_filename("modified_" + file.filename)

        df = pandas.read_csv(file)

        if "Address" in df.columns:
            df = create_csv(df, "Address", new_name)
        elif "address" in df.columns:
            df = create_csv(df, "address", new_name)
        else:
            return render_template("home.html", text="Please make sure you have an address column in your CSV file!")

        return render_template("home.html", text=df.to_html(),
        btn="download_btn.html")

@app.route("/download/")
def download():
    global new_name
    return send_file(new_name, attachment_filename="modified_file.csv", as_attachment=True)

if __name__ == "__main__":
    app.debug = True
    app.run()
