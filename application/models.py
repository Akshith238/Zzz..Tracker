from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128))
    sleeplist=db.relationship('Sleep',backref='user',lazy=True)

class Sleep(db.Model):
    __tablename__ = 'sleep'
    id = db.Column(db.Integer,unique=True,primary_key=True)
    startTime = db.Column(db.DateTime,nullable=False)
    endTime=db.Column(db.DateTime,nullable=False)
    sleepDuration = db.Column(db.Float, nullable=False)
    sleepQuality=db.Column(db.String(20),nullable=False)
    sleep_owner = db.Column(db.Integer(), db.ForeignKey('user.id'),nullable=False)
    @property
    def calculateSleepDuration(self):
        if self.startTime and self.endTime:
            return (self.endTime - self.startTime).total_seconds()/3600
        else:
            return 0
    @property
    def calculateSleepQuality(self):
        if self.sleepDuration>=8:
            return "Good"
        elif 6 <= self.sleepDuration < 8:
            return "Average"
        else:
            return "Poor"