import json
from pathlib import Path
from ..models import Movie

class Storage:
    def __init__(self, path):
        self.path = Path(path)

    def load(self):
        if not self.path.exists(): return None
        try:
            return [Movie.from_dict(x) for x in json.loads(self.path.read_text(encoding='utf-8'))]
        except Exception:
            return None

    def save(self, movies):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps([m.to_dict() for m in movies], ensure_ascii=False, indent=2), encoding='utf-8')
