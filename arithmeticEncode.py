from re import S
import numpy as np

chain = "111000111110000"

maxima = 0.0
arraychain = []
probabilidades = {}

wordTemp= ""
flag= 0
endOfChain= False

def wordInArray(word):
    if word in arraychain:
        return True
    return False


while not endOfChain:
    if flag == len(chain):
        endOfChain= True
        break
    wordTemp = chain[flag]
    
    if not wordInArray(wordTemp):
        arraychain.append(wordTemp)
        probabilidades[wordTemp] = chain.count(wordTemp) / len(chain)
        wordTemp= ""

    flag= flag + 1

if not wordTemp == "":
    arraychain.append(wordTemp)
    probabilidades[wordTemp] = chain.count(wordTemp) / len(chain)

tam = 3

array = []
intervalos = [0]

def createString(char):
    for word in arraychain:
        tempChar = char
        tempChar += word
        p = np.float64(probabilidades[char]) * probabilidades[word]
        probabilidades[tempChar] = float(np.format_float_scientific(p, precision=6))
        if len(tempChar) < tam:
            createString(tempChar)
        else:
            array.append(tempChar)
            intervalos.append(intervalos[-1] + probabilidades[tempChar])

def newDictionary():
    actualinter = 0
    newDict = {}
    for key, value in probabilidades.items():
        if len(key) == tam:
           array = [actualinter]
           actualinter += value
           array.append(actualinter)
           newDict[key] = array
           maxima = array[1]
    
    return newDict

def setChain():
    char = ""
    for word in chain:
        char = word
        createString(char)
    
    init_probs = {key: value for key, value in probabilidades.items() if len(key) == 1}
    new_dict = newDictionary()

    return init_probs, new_dict

def putSpaces(value):
    space= ""
    for _ in range(len(value), tam):
        space += " "
    value += space
    
    return value

# Codificacoin para actual y nuevo
def getChain():
    arrayChain = []
    actualPosition = 0
    newPosition = tam
    while newPosition < len(chain):
        arrayChain.append(chain[actualPosition:newPosition])
        actualPosition += tam
        newPosition += tam 
        
    arrayChain.append(putSpaces(chain[actualPosition:newPosition]))

    print(arrayChain)
    return arrayChain


def formula(a, b, arrayProbabilities):
    print(f"-> {a}, {b}, {arrayProbabilities}")
    return [a + (b - a)*arrayProbabilities[0], a + (b - a)*arrayProbabilities[1]]
    
def getValue():
    initProbs, newDictionary = setChain()
    arrayChain = getChain()
    actualArray = [0, 1]
    for value in arrayChain:
        arrayIntervalValues = newDictionary[value]
        print(f"{value} -> ", arrayIntervalValues)
        actualArray = formula(actualArray[0], actualArray[1], arrayIntervalValues)
        print(actualArray)
        print("---")
    
    return actualArray

def findInterval(valorActual, newDictionary):
    for key, value in newDictionary.items():
        if value[0] <= valorActual < value[1]:
            return key, value

def formulaDecodificacion(a, b, ai):
    print(f"-> {ai}, {a}, {b}")
    return ((ai - a) / (b - a))

def decodeChain():
    initProbs, newDictionary = setChain()
    encodedArray= getValue()
    valorActual = np.mean(encodedArray)
    arrayResponse = []
    for _ in range(0,10):
        findedKey, arrayTemp= findInterval(valorActual, newDictionary)
        valorActual = formulaDecodificacion(arrayTemp[0], arrayTemp[1], valorActual)
        arrayResponse.append(findedKey)

        print(str.join("", arrayResponse))
    
    print(newDictionary)
    print(initProbs)

decodeChain()
    
