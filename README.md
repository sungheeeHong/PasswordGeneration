## Password Generation
main에서 작동 방식 확인 가능합니다. 

**1. genEmbedModel.ipynb -> GenEmbedModel_ver2.ipynb**<br>
: 프로그램 작동 전, embedding model들을 만드는 단계입니다. 
- pos_list.npz: 각 POS 별로 단어들의 리스트를 만들어 저장되어 있습니다.<br>
  ```
  pos_list = np.load("pos_list.npz")
  pos_list['NN_list']
  ```
- word_vector.model: 일반 단어를 word vector로 embedding하는 모델. 현재 FastText
- pos_codebook.npz: 각 POS 별로 codebook의 list를 만들어 저장

**2. preprocUserInput.py**<br>
: User input이 주어졌을 때, embedding을 비롯한 preprocessing을 하는 단계입니다. 

**3. inputEncoder.py**<br>
: preprocess된 input을 가지고 secret sentence를 만드는 단계입니다. 

**4. outputEncoder.py**<br>
: secret sentence를 가지고 password를 만드는 단계입니다. 

**CodebookModule**<br>
: 단어에 특정 password rule을 적용한 결과물을 짝지어 dictionary 형태로 만드는 함수입니다. 
