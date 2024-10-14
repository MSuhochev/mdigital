from django.http import JsonResponse
from django.views.generic import ListView
import requests
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
                f"Сопроводительное письмо: {resume.cover_letter}\n"
                f"Дата отправки: {resume.date_sent}\n"
                f"Статус: {resume.status}"
            )

            # Отправка сообщения и файла резюме в Telegram
            if resume.resume_file:
                self.send_resume_with_file_to_telegram(message_text, resume.resume_file)

            response_data = {'message': "Спасибо за ваше обращение! Мы рассмотрим его в ближайшее время."}
            return JsonResponse(response_data)

        # Если форма не валидна, возвращаем ошибки
        return JsonResponse({'errors': form.errors}, status=400)

    def send_resume_with_file_to_telegram(self, message_text, resume_file):
        """
        Отправка сообщения с файлом резюме в Telegram.
        """
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendDocument"

        with resume_file.open('rb') as file_data:  # Открываем файл в режиме чтения байтов
            files = {'document': file_data}
            data = {
                'chat_id': self.telegram_chat_id,
                'caption': message_text  # Используем текст сообщения как подпись
            }

            response = requests.post(url, data=data, files=files)
            if response.status_code != 200:
                # Обработка ошибки отправки файла
                print(f"Ошибка отправки файла: {response.text}")
