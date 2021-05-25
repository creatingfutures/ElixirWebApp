from chatterbot.logic import LogicAdapter
import yaml,json
import os
import io

class ElixirLogicAdapter(LogicAdapter):

 def __init__(self, chatbot, **kwargs):
     super(ElixirLogicAdapter,self).__init__(**kwargs)
 def can_process(self, statement):
        path= os.getcwd()
       
       

 def process(self, statement):
        import random
        datafile = file('static/chatbot.yaml') 
        # Randomly select a confidence between 0 and 1
        confidence = random.uniform(0, 1)

        # For this example, we will just return the input as output
        selected_statement = input_statement
        selected_statement.confidence = confidence

        return selected_statement