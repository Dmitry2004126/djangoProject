from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from Footballer.models import Seller, Project, Buyer, Side
from Footballer.forms import GameForm, UserForm
from django.contrib.auth.models import Group


def show_info(request):
    user = request.user
    if user.is_authenticated and request.user.username != "admin":
        if user.groups.filter(name="buyer").exists():
            buyer = Buyer.objects.get(id_user_id=user.id)
            projects = Project.objects.filter(buyer=Buyer.objects.get(id=buyer.id))
            return render(request, 'refereeViewFootballers.html', {"projects": projects, "buyer": buyer, "user": user})
        else:
            seller = Seller.objects.get(id_user_id=user.id)
            projects = Project.objects.filter(seller=seller.id)
            projects = list(projects)
            return render(request, 'footballerInfo.html', {"seller": seller, "projects": projects, "request": 0})
    else:
        return render(request, 'notAccess.html')


def show_footballer(request, id_user):
    user = request.user
    if user.is_authenticated and user.groups.filter(name="buyer").exists():

        seller = Seller.objects.get(id_user_id=id_user)
        projects = Project.objects.filter(seller=seller.id)
        projects = list(projects)
        return render(request, 'footballerInfo.html', {"seller": seller, "projects": projects, "request": 1})
    else:
        return render(request, 'notAccess.html')

def main_page(request):
    if request.user.username == "admin":
        return render(request, 'main.html')
    if request.user.is_authenticated:
        return redirect("/info")
    return render(request, 'main.html')

def show_index(request):
    if request.method == "GET":
        cur_user = request.user
        if cur_user.is_authenticated:
            return redirect("/info")
        else:
            userform = UserForm()
            return render(request, 'index.html', {"form": userform})
    else:
        if request.POST.get("email") is not None:
            email = request.POST.get("email")
            password = request.POST.get("password")

            try:
                username = User.objects.get(email=email).username
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect("/info")
            except Exception:
                print("NOT CORRECT EMAIL OR PASSWORD")
                return redirect("/")
        else:
            return redirect("/index/sign")


def signup(request):
    if request.method == "GET":
        userForm = UserForm()
        return render(request, 'sign.html', {"form": userForm})
    else:
        userForm = UserForm(request.POST)
        user = User.objects.create_user(email=request.POST.get("create_email"),
                                        username=request.POST.get("create_user_name"),
                                        password=request.POST.get("create_password"))

        if userForm.is_valid():
            print(userForm.data['side'])
            if userForm.data['side'] == "1":
                my_group = Group.objects.get(name='seller')
                obj = Seller()
                obj.first_name = request.POST.get("create_first_name")
                obj.last_name = request.POST.get("create_last_name")
                obj.date_birth = request.POST.get("create_date")
                obj.side = Side.objects.get(id=userForm.data['side'])
                obj.id_user_id = user.id
                obj.save()
                my_group.user_set.add(user)
            else:
                '''from django.contrib.auth.models import Group
my_group = Group.objects.get(name='my_group_name') 
my_group.user_set.add(your_user)'''
                my_group = Group.objects.get(name='buyer')
                obj = Buyer()
                obj.first_name = request.POST.get("create_first_name")
                obj.last_name = request.POST.get("create_last_name")
                obj.id_user_id = user.id

                obj.save()
                my_group.user_set.add(user)
        login(request, user)
    return redirect("/info")


def create_game(request, id_user):
    if request.method == "GET":
        gameForm = GameForm()
        return render(request, "templateForm.html", {"form": gameForm,  "id_footballer": Seller.objects.get(id_user=id_user).id})
    else:
        gameForm = GameForm(request.POST)
        if gameForm.is_valid():
            obj = Project()
            obj.number = gameForm.cleaned_data['number']
            obj.seller = Seller.objects.get(id_user_id=id_user)
            obj.buyer = Buyer.objects.get(id_user_id=request.user.id)
            obj.date_start = gameForm.cleaned_data['date_start']
            obj.project_name = gameForm.cleaned_data['project_name']
            obj.save()
            '''
            obj = Game.objects.create(
                footballer_id=Footballer.objects.get(id_user_id=id_user).id,
                division_id=Division.objects.get(name_division=name_division).referee,
                number=gameForm.cleaned_data['number'],
                goals=gameForm.cleaned_data['goals'])
            '''
            return redirect(f"/showfootballer/{id_user}")
        else:
            print("ups")
            return redirect("/")


def delete_game(request, id_user, number_game):
    footballer_id = Seller.objects.get(id_user_id=id_user).id
    Project.objects.filter(number=number_game, seller__id_user=id_user).first().delete()
    return redirect(f"/showfootballer/{id_user}")


'''def show_club_ofDivision(request, name_division):

    clubs = division.clubs.filter(division=division.name_division)
    footballersSumGoals = []
    clubsSumPeople = []
    for club in clubs:
        footballers = Footballer.objects.filter(club=Club.objects.get(id=club.id))
        sumGoals = 0
        numberplayers = 0
        for footballer in footballers:
            footballerGames = Game.objects.filter(footballer_id=footballer.id)
            sumGoals += sum(map(lambda x: x.goals, footballerGames))
            numberplayers += 1
        footballersSumGoals.append(sumGoals)
        clubsSumPeople.append(numberplayers)
    clubs = zip(clubs, footballersSumGoals, clubsSumPeople)

    return render(request, 'refereeViewClubs.html', {"clubs": clubs, "name_division": name_division})

'''
'''def show_footballerFromGroup(request, id_club, name_division):
    footballers = Footballer.objects.filter(club=Club.objects.get(id=id_club))
    footballersSumGames = []
    footballersLastGames = []
    for footballer in footballers:
        footballerGames = Game.objects.filter(footballer_id=footballer.id)
        sumGoals = sum(map(lambda x: x.goals, footballerGames))
        footballersSumGames.append(sumGoals)
        footballersLastGames.append(max(map(lambda x: x.number, footballerGames), default=0))
    footballers = zip(footballers, footballersSumGames, footballersLastGames)
    return render(request, 'refereeViewFootballers.html',
                  {"footballers": footballers, "name_division": name_division, "id_club": id_club})
'''

''' super user admin: username - admin, email - test@test.ru, password - admin;
footballer testdjango  test2@test.ru
referee testdjango2  test@test.ru
footballer2 test3@test.ru testdjango3

footballerinfo <!-- <a href="{% url 'create_game' name_division id_club footballer.id_user_id %}" type="button" class="btn btn-primary">Add Game</a>-->
49  <a href="{% url 'delete_game' name_division id_club footballer.id_user_id game.number %}" type="button" class="btn btn-danger">Delete</a>
'''

'''
    else :
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.footballer = Footballer.objects.get(id_user_id=id_user)
            game.Referee = Referee.objects.get(id_user_id=request.user.id)
            game.save()
            return redirect(f"/showfootballer/{id_user}")
        else:
            print("ups")
            pass
        '''


# Create your views here.

# AJAX Views


def validate_username(request):
    username = request.GET.get('create_user_name', None)
    response = {
        'taken': User.objects.filter(username__exact=username).exists()
    }
    return JsonResponse(response)


def check_numberGame(request, id_seller):
    number = int(request.GET.get('number', None))
    print(number)
    if(number == ""):
        number = 0
    print(Project.objects.filter(number=number, seller__id_user=id_seller).exists())
    response = {
        'exist': Project.objects.filter(number=number, seller_id=id_seller).exists()
    }
    return JsonResponse(response)

