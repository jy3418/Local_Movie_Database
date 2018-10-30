import os, json, sqlite3
import urllib.request
import urllib.parse

#Small program to store movies found in your directory into a local database

# Change this variable for a different directory of where movies are saved
# GUI still in implementation
directory = "C:/Users/jy341/Videos"


def main():
    fileArray = []
    for file in os.listdir(directory):
        if file.endswith(".avi") or file.endswith(".mov") or file.endswith(".mp4") \
                or file.endswith(".wmv") or file.endswith(".flv"):
            fileArray.append(file[0:file.find('.')])

    for filename in fileArray:
        json_data = search_movie(filename)
        save_database(json_data)


def search_movie(moviename):
    try:
        key = '7fc0d461'
        parsedtitle = urllib.parse.urlencode({'t': moviename})
        url = 'http://www.omdbapi.com/?apikey=' + key + '&' + parsedtitle

        print("Attempting to retrieve data of " + moviename + " now.")

        uh = urllib.request.urlopen(url)
        data = uh.read()
        json_data = json.loads(data)

        if json_data['Response'] == 'True':
            return json_data
        else:
            print("Could not retrieve the data for the movie" + moviename)

    except urllib.error.URLError as e:
        print(f"Error: {e.reason}")


def save_database(json_data):
    filename = 'moviedatabase.db'
    conn = sqlite3.connect(str(filename))
    cur = conn.cursor()

    title = json_data['Title']
    if json_data['Year'] != 'N/A':
        year = int(json_data['Year'])
    else:
        year = -1
    if json_data['Runtime'] != 'N/A':
        runtime = int(json_data['Runtime'].split()[0])
    else:
        runtime = -1
    if json_data['Country'] != 'N/A':
        country = json_data['Country']
    else:
        country = 'N/A'
    if json_data['Metascore'] != 'N/A':
        metascore = float(json_data['Metascore'])
    else:
        metascore = -1
    if json_data['imdbRating'] != 'N/A':
        imdb_rating = float(json_data['imdbRating'])
    else:
        imdb_rating = -1
    if json_data['Genre'] != 'N/A':
        genre = json_data['Genre']
    else:
        genre = 'N/A'

    cur.execute("""CREATE TABLE IF NOT EXISTS MovieData(
                Title text,
                Genre text,
                Year integer,
                Runtime integer,
                Country text,
                Metascore real,
                IMDBRating real)""")
    cur.execute("SELECT * FROM MovieData WHERE Title = ? ", (title,))
    fetched_row = cur.fetchone()

    if fetched_row is None:
        cur.execute("""INSERT INTO MovieData (Title, Genre, Year, Runtime, Country, Metascore, IMDBRating)
                VALUES (?,?,?,?,?,?,?)""", (title, genre, year, runtime, country, metascore, imdb_rating))
        print(title + " was successfully saved in the database.")

        # Save a copy of the data that was stored in the database onto a text file in the same directory as videos,
        f = open(directory + '/' + title + '.txt', 'w+')
        f.write("Title: " + title + "\nGenre: " + genre + "\nYear: " + str(year) + "\nRuntime: " + str(runtime) +
                " minutes" + "\nCountry: " + country + "\nMetascore: " + str(metascore) + "\nIMDB Rating: " + str(imdb_rating))
        f.close()
    else:
        print(title + " already exists in local database. Nothing was changed.")

    conn.commit()
    conn.close()



if __name__ == '__main__':
    main()