from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages


def index(request):
    context = { 'user': User.objects.all() }
    return render(request, 'belt/index.html', context)


def regist(request):
    #postData: user's postinfo
    postData = {
        'name' : request.POST['name'],
        'username' : request.POST['username'],
        'password' : request.POST['password'],
        'password_confirm' : request.POST['password_confirm']
    }
    #to chekc errors and user info and use sessions 
    errors = User.objects.basic_validator(postData)
    if len(errors) ==0:

        request.session['id'] = User.objects.filter(username=postData['username'])[0].id
        request.session['name'] = postData['name']
        return redirect('/success')
    else: 
        for errors in errors:
            messages.info(request, errors) 
        return redirect ('/')


def login(request):
    print "inside login"
    postData = {
    'username' : request.POST['username'],
    'password' : request.POST['password']
    
    }
    #error handler checks user input
    errors = User.objects.login(postData)
    print errors
    #if theres no errors
    if len(errors) == 0:
        print "success"
        request.session['id'] = User.objects.filter(username=postData['username'])[0].id
        request.session['name'] = User.objects.filter(username=postData['username'])[0].name
        return redirect('/travel')
    for errors in errors:
        messages.info(request, errors)
    return redirect('/')

def success(request):
    context = {}
    try:
        request.session['id']
    except KeyError:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    #join = manay to many relationship=== what you joined or what you like 
    #travel_info =other's people list
    context = {
        'user': User.objects.all(),
        'travel_info': Travel.objects.exclude(join =user ),
        'join': user.join_travel.all()
    }
    return render(request, 'belt/travel.html', context)


def logout(request):
    #delte id
    del request.session['id']
    del request.session['name']
    return redirect('/')

def add(request):
#check to see validation 
   

    date_from = request.POST['date_from'],
    date_to = request.POST['date_to'],        
    destination = request.POST['destination'],
    description = request.POST['description']
    
    

    errors = Travel.objects.t_validator(request.POST)
    if errors:
        #always gonna go to this route, rework logic to see if it's an empty list
        for err in result:
            messages.error(request, err, extra_tags=addQuote)
        return redirect('/travel')
    messages.success(request, "Successfully added!")
 #checking current user's id    
    user = User.objects.get(id = request.session['id'])
    #new_q = Quotes.objects.filter(author=author,quotes=quotes)[0]
    Travel.objects.create(destination=destination, description=description, date_from=date_from, date_to=date_to) 
    
    return redirect("/travel")

def join(request, id):
    travel = Travel.objects.get(id=id)
    user = User.objects.get(id=request.session['id'])
    #adding fav list in your list 
    travel.join.add(user)

    return redirect('/travel')


def dest(request, id):
    context = {}
#show user's profile    
    user_now = User.objects.get(id = id)
    #favorite q--- many to many relationship/ fk 
    travel = Travel.objects.filter(id = id)
    context = {
        'quote_q' : travel, 
        'user' : user_now
    }
    # to check how many q 
    return render(request, 'belt/edit.html', context) 

def add_plan(request):
    #to carry over user's session? 
    user = User.objects.get(id = request.session['id'])
    return render(request, 'belt/add.html') 