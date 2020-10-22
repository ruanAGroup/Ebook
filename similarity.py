from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from scipy.linalg import norm


def tfidf_similarity(s1, s2):
    def add_space(s):
        return ' '.join(list(s))

    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = TfidfVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 计算TF系数
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))

 def similarity_sorting(books,s1):
     length=len(books)
     for i in range(length)
         similarity[i]=tfidf_similarity(s1, s2)
     while length > 0:
         for j in range(length - 1):
             if similarity[j] < similarity[j + 1]:
                 books(length + 1) = books(j)
                 books(j) = books(j+ 1)
                 books(j + 1) = books（length + 1）
             length -= 1
 return books