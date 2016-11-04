import os
import subprocess
import shutil
import PyPDF2

def sanitizeFoldername(name):
    temp = name[3:]
    temp = temp.replace("_"," ")
    temp = temp.capitalize()
    return temp

def replaceMdByPdf(file):
    return (os.path.splitext(file)[0] + ".pdf")



# pandoc --variable fontsize=12pt MANUAL.txt --latex-engine=xelatex -o example13.pdf

def batchPdfConversion(SourceFolder,DestinationFolder):

    # ***create pdfs
    files = [file for file in os.listdir(SourceFolder) if (os.path.splitext(file)[1] == ".md" and os.path.splitext(file)[0] != "index")]

    folders = [folder for folder in os.listdir(SourceFolder) if (os.path.isdir(os.path.join(SourceFolder,folder)) and folder != "assets")]

    if os.path.exists(DestinationFolder):
        shutil.rmtree(DestinationFolder)

    os.makedirs(DestinationFolder)

    #outer
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



# program starts here
batchPdfConversion(os.getcwd(),os.path.join(os.getcwd(),"assets","pdfs"))
