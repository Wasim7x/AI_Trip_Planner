import os
from logger import logging
from exception import MyException
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

class ModelLoader:
    def __init__(self, config: dict = None):
        self.config = config
        self.model_provider = config.get('provider').lower()
        self.model_name = config.get('model')
        self.api_key = config.get('api_key')

    def load_llm(self):
        """
        Load and return the LLM model.
        """
        logging.info(f"Loading model from provider: {self.config.get('provider')}")
        try:
            if self.model_provider == "groq":
                logging.info("Loading LLM from Groq..............")
                llm=ChatGroq(model=self.model_name, api_key=self.api_key)

            elif self.model_provider == "openai":
                logging.info("Loading LLM from OpenAI..............")              
                llm = ChatOpenAI(model_name=self.model_name, api_key=self.api_key)

        except Exception as e:
            raise MyException(f"Failed to load model from {self.model_provider} due to {e}")            
        
        return llm
    
                