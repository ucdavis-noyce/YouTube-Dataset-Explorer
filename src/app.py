from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

import sockpuppet
from util import map_ideology
import os

app = Flask(__name__, static_folder="../webapp")
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path) and path.count("/") > 1:
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(os.path.join(app.static_folder, path), 'index.html')

@app.route("/api/getNumSockPuppets/<ideology>")
def get_num_sock_puppets(ideology):
    ideology = map_ideology(ideology)
    return jsonify(sockpuppet.get_num_sock_puppets(ideology))

@app.route("/api/getSockPuppet/<ideology>/<puppetId>")
def get_sock_puppet(ideology, puppetId):
    ideology = map_ideology(ideology)
    return jsonify(sockpuppet.get_sock_puppet(ideology, int(puppetId)))

@app.route("/api/getSockPuppetDates/")
def get_sock_puppet_dates():
    return jsonify(sockpuppet.get_dates())

@app.route("/api/getTopVideos/<date>")
def get_top_videos(date):
    return jsonify(sockpuppet.get_top_videos(date))

