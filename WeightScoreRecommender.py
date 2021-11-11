from GetSqlData import read_data_from_sql, read_score_data_from_sql

data = read_data_from_sql()
score_data = read_score_data_from_sql()

data.to_csv('data_files/product.csv')
score_data.to_csv('data_files/score.csv')

data['id'] = data['id'].astype('int')
score_data['id'] = score_data['product_id'].astype('int')

# merge two dataframe
data_and_score = data.merge(score_data, on='id')
data_and_score.to_csv('data_files/data_and_score.csv')

print(data_and_score.__len__())

# calculate mean of vote avergae column
C = data_and_score['AVG(score)'].mean()
print(C)

# Calculate the minimum number of votes required to be in the chart, m
m = data_and_score['COUNT(score)'].quantile(0.9)
print(m)

# Filter out all qualified movies into a new DataFrame
q_movies = data_and_score.copy().loc[data_and_score['COUNT(score)'] >= m]
print(q_movies.shape, data_and_score.shape)

def weighted_rating(x, m=m, C=C):
    v = x['COUNT(score)']
    R = x['AVG(score)']
    # Calculation based on the IMDB formula
    wr = (v/(v+m)*R) + (m/(m+v)*C)
    return wr

# Define a new feature 'score' and calculate its value with `weighted_rating()`
q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

#Sort movies based on score calculated above
q_movies = q_movies.sort_values('score', ascending=False)

#Print the top 15 movies
print(q_movies[['title', 'COUNT(score)', 'AVG(score)', 'score']].head(20))