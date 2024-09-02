from django.http import JsonResponse
from django.views.generic import ListView
from blog.forms import ConsultationForm
from blog.models import Post
from blog.views import BaseTelegramNotificationView
from webdev.forms import WebCalculationForm


class WebdevView(ListView):
    model = Post
    template_name = "webdev/webdev.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Web-разработка'
        context['form'] = ConsultationForm()
        return context


class WebCalculationView(BaseTelegramNotificationView):
    telegram_chat_id = '-1002187295106'
    template_name = "webdev/webdev.html"

    def post(self, request, *args, **kwargs):
        form = WebCalculationForm(request.POST)
        if form.is_valid():
            # Сохраняем форму, но не отправляем в базу данных сразу
            cost_request = form.save(commit=False)
            # Отправляем сообщение в Telegram
            message = (f"Новая заявка:\nИмя: {cost_request.name}\nТелефон: {cost_request.phone}\n"
                       f"Ниша: {cost_request.niche}\nФункционал: {cost_request.functionality}")
            self.send_telegram_message(message)
            # Теперь сохраняем в базу данных
            cost_request.save()
            return JsonResponse({'success': True, 'message': 'Заявка принята, мы свяжемся с вами в ближайшее время.'})
        return JsonResponse({'success': False, 'message': 'Ошибка в заполнении формы.'})
