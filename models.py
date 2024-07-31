from . import db

class Users(db.Model):
    tablename = 'users'

id = db.Column(db.BigInteger, primary_key=True)
username = db.Column(db.String(255), nullable=False)
email = db.Column(db.String(255), unique=True, nullable=False)
password = db.Column(db.String(255), nullable=False)
games = db.relationship('Game',backref='Users',uselist=False,cascade='all, delete-orphan')

def details(self):
    return({'id':self.id,'username':self.username,'email':self.email})
class Game(db.Model):
    tablename = 'games'
    id = db.Column(db.BigInteger, primary_key=True)
    player1_id = db.Column(db.BigInteger,db.ForeignKey('users.id',ondelete='CASCADE'),nullable=True,unique=True)
    current_turn=db.Column(db.BigInteger,nullable=False, default='P1')
    board_state = db.Column(db.Text, nullable=False)
    winner_id = db.Column(db.BigInteger, db.ForeignKey('users.id', nullable=True))

class Moves(db.Model):
    tablename = 'moves'
    id = db.Column(db.BigInteger, primary_key=True)
    game_id = db.Column(db.BigInteger,db.ForeignKey('games.id',ondelete='CASCADE'),nullable=False,unique=True)
    player_id = db.Column(db.BigInteger, db.ForeignKey('users.id', nullable=False))
    move_number = db.Column(db.String, nullable=False)
    from_position = db.Column(db.String, nullable=False)
    to_position = db.Column(db.String, nullable=False)