from service.db import db
from datetime import datetime
import sqlalchemy as sa


class ServerCost(db.Model):
    __tablename__ = 'server_costs'

    project_url = db.Column(db.String(), sa.ForeignKey('projects.url'), nullable=False, primary_key=True)
    value = db.Column(db.Numeric(precision=10, scale=2), nullable=True)  # returns a decimal.Decimal object to prevent rounding errors. Pass asdecimal=False to this constructor if you want to just get floats out.
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, created_at=datetime.now(), updated_at=datetime.now(), **kwargs):
        """Mostly rely on default declarative SQLAlchemy constructor. Additionally set the timestamps on object creation."""
        super(ServerCost, self).__init__(**kwargs)  # use the default declarative constructor
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<project url {0} value {1}>'.format(self.url, self.value)
