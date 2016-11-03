import os
import shutil
import subprocess
import pip
import stat
import PyPDF2



## GLOBAL VARIABLES


# searches for source files in the present working directory
script_path = os.getcwd()

# md files path

notes_folder = 'source'

# destination path

destination_path_folder = 'docs'


notes_absolute_path = os.path.join(script_path,notes_folder)


destination_absolute_path = os.path.join(script_path,destination_path_folder)


# notes topic list. populate using getFolderList
folder_list = []

# TODO add lunr.js search


## ALL FUNCTIONS

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def replaceMarkdownByhtml(file):
    return os.path.splitext(file)[0] + '.html'

def sanitizeFoldername(name):
    temp = name[3:]
    temp = temp.replace("_"," ")
    temp = temp.capitalize()
    return temp


def replaceMarkdownBypdf(file):
    return os.path.splitext(file)[0] + '.pdf'


def getFolderList(SourceFolder):
    folderList = [ f for f in os.listdir(SourceFolder) if os.path.isdir(os.path.join(SourceFolder,f))]
    return folderList

def createIndexFileForFolders(SourceFolder,DestinationFolder):

    for folder in folder_list:
        files_list = [f for f in os.listdir(os.path.join(SourceFolder,folder))  if os.path.isfile(os.path.join(SourceFolder,folder,f))]
        f = open(os.path.join(DestinationFolder,folder,'index.md'),'w')
        for file in files_list:
            if os.path.splitext(file)[0] != "index":
                f.write("* ####" + "[" + sanitizeFoldername(os.path.splitext(file)[0]) + "]" + "(" + "./" + replaceMarkdownByhtml(file) + ")" + "\n")
        f.close()


def createOutputFolder(SourceFolder,DestinationFolder):

    if(os.path.exists(DestinationFolder)):
        shutil.rmtree(DestinationFolder,onerror=remove_readonly)

    shutil.copytree(SourceFolder,DestinationFolder)
    shutil.copytree(os.path.join(script_path,'assets'),os.path.join(DestinationFolder,'assets'))

def createMainIndexForFolders(SourceFolder,DestinationFolder):

    f = open(os.path.join(DestinationFolder,"index.md"),"w")

    for folder in folder_list:
        if folder != "assets":
            f.write("* " + "###" + "[" + sanitizeFoldername(folder) + "]" + "(" + "./" + folder + "/index.html" + ")" + "\n")


    f.close()



def createHtmlFiles(SourceFolder,DestinationFolder):

    for folder in folder_list:
        if(folder != "assets"):
            files_list  = [f for f in os.listdir(os.path.join(SourceFolder,folder))  if os.path.isfile(os.path.join(SourceFolder,folder,f))]

            for files in files_list:
                completed = subprocess.run(['pandoc','--css=../assets/benjamin.css','--to=html5',os.path.join(DestinationFolder,folder,files),'-o',os.path.join(DestinationFolder,folder,replaceMarkdownByhtml(files))])

    # convert outer index.md
    completed = subprocess.run(['pandoc','--css=./assets/benjamin.css','--to=html5',os.path.join(DestinationFolder,'index.md'),'-o',os.path.join(DestinationFolder, replaceMarkdownByhtml("index.md"))])



def deleteMarkdownFromDestination(DestinationFolder):
    for root, directories, files in os.walk(destination_absolute_path):
        for file in files:
            if os.path.splitext(file)[1] == ".md":
                os.remove(os.path.join(root,file))


def replaceMdByPdf(file):
    return (os.path.splitext(file)[0] + ".pdf")


## STEPS


# get topics
print("getting topics...")
folder_list = getFolderList(notes_absolute_path)

# create individual mds. source and dest is same
print("creating individual index.md files")
createIndexFileForFolders(notes_absolute_path,notes_absolute_path)


# create output folder
print("creating output folder")
createOutputFolder(notes_absolute_path,destination_absolute_path)


# create outer index.md out of folders
print("create outer index.md of topics..")
createMainIndexForFolders(notes_absolute_path,destination_absolute_path)



# convert everything to html using pandoc.
#pandoc --to=html5 input.md -o output.html
print("converting all md files to html...")
createHtmlFiles(notes_absolute_path,destination_absolute_path)



# delete all markdown files
print("deleting all md files from destination path...")
deleteMarkdownFromDestination(destination_absolute_path)

print("==========WEBSITE BUILT SUCCESSFULLY============")












