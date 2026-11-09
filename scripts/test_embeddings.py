
from app.services.embedding_service import embed_texts

sentences = [
    "Tôi quên mật khẩu máy tính",
    "Làm sao lấy lại password?",
    "Hôm nay thời tiết đẹp"
]

embeddings = embed_texts(sentences)

print("Number of sentences:", len(sentences))
print("Embedding shape:", embeddings.shape)
print("First 5 dimensions:")
print(embeddings[0][:5])

import numpy as np

similarity_matrix = np.dot(
    embeddings,
    embeddings.T
)

print("\nSimilarity Matrix:")
print(np.round(similarity_matrix, 3))
