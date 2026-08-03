"""Multilingual semantic embeddings for repo scoring.

Strategy: local sentence-transformers model `paraphrase-multilingual-MiniLM-L12-v2`
(~118 MB, multilingual 50 languages including CN/EN/FR), normalized 384-dim vectors.

- Lazy load: the model is only downloaded on the first call to `embed()` or `embed_batch()`.
- Disk cache: embeddings indexed by hash of the source text to avoid recomputation
  across runs (a typical run embeds ~3600 repos × <1 kB = 25 MB of JSON cache).
- No network beyond the initial model download (~30 s on a decent connection).

API:
    e = get_embedder()                       # lazy singleton
    vec = e.embed("texte")                   # np.ndarray shape (384,), L2-normalized
    mat = e.embed_batch(["t1", "t2", ...])   # np.ndarray shape (N, 384)
    sim = e.cosine(vec_a, vec_b)             # float in [-1, 1]
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import threading
from pathlib import Path

# Minerva only uses the PyTorch backend of sentence-transformers. If TensorFlow
# or Flax are installed in the environment (frequent on dev machines),
# `transformers` tries to import them when loading the model — which breaks as soon
# as a version of protobuf incompatible with TF's `_pb2.py` is present
# (TypeError: Descriptors cannot be created directly). We disable these backends
# BEFORE any import of sentence_transformers/transformers (lazy, in _ensure_model).
os.environ.setdefault("USE_TF", "0")
os.environ.setdefault("USE_FLAX", "0")

import numpy as np


log = logging.getLogger("minerva.embedder")

ROOT = Path(__file__).resolve().parents[1]
CACHE_FILE = ROOT / "output" / "embeddings_cache.json"

DEFAULT_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
EMBED_DIM = 384


def _hash_text(text: str) -> str:
    """Short SHA-256 (12 hex chars = 48 bits) of the source text as a cache key."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


class Embedder:
    """Lazy wrapper around sentence-transformers + persistent disk cache."""

    def __init__(self, model_name: str = DEFAULT_MODEL, cache_path: Path = CACHE_FILE):
        self.model_name = model_name
        self.cache_path = cache_path
        self._model = None  # lazy
        self._lock = threading.Lock()
        self._cache: dict[str, list[float]] = {}
        self._cache_dirty = False
        self._load_cache()

    def _load_cache(self) -> None:
        if not self.cache_path.is_file():
            return
        try:
            data = json.loads(self.cache_path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("model") == self.model_name:
                self._cache = data.get("vectors", {})
                log.info(f"Cache embeddings chargé : {len(self._cache)} entrées ({self.model_name})")
            else:
                log.info("Cache embeddings ignoré (modèle différent) — sera réécrit")
        except (json.JSONDecodeError, OSError) as exc:
            log.warning(f"Cache embeddings illisible : {exc} — repart de zéro")

    def save_cache(self) -> None:
        """Persists the cache. To be called manually after a batch (otherwise lost)."""
        if not self._cache_dirty:
            return
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"model": self.model_name, "vectors": self._cache}
        tmp = self.cache_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        tmp.replace(self.cache_path)
        self._cache_dirty = False
        log.info(f"Cache embeddings sauvegardé : {len(self._cache)} entrées")

    def _ensure_model(self):
        """Loads the model on first use (downloads ~118 MB the first time)."""
        if self._model is not None:
            return self._model
        with self._lock:
            if self._model is None:
                log.info(f"Chargement du modèle d'embeddings : {self.model_name} (premier usage)")
                from sentence_transformers import SentenceTransformer  # noqa: PLC0415
                self._model = SentenceTransformer(self.model_name)
                log.info(f"Modèle chargé ; dim = {self._model.get_sentence_embedding_dimension()}")
        return self._model

    def embed(self, text: str) -> np.ndarray:
        """Encodes a text. L2-normalized vector ready for cosine similarity = dot product."""
        if not text or not text.strip():
            return np.zeros(EMBED_DIM, dtype=np.float32)

        key = _hash_text(text)
        if key in self._cache:
            return np.asarray(self._cache[key], dtype=np.float32)

        model = self._ensure_model()
        vec = model.encode(text, normalize_embeddings=True, show_progress_bar=False)
        vec = np.asarray(vec, dtype=np.float32)
        self._cache[key] = vec.tolist()
        self._cache_dirty = True
        return vec

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        """Encodes a batch. Returns shape (N, EMBED_DIM). Cache hits maximized."""
        if not texts:
            return np.zeros((0, EMBED_DIM), dtype=np.float32)

        out = np.zeros((len(texts), EMBED_DIM), dtype=np.float32)
        to_compute_idx: list[int] = []
        to_compute_text: list[str] = []

        for i, t in enumerate(texts):
            if not t or not t.strip():
                continue  # zero vector
            key = _hash_text(t)
            if key in self._cache:
                out[i] = np.asarray(self._cache[key], dtype=np.float32)
            else:
                to_compute_idx.append(i)
                to_compute_text.append(t)

        if to_compute_text:
            model = self._ensure_model()
            vecs = model.encode(to_compute_text, normalize_embeddings=True,
                                show_progress_bar=False, batch_size=64)
            vecs = np.asarray(vecs, dtype=np.float32)
            for i, idx in enumerate(to_compute_idx):
                out[idx] = vecs[i]
                self._cache[_hash_text(to_compute_text[i])] = vecs[i].tolist()
            self._cache_dirty = True

        return out

    @staticmethod
    def cosine(a: np.ndarray, b: np.ndarray) -> float:
        """Cosine similarity. Assumes L2-normalized vectors (= dot product)."""
        a_norm = float(np.linalg.norm(a))
        b_norm = float(np.linalg.norm(b))
        if a_norm < 1e-9 or b_norm < 1e-9:
            return 0.0
        # If already normalized (always our case), dot = cosine
        return float(np.dot(a, b) / (a_norm * b_norm))


# Singleton
_embedder: Embedder | None = None
_singleton_lock = threading.Lock()


def get_embedder() -> Embedder:
    """Returns the Embedder singleton (instantiated on demand)."""
    global _embedder
    if _embedder is None:
        with _singleton_lock:
            if _embedder is None:
                _embedder = Embedder()
    return _embedder
