# 단어 set을 초기화
word_set = set()

# 파일을 열기
with open('word_list/word_list.txt', 'r', encoding='utf-8') as file:
    # 파일의 각 줄을 읽기
    for line in file:
        # 줄의 앞뒤 공백 제거
        word = line.strip()
        # 단어를 set에 추가
        word_set.add(word)
        
with open('word_list/word_list2.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # 줄의 앞뒤 공백 제거
        word = line.strip()
        # 단어를 set에 추가
        word_set.add(word)

# 결과 출력
print(word_set)