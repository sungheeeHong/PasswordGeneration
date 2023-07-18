from inputEncoder import InputEncoder
import numpy as np
from gensim.models.fasttext import FastText

class Codebook():

    def __init__(self, 
                 pos_codebook_name = 'pos_codebook.npz'):
        # object list
        self.pos_codebook = np.load(pos_codebook_name)
        self.pos_codebook_dict = {}

        # what to do
        self._make_codebook_dict()

    # function list
    def _make_codebook_dict(self):
        for name in self.pos_codebook.files:
            self.pos_codebook_dict.update({name:self.pos_codebook[name]})

    def wv_to_pv(self, pos:str, wv):
        pos_name = f'{pos}_codebook'
        cb_list = self.pos_codebook_dict[pos_name]
        for i in range(len(cb_list)):
            if np.array_equal(cb_list[i][:128], wv):
                return cb_list[i][128:]
        print(f"Error: There is no word vector in {pos}_codebook")

    def pv_to_wv(self, pos:str, pv):
        pos_name = f'{pos}_codebook'
        cb_list = self.pos_codebook_dict[pos_name]
        for i in range(len(cb_list)):
            if np.array_equal(cb_list[i][128:], pv):
                return cb_list[i][:128]
        print(f"Error: There is no password vector in {pos}_codebook")
        
class OutputEncoder(Codebook): # secret sentence -> password

    def __init__(self, 
                 inputEncoder:InputEncoder,
                 wv_model_name = 'word_vector.model'):
        
        Codebook.__init__(self)
        
        # object list
        self.secret_sent = inputEncoder.secret_sent[:]
        print("self.secret_sent: ", self.secret_sent)
        self.sent_type = inputEncoder.sent_type[:]
        self.wv_model = FastText.load(wv_model_name)
        self.decode_model = {}
        self.wv = []
        self.pv = []
        self.pwd = []

        # what to do
        self._ss_to_wv()
        self.sent_type = [s.replace('_list', '') for s in self.sent_type]
        self._get_pwd_model()
        self._make_pw_vec()
        self._decode_pw_vec()
        self._print_result()

    # function list
    def _ss_to_wv(self):
        for word in self.secret_sent:
            temp = self.wv_model.wv[word]
            self.wv.append(temp)

    def _make_pw_vec(self):
        codebook = Codebook()
        for i in range(len(self.sent_type)):
            temp = codebook.wv_to_pv(pos=self.sent_type[i], wv=self.wv[i])
            self.pv.append(temp)

    def _get_pwd_model(self):
        decode_NN = FastText.load("NN_pwd.model")
        decode_VB = FastText.load("VB_pwd.model")
        decode_JJ = FastText.load("JJ_pwd.model")
        decode_RT = FastText.load("RT_pwd.model")
        self.decode_model.update({'NN':decode_NN, 
                                  'VB':decode_VB, 
                                  'JJ':decode_JJ, 
                                  'RT':decode_RT})
        
    def _decode_pw_vec(self):
        for i in range(len(self.sent_type)):
            pos = self.sent_type[i]
            print("pos: ", pos)
            model = self.decode_model[pos]
            temp = model.wv.most_similar([self.pv[i]], topn=1)
            pwd_tup = temp[0]
            self.pwd.append(pwd_tup[0])

    def _print_result(self):
        print('-'*20)
        print("This is your secret sentence")
        print(*self.secret_sent)
        print("")
        print("This is your password")
        print(*self.pwd, sep='')
        print('-'*20)