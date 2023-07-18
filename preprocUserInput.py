# User의 Input 처리
from gensim.models.fasttext import FastText
import numpy as np
from nltk.tokenize import RegexpTokenizer
import random

class PreprocUserInput(): # input: user_input(list)

    def __init__(self, 
                 user_input:list, 
                 model_name = "word_vector.model", 
                 tokenizer = RegexpTokenizer("[\w]+"),
                 vector_size = 128):
        
        # object list
        self.user_input = user_input
        self.server_input = user_input[:]
        self.model_name = model_name
        self.tokenizer = tokenizer
        self.vector_size = vector_size
        self.rand_int = 0
        self.embed_input_list = []
        
        # what to run
        self._mix_input()
        self.embed_inputs()

    # function list
    def _mix_input(self): # user input -> server input
        self.rand_int = random.randint(0, 10000)
        self.server_input.append(self.rand_int)
        random.shuffle(self.server_input)
    
    def _randint_to_vec(self, rand_int):
        seed = rand_int
        random.seed(seed)
        np.random.seed(seed)
        random_vector = np.random.rand(self.vector_size)
        return self.normalize(random_vector)

    def embed_word(self, word:str):
        model = FastText.load(self.model_name)
        emb_word = model.wv[word]
        return self.normalize(emb_word)
    
    def normalize(self, emb_word):
        norm = np.linalg.norm(emb_word, ord=2)
        result = np.abs(emb_word / norm)
        return result
    
    def _embed_sentence(self, sentence:str):
        tokens = self.tokenizer.tokenize(sentence)
        model = FastText.load(self.model_name)

        embedding_matrix = []
        for token in tokens:
            embedding_matrix.append(model.wv[token])
        
        embedding_matrix = np.array(embedding_matrix)
        word_indices = list(range(len(embedding_matrix)))
        word_embeddings = embedding_matrix[word_indices]
        sentence_embedding = np.max(word_embeddings, axis = 0)
        return self.normalize(sentence_embedding)
    
    def embed_inputs(self):
        for input in self.server_input:
            if type(input) is int:
                embed = self._randint_to_vec(input)
            elif ' ' in input:
                embed = self._embed_sentence(input)
            else:
                embed = self.embed_word(input)
            self.embed_input_list.append(embed)