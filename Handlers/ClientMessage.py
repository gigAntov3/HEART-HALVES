def QuestionnaireMessage(selecttuple, i):
    text = selecttuple[i][0] + ', ' + str(selecttuple[i][1]) + ', ' + selecttuple[i][2] + '\n' + selecttuple[i][4]
    return text

def MyQuestionnaireMessage(selecttuple):
    text = selecttuple[0] + ', ' + str(selecttuple[1]) + ', ' + selecttuple[2] + '\n' + selecttuple[4]
    return text