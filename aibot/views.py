import uuid
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import ChatSession, Message
from decouple import config


# System prompt to restrict AI to fertility topics only
SYSTEM_PROMPT = """You are Dr. Adakings, an AI fertility guide for FertilEus Network. You ONLY answer questions related to:
- Fertility and reproductive health
- Menstrual cycles and ovulation
- IVF and assisted reproductive technologies
- Egg donation and sperm donation
- Surrogacy
- Pregnancy and conception
- Fertility testing and diagnosis
- Lifestyle factors affecting fertility

If a user asks about topics outside fertility (politics, sports, entertainment, general knowledge, etc.), politely decline and redirect them back to fertility topics.

Give a direct, useful answer before mentioning limitations. Use clear, everyday language and short paragraphs or bullets when they make the advice easier to follow. Explain the relevant general guidance, practical next steps, and when someone should seek prompt medical care. Ask one focused follow-up question only when the answer truly depends on missing details, such as cycle length, age, symptoms, or treatment history.

Be compassionate, accurate, and non-judgmental. Do not diagnose, promise outcomes, or give a generic "see a clinician" response when you can provide safe educational information. Include a brief educational-not-medical-advice reminder only when it is clinically relevant or when giving individualized-looking guidance."""


def get_ai_response(messages):
    """Get a response using Groq (llama-3.1-8b-instant, free tier)."""
    import groq as groq_sdk

    api_key = config('GROQ_API_KEY', default=None)
    if not api_key:
        raise RuntimeError('No GROQ_API_KEY configured in .env file.')

    client = groq_sdk.Groq(api_key=api_key)

    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    recent_messages = list(messages.order_by('-created_at')[:20])[::-1]
    for message in recent_messages:
        api_messages.append({"role": message.role, "content": message.content})

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=api_messages,
        max_tokens=700,
        temperature=0.4,
    )
    return completion.choices[0].message.content


def chat_view(request):
    """Main chat interface"""
    session_id = request.GET.get('session')

    if session_id:
        session = get_object_or_404(ChatSession, session_id=session_id)
        messages = session.messages.all()
    else:
        session = ChatSession.objects.first()
        if session:
            messages = session.messages.all()
        else:
            session = None
            messages = []

    all_sessions = ChatSession.objects.all()[:10]

    return render(request, 'aibot/chat.html', {
        'session': session,
        'messages': messages,
        'all_sessions': all_sessions,
    })


@csrf_exempt
@require_http_methods(["POST"])
def new_chat(request):
    """Create a new chat session"""
    session_id = str(uuid.uuid4())[:8]
    session = ChatSession.objects.create(session_id=session_id)

    Message.objects.create(
        session=session,
        role='assistant',
        content="Hello, I'm Dr. Adakings. Ask me anything about fertility, cycles, IVF, donation or surrogacy. Everything you share stays on this device."
    )

    return JsonResponse({
        'session_id': session.session_id,
        'redirect_url': f'/ai-bot/?session={session.session_id}'
    })


@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """Send a message and get AI response"""
    data = json.loads(request.body)
    session_id = data.get('session_id')
    user_message = data.get('message')

    if not session_id:
        session_id = str(uuid.uuid4())[:8]
        session = ChatSession.objects.create(session_id=session_id)
        Message.objects.create(
            session=session,
            role='assistant',
            content="Hello, I'm Dr. Adakings. Ask me anything about fertility, cycles, IVF, donation or surrogacy. Everything you share stays on this device."
        )
    else:
        session = get_object_or_404(ChatSession, session_id=session_id)

    if not user_message:
        return JsonResponse({'error': 'Missing message'}, status=400)

    Message.objects.create(session=session, role='user', content=user_message)

    messages = session.messages.all()

    try:
        ai_response = get_ai_response(messages)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error("AI response error: %s", e)
        return JsonResponse({
            'error': 'The AI assistant is temporarily unavailable. Please try again shortly.',
        }, status=503)

    Message.objects.create(session=session, role='assistant', content=ai_response)

    return JsonResponse({
        'response': ai_response,
        'session_id': session.session_id
    })


@require_http_methods(["GET"])
def get_history(request):
    """Return all chat sessions as JSON for the popup history panel"""
    sessions = ChatSession.objects.all()[:20]
    data = []
    for sess in sessions:
        first_msg = sess.messages.filter(role='user').first()
        preview = first_msg.content[:60] if first_msg else "New conversation"
        data.append({
            'session_id': sess.session_id,
            'preview': preview,
            'date': sess.updated_at.strftime('%d %b %Y'),
        })
    return JsonResponse({'sessions': data})


@require_http_methods(["GET"])
def load_session(request, session_id):
    """Return all messages for a session as JSON"""
    session = get_object_or_404(ChatSession, session_id=session_id)
    messages = [
        {'role': m.role, 'content': m.content}
        for m in session.messages.all()
    ]
    return JsonResponse({'session_id': session_id, 'messages': messages})
