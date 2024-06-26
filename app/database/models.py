from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from flask_login import UserMixin

from typing import Dict

from .database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    superuser = db.Column(db.Boolean, nullable=False, default=True)

    @property
    def is_superuser(self):
        # override UserMixin property which always returns true
        # return the value of the superuser column instead
        return self.superuser

class CountEntry(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, primary_key=True)

    count: Mapped[int] = mapped_column(Integer)
    close: Mapped[int] = mapped_column(Integer)
    rssi_avg: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rssi_std: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    rssi_min: Mapped[int] = mapped_column(Integer, nullable=True, default=None)
    rssi_max: Mapped[int] = mapped_column(Integer, nullable=True, default=None)

    latitude: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    longitude: Mapped[float] = mapped_column(Float, nullable=True, default=None)

    static_total: Mapped[int] = mapped_column(Integer)
    static_close: Mapped[int] = mapped_column(Integer)

    inst_all: Mapped[int] = mapped_column(Integer)
    inst_close: Mapped[int] = mapped_column(Integer)

    @staticmethod
    def of_dict(data: Dict):
        entry = CountEntry()
        entry.id = data.get('id', None)
        entry.timestamp = data.get('timestamp', None)

        entry.count = data.get('count', 0)
        entry.close = data.get('close', 0)
        entry.rssi_avg = data.get('rssi_avg', None)
        entry.rssi_std = data.get('rssi_std', None)
        entry.rssi_min = data.get('rssi_min', None)
        entry.rssi_max = data.get('rssi_max', None)

        entry.latitude = data.get('latitude', None)
        entry.longitude = data.get('longitude', None)

        entry.static_total = data.get('static_total', 0)
        entry.static_close = data.get('static_close', 0)

        entry.inst_all = data.get('inst_all', 0)
        entry.inst_close = data.get('inst_close', 0)

        return entry

    def to_dict(self, datetime_format="%Y-%m-%d %H:%M:%S"):
        data = {
            'id': self.id,
            'timestamp': self.timestamp.strftime(datetime_format),
            'count': self.count,
            'close': self.close,
            'rssi_avg': self.rssi_avg,
            'rssi_std': self.rssi_std,
            'rssi_min': self.rssi_min,
            'rssi_max': self.rssi_max,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'static_total':self.static_total,
            'static_close':self.static_close,
            'inst_all':self.inst_all,
            'inst_close':self.inst_close
        }
        return data
