import pandas as pd
import openpyxl
import json
import selenium

import music_scrape
import gkeep

def arrow_index(list):
    for i, s in enumerate(list):
        if '<===========' in s:
            return i
    return -1


# store album and artist data from personal list into dictionary
def music_info_to_dict(data, note_path):

    txtnote = open(note_path , 'r').readlines()
    
    txtlen = len(txtnote)
    jsonlen = len(data['artist'])
    
    print(f"No. of new album entries: {txtlen-jsonlen}")

    # if json file already has all fetched data, exit
    if jsonlen == txtlen:
        return
    
    for entry in txtnote[jsonlen:]:
        
        if entry == '\n':
            continue
        
        if ' by ' not in entry:
            entry = entry.rstrip() # remove counting '.'
            data['music project'].append(entry)
            data['artist'].append('') # leave artist empty
        else:
            entry = entry.split(' by ')
            data['music project'].append(entry[0].rstrip())
            data['artist'].append(entry[1].rstrip())
    # txtnote.close()
  

# mark if I logged my top 3 songs from album in my spotify playlist
# identified using '₹' (not logged)
def spotify_logging_status(data, note_path):
    
    txtnote = open(note_path , 'r').readlines()
    
    txtlen = len(txtnote)
    jsonlen = len(data['spotify logged'])
    
    if jsonlen == txtlen: # if json file already has fetched data, exit
        return
    
    for i, album in enumerate(data['music project'][jsonlen:]):
        
        # mark albums without ₹ as logged
        if 'â‚¹' not in album:
            data['spotify logged'].append('Yes')
            data['music project'][i+jsonlen] = data['music project'][i+jsonlen].replace(' â‚¹', '').lstrip('.')
        else:
            data['spotify logged'].append('No')
            data['music project'][i+jsonlen] = data['music project'][i+jsonlen].replace(' â‚¹', '').lstrip('.')
   
    for i, artist in enumerate(data['artist']):

        # albums with artists have ₹ in artists list
        # mark those as not logged
        if 'â‚¹' not in artist:
            continue
        else:
            data['spotify logged'][i+jsonlen] = 'No'
            data['artist'][i+jsonlen] = data['artist'][i+jsonlen].replace(' â‚¹', '')


# mark point i have currently reached in spotify logging
# identified using '<==========='
# albums below arrow are all not logged
def current_progress_marking(data):
    
    # if 'Current' in data['spotify logged']: 
    #     return
    
    # arrow can be in album or artist array
    artist_arrow = arrow_index(data['artist'])
    album_arrow = arrow_index(data['music project'])

    # mark logged status as 'Current'
    # remove arrow from array
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
    
    spotify_logging_status(data, note_path)
    
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


note_path = 'Test/test.txt'
result_file = 'Test/test.json'

with open(result_file, 'r') as jsonfile:
    data = json.load(jsonfile)

get_keep_info(data, note_path)
fill_metadata(data, result_file)

df = pd.DataFrame(data)

excel_writer = pd.ExcelWriter('Test/test.xlsx')
df.to_excel(excel_writer, index=False)
excel_writer.close()
print('\nSUCESSFULLY EXPORTED MUSIC DATA TO EXCEL!\n')
