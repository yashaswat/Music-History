import pandas as pd
import openpyxl
import json
import selenium
import music_scrape


def arrow_index(list):
    for i, s in enumerate(list):
        if '<===========' in s:
            return i
    return -1


def music_info_to_dict(data, note_path):

    if data['artist']:
        return
    
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
    
    if data['spotify logged']:
        return
    
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
    
    if 'Current' in data['spotify logged']:
        return
    
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


def get_keep_info(data, note_path):
    
    music_info_to_dict(data, note_path)
    
    spotify_logging_status(data)
    
    current_progress_marking(data)
    

def fill_metadata(data, result_file):
    
    driver = music_scrape.webdriver_init()

    start_point = len(data['release date'])
    
    
    for i, album in enumerate(data['music project'][start_point:]):
        
        try:
            info = music_scrape.fetch_album_info(driver, album)
            print(album, info)
            
            i += start_point
        
            data['runtime'].append(info[1])
            data['release date'].append(info[2])
            data['genre tags'].append(info[3])
            
            if data['artist'][i] == '':
                data['artist'][i] = info[0]

            else:
                continue

            with open(result_file, 'w') as jsonfile:
                json.dump(data, jsonfile, indent=4)
            
        except (selenium.common.exceptions.TimeoutException):
            data['runtime'].append('Error fetch')
            data['release date'].append('Error fetch')
            data['genre tags'].append(['Error fetch'])
            data['artist'][i] = 'Error fetch'
            print(album, '\n')
            continue
  
    driver.quit()


note_path = 'album_list.txt'
result_file = 'data.json'

with open(result_file, 'r') as jsonfile:
    data = json.load(jsonfile)

get_keep_info(data, note_path)
fill_metadata(data, result_file)

df = pd.DataFrame(data)

excel_writer = pd.ExcelWriter('my_music_history.xlsx')
df.to_excel(excel_writer, index=False)
excel_writer.close()
print('\nSUCESSFULLY EXPORTED MUSIC DATA TO EXCEL!\n')
