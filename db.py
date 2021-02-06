from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Game(db.Model):
   __tablename__ = 'game'
   id = db.Column(db.Integer, primary_key = True)
   teamOneId = db.Column(db.Integer, db.ForeignKey('team.id'), nullable = True)
   teamTwoId = db.Column(db.Integer, db.ForeignKey('team.id'), nullable = True)
   teamOneScore = db.Column(db.Integer, nullable = True)
   teamTwoScore = db.Column(db.Integer, nullable = True)

   
