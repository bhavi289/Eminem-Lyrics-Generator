import urllib.request as urllib2
from bs4 import BeautifulSoup
import pandas as pd
import re
from unidecode import unidecode

quote_page = 'https://www.azlyrics.com/lyrics/eminem/{}.html'
filename = 'eminem-songs.csv'
songs = pd.read_csv(filename)

for index, row in songs.iterrows():
    try:
        song_name = ''.join(c.lower() if c.isalpha() else c if c.isnumeric() else "" for c in row['song'])
        print (f"index - {index}, song name - {song_name} ")

        # songs.at[1, 'lyrics'] = "niqqa"

        

        page = urllib2.urlopen(quote_page.format(song_name))
        soup = BeautifulSoup(page, 'html.parser')

        verses = soup.find_all('div',class_=None)

        # verses = soup.find_all('p', attrs={'class': 'verse'})

        lyrics = ''

        for verse in verses:
            text = verse.text.strip()
            text = re.sub(r"\[.*\]\n", "", unidecode(text))
            if lyrics == '':
                lyrics = lyrics + text.replace('\n', '|-|')
            else:
                lyrics = lyrics + '|-|' + text.replace('\n', '|-|')

        songs.at[index, 'lyrics'] = lyrics
        # songs.set_value(index, 'lyrics', lyrics)

        print('saving {}'.format(row['song']))
        songs.head()

    except Exception as e:
        print (f"Error - {e}\nFor {row['song']}.")

    # break

print('writing to .csv')
songs.to_csv(filename, sep=',', encoding='utf-8', index=False)