
# coding: utf-8

# In[1]:

# OS.walk generates the file names in a directory tree by walking the tree either top-down or bottom-up
# Find all mp3 files
import fnmatch
import os

rootPath = '/'
pattern='*.mp3'

for root, dirs, files in os.walk(rootPath):
    for filename in fnmatch.filter(files,pattern):
        print(os.path.join(root,filename))


# In[ ]:

# Search comptuer for specific files
import fnmatch
import os

images=['*.jpg','*.jpeg','*.png','*.tif']
matches=[]

for root,dirnames, filenames in os.walk("C:\\"):
    for extensions in images:
        for filename in fnmatch.filter(filenames,extensions):
            matches.append(os.path.join(root,filename))


# In[ ]:



