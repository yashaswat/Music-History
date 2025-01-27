import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def arrow_index(list):
    for i, s in enumerate(list):
        if '<===========' in s:
            return i
    return -1

data = {
    'music project' : [],
    'artist' : [],
    'spotify logged' : []
}

f = open('album_list.txt', 'r')

for i in f.readlines():
    if ' by ' not in i:
        i = i.rstrip()
        data['music project'].append(i)
        data['artist'].append('')
    else:
        i = i.split(' by ')
        data['music project'].append(i[0].rstrip())
        data['artist'].append(i[1].rstrip())
f.close()

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

df = pd.DataFrame(data)

datatoexcel = pd.ExcelWriter('music_historyX.xlsx')
df.to_excel(datatoexcel)
datatoexcel.close()

print('Successfully exported to Excel')
