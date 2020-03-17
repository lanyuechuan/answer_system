import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from user.models import UserInfo




# /register
class RegisterView(View):
    '''显示注册页面'''

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 接收数据
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # 校验数据
        if not all([username, mobile, password, cpassword]):
            return render(request, 'register.html', context={'errmsg': '参数提交不完整请重新提交'})
        # 因为前端提交验证码，只有用户输入正确的并且是本人的手机号才能拿到正确的验证码，所以我们这里不用判断手机号的正确性，只需要对比第三方还有这边的验证码的一致性
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$', password):
            return render(request, 'register.html', context={'errmsg': '密码至少8位，并且必须有大写字母，小写字母和数字'})
        if password != cpassword:
            return render(request, 'register.html', context={'errmsg': '密码不一致'})

        # 逻辑处理
        # 1、判断是否有重复的用户名或手机号，没有重复我把注册信息加入后台数据库
        if not UserInfo.objects.filter(Q(username=username) | Q(mobile=mobile)).exists():
            # 用户密码作加密操作
            password = make_password(password)
            user = UserInfo.objects.create(username=username, password=password, mobile=mobile)
            # 返回应答
            if user:
                return redirect(reverse('user:login'))

        return render(request, 'register.html', {'errmsg': '用户名或者手机号已存在'})


# /login普通登录方式
class LoginView(View):
    '''显示登陆页面'''

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get("password")

        # 数据校验
        if not all([username, password]):
            return render(request, 'login.html', context={'errmsg': '参数提交不完整请重新提交'})


        # TODO:用户表继承AbstractUser,能用djangoo底层的认证系统包括login,logout,auth..别用session来处理了

        if not UserInfo.objects.filter(username=username).first():  # 这里拿到对应用户名的一条记录user对象
            return render(request, 'login.html', context={'errmsg': '该用户还未注册'})
        # 认证
        user = authenticate(username=username, password=password)  # 一般是传用户名密码
        # print(user)
        # 如果用户是超级用户，直接到后台管理界面
        if user:
            login(request, user)
            if not user.is_superuser:
                return redirect("subject:index")
            else:
                return redirect("/admin")

        else:
            return render(request, 'login.html', context={'errmsg': '用户名或密码错误'})


# /logout
def user_logout(request):
    logout(request)
    return redirect(reverse('user:login'))

