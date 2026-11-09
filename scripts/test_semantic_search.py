
from app.services.semantic_search import semantic_search

query = "Tôi không đăng nhập được tài khoản công ty"

results = semantic_search(query, top_k=3)

print(f"\nQuestion: {query}")

for i, result in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("Source:", result["source"])
    print("Similarity:", result["score"])
    print("Content:", result["text"][:200])
