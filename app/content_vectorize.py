from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import jieba

def tokenize_chinese(text):
    """中国語のテキストを分かち書きして返す"""
    return ' '.join(jieba.cut(text))


def prepare_tfidf_embeddings(articles, save_path='tfidf_embeddings.pkl'):
    """
    記事タイトルをTF-IDFでベクトル化し、ファイルに保存します。
    """
    # 中国語のタイトルを分かち書き
    titles = [tokenize_chinese(article['title']) for article in articles]

    # TF-IDFベクトライザの作成とフィッティング
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(titles)

    # ベクトルの形状確認
    print("TF-IDF matrix shape:", tfidf_matrix.shape)
    print("Sample TF-IDF vector (first article):", tfidf_matrix[0].toarray())

    # 記事タイトルとURL情報を含むデータを保存
    data = {
        'titles': titles,
        'urls': [article['url'] for article in articles],
        'tfidf_matrix': tfidf_matrix,
        'vectorizer': vectorizer
    }

    with open(save_path, 'wb') as f:
        pickle.dump(data, f)

    print(f"TF-IDFベクトルを{save_path}に保存しました。")
