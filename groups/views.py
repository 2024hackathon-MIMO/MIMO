from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import Group, Membership
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.db.models import Count
from django.utils import timezone

# 내 그룹보기
@login_required
def my_groups(request):
    profile = Profile.objects.get(user=request.user)
    memberships = Membership.objects.filter(profile=profile)
    groups = [membership.group for membership in memberships]
    return render(request, 'groups/my_groups.html', {'groups': groups})

# 전체 그룹 리스트
def group_list(request):
    groups = Group.objects.all()

    # 정렬기능 추가
    sort_by = request.GET.get('sort_by', 'created_at')

    if sort_by == '최신순':
        groups = Group.objects.all().order_by('created_at')  # 최신순
    elif sort_by == '오래된순':
        groups = Group.objects.all().order_by('-created_at')  # 오래된순
    elif sort_by == '다인원순':
        groups = Group.objects.all().order_by('-max_members')  # 다인원순
    elif sort_by == '소인원순':
        groups = Group.objects.all().order_by('max_members')  # 소인원순
    else:
        groups = Group.objects.all()  # 기본값으로 아순 정렬도 하지 않음

    return render(request, 'groups/group_list.html', {
        
        'groups': groups,
        'sort_by' : sort_by,
        })

# 그룹 상세보기 >> 여기서 가입하면 mygroup에 추가됨
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    user = Profile.objects.get(user=request.user)
    is_member = False

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        is_member = group.memberships.filter(id=profile.id).exists()

    members = group.memberships.all()
    member_usernames = [membership.profile.user.username for membership in members]

    context = {
        'group':group,
        'is_member':is_member,
        'author':group.author.username,
        'created_at':group.created_at.strftime('%Y.%m.%d'),
        'member_usernames':member_usernames,
    }
    return render(request, 'groups/group_detail.html', context)

# 그룹 가입하기
@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id = group_id)
    profile = get_object_or_404(Profile, user = request.user)
    if group.memberships.count() < group.max_members:
        Membership.objects.get_or_create(profile=profile, group=group)
    return redirect('groups:my_groups')

# 그룹 만들기
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid(): 
            group = form.save(commit=False)
            group.author = request.user
            group.save()
            return redirect('groups:group_list')
    else:
        form = GroupForm()
    now = timezone.localtime(timezone.now())
    context = {
        'form': form,
        'current_time': now.strftime('%Y.%m.%d'),  # 현재 시간 표시
        'author': request.user.username,  # 현재 사용자 이름 표시
    }
    return render(request, 'groups/group_create.html', context)

#검색 기능 뷰 추가
@login_required
def search(request):
    search = request.GET.get('search','')
    groups = Group.objects.filter(name__icontains=search) if search else []
    return render(request, 'groups/search_list.html', {
        'groups' : groups,
        'search' : search
    })

# 나의 그룹 >> 그룹디테일
def mygroup_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    user = Profile.objects.get(user=request.user)
    is_member = False

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        is_member = group.memberships.filter(id=profile.id).exists()

    members = group.memberships.all()
    member_usernames = [membership.profile.user.username for membership in members]

    context = {
        'group':group,
        'is_member':is_member,
        'author':group.author.username,
        'created_at':group.created_at.strftime('%Y.%m.%d'),
        'member_usernames':member_usernames,
    }
    return render(request, 'groups/my_group_detail.html', context)
