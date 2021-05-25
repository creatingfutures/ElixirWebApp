from django.shortcuts import render
from django.http import HttpResponse
import json
import os
import nltk
from django.views.decorators.csrf import csrf_exempt
import chatterbot
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import levenshtein_distance
from nltk.corpus import wordnet, stopwords
from chatbot.chatbotresponse import chatbotresponse

#nltk.download('stopwords')
chatbotresponse = chatbotresponse()
chatbot = ChatBot(
    'Elixir',
	#statement_comparison_function =jaccard_similarity,
	response_selection_method=chatbotresponse.select_response,
	logic_adapters=[
		#{
		#	'import_path':'chatbot.chatbotlogicadapter.elixirlogicadapter'
		#},
		
		{
			'import_path':'chatterbot.logic.BestMatch',
			
			#'threshold': 0.65,
			#'default_response': 'OhNo'
						
		}
		
		

		]
    #trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

path= os.getcwd()

#trainer = ChatterBotCorpusTrainer(chatbot)
chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.train(path+"\\chatbot\\static\\chatbot.yml")

# Train based on the english corpus

# Already trained and it's supposed to be persistent
 #chatbot.train("chatterbot.corpus.english")


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
	return render(request,template_name)


