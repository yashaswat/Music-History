import os
import gpsoauth
import gkeepapi
import Test.auth as auth

# login info
email = os.getenv('GKEEP_EMAIL')
master_token = os.getenv('GKEEP_MASTER_TOKEN')
note_id = os.getenv('GKEEP_NOTE_ID') # album list note
test_id = os.getenv('GKEEP_TEST_ID')

# connect to google keep account
def connect(mail=email, token=master_token):
    
    glink = gkeepapi.Keep()
    glink.authenticate(mail, token) # establish connection
    return glink


# get data from gkeep note    
def note_data(note_id):
    
    keep = connect()

    gnote = keep.get(note_id) # Music Projects I've Heard
    print(f'Note Title: {gnote.title}') # validating correct note
    
    data = gnote.text     
    return data


# update local text file with gkeep note data
def update_local_txt(file_path, note_id):
    
    gkeep_data = note_data(note_id).split('\n')
    
    with open(file_path, 'w', encoding='utf-8') as textfile:
        textfile.write('\n'.join(entry for entry in gkeep_data if entry))
    
    print('Local Txt updated from Keep Note')


# update gkeep note with local text file data
def update_keep_note(file_path, note_id=note_id):
    
    keep = connect()
    
    # get latest local note data
    with open(file_path, 'r', encoding='utf-8') as textfile:
        local_data = textfile.read()
    
    # push data to google keep    
    gnote = keep.get(note_id)
    gnote.text = local_data
    keep.sync()
    
    print('Keep Note updated from Local Txt')
           
   
if __name__ == '__main__':
    
    mode = input('Test mode (data/ukeep/ulocal): ')
    
    if mode == 'data':
        keepnote = input('View real/test note data:')
        
        if keepnote == 'real':
            print(note_data(note_id))
        elif keepnote == 'test':
            print(note_data(test_id))
        else:
            print('Error: Wrong note selected...)')
            
    elif mode == 'ukeep':
        keepnote = input('Note to update (real/test): ')
        
        if keepnote == 'real':
            update_keep_note('Music Data/album_list.txt', note_id)
        elif keepnote == 'test':
            update_keep_note('Test/test.txt', test_id)
        else:
            print('Error updating keep note...')
        
    elif mode == 'ulocal':
        keepnote = input('Local txt to update (real/test): ')
        
        if keepnote == 'real':
            update_local_txt('Music Data/album_list.txt', note_id)
        elif keepnote == 'test':
            update_local_txt('Test/test.txt', test_id)
        else:
            print('Error updating local txt')
    
    else:
        print('Wrong Mode Selected...')