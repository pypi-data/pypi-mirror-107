import requests

def ftc(fahrenheit):
    celsius = (fahrenheit - 32) / 1.8
    return celsius
    
def ctf(celsius):
    fahrenheit = (celsius * 1.8) + 32
    return fahrenheit