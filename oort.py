import os
import shutil
import subprocess
import pip
import stat
import PyPDF2
import sys



## GLOBAL VARIABLES

possible_args = ['buildwebsite','pdf2txt','webpage2txt','slideshow']


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


def combinePdfs(SourceFolder,DestinationFolder):
    files = [file for file in os.listdir(SourceFolder) if (os.path.splitext(file)[1] == ".pdf") ]

    if os.path.exists(DestinationFolder):
        shutil.rmtree(DestinationFolder)

    os.makedirs(DestinationFolder)

    merger = PyPDF2.PdfFileMerger()

    for filename in files:
        print("combining " + filename)
        merger.append(PyPDF2.PdfFileReader(open(os.path.join(SourceFolder,filename),'rb')))
        print("combined " + filename)

    merger.write(os.path.join(DestinationFolder,"combined.pdf"))


 #pandoc --latex-engine=xelatex -t beamer .\11-Exceptions.md --slide-level 2 -o example8.pdf

def convertMdToBeamer(inputFile,outputFolder):
    print("converting " + os.path.split(inputFile)[1] + " to beamer...")
    command = ['pandoc',"--latex-engine=xelatex","-t","beamer",inputFile,"--slide-level",'2','-o',os.path.join(outputFolder,replaceMdByPdf(os.path.split(inputFile)[1]))]
    subprocess.run(command)
    print("converted " + os.path.relpath(inputFile) + " to beamer...")

def batchBeamerConversion(SourceFolder,DestinationFolder):

    if not os.path.exists(DestinationFolder):
        os.makedirs(DestinationFolder)

    files = [file for file in os.listdir(SourceFolder) if (os.path.isfile(os.path.join(SourceFolder,file)) and os.path.splitext(file)[1] == ".md")]

    for file in files:
        if (os.path.exists(os.path.join(DestinationFolder,file))):
            os.remove(os.path.join(DestinationFolder,file))
        convertMdToBeamer(os.path.join(SourceFolder,file),DestinationFolder)



def batchPdfConversion(SourceFolder,DestinationFolder):

    # ***create pdfs
    files = [file for file in os.listdir(SourceFolder) if (os.path.splitext(file)[1] == ".md" and os.path.splitext(file)[0] != "index")]

    folders = [folder for folder in os.listdir(SourceFolder) if (os.path.isdir(os.path.join(SourceFolder,folder)) and folder != "assets")]

    if os.path.exists(DestinationFolder):
        shutil.rmtree(DestinationFolder)

    os.makedirs(DestinationFolder)

    #outer
    if not files:
        for file in files:
            print("starting conversion: " + file + " to pdf...")
            command = ['pandoc',"--variable","fontsize=14pt","--variable","documentclass=extarticle",os.path.join(SourceFolder,file),'--latex-engine=xelatex','--template=./assets/me.latex','-o',os.path.join(DestinationFolder,replaceMdByPdf(file))]
            subprocess.run(command)
            print("conversion completed: " + file + " to pdf...")

    #inner
    for folder in folders:
        os.makedirs(os.path.join(DestinationFolder,folder))
        filess = [file for file in os.listdir(os.path.join(SourceFolder,folder)) if (os.path.splitext(file)[1] == ".md" and os.path.splitext(file)[0] != "index")]
        for file in filess:
            print("starting conversion: " + file + " to pdf...")
            command = ['pandoc',"--variable","fontsize=14pt","--variable","documentclass=extarticle",os.path.join(SourceFolder,folder,file),'--latex-engine=xelatex','--template=./assets/me.latex','--highlight-style=pygments','-o',os.path.join(DestinationFolder,folder,replaceMdByPdf(file))]
            subprocess.run(command)
            print("conversion completed: " + file + " to pdf...")

    # ***combine pdfs
    #outer
    files = [file for file in os.listdir(DestinationFolder) if (os.path.splitext(file)[1] == ".pdf") ]

    if not files:
        merger = PyPDF2.PdfFileMerger()

        for filename in files:
            print("combining " + filename)
            merger.append(PyPDF2.PdfFileReader(open(os.path.join(DestinationFolder,filename),'rb')))
            print("combined " + filename)

        merger.write(os.path.join(DestinationFolder,"notes.pdf"))
    #inner
    folders = [folder for folder in os.listdir(DestinationFolder) if (os.path.isdir(os.path.join(SourceFolder,folder)) and folder != "assets")]

    for folder in folders:
        files = [file for file in os.listdir(os.path.join(DestinationFolder,folder)) if(os.path.splitext(file)[1] == ".pdf")]
        merger = PyPDF2.PdfFileMerger()
        for filename in files:
            print("combining " + filename)
            merger.append(PyPDF2.PdfFileReader(open(os.path.join(DestinationFolder,folder,filename),'rb')))
            print("combined " + filename)
        merger.write(os.path.join(DestinationFolder,folder,sanitizeFoldername(folder) + ".pdf"))

    print("=======PDfs generated========")




def buildwebsite():
    # get topics
    print("getting topics...")
    global folder_list
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



    # build pdfs
    batchPdfConversion(os.path.join(os.getcwd(),"source"),os.path.join(os.getcwd(),"assets","print"))

    # todo 1. integrate pdf,epub,doc,beamer,html, rtf etc. 2. any notes versions






# MAIN PROGRAM

if __name__ == "__main__":

    try:
        arg = sys.argv[1]
    except Exception as e:
        print("\nenter at least one argument. Program terminating...\n")
        sys.exit()


    if arg == "buildwebsite":
        print("building website...")
        buildwebsite()
    else:
        print("\n Wrong arguments. Enter one of the following arguments:")
        print("\n" + str(possible_args) + "\n")













