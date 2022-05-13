import praw
import re
import csv

titles = []
songs = []
artists = []
genres = []
years = []
urls = []
platform = []

# Used by Reddit to identify program
user_agent = "python ListenToThis webscraping"

reddit = praw.Reddit(username="PythonWebscrapePrac",
                     password="PythonWebScrape",
                     client_id="yYy2kShvatemZ3sMCFwPCg",
                     client_secret="xIhNPJU_ha-DcKIGqQsdxJgRCZigsA",
                     user_agent='USERAGENT'
                     )

# Subreddit
subreddit = reddit.subreddit('listentothis')

print(subreddit.display_name)

# For loop for the 70 newest post in ListenToThis subreddit
for post in subreddit.new(limit=70):
    title = post.title
    titles.append(title)

    # Post with '- -' seperator
    if ' - - ' in title:
        artist = title.split(' -')[0]
        artists.append(artist)
        song = re.search(r'- - (.*) \[', title)
        songs.append(song.group(1))

    # Posts with '-' seperator
    elif ' - ' in title:
        artist = title.split(' -')[0]
        artists.append(artist)
        song = re.search(r'- (.*) \[', title)
        songs.append(song.group(1))

    # Posts with '--' seperator
    elif ' -- ' in title:
        artist = title.split(' --')[0]
        artists.append(artist)
        song = re.search(r'-- (.*) \[', title)
        songs.append(song.group(1))

    # Posts with '—' seperator
    elif ' — ' in title:
        artist = title.split(' —')[0]
        artists.append(artist)
        song = re.search(r'— (.*) \[', title)
        songs.append(song.group(1))
    else:
        print(title)
        continue

    # Add link to list
    urls.append(post.url)

    # Add genre to list, everything between [] in title
    genre = re.search(r'\[.*\]', title)
    genres.append(genre.group(0).strip("[]"))

    # Add year to list, post should follow the format of adding the year at the end of title
    year = title[len(title) - 5:len(title) - 1]
    if year.isdecimal():
        years.append(year)
    else:
        years.append('Incorrect format')

# Determines what platform the song is on
for url in urls:
    if 'youtu.be' in url or 'youtube' in url:
        platform.append('YouTube')
    elif 'spotify' in url:
        platform.append('Spotify')
    elif 'soundcloud' in url:
        platform.append("SoundCloud")
    elif 'bandcamp' in url:
        platform.append("Bandcamp")
    else:
        platform.append('Other')

# Writing to csv file
with open('out.csv', 'w') as file:
    writer = csv.writer(file)

    # Labels for csv file
    writer.writerow(['Song', 'Artist', 'Year', 'Genre', 'Platform', 'Link'])

    # Adds a row for every song
    for i in range(len(songs)):
        writer.writerow([songs[i], artists[i], years[i], genres[i], platform[i], urls[i]])
