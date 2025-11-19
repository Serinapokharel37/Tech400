import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Folder containing document files
doc_folder = "news_docs"  # Make sure this folder exists with doc1.txt, doc2.txt, ...

# Load documents
doc_files = sorted(os.listdir(doc_folder))  # Sort to maintain doc1.txt, doc2.txt...
documents = []
for file in doc_files:
    with open(os.path.join(doc_folder, file), 'r', encoding='utf-8') as f:
        documents.append(f.read())

# Load queries
with open("queries.txt", 'r', encoding='utf-8') as f:
    queries = [line.strip() for line in f.readlines()]

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

# Open log file
with open("similarity_log.txt", "w", encoding='utf-8') as log_file:
    # Process each query
    for i, query in enumerate(queries, 1):
        query_vec = vectorizer.transform([query])
        sim_scores = cosine_similarity(query_vec, tfidf_matrix)[0]

        # Prepare results
        ranked_docs = [doc_files[j] for j in sim_scores.argsort()[::-1]]  # Most relevant first

        # Print and write to log
        output = f"Query {i}: {query}\nSimilarity scores with documents:\n"
        for doc, score in zip(doc_files, sim_scores):
            output += f"{doc}: {score:.4f}\n"
        output += f"Ranking of documents (most relevant first): {ranked_docs}\n\n"

        print(output)
        log_file.write(output)

print("All results have been saved to similarity_log.txt")
