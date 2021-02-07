from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Game(db.Model):
   __tablename__ = 'game'
   id = db.Column(db.Integer, primary_key = True)
   teamOneId = db.Column(db.Integer, db.ForeignKey('team.id'), nullable = False)
   teamTwoId = db.Column(db.Integer, db.ForeignKey('team.id'), nullable = False)
   teamOneScore = db.Column(db.Integer, nullable = True)
   teamTwoScore = db.Column(db.Integer, nullable = True)

   def __init__(self, **kwargs):
      self.teamOneId = kwargs.get('teamOneId', 0)
      self.teamTwoId = kwargs.get('teamTwoId', 0)
      self.teamOneScore = 0
      self.TeamTwoScore = 0

   def serialize(self):
        return {
            'game_id': self.id,
            'teamOneId': self.teamOneId,
            'teamTwoId': self.teamTwoId,
            'teamOneScore': self.teamOneScore,
            'TeamTwoScore': self.TeamTwoScore
        }

class Player(db.Model):
   __tablename__ = 'player'
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String, nullable = False)

   def __init__(self, **kwargs):
      self.name = kwargs.get('name', '')

   def serialize(self):
      return {
         'player_id': self.id,
         'name': self.name
      }

class Team(db.Model):
   __tablename__ = 'team'
   id = db.Column(db.Integer, primary_key = True)
   playerOneId = db.Column(db.Integer, db.ForeignKey('player.id'), nullable = False)
   playerTwoId = db.Column(db.Integer, db.ForeignKey('player.id'), nullable = False)

   def __init__(self, **kwargs):
      self.playerOneId = kwargs.get('playerOneId', 0)
      self.playerTwoId = kwargs.get('playerTwoId', 0)
      
   def serialize(self):
      return {
         'team_id': self.id,
         'playerOneId': self.playerOneId,
         'playerTwoId': self.playerTwoId
      }

class Shot(db.Model):
   __tablename__ = 'shot'
   id = db.Column(db.Integer, primary_key = True)
   shotType = db.Column(db.String, nullable = False)
   shotOutcome = db.Column(db.String, nullable = False)
   shotNumber = db.Column(db.Integer, nullable = False)

   playerId = db.Column(db.Integer, db.ForeignKey('player.id'), nullable = False)
   gameId = db.Column(db.Integer, db.ForeignKey('game.id'), nullable = False)

   def __init__(self, **kwargs):
      self.shotType = kwargs.get('shotType', "")
      self.shotOutcome = kwargs.get('shotOutcome', "")
      self.shotNumber = kwargs.get('shotNumber', 0)
      self.playerId = kwargs.get('playerId', 0)
      self.gameId = kwargs.get('gameId', 0)
      
   def serialize(self):
      return {
         'shot_id': self.id,
         'shotType': self.shotType,
         'shotOutcome': self.shotOutcome,
         'shotNumber': self.shotNumber,
         'playerId': self.playerId,
         'gameId': self.gameId
      }
