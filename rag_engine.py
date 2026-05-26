# rag_engine.py
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


class RAGEngine:
    def __init__(self, kb_path: str):
        self.kb_path = kb_path

        if not os.path.exists(self.kb_path):
            raise FileNotFoundError(f"ไม่พบไฟล์ Knowledge Base: {self.kb_path}")

        self.model = SentenceTransformer(EMBED_MODEL)
        self.chunks = self._load_and_chunk(self.kb_path)

        if len(self.chunks) == 0:
            raise ValueError(
                "Knowledge Base ว่าง หรืออ่านข้อมูลไม่ได้ กรุณาใส่ข้อมูลในไฟล์ knowledge/milklab_kb.txt"
            )

        self.index, self.embeddings = self._build_index()

    def _load_and_chunk(self, path: str) -> list[str]:
        with open(path, "r", encoding="utf-8") as file:
            text = file.read().strip()

        if not text:
            return []

        chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
        return chunks

    def _build_index(self):
        embeddings = self.model.encode(self.chunks, show_progress_bar=False)
        embeddings = np.array(embeddings, dtype="float32")

        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        return index, embeddings

    def search(self, query: str, top_k: int = 3) -> list[str]:
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding, dtype="float32")

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        top_k = min(top_k, len(self.chunks))

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for i in indices[0]:
            if 0 <= i < len(self.chunks):
                results.append(self.chunks[i])

        return results