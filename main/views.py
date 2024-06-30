from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Assigned_Role,Problem
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Problem, Assigned_Role,Role
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        print(user)
        if user:
            auth_login(request, user)
            try:
                assigned_role = Assigned_Role.objects.get(user=user)
                role = assigned_role.role.name
                request.session['role'] = role
                request.session['name'] = assigned_role.name
                if role == 'Manager':
                    return redirect('DashBoard')
                elif role == 'Hint_Writter':
                    return redirect('DashBoard')
                elif role == 'Hint_Reviewer':
                    return redirect('DashBoard')
            except Assigned_Role.DoesNotExist:
                return render(request, 'login.html', {'error': 'Assigned role not found'})

        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='login')
def DashBoard(request):
    role = request.session.get('role')

    if not role:
        return redirect('login')
    
    if role == 'Manager':
        problemsR = Problem.objects.filter(reviewed=True)
        problemsPH = Problem.objects.filter(Q(small_hint=None) | Q(small_hint=''))
        problemsPR = Problem.objects.filter(reviewed=False).exclude(small_hint='')
        return render(request, 'DashBoard.html', {
            'problemsR': problemsR,
            'problemsPH': problemsPH,
            'problemsPR': problemsPR,
        })
    
    elif role == 'Hint_Writter':
        problemsPH = Problem.objects.filter(small_hint='')
        return render(request, 'DashBoard.html', {'problemsPH': problemsPH})
    
    elif role == 'Hint_Reviewer':
        problemsPR = Problem.objects.filter(reviewed=False).exclude(small_hint='')
        return render(request, 'DashBoard.html', {'problemsPR': problemsPR})
    
    else:
        return redirect('login')

@login_required(login_url='login')
def AddQuestion(request):
    Hrole = Role.objects.get(name='Hint_Writter')
    Rrole = Role.objects.get(name='Hint_Reviewer')
    
    if request.method == 'POST':
        day = request.POST.get('day')
        problem_name = request.POST.get('problem_name')
        problem_link = request.POST.get('problem_link')
        difficulty = request.POST.get('difficulty')
        topic = request.POST.get('topic')
        subtopic = request.POST.get('subtopic')
        final_youtube_link = request.POST.get('final_youtube_link')
        record_by = request.POST.get('record_by')
        hint_writer_id = request.POST.get('hint_writer')
        deadline = request.POST.get('deadline')
        reviewer_id = request.POST.get('reviewer')
        reviewed = request.POST.get('reviewed')
        reviewer_deadline = request.POST.get('reviewer_deadline')
        # Hid = Assigned_Role.objects.get(id=hint_writer_id)
        # Rid = Assigned_Role.objects.get(id=reviewer_id)
        
        # Create a new Problem object
        new_problem = Problem.objects.create(
            day=day,
            problem_name=problem_name,
            problem_link=problem_link,
            difficulty=difficulty,
            topic=topic,
            subtopic=subtopic,
            final_youtube_link=final_youtube_link,
            record_by=record_by,
            hint_writer_id=hint_writer_id,
            deadline=deadline,
            reviewer_id=reviewer_id,
            reviewer_deadline=reviewer_deadline,
            
        )

        return redirect('DashBoard')

    hint_writers = Assigned_Role.objects.filter(role=Hrole)
    reviewers = Assigned_Role.objects.filter(role=Rrole)

    return render(request, 'AddQuestion.html', {'hint_writers': hint_writers, 'reviewers': reviewers})

@login_required(login_url='login')
def EditQuestion(request, Pid):
    problem = get_object_or_404(Problem, id=Pid)
    assigned_roles = Assigned_Role.objects.all()
    
    if request.method == 'POST':
        problem.day = request.POST['day']
        problem.problem_name = request.POST['problem_name']
        problem.problem_link = request.POST['problem_link']
        problem.difficulty = request.POST['difficulty']
        problem.topic = request.POST['topic']
        problem.subtopic = request.POST['subtopic']
        problem.final_youtube_link = request.POST.get('final_youtube_link', None)
        problem.record_by = request.POST['record_by']
        problem.hint_writer = get_object_or_404(Assigned_Role, id=request.POST['hint_writer'])
        problem.deadline = request.POST['deadline']
        problem.small_hint = request.POST['small_hint']
        problem.big_hint = request.POST['big_hint']
        
        if request.session['role'] in ['Hint_Reviewer', 'Manager']:
            problem.reviewer = get_object_or_404(Assigned_Role, id=request.POST['reviewer'])
            problem.reviewed = 'reviewed' in request.POST
            problem.reviewer_deadline = request.POST['reviewer_deadline']
            problem.remark_for_small_hint = request.POST['remark_for_small_hint']
            problem.remark_for_big_hint = request.POST['remark_for_big_hint']
        
        problem.save()
        return redirect('DashBoard')  
    
    return render(request, 'EditQuestion.html', {
        'problem': problem,
        'assigned_roles': assigned_roles
    })




