import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
from subject.models import Subject, SubOption, SubType
from user.models import UserInfo


class IndexView(LoginRequiredMixin,View):
    def get(self,request):
        """显示答题页面"""
        types = SubType.objects.all()
        # 这里直接把user给过去，用来判断是否登录，否则不能答题
        user = request.user
        # 不是超级用户才传过去
        if not user.is_superuser:
            # 查询出所有用户的得分score,每答对一题积一分(排行榜)降序
            users_qlist = UserInfo.objects.all().order_by('-score')
            users = []
            for user in users_qlist:
                if not user.is_superuser:
                    users .append(user)
            # 查询出所有题目的名称
            subs = Subject.objects.all()
            # 查询出每个题目对应的所有选项,用字典存放
            dict = {}
            for sub in subs:
                sub_options = sub.suboption_set.all()
                # print(sub_options)
                dict[sub] = sub_options
                # print(dict)

            return render(request, "index.html", {'types':types,'user':user, 'users':users, 'dict':dict})
        return redirect("/admin")


class DetailView(LoginRequiredMixin,View):
    def get(self,request, type_id):
        # 查询出所有用户的得分score,每答对一题积一分(排行榜)降序
        users_qlist = UserInfo.objects.all().order_by('-score')
        users = []
        for user in users_qlist:
            if not user.is_superuser:
                users.append(user)
        """查询出type_id下的所有题目"""
        # 根据type_id去查询是那个类型对象
        type_obj = SubType.objects.filter(id=type_id).first()
        # 查询出该类型下对应的所有题目
        subjects = type_obj.subject_set.all()
        dict = {}
        for sub in subjects:
            sub_options = sub.suboption_set.all()
            # print(sub_options)
            dict[sub] = sub_options
        # 传递到前端
        return render(request,"detail.html",{"type_obj":type_obj,'users':users,'dict':dict,'type_id':type_id})

    def post(self, request):
        """进行答题处理"""
        user = request.user
        # 当前用户的初始得分为user_initial
        user_initial = user.score
        type_id = request.POST.get("type_id")
        print(type_id)
        if type_id:
            # 根据type_id去查询对象
            type_obj = SubType.objects.filter(id=type_id).first()
            # print(type_obj.type)
            # 没有登陆则跳转到登录页面
            if user.is_authenticated:
                # 除后台管理员外的所有用户得分
                users_qlist = UserInfo.objects.all().order_by('-score')
                users = []
                for userr in users_qlist:
                    if not userr.is_superuser:
                        users.append(userr)
                # 查询出该类型（比如运动）下的所有题目
                subs = type_obj.subject_set.all()
                # 查询出每个题目对应的所有选项,用字典存放
                dict = {}
                for sub in subs:
                    sub_options = sub.suboption_set.all()
                    # print(sub_options)
                    dict[sub] = sub_options
                user_answer_list = []
                for sub in subs:
                    # 单选
                    if sub.sub_type == 0:
                        user_answer = request.POST.get(sub.sub)
                        if user_answer:
                            user_answer_list.append(user_answer)

                        else:
                            msg = "请把题做完再提交"
                            return render(request, "detail.html", {'msg': msg, 'user': user, 'users': users, 'dict': dict})
                    # 多选
                    else:
                        user_answer = request.POST.getlist(sub.sub)
                        if user_answer:
                            user_answer_list.append(user_answer)

                        else:
                            msg = "请把题做完再提交!"
                            return render(request, "detail.html", {'msg': msg, 'user': user, 'users': users, 'dict': dict})
                list3 = []
                user_answer_list = [str(i) for i in user_answer_list]
                # print("用户的答案为={}".format(user_answer_list))
                # 用户本次答题得分
                user_this_score = 0
                for sub in subs:
                    for user_answer in user_answer_list:
                        if sub.answer == user_answer:
                            # 正确则查出这是哪道题（因为每道题分数不一样）
                            s_obj = Subject.objects.filter(answer=sub.answer).first()
                            # print(s_obj.sub_score)
                            user_this_score = user_this_score + s_obj.sub_score
                            # print(user_this_score)
                            list3.append(1)
                # 用户最终得分
                user.score = user_initial + user_this_score
                # print("用户最终得分{}".format(user.score))
                user.save()

                msg = "{}您好，您上次总得分是{},您本次共答对{}道题，积{}分，本次答题后总得分为{}".format(user.username, user_initial, len(list3),user_this_score, user.score)
                return render(request, "detail.html",
                              {'type_obj': type_obj, 'msg': msg, 'user': user, 'users': users, 'dict': dict})

        if request.user.is_authenticated:
            # 用户初始得分
            users_qlist = UserInfo.objects.all().order_by('-score')
            users = []
            for user in users_qlist:
                if not user.is_superuser:
                    users.append(user)
            msg = "请勿重复提交此类题,请点击回到首页继续答题或注销退出"
            return render(request, "detail.html",{'msg':msg,'users':users})
