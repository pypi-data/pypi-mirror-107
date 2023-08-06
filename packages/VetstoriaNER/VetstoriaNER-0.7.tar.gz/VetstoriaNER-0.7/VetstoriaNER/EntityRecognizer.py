import spacy
import os
import sys
from os import environ

class EntityRecognizer():
    def __init__(self,model_name=""):
        self.model_name = None
        if model_name:
            self.model_name = model_name 
        else:
            env_var = environ.get('MODEL_PATH')
            if env_var:
                self.model_name = env_var

        if self.model_name == None or self.model_name == "":
            raise Exception("Spacy model not found. Please pass model path Or define MODEL_PATH enviroment variable") 
            sys.exit(1)    
        else:
            try:
                self.nlp = spacy.load(self.model_name)
            except Exception as e:
                print(e,'\n>>> please pass the correct path to the model or the actual shortlinked name of the model')
                sys.exit(1)

    def recognizeSpecies(self,input_text):
        recognized_species_list = []
        doc = self.nlp(input_text)
        for ent in doc.ents:
            recognized_species_list.append(ent.text)

        if len(recognized_species_list)==0:
            return None
        else:    
            return recognized_species_list 
