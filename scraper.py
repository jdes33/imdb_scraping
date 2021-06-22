import requests
from bs4 import BeautifulSoup
import pandas as pd

URLs = ['https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating',
        'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=101&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=201&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=301&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=401&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=501&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=601&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=701&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=801&ref_=adv_nxt',
        'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=901&ref_=adv_nxt']

titles = []
links = []
years = []
ratings = []
durations =[]
genres = []
votes = []
synopses = []
metascores = []
grosses = []

for URL in URLs:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    list_of_movies = soup.find_all('div', class_='lister-item mode-advanced')
    for movie in list_of_movies:

        title = movie.find('h3',class_='lister-item-header').find('a').text
        link = 'https://www.imdb.com/' + movie.find('h3',class_='lister-item-header').find('a')['href']
        try:
            year = int(movie.find('h3',class_='lister-item-header').find('span', class_='lister-item-year text-muted unbold').text[1:-1])
        except:
            try:
                year = int(movie.find('h3',class_='lister-item-header').find('span', class_='lister-item-year text-muted unbold').text.split()[-1][1:-1])
            except:
                print("error whilst retreiving year")
                print(movie.find('h3',class_='lister-item-header').find('span', class_='lister-item-year text-muted unbold').text)
                year = input("Enter year or press enter if not available:")
                if year:
                    year = int(year)
                else:
                    year = None
        rating = float(movie.find('div', class_='ratings-bar').find('strong').text)

        bonus_info = movie.find_all('p', class_='text-muted')
        try:
            age_rating = bonus_info[0].find('span', class_='certificate').text
        except:
            age_rating = None
        duration_mins = int(bonus_info[0].find('span', class_='runtime').text.split()[0])
        movie_genres = [g.strip() for g in bonus_info[0].find('span', class_='genre').text.split(',')]
        synopsis = bonus_info[1].text.strip()
        try:
            metascore = int(movie.find('div', class_='ratings-bar').find('div', class_='inline-block ratings-metascore').find('span', class_='metascore favorable').text.strip())
        except:
            metascore = None
        misc = movie.find('p', class_='sort-num_votes-visible').find_all('span')
        num_votes = None
        gross = None
        if len(misc) >= 2 and misc[0].text == 'Votes:':
            num_votes = int(misc[1].text.replace(',', '').strip())
        if len(misc) == 5 and misc[-2].text == 'Gross:':
            gross = misc[-1].text #leave as str representation for now

        titles.append(title)
        links.append(link)
        years.append(year)
        ratings.append(rating)
        durations.append(duration_mins)
        genres.append(movie_genres)
        votes.append(num_votes)
        synopses.append(synopsis)
        metascores.append(metascore)
        grosses.append(gross)


# making pandas data frame
movies = pd.DataFrame({'title': titles, 'link':links, 'year':years, 'rating':ratings, 'runtime_mins':durations, 'genres':genres, 'votes':votes, 'metascore':metascores, 'gross':grosses, 'synopsis':synopses,}) 

movies.to_csv('movies.csv')




# MAYBE USE category DTYPE FOR GENRES, https://pbpython.com/pandas_dtypes.html

# EXAMPLE QUERIES:
# movies.sort_values(by=['year', 'rating'], ascending=False).loc[:, ['title', 'year', 'rating']] # THIS IS A LOVELY QUERY

# these queries adds a difference column and then prints the first 50 that have similar imdb and metascore ratings 
# movies['difference'] = abs(movies.rating*10 - movies.metascore)
# movies.sort_values(by='difference').loc[:, ['title','difference']].head(50)

# movies.groupby('year').rating.mean().sort_values(ascending=False) #calculates mean rating per year and then sorts

# get all movies where one of their genres in crime
# movies.loc[movies.genres.apply(lambda x: "Crime" in x)].loc[:, ['title', 'genres']]

# movies.loc[(movies.rating > 7.8) & (movies.year > 2017)].title
# movies.loc[movies.rating.notnull()]
# movies.loc[:, ['title', 'rating', 'num_users_formed_rating']]
# movies.ratings.describe()
# movies.ratings.describe()
# movies.year.astype('object').describe() # i believe this converts to string and shows which year most movies were made (from the list)
# movies.year.unique()
# movies.sort_values(by='rating', ascending=False)
# movies.sort_values(by=['rating', 'year'])
# movies.rating.fillna("Unknown") #probs don't need this
# movies.rating.replace(8, 10)

# note: we can use map() function with a series to transform each value or we can use apply() function to transform each row



