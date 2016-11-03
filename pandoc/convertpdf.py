import os
import subprocess
import shutil
import PyPDF2


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



def replaceMdByPdf(file):
    return (os.path.splitext(file)[0] + ".pdf")



# pandoc --variable fontsize=12pt MANUAL.txt --latex-engine=xelatex -o example13.pdf

def batchPdfConversion(SourceFolder,DestinationFolder):
    files = [file for file in os.listdir(SourceFolder) if (os.path.splitext(file)[1] == ".md" and os.path.splitext(file)[0] != "index")]

    if os.path.exists(DestinationFolder):
        shutil.rmtree(DestinationFolder)

    os.makedirs(DestinationFolder)

    for file in files:
        print("starting conversion: " + file + " to pdf...")
        command = ['pandoc',"--variable","fontsize=16pt",os.path.join(SourceFolder,file),'--latex-engine=xelatex','--template=me.latex','-o',os.path.join(DestinationFolder,replaceMdByPdf(file))]
        subprocess.run(command)
        print("conversion completed: " + file + " to pdf...")



# program starts here
batchPdfConversion(os.getcwd(),os.path.join(os.getcwd(),"pdfs"))

combinePdfs(os.path.join(os.getcwd(),"pdfs"),os.path.join(os.getcwd(),"assets"))