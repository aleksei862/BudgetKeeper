from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import AIMessage


@login_required
def agent_page(request):
    # Получаем историю сообщений текущего пользователя
    history = AIMessage.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'agent_app/agent.html', {'history': history})


@login_required
def agent_send(request):
    if request.method == 'POST':
        user_text = request.POST.get('message', '').strip()
        if not user_text:
            return JsonResponse({'error': 'Пустое сообщение'}, status=400)

        # 1. Сохраняем вопрос пользователя
        AIMessage.objects.create(user=request.user, role='user', content=user_text)

        # 2. Генерируем ответ (МОК ИИ-АГЕНТА)
        text_lower = user_text.lower()
        if 'привет' in text_lower or 'здравствуй' in text_lower:
            ai_reply = "Здравствуйте! Я ИИ-ассистент приложения BudgetKeeper. Я помогаю следить за финансами. Чем могу помочь?"
        elif 'потрат' in text_lower or 'расход' in text_lower:
            ai_reply = "Для просмотра расходов перейдите в личный кабинет. Там вы увидите вашу статистику."
        elif 'отчет' in text_lower or 'напиши' in text_lower:
            ai_reply = "Извините, я не могу писать отчеты за вас. Но я могу подсказать, как работает приложение."
        else:
            ai_reply = "Я вас понял. Пожалуйста, задайте вопрос, связанный с вашими финансами или приложением BudgetKeeper."

        # 3. Сохраняем ответ ИИ
        AIMessage.objects.create(user=request.user, role='assistant', content=ai_reply)

        return JsonResponse({'reply': ai_reply})
    return JsonResponse({'error': 'Invalid method'}, status=405)


from django.shortcuts import render

# Create your views here.
