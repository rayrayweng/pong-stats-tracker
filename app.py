import json
from db import db, Game, Player, Team
from flask import Flask, request

db_filename = "pong.db"
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/api/players/', methods=["GET"])
def get_players():
    players = Player.query.all()
    res = {'success': True, 'data': [p.serialize() for p in players]}
    return json.dumps(res), 200

@app.route('/api/player/', methods=['POST'])
def create_player():
    post_body = json.loads(request.data)
    name = post_body.get('name', "")

    player = Player(
        name = name
    )

    db.session.add(player)
    db.session.commit()

    return json.dumps({'success': True, 'data': player.serialize()}), 201

