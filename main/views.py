from datetime import datetime, timedelta
from django.utils.dateformat import DateFormat
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *
from .models import *
from .serializers import openTimeSerializer
from django.http import *
from django.urls import reverse

# 열람시간 설정 api
@api_view(['POST'])
def set_open_time(request):
    user = request.user
    serializer = openTimeSerializer(data = request.data)
    if serializer.is_valid():
        open_time, created = openTime.objects.get_or_create(user=user)
        open_time.morning_time = serializer.validated_data['morning_time']
        open_time.night_time = serializer.validated_data['night_time']
        open_time.save()
        return Response({'message': 'Open time set successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 열람시간 수정
def modify_time(request):
    user = request.user
    open_time, created = openTime.objects.get_or_create(user=user, defaults={'morning_time': '05:00:00', 'night_time': '21:00:00'})
    if request.method == 'POST':
        form = OpenTimeForm(request.POST, instance=open_time)
        if form.is_valid():
            form.save()
            return redirect('main:main')
    else:
        form = OpenTimeForm(instance=open_time)
    return render(request, 'main/modify_time.html', {'form': form})

# 메인화면을 렌더링 + 현재시간 띄우기 + 열람시간 띄우기 + 낮인지 밤인지 열람시간에 따라 메세지 확인 할 수 있는 지에 따라 템플릿에 다르게 표시하기
def main(request):
    user = request.user
    open_time = openTime.objects.filter(user=user).first()
    now = timezone.localtime(timezone.now())
    current_time = now.time()

    if open_time:
        morning_time = open_time.morning_time
        night_time = open_time.night_time
    else:
        morning_time = datetime.strptime('05:00:00', '%H:%M:%S').time()
        night_time = datetime.strptime('21:00:00', '%H:%M:%S').time()

    # 디버깅을 위해 시간 출력
    #print(f"현재 시간: {current_time}, 모닝 시간: {morning_time}, 나잇 시간: {night_time}")

    today = timezone.now().date()
    user_profile, created = Profile.objects.get_or_create(user=user)
    user_message = Message.objects.filter(nick=user_profile, created_at__date=today).first()
    user_has_written_message = Message.objects.filter(nick=user_profile, created_at__date=today).exists()

    # 오늘 작성된 메시지들
    messages = Message.objects.filter(created_at__date=today).order_by('created_at')
    #print(messages)

    # 메시지를 작성한 사용자들
    users_with_messages = [message.nick.user for message in messages]

    # 사용자 수
    user_count = len(users_with_messages)

    # 현재 사용자 위치
    if user in users_with_messages:
        current_user_index = users_with_messages.index(user)
        next_user_index = (current_user_index + 1) % user_count

        next_user_message = messages[next_user_index]
        
    else:
        next_user_message = None
    #print(next_user_message)

    context = {
        'morning_time': morning_time,
        'night_time': night_time,
        'current_time': now.strftime('%m월 %d일'),  # 현재시간 표기
        'can_open_message': False,  # 메세지 열람가능 여부
        'user_has_written_message': user_has_written_message,
        'user_message': user_message,
        'messages': messages,
        'next_user_message': next_user_message,
        'user_count': user_count,
    }

    # 아침 시간대(5시~12시)
    if datetime.strptime('05:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('12:00:00', '%H:%M:%S').time():
        # 모닝(만약 9시로 지정했으면)
        if morning_time <= current_time <= (datetime.combine(now.date(), morning_time) + timedelta(hours=1)).time():
            if user_has_written_message:
                context['time_message'] = "아래의 카드를 확인하고 활기찬 아침을 시작해봐요."
            else:
                context['time_message'] = "오늘의 메시지를 등록하고 따뜻한 한 마디를 주고 받아보세요."
        # 모닝전(5시부터 9시 전까지는 이 문구가 뜨는 것)
        else:
            context['time_message'] = f"따뜻한 아침을 준비중이에요. 우리가 약속한 {morning_time.strftime('%I:%M %p')}에 만나요."
    # 밤 시간대(21시~0시~4시 59분 59초)
    elif (datetime.strptime('21:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('04:59:59', '%H:%M:%S').time()):
        # 나잇
        if night_time <= current_time <= (datetime.combine(now.date(), night_time) + timedelta(hours=1)).time():
            if user_has_written_message:
                context['time_message'] = "아래의 카드 하나를 선택해 따뜻한 한마디로 좋은 밤을 시작해봐요."
            else:
                context['time_message'] = "오늘의 메시지를 등록하고 따뜻한 한 마디를 주고 받아보세요."
        # 현재시간이 9시 이후라 else에도 해당하지않는데 elif에는 해당하나 if night_time~에 해당하지않는 경우
        elif current_time < night_time:
            if user_has_written_message:
                context['time_message'] = f"잠들기전, 우리가 약속한 {night_time.strftime('%I:%M %p')}에 만나요."
            else:
                context['time_message'] = "오늘의 메시지를 등록하고 따뜻한 한 마디를 주고 받아보세요."
    # 모닝 후, 나잇 전 (오전 12시(정오)부터 저녁 9시(21시))
    else:
        context['time_message'] = f"잠들기전, 우리가 약속한 {night_time.strftime('%I:%M %p')}에 만나요."

    # 선택적 열람을 위해
    if open_time:
        # 현재 시간 = 지정한 모닝메세지 열람시간 ~ 1h
        if morning_time <= current_time <= (datetime.combine(now.date(), morning_time) + timedelta(hours=1)).time():
            context['can_open_messages'] = True
            if not Notification.objects.filter(user=user, message="모닝메세지를 열람할 수 있습니다.").exists():
                Notification.objects.create(user=user, message="모닝메세지를 열람할 수 있습니다.")
        # 현재시간 = 지정한 나잇메세지 열람시간 ~ + 1h
        elif night_time <= current_time <= (datetime.combine(now.date(), night_time) + timedelta(hours=1)).time():
            context['can_open_messages'] = True
            if not Notification.objects.filter(user=user, message="나잇메세지를 열람할 수 있습니다.").exists():
                Notification.objects.create(user=user, message="나잇메세지를 열람할 수 있습니다.")

    return render(request, 'main/main.html', context)

# 메시지 열람하기 >> 모닝 나잇 따로 분류해야할 듯
def message_list(request):
    user_profile = Profile.objects.get(user=request.user)
    user_groups = Group.objects.filter(memberships__profile=user_profile)

    today = timezone.now().date()
    messages = Message.objects.filter(created_at__date=today).filter(
        models.Q(group__in=user_groups) | models.Q(group__isnull=True)
    ).order_by('created_at')

    # 나잇/모닝 열람시간에 맞는 메세지 조회
    open_time = openTime.objects.filter(user=request.user).first()
    if open_time:
        morning_time = open_time.morning_time
        night_time = open_time.night_time
    else:
        morning_time = datetime.strptime('06:00:00', '%H:%M:%S').time()
        night_time = datetime.strptime('23:00:00', '%H:%M:%S').time()

    now = timezone.localtime(timezone.now())
    current_time = now.time()

    # 시간대 결정
    time_period = get_time_period(current_time, morning_time, night_time)

    if time_period == 'night':
        messages = messages.filter(night_mes__isnull=False)
    elif time_period == 'morning':
        messages = messages.filter(morning_mes__isnull=False)
    else:
        messages = messages.none()  # 현재 시간대에 해당하는 메시지가 없을 때

    user_message = messages.filter(nick=user_profile).first()
    next_user_message = None

    if user_message:
        user_message_index = list(messages).index(user_message)
        next_user_index = (user_message_index + 1) % len(messages)
        next_user_message = messages[next_user_index]

    # 현재 사용자가 좋아요를 눌렀는지 여부 확인
    user_morning_liked_message_ids = user_profile.morning_liked_messages.values_list('id', flat=True)
    user_night_liked_message_ids = user_profile.night_liked_messages.values_list('id', flat=True)

    context = {
        'messages': messages,
        'time_period': time_period,
        'next_user_message': next_user_message,
        'user_morning_liked_message_ids': user_morning_liked_message_ids,
        'user_night_liked_message_ids': user_night_liked_message_ids,
    }

    return render(request, 'main/message_list.html', context)

# 메세지 작성하기
@login_required
def message_create(request):
    user = request.user
    now = timezone.localtime(timezone.now())
    current_time = now.time()
    today = now.date()
    user_profile, created = Profile.objects.get_or_create(user=user)

    # 디버깅을 위해 시간 출력
    print(f"현재 시간: {current_time}")

    # 어제 날짜 계산
    yesterday = today - timedelta(days=1)

    # 초기화 로직: 어제 작성한 메시지를 삭제
    deleted_messages_count, _ = Message.objects.filter(nick=user_profile, created_at__date=yesterday).delete()
    print(f"삭제된 메시지 수: {deleted_messages_count}")

    user_has_written_message = Message.objects.filter(nick=user_profile, created_at__date=today).exists()
    context = {
        'current_time': now.strftime('%m월 %d일'),  # 현재시간 표기
        'user_has_written_message': user_has_written_message,
    }
    if request.method == "POST":
        form = MessageForm(request.POST, user=request.user)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            user_profile.nickname = nickname
            user_profile.save()

            message = form.save(commit=False)
            message.nick = user_profile
            message.save()
            
            # 작성 후 메시지 미리보기 페이지로 리디렉션
            return redirect('main:message_view', message_id=message.id)
    else:
        form = MessageForm(user=request.user)

    context['form'] = form
    return render(request, 'main/message_create.html', context)

def message_view(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    context = {
        'message': message,
        'current_time': timezone.localtime(timezone.now()).strftime('%m월 %d일'),  # 현재시간 표기
    }
    return render(request, 'main/message_view.html', context)

# 알람기능 함수(모닝, 나잇메세지에 관한 알람만 받음)
def alarm(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-timestamp')
    return render(request, 'main/notifications.html', {'notifications':notifications})

# 좋아요 기능 함수
def like_message(request, id, type):  # 'type'을 위치 인자로 받습니다.
    message = get_object_or_404(Message, id=id)
    profile = Profile.objects.get(user=request.user)

    if type == 'morning':
        if profile in message.morninglikes.all():
            message.morninglikes.remove(profile)
        else:
            message.morninglikes.add(profile)
    elif type == 'night':
        if profile in message.nightlikes.all():
            message.nightlikes.remove(profile)
        else:
            message.nightlikes.add(profile)

    return redirect('main:message_list')

# 메세지 수정
def update(request, id):
    message = get_object_or_404(Message, id=id)
    # 9:21 수정(수정부분에도 드롭다운에는 가입된 그룹만 있어야함)
    user_profile = Profile.objects.get(user=request.user)
    user_groups = Group.objects.filter(memberships__profile=user_profile)

    if request.method == "POST":
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            user_profile, created = Profile.objects.get_or_create(user=request.user)
            user_profile.save()
            message = form.save(commit=False)
            message.nick = user_profile
            message.save()
            return redirect('main:main')
    else:
        form = MessageForm(instance=message)
        form.fields['group'].queryset = user_groups  # 9:21수정
    
    return render(request, 'main/update.html', {'form': form, 'message': message})   

# 나잇/모닝 열람시간에 맞는 메세지 조회하도록
def get_time_period(current_time, morning_time, night_time):
    # 모닝 시간대 종료 시간 계산
    morning_end_time = (datetime.combine(datetime.today(), morning_time) + timedelta(hours=1)).time()
    # 나잇 시간대 종료 시간 계산
    night_end_time = (datetime.combine(datetime.today(), night_time) + timedelta(hours=1)).time()

    if morning_time <= current_time <= morning_end_time:
        return 'morning'
    elif night_time <= current_time <= night_end_time:
        return 'night'
    else:
        return 'none'