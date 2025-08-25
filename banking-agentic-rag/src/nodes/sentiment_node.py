from transformers import pipeline
from states.banking_state import BankingState
from utils.services.create_jira_ticket import create_jira_ticket
from utils.config.llm_config import LLMConfig
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
# Load once (avoids reloading the model each time)
sentiment_pipeline = pipeline("sentiment-analysis")

_llm = LLMConfig.getLLM()
system_message = SystemMessagePromptTemplate.from_template("""
You are an expert assistant responsible for creating Jira tickets based on user queries and sentiment.
Follow these rules:
- Analyze the user's query and the sentiment score.
- Extract actionable details from the query.
- Respond with a single concise string that confirms a Jira ticket has been created, starting with "Jira Details:" followed by the ticket summary. 
- Do NOT add extra commentary, JSON, sentiment details or unrelated content.
""")

# 2️⃣ Human message template
human_message = HumanMessagePromptTemplate.from_template("""
User query: {user_query}
Sentiment score: {sentiment}
""")

# 3️⃣ Combine into a ChatPromptTemplate
jira_prompt = ChatPromptTemplate.from_messages([system_message, human_message])
parser = StrOutputParser()

chain = jira_prompt | _llm | parser
def analyze_sentiment(text: str) -> dict:
    """Run sentiment analysis and return label + score."""
    result = sentiment_pipeline(text)[0]
    return {
        "label": result["label"].lower(),
        "score": result["score"]
    }
def getSentimentResponse( sentiment: str, query: str):
    inputs = {
        "user_query": query,
        "sentiment": sentiment
    }
    jira_ticket_summary_response = chain.invoke(inputs)
    return jira_ticket_summary_response

def sentiment_node(state: BankingState):
    """
    LangGraph node for sentiment analysis.
    Creates a JIRA ticket if negative sentiment with high confidence.
    """
    try:
        if "actions" in state.intents: 
          query = state.user_query
          sentiment_result = analyze_sentiment(state.user_query)
          sentiment = sentiment_result["label"]
          score = sentiment_result["score"]
          print(f"*******{sentiment}")
          jira_ticket_summary_response = ""
        #   How can I dispute a transaction and what is the bank's refund policy?
          if sentiment == 'negative' :
            jira_ticket_summary_response = getSentimentResponse(sentiment, query)   
          
          response = f"{state.response} \n {jira_ticket_summary_response}"
          print(f"*******{response}")
          if sentiment == "negative":
              # TODO: integrate JIRA ticket creation
            #   result = create_jira_ticket(query)
              return {
                  "action_taken": "Jira created",
                  "status": "success",
                  "response": response,
                  "sentiment": sentiment
                  # "confidence": score
              }
        return {
            "action_taken": "Jira created",
            "status": "success",
            "response": response,
            "sentiment": sentiment
            # "confidence": score
        }

    except Exception as e:
        return {
            "action_taken": None,
            "status": "error",
            "response": f"Error in sentiment_node: {str(e)}"
        }
