#SCORES_6 = [8640,720,720,720,720,120,120,120,20,20]
SCORES_6 = [13112, 1458, 1458, 1458, 1458, 162, 162, 162, 9, 9]
#SCORES_5 = [50000,720,720,720,720,720]
SCORES_5 = [59049, 1458, 1458, 1458, 1458, 1458]


WHITE_6PATTERNS = [[0, 1, 1, 1, 1, 0],
                   [0, 1, 1, 1, 0, 0],
                   [0, 0, 1, 1, 1, 0],
                   [0, 1, 1, 0, 1, 0],
                   [0, 1, 0, 1, 1, 0],
                   [0, 0, 1, 1, 0, 0],
                   [0, 0, 1, 0, 1, 0],
                   [0, 1, 0, 1, 0, 0],
                   [0, 0, 1, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0]]


WHITE_5PATTERNS = [[1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 0],
                   [0, 1, 1, 1, 1],
                   [1, 1, 0, 1, 1],
                   [1, 0, 1, 1, 1],
                   [1, 1, 1, 0, 1]]


BLACK_6PATTERNS = [[0, 2, 2, 2, 2, 0],
                   [0, 2, 2, 2, 0, 0],
                   [0, 0, 2, 2, 2, 0],
                   [0, 2, 2, 0, 2, 0],
                   [0, 2, 0, 2, 2, 0],
                   [0, 0, 2, 2, 0, 0],
                   [0, 0, 2, 0, 2, 0],
                   [0, 2, 0, 2, 0, 0],
                   [0, 0, 2, 0, 0, 0],
                   [0, 0, 0, 2, 0, 0]]


BLACK_5PATTERNS = [[2, 2, 2, 2, 2],
                   [2, 2, 2, 2, 0],
                   [0, 2, 2, 2, 2],
                   [2, 2, 0, 2, 2],
                   [2, 0, 2, 2, 2],
                   [2, 2, 2, 0, 2]]


def evaluate(vector):
    score = {'white': 0, 'black': 0}
    length = len(vector)

    if length == 5:
        for i in range(len(WHITE_5PATTERNS)):
            if WHITE_5PATTERNS[i] == vector:
                score['white'] += SCORES_5[i]
            if BLACK_5PATTERNS[i] == vector:
                score['black'] += SCORES_5[i]
        return score

    for i in range(length - 5):
        temp = [vector[i], vector[i + 1], vector[i + 2],
                vector[i + 3], vector[i + 4]]
        for i in range(len(WHITE_5PATTERNS)):
            if WHITE_5PATTERNS[i] == temp:
                score['white'] += SCORES_5[i]
            if BLACK_5PATTERNS[i] == temp:
                score['black'] += SCORES_5[i]

    for i in range(length - 6):
        temp = [vector[i], vector[i + 1], vector[i + 2],
                vector[i + 3], vector[i + 4], vector[i + 5]]
        for i in range(len(WHITE_6PATTERNS)):
            if WHITE_6PATTERNS[i] == temp:
                score['white'] += SCORES_6[i]
            if BLACK_6PATTERNS[i] == temp:
                score['black'] += SCORES_6[i]
    return score