from App.database import db
from datetime import datetime, timedelta


class ShiftType(db.Model):
    __tablename__ = 'shift_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  
    start_time = db.Column(db.Time, nullable=False)              
    end_time = db.Column(db.Time, nullable=False)                
    is_overnight = db.Column(db.Boolean, default=False)

    shifts = db.relationship("Shift", backref="type", lazy=True)

    def get_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "start_time": self.start_time.strftime("%H:%M"),
            "end_time": self.end_time.strftime("%H:%M"),
            "is_overnight": self.is_overnight
        }