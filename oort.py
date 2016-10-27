import os
import shutil
import subprocess
import pip


def replaceMarkdownByhtml(file):
    return os.path.splitext(file)[0] + '.html'

# searches for source files in the present working directory
script_path = os.getcwd()

# md files path

notes_folder = 'source'

# destination path

destination_path_folder = 'docs'


notes_absolute_path = os.path.join(script_path,notes_folder)


destination_absolute_path = os.path.join(script_path,destination_path_folder)


# TODO add lunr.js search


# populate note topics in a list
folder_list = [ f for f in os.listdir(notes_absolute_path) if os.path.isdir(os.path.join(notes_absolute_path,f))]


# create outer index.md out of these

f = open("index.md","w")

for folder in folder_list:
    f.write("* " + "[" + folder + "]" + "(" + "./docs/" + folder + ")" + "\n")

f.close()

# create destination folder
    # delete docs folder
if(os.path.exists(destination_absolute_path)):
    shutil.rmtree(destination_path_folder)

    #create empty docs folder
os.makedirs(destination_path_folder)



# copy assets and contents of source folders inside docs.


# #    pandoc --to=html5 input.md -o output.html




# for files in md_page_list:
#     completed = subprocess.run(['pandoc','--css=../assets/benjamin.css','--to=html5',os.path.join(markdownAbsolutePath,files),'-o',os.path.join(destination_path_folder,replaceMarkdownByhtml(files))])















