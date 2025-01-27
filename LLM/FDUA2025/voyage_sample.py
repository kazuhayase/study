import voyageai
import numpy as np
from sklearn.neighbors import NearestNeighbors

vo = voyageai.Client()
# This will automatically use the environment variable VOYAGE_API_KEY.
# Alternatively, you can use vo = voyageai.Client(api_key="<your secret key>")

#result = vo.embed(["hello world"], model="voyage-3")

documents = [
    "The Mediterranean diet emphasizes fish, olive oil, and vegetables, believed to reduce chronic diseases.",
    "Photosynthesis in plants converts light energy into glucose and produces essential oxygen.",
    "20th-century innovations, from radios to smartphones, centered on electronic advancements.",
    "Rivers provide water, irrigation, and habitat for aquatic species, vital for ecosystems.",
    "Apple’s conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.",
    "Shakespeare's works, like 'Hamlet' and 'A Midsummer Night's Dream,' endure in literature."
]

# Embed the documents
""" doc_embds = vo.embed(
    documents, model="voyage-3", input_type="document"
).embeddings"""

query = "When is Apple's conference call scheduled?" 


# Get the embedding of the query
""" query_embd = vo.embed([query], model="voyage-3", input_type="query").embeddings[0]
 """
# Compute the similarity
# Voyage embeddings are normalized to length 1, therefore dot-product and cosine 
# similarity are the same.
""" similarities = np.dot(doc_embds, query_embd)

retrieved_id = np.argmax(similarities)
print(documents[retrieved_id])
 """
# Use the k-nearest neighbor algorithm to identify the top-k documents with the highest similarity
""" nbrs = NearestNeighbors(n_neighbors=3, algorithm='auto').fit(doc_embds)
distances, indices = nbrs.kneighbors([query_embd])
retrieved_docs = [documents[index] for index in indices[0]]
print(retrieved_docs)
 """
# Reranking
documents_reranked = vo.rerank(query, documents, model="rerank-2", top_k=3)
for r in documents_reranked.results:
    print(f"Document: {r.document}")
    print(f"Relevance Score: {r.relevance_score}")
    print(f"Index: {r.index}")
    print()
    
