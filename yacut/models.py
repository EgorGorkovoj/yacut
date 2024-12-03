from datetime import datetime

from yacut import db
from settings import MAX_LENGTH_ORIGINAL_LINK, MAX_LENGTH_SHORT_LINK


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL_LINK), nullable=False)
    short = db.Column(
        db.String(MAX_LENGTH_SHORT_LINK), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())

    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp
        )

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])
