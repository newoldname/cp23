from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView

from apply.models import Application
from meeting.models import Project


# Create your views here.
def index(request):
    return render(
        request,
        'apply/index.html',
    )


class ApplicationList(LoginRequiredMixin, ListView):
    model = Application
    ordering = '-pk'

    # def dispatch(self, request, *args, **kwargs):
    #     if request.path.split("/")[-3] == "list":
    #         self.isOneProject = True
    #     else:
    #         self.isOneProject = False
    #     print(self.isMine)
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ApplicationList, self).get_context_data()
        myApplication = {}
        # appliedProject = []
        for i in context['application_list']:
            if i.author == self.request.user:
                nowProject = Project.objects.filter(id=i.meeting.pk)

                myApplication[i] = nowProject[0]
                # print(nowProject[0])
                # appliedProject.append(nowProject)

        context['application_list'] = myApplication
        # context['project_list'] = appliedProject
        return context


class ApplicationCreate(LoginRequiredMixin, CreateView):
    model = Application
    fields = ["answer1", "answer2", "answer3"]

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `Ipsum` instance exists
        before going any further.
        """
        self.nowProject = get_object_or_404(Project, pk=kwargs['projectPk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(ApplicationCreate, self).get_form(form_class)

        if self.nowProject.question1 is None:
            form.fields["answer1"].label = "첫 번째 질문이 기재되지 않았습니다."
            form.fields["answer1"].widget.attrs["hidden"] = ""
        else:
            form.fields["answer1"].label = "질문1: " + self.nowProject.question1
            form.fields['answer1'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'

        if self.nowProject.question2 is None:
            form.fields["answer2"].label = "두 번째 질문이 기재되지 않았습니다."
            form.fields["answer2"].widget.attrs["hidden"] = ""
        else:
            form.fields["answer2"].label = "질문2: " + self.nowProject.question2
            form.fields['answer2'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'

        if self.nowProject.question3 is None:
            form.fields["answer3"].label = "세 번째 질문이 기재되지 않았습니다."
            form.fields["answer3"].widget.attrs["hidden"] = ""
        else:
            form.fields["answer3"].label = "질문3: " + self.nowProject.question3
            form.fields['answer3'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'

        return form

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            form.instance.meeting = self.nowProject
            return super(ApplicationCreate, self).form_valid(form)
        else:
            return redirect("/meeting/")


class ApplicationUpdate(LoginRequiredMixin, UpdateView):
    model = Application
    fields = ["answer1", "answer2", "answer3"]

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `Ipsum` instance exists
        before going any further.
        """
        if request.user.is_authenticated and request.user == self.get_object().author:
            self.nowProject = self.get_object().meeting

            return super(ApplicationUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(ApplicationUpdate, self).get_form(form_class)

        if self.nowProject.question1 is None:
            form.fields["answer1"].label = "첫 번째 질문이 기재되지 않았습니다."
            form.fields["answer1"].widget.attrs["hidden"] = ""
        else:
            form.fields["answer1"].label = "질문1: " + self.nowProject.question1
            form.fields['answer1'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'

        if self.nowProject.question2 is None:
            form.fields["answer2"].label = "두 번째 질문이 기재되지 않았습니다."
            form.fields["answer2"].widget.attrs["hidden"] = ""
        else:
            form.fields["answer2"].label = "질문2: " + self.nowProject.question2
            form.fields['answer2'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'

        if self.nowProject.question3 is None:
            form.fields["answer3"].label = "세 번째 질문이 기재되지 않았습니다."
            form.fields["answer3"].widget.attrs["hidden"] = ""
        else:
            form.fields["answer3"].label = "질문3: " + self.nowProject.question3
            form.fields['answer3'].widget.attrs["style"] = 'margin: 10px 0px 10px 0px'

        return form


def selectPeople(request, projectPk):
    if request.method == "GET":
        nowProject = get_object_or_404(Project, pk=projectPk)
        if nowProject.author != request.user or nowProject.is_finish:
            raise PermissionDenied()
        allApplications = Application.objects.filter(meeting=nowProject)
        allApplicationsInfo = {}
        for i in allApplications:
            allApplicationsInfo[i.pk] = i

        return render(request,
                      "apply/choose_application.html",
                      {
                          "project": nowProject,
                          "application_list": allApplicationsInfo
                      })
    elif request.method == "POST":
        for key, value in request.POST.items():
            if key != "csrfmiddlewaretoken":
                applyAppliaction = get_object_or_404(Application, pk=int(key))
                applyAppliaction.is_apply = True
                applyAppliaction.save()
        nowProject = get_object_or_404(Project, pk=projectPk)
        nowProject.is_finish = True
        nowProject.save()
        return HttpResponseRedirect(f"/meeting/{projectPk}")
