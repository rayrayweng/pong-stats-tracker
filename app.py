import json
from db import db, Game, Player, Team, Shot
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

@app.route('/api/player/<int:player_id>/', methods=['DELETE'])
def delete_player(player_id):
    player = Player.query.get(player_id)
    if not player:
        return json.dumps({'success': False, 'error': 'Player not found!'}), 404
    db.session.delete(player)
    db.session.commit()
    return json.dumps({'success': True, 'data': player.serialize()}), 201

@app.route('/api/teams/', methods=["GET"])
def get_teams():
    teams = Team.query.all()
    res = {'success': True, 'data': [t.serialize() for t in teams]}
    return json.dumps(res), 200

@app.route('/api/team/', methods=['POST'])
def create_team():
    post_body = json.loads(request.data)
    playerOneId = post_body.get('playerOneId', 0)
    playerTwoId = post_body.get('playerTwoId', 0)

    team = Team(
        playerOneId = playerOneId,
        playerTwoId = playerTwoId
    )

    db.session.add(team)
    db.session.commit()

    return json.dumps({'success': True, 'data': team.serialize()}), 201

@app.route('/api/team/<int:team_id>/', methods=['DELETE'])
def delete_team(team_id):
    team = Team.query.get(player_id)
    if not team:
        return json.dumps({'success': False, 'error': 'Team not found!'}), 404
    db.session.delete(team)
    db.session.commit()
    return json.dumps({'success': True, 'data': team.serialize()}), 201

@app.route('/api/games/', methods=["GET"])
def get_games():
    games = Game.query.all()
    res = {'success': True, 'data': [g.serialize() for g in games]}
    return json.dumps(res), 200

@app.route('/api/game/<int:game_id>', methods=["GET"])
def get_game():
    game = Game.query.filter_by(id=game_id).first()
    if not game:
        return json.dumps({'success': False, 'error': 'Game not found!'}), 404
    return json.dumps({'success': True, 'data': game.serialize()}), 200

@app.route('/api/game/<int:teamOneId>/<int:teamTwoId>/', methods=['POST'])
def create_game(teamOneId, teamTwoId):
    post_body = json.loads(request.data)
    teamOneScore = post_body.get('teamOneScore', 0)
    teamTwoScore = post_body.get('teamTwoScore', 0)

    game = Game(
        teamOneId = teamOneId,
        teamTwoId = teamTwoId,
        teamOneScore = teamOneScore,
        teamTwoScore = teamTwoScore
    )

    db.session.add(game)
    db.session.commit()

    return json.dumps({'success': True, 'data': game.serialize()}), 201

@app.route('/api/game/<int:game_id>/', methods=['DELETE'])
def delete_game(game_id):
    game = Game.query.get(game_id)
    if not game:
        return json.dumps({'success': False, 'error': 'Game not found!'}), 404
    db.session.delete(game)
    db.session.commit()
    return json.dumps({'success': True, 'data': game.serialize()}), 201

#sus? maybe separate
@app.route('/api/shots/<int:gameId>/<int:playerId>', methods=["GET"])
def get_shots_by_game_or_player(gameId, playerId):
    shots = Shot.query.filter_by(gameId=gameId).filter_by(playerId=playerId)
    if game_id == 0:
        shots = Shot.query.filter_by(playerId=playerId)
    elif player_id == 0:
        shots = Shot.query.filter_by(gameId=gameId)
    res = {'success': True, 'data': [s.serialize() for s in shots]}
    return json.dumps(res), 200

@app.route('/api/game/<int:game_id>/<int:player_id>/', methods=['POST'])
def create_shot(game_id, player_id):
    post_body = json.loads(request.data)
    shotType = post_body.get('shotType', "")
    shotOutcome = post_body.get('shotOutcome', "")
    shotNumber = post_body.get('shotNumber', 0)
    
    shot = Shot(
        shotType = shotType,
        shotOutcome = shotOutcome,
        shotNumber = shotNumber,
        game_id = game_id,
        player_id = player_id
    )

    db.session.add(shot)
    db.session.commit()

    return json.dumps({'success': True, 'data': shot.serialize()}), 201


@app.route('/api/game/edit/<int:gameId>/<int:playerId>/', methods=['POST'])
def edit_shot(game_id, player_id):
    shot = Shot.query.filter_by(playerId=playerId).filter_by(gameId=gameId).first()
    if not shot:
        return json.dumps({'success': False, 'error': 'Shot not found!'}), 404

    post_body = json.loads(request.data)
    shot.shotType = post_body.get('shotType', "")
    shot.shotOutcome = post_body.get('shotOutcome', "")
    shot.shotNumber = post_body.get('shotNumber', "")

    db.session.commit()
    return json.dumps({'success': True, 'data': shot.serialize()}), 200
