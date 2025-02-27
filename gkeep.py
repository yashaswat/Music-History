import os
import gpsoauth
import gkeepapi
import auth

# login info
email = auth.email
master_token = auth.master_token
note_id = auth.note_id # album list note


def gkeep_get(email, master_token, note_id):
    
    keep = gkeepapi.Keep()
    keep.authenticate(email, master_token) # establish connection

    gnote = keep.get(note_id) # Music Projects I've Heard
    print(gnote.title) # validating correct note
    
    data = gnote.text     
    return data

    
if __name__ == '__main__':
       
    with open('test.txt', 'w', encoding='utf-8') as f:
        f.write(gkeep_get(email, master_token, note_id))
        f.close()
    