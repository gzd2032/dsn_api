from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Locations(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    prefix_id = db.relationship('Prefixes', backref='locations',
                             cascade='all, delete-orphan',  lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def __init__(self, name):
        self.name = name
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def details(self):
        return {
            'id': self.id,
            'name': self.name,
            'prefixes': [ prefix.short() for prefix in self.prefix_id]
        }


class Prefixes(db.Model):
    __tablename__ = 'prefixes'

    id = db.Column(db.Integer, primary_key=True)
    dsn_prefix = db.Column(db.String, unique=True, nullable=False)
    comm_prefix = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def __init__(self, dsn_prefix):
        self.dsn_prefix = dsn_prefix
        
    def format(self):
        return {
            'id': self.id,
            'description': self.description,
            'dsn_prefix': self.dsn_prefix,
            'comm_prefix': self.comm_prefix,
            'location': self.locations.name,
            'location_id': self.locations.id
        }
    
    def short(self):
        return {
            'id': self.id,
            'dsn_prefix': self.dsn_prefix,
            'comm_prefix': self.comm_prefix,
            'location': self.locations.name
        }


