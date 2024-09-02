from django.http import JsonResponse
from django.views.generic import ListView

from blog.forms import ConsultationForm
from blog.models import Post
from blog.views import BaseTelegramNotificationView
from career.forms import ResumeForm


class CareerView(ListView):
    model = Post
    template_name = "career/career.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Карьера'
        context['form'] = ConsultationForm()
        return context


class ResumeView(BaseTelegramNotificationView):
    telegram_chat_id = '-1002003513414'

    def post(self, request):
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            # Сохранение данных
            resume = form.save()

            # Создание текстового сообщения
            message_text = (
                f"Новое резюме:\n\n"
                f"Имя: {resume.first_name}\n"
                f"Фамилия: {resume.last_name}\n"
                f"Email: {resume.email}\n"
                f"Файл резюме: {resume.resume_file.url}\n"
                f"Дата отправки: {resume.date_sent}\n"
                f"Статус: {resume.status}"
            )
            # Отправка сообщения в Telegram
            self.send_telegram_message(message_text)

            response_data = {'message': "Спасибо за ваше обращение! Мы рассмотрим ваше резюме в ближайшее время."}
            return JsonResponse(response_data)

        # Если форма не валидна, возвращаем ошибки
        return JsonResponse({'errors': form.errors}, status=400)
