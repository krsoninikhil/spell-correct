from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.spell_correct import spell_correct


class SpellCorrect(APIView):
    '''
    Receive query words, correct the spelling and return them.
    '''
    def get(self, request):
        '''
        Expects a comma seperated list of words.
        '''
        res = None
        if 'words' in request.query_params:
            words = request.query_params['words'].split(',')
            res = spell_correct(words, request.query_params.get('method'))
        
        return Response(res, status=status.HTTP_200_OK)
        
    def post(self, request):
        '''
        Expects a list of words with content-type: application/json.
        '''
        res = None
        stat = status.HTTP_200_OK
        if 'words' in request.data:
            words = request.data['words']
            if isinstance(words, list):
                res = spell_correct(words, request.data.get('method'))
            else:
                res = {"details": "Expecting a list of words"}
                stat = status.HTTP_400_BAD_REQUEST

        return Response(res, status=stat)
       
