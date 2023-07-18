# class:InputEncoder
from preprocUserInput import PreprocUserInput
from gensim.models.fasttext import FastText
import numpy as np

class InputEncoder(PreprocUserInput):

    def __init__(self, 
                 preprocUserInput:PreprocUserInput, 
                 model_name = "word_vector.model", 
                 pos_list_name = "pos_list.npz", 
                 dot_product = None): # HE로 전환 시 class화 해서 여기에 끼우면 됨. 
        
        # object list
        self.preprocUserInput = preprocUserInput
        self.rand_seed = preprocUserInput.rand_int
        # self.server_input = preprocInput.server_input
        self.embed_input_list = preprocUserInput.embed_input_list
        self.sent_type = []
        self.model = FastText.load(model_name)
        self.pos_list = np.load(pos_list_name)
        self.dot = dot_product

        # what to run
        self._choose_sent_type()
        if self.dot == None:
            self.dot = self._get_bulk_dot_product
        self._search_over_threshold()

    # function list
    def _choose_sent_type(self):
        if self.rand_seed % 2 == 0:
            self.sent_type = ['NN_list', 'VB_list', 'NN_list', 'NN_list']
        else:
            self.sent_type = ['NN_list', 'VB_list', 'NN_list', 'JJ_list']

    def _get_wv_from_pos_list(self, pos_list:list):
        result = []
        for i in range(len(pos_list)):
            wv = self.model.wv[pos_list[i]]
            norm_wv = self.preprocUserInput.normalize(wv)
            result.append(norm_wv)
        return result
    
    def _get_bulk_dot_product(self, selected_pos_wv, embed_input_list):
        # HE 이전, 평문 상에서 HE와 최대한 비슷하게 구현하기 위해 만든 함수
        # selected_pos_wv에 있는 모든 단어들과 embed_input_list의 cos 계산 값을 array로 전달. 
        result = []
        for i in range(len(selected_pos_wv)):
            cos_sim = np.dot(selected_pos_wv[i], embed_input_list)
            result.append(cos_sim)
        return result
    
    def _search_over_threshold(self, threshold = 0.7):
        index_result = []
        choosed_cos_sim = []

        for i in range(len(self.sent_type)):
            selected_pos = self.pos_list[self.sent_type[i]]
            selected_pos_wv = self._get_wv_from_pos_list(selected_pos)
            cos_result = self.dot(selected_pos_wv=selected_pos_wv, embed_input_list=self.embed_input_list[i])
            
            length = len(selected_pos)
            index = self.rand_seed % length
            start_index = index
            while True:
                if cos_result[index] > 0.7:
                    index_result.append(index)
                    choosed_cos_sim.append(cos_result[index])
                    break
                index += 1
                if index == length: # 끝 점에 도달하면 초기화
                    index = 0
                if index == start_index:
                    print(f"Nothing similar with {self.sent_type[i]}")
                    break
        
        secret_sent = self._show_word_from_index(index_result=index_result)
        self._print_result(secret_sent=secret_sent, choosed_cos_sim=choosed_cos_sim)

    def _show_word_from_index(self, index_result:list):
        result = []
        for i in range(len(index_result)):
            sent_comp = self.sent_type[i]
            idx = index_result[i]
            result.append(self.pos_list[sent_comp][idx])
        result[0] = result[0].capitalize()
        return result

    def _print_result(self, secret_sent:list, choosed_cos_sim:list):
        print('-'*20)
        print("This is your input")
        print(*self.preprocUserInput.user_input, sep=' | ')
        print("")
        print("This is server input")
        print(*self.preprocUserInput.server_input, sep=' | ')
        print("")
        print("This is your secret sentence")
        print(*secret_sent)
        print("")
        print("This is each cosine similarity")
        print(*choosed_cos_sim, sep=' | ')
        print('-'*20)
