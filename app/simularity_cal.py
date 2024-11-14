from sklearn.metrics.pairwise import cosine_similarity
import pickle
from content_vectorize import tokenize_chinese


def search_similar_articles_tfidf(user_sentence, embeddings_path='tfidf_embeddings.pkl', top_n=5):
    """
    ユーザーが入力したセンテンスに基づいて、TF-IDFを用いて関連性の高いファクトチェック記事を検索します。
    """
    # 事前に保存したTF-IDFデータをロード
    with open(embeddings_path, 'rb') as f:
        data = pickle.load(f)

    titles = data['titles']
    urls = data['urls']
    tfidf_matrix = data['tfidf_matrix']
    vectorizer = data['vectorizer']

    # ユーザー入力を分かち書きしてからTF-IDFでベクトル化
    user_tfidf = vectorizer.transform([tokenize_chinese(user_sentence)])
    print("User TF-IDF vector:", user_tfidf.toarray())

    # コサイン類似度を計算
    cosine_similarities = cosine_similarity(user_tfidf, tfidf_matrix).flatten()
    print("Cosine similarities:", cosine_similarities)

    # 類似度が高い順にソートして上位top_n件を取得
    top_indices = cosine_similarities.argsort()[-top_n:][::-1]
    
    results = []
    for idx in top_indices:
        results.append({
            'title': titles[idx],
            'url': urls[idx],
            'similarity_score': cosine_similarities[idx]
        })

    return results
