from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
 

chatbot = ChatBot(
    'Elixir',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

 

# Train based on the english corpus

# Already trained and it's supposed to be persistent
# chatbot.train("chatterbot.corpus.english")


@csrf_exempt
def get_response(request):
	response = {'status': None}

	if request.method == 'GET':
		# data = json.loads(request.body.decode('utf-8'))
		userText = request.GET.get('msg')

		response = chatbot.get_response(userText).text

	return HttpResponse(
		json.dumps(response),
			content_type="application/json"
		)



def home(request, template_name="home.html"):
	return render_to_response(template_name)
