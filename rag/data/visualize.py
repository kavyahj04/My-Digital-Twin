import chromadb
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# 1. Connect to your database
client = chromadb.PersistentClient(path="my_vectordb")
collection = client.get_collection(name="digital-twin")

# 2. Extract embeddings, metadata, and documents
results = collection.get(include=["embeddings", "metadatas", "documents"])
embeddings = results["embeddings"]
metadatas = results["metadatas"]

if embeddings is not None and len(embeddings) > 0:
    # 3. Reduce 384 dimensions to 2D using PCA
    pca = PCA(n_components=2)
    reduced_vectors = pca.fit_transform(embeddings)

    # 4. Plot points
    plt.figure(figsize=(10, 6))
    
    # Color points by source_type
    categories = list(set(m.get("source_type", "default") for m in metadatas))
    color_map = {cat: i for i, cat in enumerate(categories)}
    colors = [color_map[m.get("source_type", "default")] for m in metadatas]

    scatter = plt.scatter(
        reduced_vectors[:, 0], 
        reduced_vectors[:, 1], 
        c=colors, 
        cmap="tab10", 
        alpha=0.7
    )

    plt.title("ChromaDB Vector Embeddings (PCA 2D Projection)")
    plt.xlabel("PCA Axis 1")
    plt.ylabel("PCA Axis 2")
    plt.colorbar(scatter, ticks=range(len(categories)), format=plt.FuncFormatter(lambda val, loc: categories[int(val)] if int(val) < len(categories) else ""))
    plt.show()
else:
    print("No embeddings found in collection. Make sure you passed embeddings or query results.")