import tempfile
from pathlib import Path
from peli_cita.services.storage import Storage
from peli_cita.services.movie_service import MovieService

def test_add_and_rate_persists():
    with tempfile.TemporaryDirectory() as d:
        s = MovieService(Storage(Path(d) / 'movies.json'))
        m = s.add('Mi película', 'Disney', 2026)
        s.rate(m, 'nicolas', 5)
        s.rate(m, 'jaeline', 4)
        s2 = MovieService(Storage(Path(d) / 'movies.json'))
        loaded = next(x for x in s2.movies if x.title == 'Mi película')
        assert loaded.watched is True
        assert loaded.rating_nicolas == 5
        assert loaded.rating_jaeline == 4
        assert loaded.average_rating == 4.5
