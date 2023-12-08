def create_word_set():
    word_set = set()

    with open('word_list/word_list.txt', 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            word_set.add(word)

    with open('word_list/word_list2.txt', 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            word_set.add(word)
    
    return word_set