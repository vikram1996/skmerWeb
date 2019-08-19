from django.conf import settings
import os


def runqueryscript(inputquery,reflib,add=False):
    fastQ = inputquery.fastQ
    querypath = settings.MEDIA_ROOT +"/"+ fastQ.name
    reflibpath = settings.BASE_DIR+"/skmerCore/"+reflib
    reflibjcpath = settings.BASE_DIR+"/skmerCore/"+reflib+"_phylo"
    outputprefix = settings.MEDIA_ROOT +"/"+str(inputquery.createUser.pk)+"/"+os.path.dirname(fastQ.name)
    outputprefixjc = settings.MEDIA_ROOT +"/"+str(inputquery.createUser.pk)+"/jc"+os.path.dirname(fastQ.name)

    qstring = "skmer query "+ querypath+" " + reflibpath + " -o " + outputprefix
    qstringjc = "skmer query "+ querypath+" " + reflibjcpath + " -o " + outputprefixjc+ " -t"
    os.system(qstring)

    if add == True:
        qstring= qstring+" -a"
        qstringjc = qstringjc + " -a"


    os.system(qstring)
    os.system(qstringjc)


    return([str(inputquery.createUser.pk)+"/"+os.path.dirname(fastQ.name)+"-"+fastQ.name.split('/')[1].split('.')[0].lower()+".txt" ,
    str(inputquery.createUser.pk)+"/jc"+os.path.dirname(fastQ.name)+"-"+fastQ.name.split('/')[1].split('.')[0].lower()+".txt" ])







