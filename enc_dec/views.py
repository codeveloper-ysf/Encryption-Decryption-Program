from django.shortcuts import render
import math
import random
from .models import Method
# Create your views here.


def homePage(request):
    methods = Method.objects.all()
    return render(request, 'enc_dec/homepage.html', {'methods': methods})


def cipher(request, pk):
    method = Method.objects.get(pk=pk)
    message = request.GET.get("message")
    encrypt = request.GET.get("crypt")
    result = ""
    if(method.name == "Caesar Cipher"):
        shiftPattern = request.GET.get("shiftPattern")
        if(message != None and shiftPattern != None):
            if(encrypt == "true"):
                result = Caesar.encryption(message, int(shiftPattern))
            else:
                result = Caesar.decryption(message, int(shiftPattern))
    elif(method.name == "Vigenere Cipher"):
        key = request.GET.get("key")
        if(message != None and key != None):
            if(len(key) <= len(message)):
                if(encrypt == "true"):
                    result = Vigenere.encryption(message, key)
                else:
                    result = Vigenere.decryption(message, key)
            else:
                result = "Error: len(vigenere_key)>len(message)"
    elif(method.name == "Shifting"):
        shiftPattern = request.GET.get("shiftPattern")
        if(message != None and shiftPattern != None):
            if(encrypt == "true"):
                result = Shifting.encryption(message, int(shiftPattern))
            else:
                result = Shifting.decryption(message, int(shiftPattern))
    elif(method.name == "Private Library"):
        if(message != None):
            if(encrypt == "true"):
                result = Private.encryption(message)
            else:
                result = Private.decryption(message)
    return render(request, 'enc_dec/method.html', {"method": method, "result": result})


class Caesar():
    def encryption(text, s):
        result = ""
        for i in range(len(text)):
            char = text[i]
            if (char.isupper()):
                result += chr((ord(char) + s-65) % 26 + 65)
            else:
                result += chr((ord(char) + s - 97) % 26 + 97)
        return result

    def decryption(message, key):
        key = -key
        encrypted = ''
        for symbol in message:
            if symbol.isalpha():
                num = ord(symbol)
                num += key
                if symbol.isupper():
                    if num > ord('Z'):
                        num -= 26
                    elif num < ord('A'):
                        num += 26
                elif symbol.islower():
                    if num > ord('z'):
                        num -= 26
                    elif num < ord('a'):
                        num += 26
                encrypted += chr(num)
            else:
                encrypted += symbol
        return encrypted


class Vigenere():

    def new_alph(char):
        char = char.lower()
        alph = 'abcdefghijklmnopqrstuvwxyz'
        new_alph = alph[alph.index(char):] + alph[:alph.index(char)]
        return new_alph

    def encryption(text, big_key):
        res = ''
        alph = 'abcdefghijklmnopqrstuvwxyz'
        if len(big_key) <= len(text):
            big_key = big_key * (len(text) // len(big_key)) + \
                big_key[:len(text) % len(big_key)]
        i = 1
        for char in big_key:
            new = Vigenere.new_alph(char)
            for t in text:
                if alph.count(t) == 1:
                    res += new[alph.index(t)]
                    text = text[i:]
                    break
                elif alph.count(t.lower()) == 1:
                    res += new[alph.index(t.lower())].upper()
                    text = text[i:]
                    break
                else:
                    res += t
                    text = text[i:]
                    break
                i += 1
        return res

    def decryption(text, big_key):
        res = ''
        alph = 'abcdefghijklmnopqrstuvwxyz'
        if len(big_key) <= len(text):
            big_key = big_key * (len(text) // len(big_key)) + \
                big_key[:len(text) % len(big_key)]
        i = 1
        for char in big_key:
            new = Vigenere.new_alph(char)
            for t in text:
                if alph.count(t) == 1:
                    res += alph[new.index(t)]
                    text = text[i:]
                    break
                elif alph.count(t.lower()) == 1:
                    res += alph[new.index(t.lower())].upper()
                    text = text[i:]
                    break
                else:
                    res += t
                    text = text[i:]
                    break
                i += 1
        return res


class Shifting():
	def encryption(message, key):
		leftFirst = message[0 : key]
		leftSecond = message[key :]
		return (leftSecond + leftFirst)

	def decryption(message, key):
		rightFirst = message[0: len(message)-key]
		rightSecond = message[len(message)-key : ]
		return (rightSecond + rightFirst)


class Private():
    encryption_letters = {'a': 'b', 'b': 'e', 'c': 'v', 'd': 'j', 'e': 'Q', 'f': 'w', 'g': 'T', 'h': 'l', 'i': 'O', 'j': 'y', 'k': 'A', 'l': 'W', 'm': 'N',
                          'n': 'c', 'o': 'h', 'p': 'F', 'q': 'o', 'r': 'D', 's': 'M', 't': 'C', 'u': 'J', 'x': 'L', 'w': 'Y', 'v': 'I', 'y': 'x', 'z': 'E',
                          'A': 'K', 'B': 'X', 'C': 'B', 'D': 'i', 'E': 'R', 'F': 'd', 'G': 'S', 'H': 'H', 'I': 'n', 'J': 'P', 'K': 'f', 'L': 'U', 'M': 's',
                          'N': 'r', 'O': 'g', 'P': 't', 'Q': 'Z', 'R': 'G', 'S': 'm', 'T': 'z', 'U': 'q', 'X': 'V', 'W': 'p', 'V': 'u', 'Y': 'k', 'Z': 'a',
                          ' ': '.', '?': '!', '.': '?', '!': "'", "'": ' '}

    decryption_letters = {'a': 'Z', 'b': 'a', 'e': 'b', 'v': 'c', 'j': 'd', 'Q': 'e', 'w': 'f', 'T': 'g', 'l': 'h', 'O': 'i', 'y': 'j', 'A': 'k',
                          'W': 'l', 'N': 'm', 'c': 'n', 'h': 'o', 'F': 'p', 'o': 'q', 'D': 'r', 'M': 's', 'C': 't', 'J': 'u', 'L': 'x',
                          'Y': 'w', 'I': 'v', 'x': 'y', 'E': 'z', 'K': 'A', 'X': 'B', 'B': 'C', 'i': 'D', 'R': 'E', 'd': 'F', 'S': 'G',
                          'H': 'H', 'n': 'I', 'P': 'J', 'f': 'K', 'U': 'L', 's': 'M', 'r': 'N', 'g': 'O', 't': 'P', 'Z': 'Q', 'G': 'R',
                          'm': 'S', 'z': 'T', 'q': 'U', 'V': 'X', 'p': 'W', 'u': 'V', 'k': 'Y', '.': ' ', '!': '?', '?': '.', "'": '!', ' ': "'"}

    def encryption(message):
        encrypted = ""
        for i in message:
            encrypted += Private.encryption_letters[i]
        return encrypted

    def decryption(message):
        decrypted = ""
        for i in message:
            decrypted += Private.decryption_letters[i]
        return decrypted
