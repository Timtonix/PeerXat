# IP:Port: http://127.0.0.1:5000/
from flask import Flask, render_template, make_response, redirect, url_for, request
import client

app = Flask(__name__)


@app.route("/")
def mainPage():
    return "<h1>Hello<h1>"


@app.route("/login", methods=['GET', 'POST'])
def loginPage():
    if request.method == 'GET':
        if request.cookies.get("login") == "True":
            reply = make_response(redirect(url_for("mainPage")))
            return reply
        else:
            reply = make_response(render_template('login.html'))
            reply.set_cookie("login", "True")
            return reply
    elif request.method == 'POST':
        reply = make_response("PRORTTT")
        reply.set_cookie("login", "True")
        reply.set_cookie("username", request.form['nm'])
        client.client.main(request.form['nm'])
        return reply


if __name__ == '__main__':
    app.run()
