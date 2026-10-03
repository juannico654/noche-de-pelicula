from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Movie:
    id: str
    title: str
    studio: str
    year: int
    genre: str = "Animación"
    watched: bool = False
    rating_nicolas: Optional[int] = None
    rating_jaeline: Optional[int] = None
    custom: bool = False

    @property
    def average_rating(self):
        ratings = [r for r in (self.rating_nicolas, self.rating_jaeline) if r is not None]
        return round(sum(ratings) / len(ratings), 1) if ratings else None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
