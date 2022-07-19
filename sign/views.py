from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from sign.models import Event, Guest


# Create your views here.
def index(request):
    context = {}
    context['hello'] = 'HELLO WORLD'
    return render(request, "index.html", context)


# 退出登录
@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/index/')
    return response


def login_action(request):
    if request.method == "POST":
        # 寻找名为 "username"和"password"的POST参数，而且如果参数没有提交，返回一个空的字符串。
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username == '' or password == '':
            return render(request, "index.html", {"error": "username or password null!"})

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 验证登录
            response = HttpResponseRedirect('/event_manage/')  # 登录成功跳转发布会管理
            request.session['username'] = username  # 将 session 信息写到服务器
            return response
        else:
            return render(request, "index.html", {"error": "username or password error!"})
    # 防止直接通过浏览器访问 /login_action/ 地址。
    return render(request, "index.html")


# 发布会管理
@login_required
def event_manage(request):
    # username = request.COOKIES.get('user', '')
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    return render(request, "event_manage.html", {"user": username,
                                                 "events": event_list})

# 搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username,
                                                 "events": event_list})


@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username = request.session.get('username', '')

    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    print("`````````````````````````",page)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


# 跳转签到页
@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)  # 签到人数
    sign_list = Guest.objects.filter(sign="1", event_id=event_id)  # 已签到数
    guest_data = str(len(guest_list))
    sign_data = str(len(sign_list))
    return render(request, 'sign_index.html', {'event': event,
                                               'guest': guest_data,
                                               'sign': sign_data})


# 前端签到页面
@login_required
def sign_index2(request, event_id):
    event_name = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index2.html', {'eventId': event_id,
                                                'eventNanme': event_name})


# 签到动作
# @login_required
# def sign_index_action(request,event_id):
#     event = get_object_or_404(Event, id=event_id)
#     guest_list = Guest.objects.filter(event_id=event_id)
#     guest_data = str(len(guest_list))
#     print(guest_data)
#     sign_data = 0   #计算发布会“已签到”的数量
#     for guest in guest_list:
#         if guest.sign == True:
#             sign_data += 1
#
#     phone =  request.POST.get('phone','')
#
#     result = Guest.objects.filter(phone = phone)
#     print("result:",result)
#     if not result:
#         return render(request, 'sign_index.html', {'event': event,'hint': 'phone error.','guest':guest_data,'sign':sign_data})
#
#     result = Guest.objects.filter(phone = phone,event_id = event_id)
#     if not result:
#         return render(request, 'sign_index.html', {'event': event,'hint': 'event id or phone error.','guest':guest_data,'sign':sign_data})
#
#     result = Guest.objects.get(event_id = event_id,phone = phone)
#
#     if result.sign:
#         return render(request, 'sign_index.html', {'event': event,'hint': "user has sign in.",'guest':guest_data,'sign':sign_data})
#     else:
#         Guest.objects.filter(event_id = event_id,phone = phone).update(sign = '1')
#         return render(request, 'sign_index.html', {'event': event,'hint':'sign in success!',
#             'user': result,
#             'guest':guest_data,
#             'sign':str(int(sign_data)+1)
#             })


'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''


@login_required
def sign_index_action(request, event_id):
    # 查出属于那个发布会对象（头顶显示）
    event = get_object_or_404(Event, id=event_id)
    # 取目标手机号码
    iPhone = request.POST.get("iphone", '')
    # 查询嘉宾人数
    guest_list = Guest.objects.filter(event_id=event_id)
    guest_data = str(len(guest_list))
    # 签到数
    sign_data = 0
    for guest in guest_list:
        if guest.sign == 1:
            sign_data += 1

    # 查目标手机是否存在
    result_filter = Guest.objects.filter(event_id=event_id, phone=iPhone)
    if not result_filter:
        return render(request, 'sign_index.html',
                      {'event': event, 'sign': sign_data, 'hint': 'event id or phone error', 'sign': sign_data, "guest": guest_data})

    result_get = Guest.objects.get(event_id=event_id, phone=iPhone)
    if result_get.sign:
        return render(request, 'sign_index.html',
                      {'event': event, 'hint': "user has sign in.", 'guest': guest_data, 'sign': sign_data})

    else:
        result_filter.update(sign='1')
        sign_data += 1
        return render(request, 'sign_index.html', {
            'event': event,
            'user': result_filter,
            'hint': "user sign in success!.",
            'sign': sign_data,
            "guest": guest_data
        })


