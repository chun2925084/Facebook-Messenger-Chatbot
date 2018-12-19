
from database_connect import read_question
from database_connect import read_solution

def send_question(text):
    k = read_question(text)
    print(k[0])
    return k[0]

def send_solution(text):
    k = read_solution(text)
    return k