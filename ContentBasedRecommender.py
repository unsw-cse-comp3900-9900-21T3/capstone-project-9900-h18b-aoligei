from GetSqlData import read_data_from_sql, read_score_data_from_sql
from sklearn.feature_extraction.text import TfidfVectorizer
# Using sklearn's linear_kernel() instead of cosine_similarities() since it is faster.
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
from ast import literal_eval
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

metadata = read_data_from_sql()

# print(metadata.head())

"""
=====================================
Content based on the Description
=====================================
"""

# Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')

# Replace NaN with an empty string
metadata['description'] = metadata['description'].fillna('')

# Construct the required TF-IDF matrix by fitting and transforming the data
tfidf_matrix = tfidf.fit_transform(metadata['description'])

# print(tfidf_matrix.shape)

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
# print(cosine_sim.shape, cosine_sim[1])
# Construct a reverse map of indices and movie titles
indices = pd.Series(metadata.index, index=metadata['title']).drop_duplicates()


# print(indices[:5])

def get_recommendations(title, cosine_sim, indices):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies

    return metadata.iloc[movie_indices]


# print(get_recommendations('Spider-Man - Homecoming', cosine_sim, indices))
# print("========================================")
# print(get_recommendations('Commuter | Blu-ray + UHD, The', cosine_sim, indices))
#

"""
=======================================================================================
Content based on the Format Description and detail , rating, and format, and categories
=======================================================================================
"""


# Function to convert all strings to lower case and strip names of spaces
def clean_data_details(x):
    if isinstance(x, list):
        return [str.lower(i.replace("\r\n\r\n", ",")) for i in x]
    else:
        # Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace("\r\n\r\n", ","))
        else:
            return ''


metadata['details'] = metadata['details'].apply(clean_data_details)


# print(metadata['details'].head(5)[0])


# def str_data(x):
#     if isinstance(x, list):
#         return [str.lower(i) for i in x]
#     else:
#         # Check if director exists. If not, return empty string
#         if isinstance(x, str):
#             return str.lower(x)
#         else:
#             return ''


# features = ['category_id', 'format_id', 'publishDate', 'rating_id']
# for feature in features:
#     metadata[feature] = metadata[feature].apply(str_data)
#
# print(metadata['publishDate'].head(5))


def create_soup(x):
    return ''.join(x['details']) + ' ' + str(x['category_id']) + ' ' + str(x['format_id']) + ' ' + str(
        x['rating_id']) + ' ' + str(x['publishDate'])


metadata['soup'] = metadata.apply(create_soup, axis=1)
#
metadata.to_csv('data_files/test.csv')
# print(metadata[['soup']].head(2))


count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(metadata['soup'])

# print(count_matrix.shape)
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
# Reset index of your main DataFrame and construct reverse mapping as before
metadata = metadata.reset_index()
indices2 = pd.Series(metadata.index, index=metadata['title'])


# check= get_recommendations('Spider-Man - Homecoming', cosine_sim2, indices2)
#
# print(check)