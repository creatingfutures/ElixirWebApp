import chatterbot
import random


class chatbotresponse:
    """description of class"""

    def select_response(chatbotresponse,statement:chatterbot.conversation.Statement, statement_list, storage=None):
     #default_text = 'I am sorry, I did not understand what you said'
     #filtered_responses = list(filter(chatbotresponse.filter_statementlist, statement_list))
   #  if(len(statement_list) >0):
        resp = random.choice(statement_list)
    # else:
        #resp = chatterbot.conversation.Statement(default_text)

        return chatterbot.conversation.Statement(resp.text)
    

    def filter_statementlist(self,statement):
        if (statement.confidence >0):
            return True
        else:
            return False
