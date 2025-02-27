import os
import gpsoauth
import gkeepapi
import auth

email = auth.email
master_token = auth.master_token

keep = gkeepapi.Keep()
keep.authenticate(email, master_token)

note = keep.createNote('Todo', 'Eat breakfast')
note.pinned = True
note.color = gkeepapi.node.ColorValue.Red

keep.sync()