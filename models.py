# Models for the type of data in the database

from database import db


# Database model for a single user
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    authenticated = db.Column(db.Boolean, default=False)
    trades = db.relationship('Trade', backref='user')
    

    def is_active(self):
        return True

    def get_id(self):
        return self.id
    
    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
    
    def __repr__(self):
        return f"<User> {self.name}"
    


# Database model for a single trade
class Trade(db.Model):
    trade_id = db.Column(db.Integer, primary_key = True)
    ticker = db.Column(db.String(10), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    buy_or_sell = db.Column(db.String(10), nullable = False)
    currency = db.Column(db.String(10), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Trade> {'Buy' if self.buy_or_sell == 'buy' else 'Sell'} {self.ticker} at {self.price} {self.currency}"
