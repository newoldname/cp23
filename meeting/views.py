from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from meeting.models import Project


# Create your views here.
def index(request):
    return render(
        request,
        'meeting/index.html',
    )


class ProjectList(ListView):
    model = Project
    ordering = '-pk'

    def dispatch(self, request, *args, **kwargs):
        if request.path.split("/")[-2] == "my":
            self.isMine = True
        else:
            self.isMine = False
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectList, self).get_context_data()
        if self.isMine:
            myProject = []
            for i in context['project_list']:
                if i.author == self.request.user:
                    myProject.append(i)
            context['project_list'] = myProject
            context['isMine'] = 'True'
        return context


class ProjectDetail(DetailView):
    model = Project


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ["title", "content", "information", "question1", "question2", "question3"]


    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(ProjectCreate, self).get_form(form_class)
        form.fields['title'].widget.attrs["placeholder"] = '프로그램의 이름을 알려주세요'
        form.fields['title'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'
        form.fields['content'].widget.attrs["placeholder"] = '어떤 프로그램을 하고 싶은 지 알려주세요'
        form.fields['content'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'
        form.fields['information'].widget.attrs['placeholder'] = '선발된 지원자에게 보여줄 메시지입니다. 전화번호, 오픈카톡 채팅방 링크 등 자유롭게 작성하세요.'
        form.fields['information'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'
        form.fields['question1'].widget.attrs['placeholder'] = '지원자에게 궁금한 부분을 물어보세요. '
        form.fields['question1'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'
        form.fields['question2'].widget.attrs['placeholder'] = '지원자에게 궁금한 부분을 물어보세요. '
        form.fields['question2'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'
        form.fields['question3'].widget.attrs['placeholder'] = '지원자에게 궁금한 부분을 물어보세요. '
        form.fields['question3'].widget.attrs["style"] = 'margin: 10px 0px 20px 0px'
        return form

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(ProjectCreate, self).form_valid(form)
        else:
            return redirect("/meeting/")


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ["title", "content", "information", "question1", "question2", "question3"]

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(ProjectUpdate, self).get_form(form_class)
        form.fields['title'].widget.attrs["placeholder"] = '프로그램의 이름을 알려주세요'
        form.fields['title'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'
        form.fields['content'].widget.attrs["placeholder"] = '어떤 프로그램을 하고 싶은 지 알려주세요'
        form.fields['content'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'
        form.fields['information'].widget.attrs['placeholder'] = '선발된 지원자에게 보여줄 메시지입니다. 전화번호, 오픈카톡 채팅방 링크 등 자유롭게 작성하세요.'
        form.fields['information'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'
        form.fields['question1'].widget.attrs['placeholder'] = '지원자에게 궁금한 부분을 물어보세요. '
        form.fields['question1'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'
        form.fields['question2'].widget.attrs['placeholder'] = '지원자에게 궁금한 부분을 물어보세요. '
        form.fields['question2'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'
        form.fields['question3'].widget.attrs['placeholder'] = '지원자에게 궁금한 부분을 물어보세요. '
        form.fields['question3'].widget.attrs["style"] = 'margin: 10px 0px 20px 0px'

        return form

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(ProjectUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
