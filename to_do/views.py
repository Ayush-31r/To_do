from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
# Create your views here.




class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'Task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Task'] = context['Task'].filter(user=self.request.user)
        context['count'] = context['Task'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['Task'] = context['Task'].filter(title__icontains = search_input)
            context['search_input'] = search_input
        return context
    
class TaskDescription(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'Task'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    # fields = ['title', 'description']
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'Task'
    success_url = reverse_lazy('task')


class CustomLoginView(LoginView):
    template_name = 'to_do/login.html'
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('task')
class Customlogout(LogoutView):
    def get_success_url(self):
        return redirect('login')

class RegisterPage(FormView):
    template_name = 'to_do/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterPage, self).get(*args, *kwargs)