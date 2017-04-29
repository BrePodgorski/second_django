from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote, Favorite

#THIS IS YOUR NEW EXAM
def index(request):
    return render(request, 'great_project/index.html')

def register(request):
    data={
    'name':request.POST['name'],
    'alias':request.POST['alias'],
    'email':request.POST['email'],
    'password':request.POST['password'],
    'conf_password':request.POST['conf_password'],
    'birthday': request.POST['birthday'],
    }
    new_user=User.objects.register(data)
    print new_user
    if new_user['errors']:
        for error in new_user['errors']:
            messages.add_message(request, messages.ERROR,error)
        return redirect('/')
    else:
            request.session['user']=new_user['user'].id
            return redirect('/quotes',data)
    return render(request, 'great_project/quotes.html', data)

def login(request):
    data={
    'email':request.POST['email'],
    'password':request.POST['password']
    }
    found_user=User.objects.login(data)
    if found_user['errors']==None:
        request.session['user']=found_user['user'].id
        return redirect('/quotes',data)
    else:
        for error in found_user['errors']:
            messages.add_message(request, messages.ERROR,error)
        return redirect('/')
    return redirect('/quotes',data)

def logout_view(request):
    request.session.clear()
    return redirect('/')

def quotes(request):
    if 'user' not in request.session:
        messages.add_message(request,messages.ERROR, 'You must be logged in to view that page')
        return redirect('/')
    current_user=User.objects.get(id=request.session['user'])
    all_quotes=Quote.objects.all()
    print all_quotes
    my_fav_list=[]
    quotable_quotes_list=[]
    # my_quote_list=[]
    for my_quote in all_quotes:
        my_quote.favorite=True
    try:
        Favorite.objects.get(user=current_user, quote=my_quote)
        my_fav_list.append(my_quote)
        Favorite.objects.filter(user=current_user)
        # my_fav_list.append(this_quote)
    except:
        my_quote.favorite=False
        quotable_quotes_list.append(my_quote)
        Favorite.objects.exclude(user=current_user)

    data={
        'current_user': current_user,
        'my_faves':  my_fav_list,
        'quotable_quotes': quotable_quotes_list
        # 'my_quotes':Quote.objects.filter(creator=current_user)
    }

    return render(request, 'great_project/quotes.html',data)

def process_quotes(request):
    # quotable_quotes_list=[]
    current_user=User.objects.get(id=request.session['user'])
    data={
        'quoted_by':request.POST['quoted_by'],
        'content':request.POST['content'],
        'creator':current_user,
    }
    my_quote=Quote.objects.process_quotes(data)
    print my_quote

    if my_quote['errors']==None:
        # quotable_quotes_list.append(my_quote)
        # print my_quote
        return redirect('/quotes',data)
    else:
        for error in my_quote['errors']:
            messages.add_message(request, messages.ERROR,error)
        return redirect('/quotes')
    # return redirect('/quotes')

def add_to_fav(request, my_quote_id):
    a_quote=Quote.objects.get(id=my_quote_id)
    a_user=User.objects.get(id=request.session['user'])
    Favorite.objects.create(user=a_user, quote=a_quote)

    return redirect ('/quotes')

def remove_from_fav(request, my_quote_id):
    bad_quote=Quote.objects.get(id=my_quote_id)
    bad_user=User.objects.get(id=request.session['user'])
    Favorite.objects.get(user=bad_user, quote=bad_quote).delete()
    # bad_quote.favorite=False
    return redirect('/quotes')

def user(request, a_user_id):
    if 'user' not in request.session:
        messages.add_message(request,messages.ERROR, 'You must be logged in to view that page')
        return redirect('/')
    the_user=User.objects.get(id=a_user_id)
    print the_user.name
    their_quotes=Quote.objects.filter(creator=the_user)
    their_quotes.num_posted=Quote.objects.filter(creator=the_user).count()
    print their_quotes
    data={
        'the_user':the_user,
        'their_quotes':their_quotes,
        'their_quotes.num_posted':their_quotes.num_posted
    }
    return render(request, 'great_project/user.html',data)
