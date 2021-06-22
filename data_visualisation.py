import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


#df = sns.load_dataset("penguins")
movies = pd.read_csv('movies.csv', index_col=0)
#sns.distplot(a=movies.year, kde=False)

#sns.jointplot(x=movies.year, y=movies.rating, kind="kde")

#sns.swarmplot(x=movies.year, y=movies.rating)

#sns.scatterplot(x=movies.loc[:,'Western'].year, y=movies.rating, hue=movies.genres)

crime_movies = movies.loc[movies.genres.apply(lambda x: "Crime" in x)]
thriller_movies = movies.loc[movies.genres.apply(lambda x: "Thriller" in x)]
drama_movies = movies.loc[movies.genres.apply(lambda x: "Drama" in x)]
mystery_movies = movies.loc[movies.genres.apply(lambda x: "Mystery" in x)]
romance_movies = movies.loc[movies.genres.apply(lambda x: "Romance" in x)]

sns.regplot(x=crime_movies.year, y=crime_movies.votes, label='crime')
sns.regplot(x=thriller_movies.year, y=thriller_movies.votes, label='thriller')
sns.regplot(x=drama_movies.year, y=drama_movies.votes, label='drama')
sns.regplot(x=mystery_movies.year, y=mystery_movies.votes, label='mystery')
sns.regplot(x=romance_movies.year, y=romance_movies.votes, label='romance')



plt.legend()
plt.show()
