from django.shortcuts import render , redirect
from .models import *
from django.http import Http404
from .forms import  inputQueryForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from skmerCore import scripts



# Create your views here.



@login_required(login_url="skmerHome")
def viewQueries(request, skmerUserId):
    try:
        user = skmerUser.objects.get(pk = skmerUserId)
    except skmerUser.DoesNotExist:
        raise Http404("User does not exist")

    if str(request.user.pk) != str(skmerUserId):
        return redirect('skmerHome')

    queriesOfUser = inputQueryFile.objects.filter(createUser=request.user)
    analysesOfUser =[]
    for q in queriesOfUser:
        analysis = analysisFile.objects.get(createInputFile = q)
        analysesOfUser.append(analysis)


    if request.method == 'POST':
        form = inputQueryForm(request.POST, request.FILES)
        files = request.FILES.getlist('fastQ')
        if form.is_valid():
            inputFileInstance  = [inputQueryFile() for i in range(len(files))]
            outputfile  = [analysisFile() for i in range(len(files))]
            for index,f in enumerate(files):
                print(f)
                inputFileInstance[index].collectionName = form.cleaned_data['collectionName']
                if form.cleaned_data['collectionName'] == "":
                    inputFileInstance[index].collectionName = "Unnamed Collection"

                inputFileInstance[index].fileExtension = f.name.split('.')[-1]
                inputFileInstance[index].fastQ = f
                inputFileInstance[index].biologicalName = f.name.split('/')[-1].split('.')[0]
                inputFileInstance[index].createUser = request.user
                inputFileInstance[index].save()

                #To do hardcoded change later
                filepaths = scripts.runqueryscript(inputFileInstance[index], "reflib", False)
                outputfile[index].createUser = inputFileInstance[index].createUser
                outputfile[index].distanceEdit = filepaths[0]
                outputfile[index].distanceJukesCantor = filepaths[1]
                outputfile[index].createInputFile = inputFileInstance[index]
                outputfile[index].save()

            messages.success(request, "Files uploaded Successfully")
            return redirect('queryView', skmerUserId=request.user.pk)
    else:
        form = inputQueryForm()


    context = { 'usersFiles' : zip(queriesOfUser,analysesOfUser),
                'filecount' : len(queriesOfUser),
                'form' : form}
    return render(request, 'query/viewQueries.html', context)

@login_required(login_url="skmerHome")
def deleteQuery(request,skmerUserId, queryId):
    try:
        user = skmerUser.objects.get(pk = skmerUserId)
    except skmerUser.DoesNotExist:
        raise Http404("User does not exist")

    if str(request.user.pk) != str(skmerUserId):
        return redirect('skmerHome')

    inputQueryFile.objects.filter(pk=queryId).delete()
    return redirect('queryView', skmerUserId=request.user.pk)


def getQueryDistancesFromFile(queryId):
    try:
        analysisInstance = analysisFile.objects.filter(createInputFile = queryId)[:1].get()
        editDistancecontent = open(analysisInstance.distanceEdit.path , "r").read().strip().split('\n')
        jukesCantorDistancecontent = open(analysisInstance.distanceJukesCantor.path,"r").read().strip().split('\n')
        editDistances = list()
        jukesCantorDistances= list()
        reflist = list()

        for i in range(0,len(editDistancecontent)):
            reflist.append(editDistancecontent[i].split('\t')[0])
            editDistances.append(editDistancecontent[i].split('\t')[1])
            jukesCantorDistances.append(jukesCantorDistancecontent[i].split('\t')[1])


        return zip(reflist , editDistances , jukesCantorDistances)
    except ObjectDoesNotExist:
        return None



@login_required(login_url="skmerHome")
def viewDistance(request , skmerUserId, queryId):
    try:
        user = skmerUser.objects.get(pk = skmerUserId)
        query = inputQueryFile.objects.get(pk = queryId)
        analysis = analysisFile.objects.get(createInputFile = queryId)
    except skmerUser.DoesNotExist:
        raise Http404("User does not exist")

    if str(request.user.pk) != str(skmerUserId):
        return redirect('skmerHome')

    context = { 'distancetable' : getQueryDistancesFromFile(queryId),
                'query' : query,
                'analysis': analysis}

    return render(request, 'query/viewDistance.html', context)



