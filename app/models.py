from . import db

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    games = db.relationship('Games',backref='player',uselist=True,cascade='all, delete-orphan')

    def details(self):
        return({'id':self.id,'username':self.username,'email':self.email})
    
class Games(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.BigInteger, primary_key=True)
    player_id = db.Column(db.BigInteger,db.ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    board_state = db.Column(db.Text, nullable=False)
    human_won = db.Column(db.Boolean, nullable=True)
    current_user = db.Column(db.String(10), nullable=False, default='Human')

