from django.urls import path
from app.views import SpellCorrect


urlpatterns = [
    path('', SpellCorrect.as_view(), name='spellcorrect'),
]
