import re

global unit_scale_dict
global ten_scale_dict
global other_scale_sict
global currency_dict


other_scale_sict = {

    "hundred":int(1e2),
    "thousand":int(1e3),
    "million":int(1e6),
    "billion":int(1e9),
    "trillion":int(1e12),
    "quadrillion":int(1e15)

}

ten_scale_dict = {

    "twenty":20,
    "thirty":30,
    "forty":40,
    "fifty":50,
    "sixty":60,
    "seventy":70,
    "eighty":80,
    "ninety":90
}

unit_scale_dict = {
    "one":1,
    "two":2,
    "three":3,
    "four":4,
    "five":5,
    "six":6,
    "seven":7,
    "eight":8,
    "nine":9,
    "ten":10,
    "eleven":11,
    "twelve":12,
    "thirteen":13,
    "fourteen":14,
    "fifteen":15,
    "sixteen":16,
    "seventeen":17,
    "eighteen":18,
    "nineteen":19
}

currency_dict = {
    "dollars":"$",
    "dollar":"$",
    "rupees":"₹",
    "rupee":"₹",
    "dirham":"د.إ",
    "dirhams": "د.إ",
    "yuan":"¥",
    "yuans": "¥",
    "euro":"€",
    "euros": "€",
    "pound":"£",
    "pounds": "£"
}

class Spoken2Written:
    def __init__(self):
        pass

    def space_separated_letters(self, sentence):
        return re.sub(r'(?<=\b\w)\s(?=\w\b)', "", sentence)

    def process_tuples(self, sentence):

        tuples_dict = {
            "single": 1,
            "double": 2,
            "triple": 3,
            "quadruple": 4
        }

        skip_single_letter_flag = -1
        newWordList = []
        newSent = ""

        wordList = sentence.split(" ")
        for i, word in enumerate(wordList):

            newWord = word

            if word in tuples_dict:
                if i + 1 <= len(wordList) - 1:
                    newWord = tuples_dict[word] * wordList[i + 1]
                    skip_single_letter_flag = i + 1

            if skip_single_letter_flag == i:
                continue

            newSent = newSent + " " + newWord

        return newSent.lstrip()

    def process_currency(self, sentence):

        wordList = sentence.split()
        newSent = ""
        newWord = ""
        number = 0
        newNum = 0
        isNumber = False

        for word in wordList:
            newWord = word

            if word in unit_scale_dict:
                newNum = unit_scale_dict[word]
                number = number + newNum
                continue
            if word in ten_scale_dict:
                newNum = ten_scale_dict[word]
                number = number + newNum
                continue
            if word in other_scale_sict:
                newNum = other_scale_sict[word]
                number = number * newNum
                continue
            if word == "and":
                continue
            if word in currency_dict:
                newWord = currency_dict[word] + str(number)
                number = 0

            newSent = newSent + " " + newWord

        return newSent.lstrip()

    def preprocess(self, sentence):

        sentence = re.sub("\t", "", sentence)
        sentence = re.sub("\n", " ", sentence)
        return sentence

    def convert(self, sentence):

        sentence = self.preprocess(sentence)
        sentence = self.space_separated_letters(sentence)
        sentence = self.process_tuples(sentence)
        sentence = self.process_currency(sentence)

        return sentence