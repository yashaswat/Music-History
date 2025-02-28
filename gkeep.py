import os
import gpsoauth
import gkeepapi
import auth

# login info
email = auth.email
master_token = auth.master_token
note_id = auth.note_id # album list note


# connect to google keep account
def connect(mail=email, token=master_token):
    
    glink = gkeepapi.Keep()
    glink.authenticate(mail, token) # establish connection
    return glink


# get data from gkeep note    
def note_data(note_id=note_id):
    
    keep = connect()

    gnote = keep.get(note_id) # Music Projects I've Heard
    print(f'Note Title: {gnote.title}') # validating correct note
    
    data = gnote.text     
    return data


# update local text file with gkeep note data
def update_local_txt(file_path, note_id=note_id):
    
    gkeep_data = note_data()
    
    with open(file_path, 'w', encoding='utf-8') as textfile:
        textfile.write(gkeep_data)
    
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
    
    mode = input('Test mode: ')
    
    if mode == 'data':
        print(note_data(note_id))
            
    elif mode == 'ukeep':
        update_keep_note('test.txt', note_id)
        
    elif mode == 'ulocal':
        update_local_txt('test.txt', note_id)