from flask import Flask, redirect, url_for, render_template
from configs import colors

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/customize')
def customize():
    return render_template("customize.html", primary_colors=colors.primary, secondary_colors=colors.secondary)


if __name__ == "__main__":
    app.run(debug=True)