from . import db

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    games = db.relationship('Game',backref='Users',uselist=True,cascade='all, delete-orphan')

    def details(self):
        return({'id':self.id,'username':self.username,'email':self.email})
    
class Games(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.BigInteger, primary_key=True)
    player1_id = db.Column(db.BigInteger,db.ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    board_state = db.Column(db.Text, nullable=False)
    human_won = db.Column(db.Boolean, nullable=True)

class Moves(db.Model):
    __tablename__ = 'moves'
    id = db.Column(db.BigInteger, primary_key=True)
    game_id = db.Column(db.BigInteger,db.ForeignKey('games.id',ondelete='CASCADE'),nullable=False)
    player_id = db.Column(db.BigInteger, db.ForeignKey('users.id', nullable=False))
    move_number = db.Column(db.String, nullable=False)
    from_position = db.Column(db.String, nullable=False)
    to_position = db.Column(db.String, nullable=False)
