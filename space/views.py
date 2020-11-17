import json
from typing import Pattern
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot, comparisons, response_selection
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatterbot = ChatBot('Default Response Example Bot',    
        logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90,
            "statement_comparison_function": comparisons.LevenshteinDistance,
            "response_selection_method": response_selection.get_most_frequent_response
        }
    ])
    # trainer1 = ChatterBotCorpusTrainer(chatterbot)

    # trainer1.train("chatterbot.corpus.english.conversations")
    # trainer.train("chatterbot.corpus.english.humor")

    training_data_quesans = open('./ques_ans.txt').read().splitlines()
    training_data_personal = open('./personal_ques.txt').read().splitlines()

    training_data = training_data_quesans + training_data_personal

    trainer = ListTrainer(chatterbot)
    trainer.train(training_data)  
    
   



    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        response = self.chatterbot.get_response(input_data)

        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': self.chatterbot.name
        })