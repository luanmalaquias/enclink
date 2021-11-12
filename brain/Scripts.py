import random
import string

def generateUrl():  
    let = string.ascii_letters
    tem = random.sample(let, 6)
    url = "".join(tem)
    return url