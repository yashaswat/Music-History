import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import music_scrape


def arrow_index(list):
    for i, s in enumerate(list):
        if '<===========' in s:
            return i
    return -1


def music_info_to_dict(data, note_path):

    f = open(note_path , 'r')

    for entry in f.readlines():
        
        if entry == '\n':
            continue
        
        if ' by ' not in entry:
            entry = entry.rstrip()
            data['music project'].append(entry)
            data['artist'].append('')
        else:
            entry = entry.split(' by ')
            data['music project'].append(entry[0].rstrip())
            data['artist'].append(entry[1].rstrip())
    f.close()
  

def spotify_logging_status(data):
    
    for i, album in enumerate(data['music project']):

        if 'â‚¹' not in album:
            data['spotify logged'].append('Yes')
            data['music project'][i] = data['music project'][i].replace(' â‚¹', '').lstrip('.')
        else:
            data['spotify logged'].append('No')
            data['music project'][i] = data['music project'][i].replace(' â‚¹', '').lstrip('.')
   
    for i, artist in enumerate(data['artist']):

        if 'â‚¹' not in artist:
            continue
        else:
            data['spotify logged'][i] = 'No'
            data['artist'][i] = data['artist'][i].replace(' â‚¹', '')


def current_progress_marking(data):
    
    artist_arrow = arrow_index(data['artist'])
    album_arrow = arrow_index(data['music project'])

    if album_arrow != -1:

        data['music project'][album_arrow] = data['music project'][album_arrow].replace('<===========', '')
        data['spotify logged'][album_arrow] = 'Current'

        for i in range(album_arrow+1, len(data['music project'])):
            data['spotify logged'][i] = 'No'
        
    if artist_arrow != -1:

        data['artist'][artist_arrow] = data['artist'][artist_arrow].replace('<===========', '')
        data['spotify logged'][artist_arrow] = 'Current'

        for i in range(artist_arrow+1, len(data['music project'])):
            data['spotify logged'][i] = 'No'


def fill_metadata(data, error_log):
    
    driver = music_scrape.webdriver_init()
    
    for i, album in enumerate(data['music project']):
        
        if i > 0 and i % 5 == 0:
            driver.delete_all_cookies()
            driver.execute_script("window.localStorage.clear();")
            driver.refresh()
            
        if i > 0 and i % 15 == 0:
            driver.quit()
            driver = music_scrape.webdriver_init()
        
        info = music_scrape.fetch_album_info(driver, album)
        print(album, info)
        
        data['runtime'] = info[1]
        data['release date'] = info[2]
        data['genre tags'] = info[3]
        
        try:
            if data['artist'][i] == '':
                data['artist'] = info[0]
            
            else:
                continue
        
        except IndexError:
            data['artist'] = 'Error'
            error_log.append(album)


note_path = 'album_list.txt'

data = {
    'music project' : [],
    'artist' : [],
    'runtime' : [],
    'release date' : [],
    'spotify logged' : [],
    'genre tags' : []
}

error_log = []

music_info_to_dict(data, note_path)
spotify_logging_status(data)
current_progress_marking(data)
fill_metadata(data, error_log)

df = pd.DataFrame(data)

datatoexcel = pd.ExcelWriter('my_music_history.xlsx')
df.to_excel(datatoexcel)
datatoexcel.close()

if error_log:
    print(f'Error in following albums: {error_log}')
    print('\n Rest exported sucessfully')
else:
    print('Successfully exported to Excel')