import random
from .storage import Storage
from ..data.movies import default_movies

class MovieService:
    def __init__(self, storage):
        self.storage = storage
        self.movies = storage.load() or default_movies()
        self.storage.save(self.movies)

    def save(self): self.storage.save(self.movies)
    def available(self, include_watched=False, studio=None):
        xs = self.movies if include_watched else [m for m in self.movies if not m.watched]
        return [m for m in xs if not studio or m.studio == studio]
    def random_movie(self, include_watched=False, studio=None):
        xs = self.available(include_watched, studio)
        return random.choice(xs) if xs else None
    def add(self, title, studio, year):
        import re
        mid = re.sub(r'[^a-z0-9]+','_',title.lower()).strip('_') + '_' + str(random.randint(1000,9999))
        m = __import__('peli_cita.models', fromlist=['Movie']).Movie(mid,title,studio,year,custom=True)
        self.movies.append(m); self.save(); return m
    def toggle_watched(self, movie): movie.watched = not movie.watched; self.save()
    def rate(self, movie, person, stars):
        setattr(movie, f'rating_{person}', stars); movie.watched = True; self.save()
