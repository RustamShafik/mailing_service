from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.views import View
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Mailing, Attempt
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from clients.models import Client
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(user=user)

class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'status', 'message', 'recipients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = ['start_time', 'end_time', 'status', 'message', 'recipients']
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Mailing.objects.none()  # менеджерам нельзя редактировать чужие рассылки
        return Mailing.objects.filter(user=user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Менеджеры').exists():
            return Mailing.objects.none()  # менеджерам нельзя удалять чужие рассылки
        return Mailing.objects.filter(user=user)

class SendMailingView(LoginRequiredMixin, View):
    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        user = request.user
        # менеджерам запрещаем отправку чужих рассылок
        if user.groups.filter(name='Менеджеры').exists():
            raise Http404("Менеджерам запрещена ручная отправка рассылок.")

        if mailing.user != user:
            raise Http404("Нет доступа к этой рассылке.")

        recipients = mailing.recipients.all()
        success = True
        response_log = ""

        for client in recipients:
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=None,  # ⚠️ при необходимости замени
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                response_log += f"Sent to {client.email}\n"
            except Exception as e:
                success = False
                response_log += f"Failed to {client.email}: {str(e)}\n"

        Attempt.objects.create(
            mailing=mailing,
            status="Успешно" if success else "Не успешно",
            server_response=response_log
        )

        if mailing.status == "Создана":
            mailing.status = "Запущена"
            mailing.save()

        messages.success(request, "Попытка отправки завершена.")
        return redirect('mailing_list')

def test_email(request):
    send_mail(
        subject='Тестовое письмо',
        message='Это тестовое письмо, отправленное из Django.',
        from_email=None,  # будет использовать DEFAULT_FROM_EMAIL из settings.py
        recipient_list=['shafikovr@mail.ru'],
        fail_silently=False,
    )
    return HttpResponse('Письмо отправлено')

class AttemptListView(ListView):
    model = Attempt
    template_name = 'mailings/attempt_list.html'
    context_object_name = 'attempts'

@method_decorator(cache_page(60 * 5), name='dispatch')  # кеш на 5 минут
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing_count'] = Mailing.objects.count()
        context['active_mailing_count'] = Mailing.objects.filter(status='Запущена').count()
        context['client_count'] = Client.objects.count()
        context['latest_attempts'] = Attempt.objects.order_by('-timestamp')[:5]
        return context

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'mailings/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_mailings = Mailing.objects.filter(user=user)

        context['success_count'] = Attempt.objects.filter(
            mailing__in=user_mailings, status='Успешно'
        ).count()

        context['fail_count'] = Attempt.objects.filter(
            mailing__in=user_mailings, status='Не успешно'
        ).count()

        context['message_count'] = Attempt.objects.filter(
            mailing__in=user_mailings, status='Успешно'
        ).count()

        return context
