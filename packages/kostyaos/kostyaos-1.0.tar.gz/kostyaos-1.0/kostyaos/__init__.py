def dos():
    input0 = input("COMMAND ")
    input1 = input("FIRST ATTRIBUTE ")
    input2 = input("SECOND ATTRIBUTE ")
    input3 = input("THIRD ATTRIBUTE ")
    if input0.lower() == 'help':
        print("Сommand: desktop   It is for: download desktop version (I created this apps with web2desk)    Command: donut   It is for: motivation for developers    Command: support   It is for: support (yes, it's all)   Сommand: wiki   It is for: know more about Kostya OS  Сommand: edit   It is for: edit source code of Kostya OS   Command: grint   It is for: go to graрhic interface   Command: links   It is for: connect for me   Command: cube   First attribute: int   It is for: put the int to cube    Command: quad   First attribute: int   It is for: put the int to quadrate    Command: exp   First attribute: int   Second attribute: exponitiation   It is for: put the int to exponitiation    Command: math   First attribute: int   Second attribute: +, -, *, or /   Third attribute: int   It is for: calculate    Command: versions   If you dont like new versions, you can use old    Command: kostyaos, kostya-os, info   It is for: Know version of OS   Command: lang   It is for: go to the another language (The English version is more advanced than the other languages,   'https://kostya-os.ru'>here it is. )  <h6>boot<h6>   ")
        input0 = ''
    
    elif input0.lower() == "desktop":
        print('This links teleport you to disk.yandex.ru, https://disk.yandex.ru/d/BE8lHDAR-u9HJg Windows, https://disk.yandex.ru/d/CyqgTPD5dLdZ5A macOS, https://disk.yandex.ru/d/WWC1t8wH8Ps7cg linux.')
    
    elif input0.lower() == "donut":
        print(' "https://vk.com/donut/kostyaos">Donut for developers ')
    
    elif input0.lower() == "support":
        print(' "https://vk.com/kostyaos">Support of Kostya OS ')
    
    elif input0.lower() == "wiki":
        print(' "https://kostya-os.ru/wiki.html">Wiki of Kostya OS ')
    
    elif input0.lower() == "edit":
        print(' "https://kostya-os.ru/edit.html">Edit page ')
    
    elif input0.lower() == 'versions':
        print(' "https://kostya-os.ru/versions/">All versions ')  
    
    elif input0.lower() == "grint":
        print('https://kostya-os.ru/graphic.html')
    
    elif input0.lower() == 'kostyaos' or input0.lower() == 'kostya-os' or input0.lower() == 'info':
        print('Kostya OS version PYTHON edition © 2020 - 2021 Konstantin Babin')
    
    elif input0.lower() == 'lang':
        print('It is English version. There is:  "https://kostya-os.ru/versions/russian.html" Русская версия(не обновляется) ')
    
    elif input0.lower() == 'cube':
        print(input1 * input1 * input1)
    
    elif input0.lower() == 'quad':
        print(int(input1) * int(input1))
    
    elif input0.lower() == 'exp':
        exp = int(input1)
        for i in range(int(input2)): 
            exp = exp * int(input1)
        
        print(exp)     
    
    elif input0.lower() == 'links':
        print( "Hi, I'm Kostya, it is links for connect to me:  'https://vk.com/kostyaos'>My account in VK   'tel:89257929718'>My phone int   'mailto:holojva@gmail.com'>My Email ")
    elif input0.lower() == 'math' :
        if input2 == '*' :
            print(int(input1) * int(input3))
            input0 = ''
            input1 = ''
            input2 = ''
            input3 = ''
        
        if input2 == '+':
            print(int(input1) + int(input3))
            input0 = ''
            input1 = ''
            input2 = ''
        
        if input2 == '-':
            print(int(input1) - int(input3))
            input0 = ''
            input1 = ''
            input2 = ''
        
        if input2 == '/':
            print(int(input1) / int(input3))
            input0 = ''
            input1 = ''
            input2 = ''
        
    elif input0.lower() == 'boot':
        print('How I boot in browser?!   Where is your brain?!')
    
    
    else:
        print('What is you said?' + ' ' + input0)
while True :
    dos()

 

