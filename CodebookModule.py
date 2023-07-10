# 함수화 하기
def Codebook_HorizontalSliding(vocab:list):
    hor = {'hor1' : 'qwertyuiop', 'hor2' : 'asdfghjkl', 'hor3' : 'zxcvbnm'}
    coded_data = []
    for token in vocab:
        coded_temp = ''
        for a_index in range(len(token)):
            # out of range 처리
            if a_index + 1 == len(token):
                coded_data.append(coded_temp + token[a_index])
                break
            # 1. 연속된 두 단어가 같은 horizontal line 상에 있는지 확인
            if (token[a_index] in hor['hor1']) & (token[a_index + 1] in hor['hor1']):
                # startpoint, endpoint에 각각의 인덱스 저장
                startpoint = hor['hor1'].index(token[a_index])
                endpoint = hor['hor1'].index(token[a_index + 1])
                # 예외처리: startpoint, endpoint가 같은 경우
                if startpoint == endpoint:
                    coded_temp += token[a_index]
                    continue
                for i in range(startpoint, endpoint, 1 if endpoint > startpoint else -1):
                    coded_temp += hor['hor1'][i]
            elif (token[a_index] in hor['hor2']) & (token[a_index + 1] in hor['hor2']):
                # startpoint, endpoint에 각각의 인덱스 저장
                startpoint = hor['hor2'].index(token[a_index])
                endpoint = hor['hor2'].index(token[a_index + 1])
                # 예외처리: startpoint, endpoint가 같은 경우
                if startpoint == endpoint:
                    coded_temp += token[a_index]
                    continue
                for i in range(startpoint, endpoint, 1 if endpoint > startpoint else -1):
                    coded_temp += hor['hor2'][i]
            elif (token[a_index] in hor['hor3']) & (token[a_index + 1] in hor['hor3']):
                # startpoint, endpoint에 각각의 인덱스 저장
                startpoint = hor['hor3'].index(token[a_index])
                endpoint = hor['hor3'].index(token[a_index + 1])
                # 예외처리: startpoint, endpoint가 같은 경우
                if startpoint == endpoint:
                    coded_temp += token[a_index]
                    continue
                for i in range(startpoint, endpoint, 1 if endpoint > startpoint else -1):
                    coded_temp += hor['hor3'][i]
            else:
                coded_temp += token[a_index]
    codebook = {vocab[i] : coded_data[i] for i in range(len(vocab))}
    return codebook

def Codebook_ChangeVowel(vocab:list, substitute:str='QWERTY'): # substitute: 모음 대신 넣을 것(string)
    vowels = 'aeiou'
    coded_data = []

    for token in vocab:
        coded_temp = ''
        v_index = 0
        for alphabet in token:
            # out of range 처리
            if v_index == len(substitute):
                v_index = 0
            # 모음이 나오면 change로 변환
            if alphabet in vowels:
                coded_temp += substitute[v_index]
                v_index += 1
            else:
                coded_temp += alphabet
        coded_data.append(coded_temp)
    codebook = {vocab[i] : coded_data[i] for i in range(len(vocab))}
    return codebook

def SthToString(sth:list): # Input이 어떻게 들어올지 모르겠어서 일단 만들어둠. 원하는 모음을 대체할 것을 리스트 형태로 넣으면 string으로 변환해 돌려줌. 
    if len(sth) == 0:
        print("There is nothing in input. ")
        print("Default is QWERTY. ")
        string = 'QWERTY'
        return string
    elif len(sth) == 1:
        string = str(sth)
        return string
    else:
        for i in range(len(sth)):
            string += str(sth[i])
        return string
