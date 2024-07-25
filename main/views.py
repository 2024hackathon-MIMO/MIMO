from datetime import datetime, timedelta
from django.utils.dateformat import DateFormat
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *
from .models import *
from .serializers import openTimeSerializer

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
    open_time, created = openTime.objects.get_or_create(user=user, defaults={'morning_time': '06:00:00', 'night_time': '23:00:00'})
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
        morning_time = datetime.strptime('08:00:00', '%H:%M:%S').time()
        night_time = datetime.strptime('23:00:00', '%H:%M:%S').time()

    context = {
        'morning_time': morning_time,
        'night_time': night_time,
        'current_time' : now.strftime('%m월 %d일'), # 현재시간 표기
        'can_open_message' : False, # 메세지 열람가능 여부
    }

    # 디버깅을 위해 시간 출력
    print(f"현재 시간: {current_time}, 모닝 시간: {morning_time}, 나잇 시간: {night_time}")

    today = timezone.now().date()
    user_profile, created = Profile.objects.get_or_create(user=user)
    user_has_written_message = Message.objects.filter(nick=user_profile, created_at__date=today).exists()
    context['user_has_written_message'] = user_has_written_message

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
    # 밤 시간대(21시~24시 및 0시~4시)
    elif (datetime.strptime('21:00:00', '%H:%M:%S').time() <= current_time <= datetime.strptime('04:00:00', '%H:%M:%S').time()):
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
        morning_time = open_time.morning_time
        night_time = open_time.night_time

        # 현재 시간 = 지정한 모닝메세지 열람시간 ~ 1h
        if morning_time <= current_time <= (datetime.combine(now.date(), morning_time) + timezone.timedelta(hours=1)).time():
            context['can_open_messages'] = True
            if not Notification.objects.filter(user=user, message = "모닝메세지를 열람할 수 있습니다.").exists():
                Notification.objects.create(user=user, message = "모닝메세지를 열람할 수 있습니다.")
        # 현재시간 = 지정한 나잇메세지 열람시간 ~ + 1h
        elif night_time <= current_time <= (datetime.combine(now.date(), night_time) + timezone.timedelta(hours=1)).time():
            context['can_open_messages'] = True
            if not Notification.objects.filter(user=user, message = "나잇메세지를 열람할 수 있습니다.").exists():
                Notification.objects.create(user=user, message = "나잇메세지를 열람할 수 있습니다.")

    return render(request, 'main/main.html', context)

# 메시지 열람하기
def message_list(request):
    today = timezone.now().date()
    messages = Message.objects.filter(created_at__date=today)
    return render(request, 'main/message_list.html', {'messages': messages})

# 메세지 작성하기
def message_create(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            user_profile, created = Profile.objects.get_or_create(user=request.user)
            user_profile.nickname = nickname
            user_profile.save()

            message = form.save(commit=False)
            message.nick = user_profile

            message.save()
            return redirect('main:main')
        
    else:
        form = MessageForm()

    return render(request, 'main/message_create.html', {'form': form})

# 알람기능 함수(모닝, 나잇메세지에 관한 알람만 받음)
def alarm(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-timestamp')
    return render(request, 'main/notifications.html', {'notifications':notifications})