import os
import re


def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.split()


def build_index(doc_folder):
    docs = {}
    dictionary = {}
    index = {}

    doc_id = 1
    for filename in os.listdir(doc_folder):
        if filename.endswith(".txt"):
            path = os.path.join(doc_folder, filename)
            content = open(path, "r", encoding="utf-8").read()
            tokens = tokenize(content)

            docs[doc_id] = filename

            for token in tokens:
                dictionary[token] = dictionary.get(token, 0) + 1

                if token not in index:
                    index[token] = set()
                index[token].add(doc_id)

            doc_id += 1

    return docs, dictionary, index



def boolean_and(p1, p2):
    return p1.intersection(p2)

def boolean_or(p1, p2):
    return p1.union(p2)

def boolean_not(p1, all_docs):
    return all_docs - p1



def process_query(query, index, all_docs):
    tokens = query.split()

    if len(tokens) == 3:
        t1, op, t2 = tokens

        p1 = index.get(t1, set())
        p2 = index.get(t2, set())

        if op.upper() == "AND":
            return boolean_and(p1, p2)
        elif op.upper() == "OR":
            return boolean_or(p1, p2)
        else:
            return "Unknown operator."

    elif len(tokens) == 2 and tokens[0].upper() == "NOT":
        t = tokens[1]
        p = index.get(t, set())
        return boolean_not(p, all_docs)

    else:
        return "Invalid query format."



if __name__ == "__main__":
    doc_folder = "documents"     # Folder with .txt files
    docs, dictionary, index = build_index(doc_folder)

    all_docs = set(docs.keys())

    print("✅ Documents Loaded:", docs)
    print("\n📘 Dictionary:", dictionary)
    print("\n📚 Inverted Index:", index)

    while True:
        q = input("\n🔍 Enter Boolean Query (e.g., 'iphone AND apple', or type 'exit'): ")
        if q.lower() == "exit":
            break
        result = process_query(q, index, all_docs)
        print("✅ Result:", result)

