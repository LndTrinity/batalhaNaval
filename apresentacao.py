from colorama import Fore, Style
import random 
import os
import time
import math

jogo = []
jogoPlayer = []
jogoPlayer_ = []
alfabeto = [chr(i) for i in range(ord('A'), ord('Z')+1)]
cores = [Fore.BLUE,Fore.CYAN,Fore.GREEN,Fore.LIGHTBLACK_EX,Fore.MAGENTA,Fore.RED,Fore.YELLOW]

coordenadaTentada = []
playerNome = ""
playerPontos = 0
acertos= []
acertosPA = []
acertosPH = []
acertosCru = []
acertosFra = []
playerPosicoesPH = []
playerPosicoesPA = []
playerPosicoesCRU = []
playerPosicoesFra = []
zonaDeColisao = []

BotCoordenadaTentada = []
BotAcertos= []
BotAcertosPA = []
BotAcertosPH = []
BotAcertosCru = []
BotAcertosFra = []
BotCheckPoint = []
BotInstruções = [[+1,0],[-1,0],[0,+1],[0,-1]]
BotInstruçõesEx = []
BotProximoTiro = []

tamanhoHorizontal = int(10)
tamanhoVertical = int(10)
tamanhoPH = 5
tamanhoPA = 7
tamanhoCRU = 3
tamanhoFra = 3

mostrarResposta = 0
contaRodadas = 0
playerNavios = 4
botNavios = 4
mensagem = ""
def ranking():
    if os.path.isfile("ranking.txt"):
        with open("ranking.txt", "r") as arq:
            ranking = arq.readlines()
            return ranking
    else:
        return ""

def verifica_colisao():
    retorno = 0
    for i in range(1, len(playerPosicoesPH)):
        item = playerPosicoesPH[i]
        if item in zonaDeColisao:
            retorno = 1
        
    for i in range(1, len(playerPosicoesPA)):
        item = playerPosicoesPA[i]
        if item in zonaDeColisao:
            retorno = 2
        
    for i in range(1, len(playerPosicoesCRU)):
        item = playerPosicoesCRU[i]
        if item in zonaDeColisao:
            retorno = 3
        
    for i in range(1, len(playerPosicoesFra)):
        item = playerPosicoesFra[i]
        if item in zonaDeColisao:
            retorno = 4
    if retorno != 0:
        return retorno
    else:
        return False
def adiciona_zona_colisao():
    zonaDeColisao.clear()
    adicionar_zona_navio(playerPosicoesPH, tamanhoPH)
    adicionar_zona_navio(playerPosicoesPA, tamanhoPA)
    adicionar_zona_navio(playerPosicoesCRU, tamanhoCRU)
    adicionar_zona_navio(playerPosicoesFra, tamanhoFra)

def adicionar_zona_navio(posicoes, tamanho):
    if posicoes[0] == "horizontal":
        adicionar_zona_horizontal(posicoes, tamanho)
    elif posicoes[0] == "vertical":
        adicionar_zona_vertical(posicoes, tamanho)

def adicionar_zona_horizontal(posicoes, tamanho):
    for i in range(1, len(posicoes)):
        x, y = map(int, posicoes[i])
        zonaDeColisao.append([x - 1, y])
        zonaDeColisao.append([x + 1, y])
    # Adiciona extremidades horizontais
    x, y = map(int, posicoes[-1])
    zonaDeColisao.append([x, y + 1])
    zonaDeColisao.append([x, y - tamanho])

def adicionar_zona_vertical(posicoes, tamanho):
    for i in range(1, len(posicoes)):
        x, y = map(int, posicoes[i])
        zonaDeColisao.append([x, y + 1])
        zonaDeColisao.append([x, y - 1])
    # Adiciona extremidades verticais
    x, y = map(int, posicoes[-1])
    zonaDeColisao.append([x + 1, y])
    zonaDeColisao.append([x - tamanho, y])

def verifica_colisao2(tabuleiro, ph_x,ph_y,ph_v,  pA_x,pA_y,pA_v,  cor_x,cor_y,cor_v,  fra_x,fra_y,fra_v):
    retorno = 0
    x = jogo
    if tabuleiro != 'bot':
        x = jogoPlayer_

    if ph_v <= 5:
        i = int(ph_x)
        while i < ph_x + tamanhoPH:
            if x[ph_y][i] != "🟠":
                # print(f"colidiu {x[ph_y][i]}")
                retorno = 1
            i += 1
    else:
        i = int(ph_y)
        while i < ph_y + tamanhoPH:
            if x[i][ph_x] != "🟠":
                # print(f"colidiu {x[i][ph_x]}")
                retorno = 1
            i += 1

    if pA_v <= 5:
        i = int(pA_x)
        while i < pA_x + tamanhoPA:
            if x[pA_y][i] != "🟡":
                # print(f"colidiu {x[pA_y][i]}")
                retorno = 1
            i += 1
    else:
        i = int(pA_y)
        while i < pA_y + tamanhoPA:
            if x[i][pA_x] != "🟡":
                # print(f"colidiu {x[i][pA_x]}")
                retorno = 1
            i += 1

    if cor_v <= 5:
        i = cor_x
        while i < cor_x + tamanhoCRU :
            if x[cor_y][i] != "🟢":
                # print(f"colidiu {x[cor_y][i]}")
                retorno = 1
            i += 1
    else:
        i = cor_y
        while i < cor_y + tamanhoCRU :
            if x[i][cor_x] != "🟢":
                # print(f"colidiu {x[i][cor_x]}")
                retorno = 1
            i += 1

    if fra_v <= 5:
        i = fra_x
        while i < fra_x + tamanhoFra :
            if x[fra_y][i] != "🟣":
                # print(f"colidiu {x[fra_y][i]}")
                retorno = 1
            i += 1
    else:
        i = fra_y
        while i < fra_y + tamanhoFra :
            if x[i][fra_x] != "🟣":
                # print(f"colidiu {x[i][fra_x]}")
                retorno = 1
            i += 1
    if retorno >= 1:
        return True
    else:
        return False

     
def randomizador(enviar):

    #porta helicopteros
    ph_v = random.randint(0,10)
    if ph_v <= 5: # é hotizontal
        ph_x = random.randint(0,tamanhoHorizontal - 6) #define as coordenadas iniciais (horizontal)
        ph_y = random.randint(0,tamanhoVertical - 1) #define a coordenada inicial vertical
    else:         # é vertical
        ph_x = random.randint(0,tamanhoHorizontal - 1) #define as coordenadas iniciais (horizontal)
        ph_y = random.randint(0,tamanhoVertical - 6) #define a coordenada inicial vertical

    #porta avioes
    pA_v = random.randint(0,10)
    if pA_v <= 5: # é horizontal
        pA_x = random.randint(0,tamanhoHorizontal - 10) #define as coordenadas iniciais do porta Avioes (horizontal)
        pA_y = random.randint(0,tamanhoVertical- 1 ) #define as coordenadas iniciais do porta Avioes  (vertical)       
    else:
        pA_x = random.randint(0,tamanhoHorizontal - 1) #define as coordenadas iniciais do porta Avioes (horizontal)
        pA_y = random.randint(0,tamanhoVertical - 10) #define as coordenadas iniciais do porta Avioes  (vertical)
    
    #corveta
    cor_v = random.randint(0,10)
    if cor_v <= 5: # e horizontal
        cor_x = random.randint(0,tamanhoHorizontal - 4)
        cor_y = random.randint(0,tamanhoVertical- 1)
    else:
        cor_x = random.randint(0,tamanhoHorizontal -1 )
        cor_y = random.randint(0,tamanhoVertical - 4)

    #fragata
    fra_v = random.randint(0,10)
    if fra_v <= 5:
        fra_x = random.randint(0,tamanhoHorizontal - 4)
        fra_y = random.randint(0,tamanhoVertical - 1)
    else:
        fra_x = random.randint(0,tamanhoHorizontal - 1)
        fra_y = random.randint(0,tamanhoVertical - 4)

    # print(ph_x,ph_y,ph_v,  pA_x,pA_y,pA_v,  cor_x,cor_y,cor_v,  fra_x,fra_y,fra_v)

    if enviar == 1:
        monta_jogo(ph_x,ph_y,ph_v,  pA_x,pA_y,pA_v,  cor_x,cor_y,cor_v,  fra_x,fra_y,fra_v)
        
    else:
        return ph_x,ph_y,ph_v,  pA_x,pA_y,pA_v,  cor_x,cor_y,cor_v,  fra_x,fra_y,fra_v
def monta_jogo(ph_x,ph_y,ph_v,  pA_x,pA_y,pA_v,  cor_x,cor_y,cor_v,  fra_x,fra_y,fra_v):
    for i in range (0,tamanhoVertical):
        _ = 0
        
        jogo.append([])
        while _ < tamanhoHorizontal:
            jogo[i].append("🔵")
            _ += 1

        
    if ph_v <= 5:
        i = ph_x
        while i < ph_x + tamanhoPH and i <= tamanhoHorizontal and i <= tamanhoVertical:
            jogo[ph_y][i] = "🟠"
            i += 1
    else:
        i = ph_y
        while i < ph_y + tamanhoPH and i <= tamanhoHorizontal and i <= tamanhoVertical:
            jogo[i][ph_x] = "🟠"
            i += 1

    if pA_v <= 5:
        i = pA_x
        while i < pA_x + tamanhoPA and i <= tamanhoHorizontal and i <= tamanhoVertical:
            jogo[pA_y][i] = "🟡"
            i += 1
    else:
        i = pA_y
        while i < pA_y + tamanhoPA and i <= tamanhoHorizontal and i <= tamanhoVertical:
            jogo[i][pA_x] = "🟡"
            i += 1

    if cor_v <= 5:
        i = cor_x
        while i < cor_x + tamanhoCRU and i <= tamanhoHorizontal and i <= tamanhoVertical:
            jogo[cor_y][i] = "🟢"
            i += 1
    else:
        i = cor_y
        while i < cor_y + tamanhoCRU and i <= tamanhoHorizontal and i <= tamanhoVertical:
            jogo[i][cor_x] = "🟢"
            i += 1

    if fra_v <= 5:
        i = fra_x
        while i < fra_x + tamanhoFra and i < tamanhoHorizontal and i <= tamanhoVertical:
            jogo[fra_y][i] = "🟣"
            i += 1
    else:
        i = fra_y
        while i < fra_y + tamanhoFra and i < tamanhoHorizontal and i <= tamanhoVertical :
            jogo[i][fra_x] = "🟣"
            i += 1


    verificaColisao = verifica_colisao2("bot", ph_x,ph_y,ph_v,  pA_x,pA_y,pA_v,  cor_x,cor_y,cor_v,  fra_x,fra_y,fra_v)
    if verificaColisao:
        return False
    else:
        return True
   
def mostrar():

    print(" ", end="")
    for x in range (0, tamanhoHorizontal):
        print(f" {alfabeto[x]}", end="")
    print()
  
    for i in range (0,tamanhoVertical): #altura
        print(alfabeto[i], end="")
        
        j = 0
        while j < tamanhoHorizontal:   
            print(f'{jogo[i][j]}', end="")
            j += 1
        print()
def mostrar_dois(mostrarResposta):
    # os.system("cls")

    print(" ", end="")
    for x in range (0, tamanhoHorizontal):
        print(f" {alfabeto[x]}", end="")
    print()

    for i in range (0,tamanhoVertical): #altura
        print(alfabeto[i], end="")
        
        j = 0
        while j < tamanhoHorizontal:
            if mostrarResposta == 1:
                print(jogo[i][j])
            else:
                if jogo[i][j] != "🔵":
                    if jogo[i][j] == "❌":
                        print("❌")
                    else:
                        print("🔵")
                else:
                    print(f'{jogo[i][j]}', end="")
            j += 1

        print(' ', end="")
        print(f"{alfabeto[i]}", end="")
        print()
def verifica_afundar(navio):
    mensagem = ""
    if navio == "ph":
        if len(acertosPH) > tamanhoPH - 1:
            mensagem = "Afundamos um Porta helicopteros inimigo"
            return "ph", mensagem 
        else:
            return False  
    if navio == "pa":
        if len(acertosPA) > tamanhoPA - 1:
            mensagem = "Afundamos um Porta aviões inimigo"
            return "pa", mensagem
        else:
            return False
    if navio == "cru":
        if len(acertosCru) > tamanhoCRU - 1:
            mensagem = "Afundamos uma Corveta inimiga"
            return "cru", mensagem
        else:
            return False
    if navio == "fra":
        if len(acertosFra) > tamanhoFra - 1:
            mensagem = "Afundamos uma Fragata inimiga"
            return "fra", mensagem
        else:
            return False
def afundar(navio): 
    global botNavios
    lista = []
    if navio == "ph":
        lista = acertosPH
    elif navio == "pa":
        lista = acertosPA
    elif navio == "cru":
        lista = acertosCru
    elif navio == "fra":
        lista = acertosFra

    for i_ in range(0, len(lista)):
                coordenadas = lista
                coordenadas2 = coordenadas[i_]
                x = coordenadas2[0]
                y = coordenadas2[1]
                jogo[x][y] = "❌"  
    botNavios -= 1
def verifica_acerto(x,y):
    global playerPontos
    mensagem = ""
    afundou = ""
    if jogo[x][y] != "🔵":
        if jogo[x][y] == "🟠":
            jogo[x][y] = '🔴'
            acertosPH.append([x,y])
            afundou = verifica_afundar("ph")
            if afundou:
                afundar("ph")
                playerPontos = playerPontos + tamanhoPH * 10
                mensagem = afundou[1]
            else:
                playerPontos = playerPontos + 10
                mensagem = "Acertamos algo Capitão"

        elif jogo[x][y] == "🟡":
            jogo[x][y] = '🔴'
            acertosPA.append([x,y])
            afundou = verifica_afundar("pa")
            if afundou:
                afundar("pa")
                playerPontos = playerPontos + 10 * tamanhoPA
                mensagem = afundou[1]
            else:
                playerPontos = playerPontos + 10
                mensagem = "Acertamos algo Capitão"

        elif jogo[x][y] == "🟢":
            jogo[x][y] = '🔴'
            acertosCru.append([x,y])
            afundou = verifica_afundar("cru")
            if afundou:
                afundar("cru")
                playerPontos = playerPontos + 10 * tamanhoCRU
                mensagem = afundou[1]
            else:
                playerPontos = playerPontos + 10
                mensagem = "Acertamos algo Capitão"

        elif jogo[x][y] == "🟣":
            jogo[x][y] = '🔴'
            acertosFra.append([x,y])
            afundou = verifica_afundar("fra")
            if afundou:
                afundar("fra")
                playerPontos = playerPontos + 10 * tamanhoFra
                mensagem = afundou[1]
            else:
                playerPontos = playerPontos + 10
                mensagem = "Acertamos algo Capitão"
        acertos.append([x,y])

        return mensagem
    else:
        jogo[x][y] = "⚫"
        return False
def monta_jogo2():
    jogoPlayer_.clear()
    for i in range (0,tamanhoVertical):
        _ = 0
        
        jogoPlayer_.append([])
        while _ < tamanhoHorizontal:
            jogoPlayer_[i].append("🔵")
            _ += 1

def monta_jogo_set_ph(x,y,v):
    playerPosicoesPH.clear()
    if v <= 5:
        i = x
        playerPosicoesPH.append('horizontal')
        while i < x + tamanhoPH:
            jogoPlayer_[y][i] = "🟠"
            playerPosicoesPH.append([y,i])
            i += 1
    else:
        i = y
        playerPosicoesPH.append('vertical')
        while i < y + tamanhoPH:
            jogoPlayer_[i][x] = "🟠"
            playerPosicoesPH.append([i,x])
            i += 1
def monta_jogo_set_pa(x,y,v):
    playerPosicoesPA.clear()
    if v <= 5:
        i = x
        playerPosicoesPA.append('horizontal')
        while i < x + tamanhoPA:
            jogoPlayer_[y][i] = "🟡"
            playerPosicoesPA.append([y,i])
            i += 1
    else:
        i = y
        playerPosicoesPA.append('vertical')
        while i < y + tamanhoPA:
            jogoPlayer_[i][x] = "🟡"
            playerPosicoesPA.append([i,x])
            i += 1
def monta_jogo_set_cru(x,y,v):
    playerPosicoesCRU.clear()
    if v <= 5:
        i = x
        playerPosicoesCRU.append('horizontal')
        while i < x + tamanhoCRU and i < tamanhoHorizontal and i <= tamanhoVertical:
            jogoPlayer_[y][i] = "🟢"
            playerPosicoesCRU.append([y,i])
            i += 1
    else:
        i = y
        playerPosicoesCRU.append('vertical')
        while i < y + tamanhoCRU and i < tamanhoHorizontal and i <= tamanhoVertical:
            jogoPlayer_[i][x] = "🟢"
            playerPosicoesCRU.append([i,x])
            i += 1
def monta_jogo_set_fra(x,y,v):
    playerPosicoesFra.clear()
    if v <= 5:
        i = x
        playerPosicoesFra.append("horizontal")
        while i < x + tamanhoFra and i < tamanhoHorizontal and i <= tamanhoVertical:
            jogoPlayer_[y][i] = "🟣"
            playerPosicoesFra.append([y,i])
            i += 1
    else:
        i = y
        playerPosicoesFra.append("vertical")
        while i < y + tamanhoFra and i < tamanhoHorizontal and i <= tamanhoVertical :
            jogoPlayer_[i][x] = "🟣"
            playerPosicoesFra.append([i,x])
            i += 1

    
def mostrar_player():
    # os.system("cls")
    print("  ", end="")
    
    for x in range (0, tamanhoHorizontal):
        print(f" {alfabeto[x]}", end="")
    print()

    for i in range (0,tamanhoVertical): #altura
        if i < 9:
            print(f" {i + 1}", end='')
        else:
            print(f"{i + 1}", end='')
        
        j = 0
        while j < tamanhoHorizontal:
            if jogoPlayer_[i][j] != '🔵':
                print(jogoPlayer_[i][j], end="")
            else:
                print(f'🔵', end="")
            j += 1
       
        
        print(f"{i + 1}", end='')
        print()
def posiciona_portaHelicopteros():
    
    if jogoPlayer_ == []:
        monta_jogo2()
    
    V = 0
    while True:
        try:
            os.system("cls")
            monta_jogo2()
            monta_jogo_set_ph(0,0,V)
            
            mostrar_player()
            print("Este 🟠🟠🟠🟠🟠 é seu Porta Helicopteros, escolha se ele sera posicionado na horizontal ou vertical. \n Obs: Deixe uma casa de distância entre os navios! ")
            escolhaV = int(input(f" 1 - Para Vertical. \n 2 - Para Horizontal. \n Sua resposta: "))
  
            if escolhaV == 1:
                V = 6
                mensagem = "Insira a cordenada SUPERIOR desejada. A - " +alfabeto[tamanhoHorizontal - 1] + "\n Sua resposta: "
                mensagem2 = f"agora insira a cordenada LATEAL desejada. 1 - {tamanhoVertical}\n Sua resposta: "
            elif escolhaV == 2:
                mensagem = "Insira a cordenada SUPERIOR desejada: A - "+ alfabeto[tamanhoVertical -tamanhoPH]+ "\n Sua resposta: "
                mensagem2 = f"agora insira a cordenada LATEAL desejada. 1 - {tamanhoHorizontal} \n Sua resposta: "
                V = 1
            else: 
                raise ValueError            
            os.system('cls')
            jogoPlayer_.clear()
            monta_jogo2()  
            monta_jogo_set_ph(0,0,V)
            mostrar_player()

            escolhaX = input(mensagem).upper()
            escolhaX = alfabeto.index(escolhaX)
            os.system('cls')
            jogoPlayer_.clear()
            monta_jogo2() 
            monta_jogo_set_ph(escolhaX,0,V)    
            mostrar_player()     
            escolhaY = int(input(mensagem2))
            escolhaY_ = escolhaY - 1
            os.system('cls')
            jogoPlayer_.clear()                
            monta_jogo2()
            monta_jogo_set_ph(escolhaX,escolhaY_,V) 
            mostrar_player() 

            menu = input("Confirmar as coordenadas selecionadas? y / n ").upper()
            os.system('cls')
                
            if not menu or menu == "Y":
                break
            monta_jogo2()
        except ValueError:
            os.system('cls')
            print("Valor inválido. ")
            time.sleep(1)
        except IndexError:
            print("Valor inválido. ")
            time.sleep(1)
            os.system('cls')
            
    return(escolhaX,escolhaY_,V)
def posiciona_portaAvioes(escolhaX,escolhaY_,ph_v):
    V = 0
    while True:
        try:
            os.system("cls")
            jogoPlayer_.clear()
            # verifica_colisao2(0,0,"pa")
            monta_jogo2()
            monta_jogo_set_ph(escolhaX,escolhaY_,ph_v)
            monta_jogo_set_pa(tamanhoHorizontal - 1 ,0,6)
            mostrar_player()
            print("Este 🟡🟡🟡🟡🟡 é seu Porta Aviões, escolha se ele sera posicionado na horizontal ou vertical \n Obs: Deixe uma casa de distância entre os navios!")
            escolhaV = int(input(f" 1 - Para Vertical. \n 2 - Para Horizontal. \n Sua resposta: "))
            espaco = 1
            if escolhaV == 1:
                V = 6
                mensagem = "Insira a cordenada SUPERIOR desejada. A - " +alfabeto[tamanhoHorizontal - 1] + "\n Sua resposta: "
                mensagem2 = f"agora insira a cordenada LATEAL desejada. 1 - {tamanhoVertical}\n Sua resposta: "
            elif escolhaV == 2:
                mensagem = "Insira a cordenada SUPERIOR desejada: A - "+ alfabeto[tamanhoVertical -tamanhoPA]+ "\n Sua resposta: "
                mensagem2 = f"agora insira a cordenada LATEAL desejada. 1 - {tamanhoHorizontal} \n Sua resposta: "
                espaco = tamanhoPA
                V = 1
            else: 
                raise ValueError
            os.system("cls")
            jogoPlayer_.clear()
            monta_jogo2()
            monta_jogo_set_ph(escolhaX,escolhaY_,ph_v)
            monta_jogo_set_pa(tamanhoHorizontal - espaco,0,V)
            mostrar_player()

            pa_x = input(mensagem).upper()
            pa_x = alfabeto.index(pa_x)
            jogoPlayer_.clear()
            os.system('cls')
            monta_jogo2()
            monta_jogo_set_ph(escolhaX,escolhaY_,ph_v)
            monta_jogo_set_pa(pa_x,0,V)
            mostrar_player()

            pa_y = int(input(mensagem2))
            pa_y_ = pa_y - 1
            os.system('cls')
            jogoPlayer_.clear()
            monta_jogo2()
            monta_jogo_set_ph(escolhaX,escolhaY_,ph_v)
            monta_jogo_set_pa(pa_x,pa_y_,V)
            mostrar_player()
    
            menu = input("Confirma a posição selecionada? y / n ").upper()
        # verifica_colisao(escolhaX,escolhaY_,pa_x,pa_y_,0,0,0,0)
            if menu == "Y" or not menu:
                break
        except ValueError:
            os.system('cls')
            print("Valor inválido. ")
            time.sleep(2)
        except IndexError:
            print("Valor inválido. ")
            time.sleep(2)
            os.system('cls')

    return(pa_x,pa_y_,V)
def posiciona_corveta(escolhaX,escolhaY_,ph_v,pa_x,pa_y_,pa_y_v):
    while True:
        try:
            V = 6
            mensagem = ""
            mensagem2 = ""
            cor_y = tamanhoVertical
            
            jogoPlayer_.clear()
            os.system("cls")
            monta_jogo2()
            monta_jogo_set_ph(escolhaX,escolhaY_,ph_v)
            monta_jogo_set_pa(pa_x,pa_y_,pa_y_v)
            monta_jogo_set_cru(0,tamanhoVertical - tamanhoCRU,V)
            mostrar_player()
            print("Este 🟢🟢🟢 é sua corveta, escolha se ele sera posicionado na horizontal ou vertical \n Obs: Deixe uma casa de distância entre os navios!")
            escolhaV = int(input(f" 1 - Para Vertical. \n 2 - Para Horizontal. \n Sua resposta: "))
            if escolhaV == 1:
                V = 6
                mensagem = "Insira a cordenada SUPERIOR desejada. A - " +alfabeto[tamanhoHorizontal - 1] + "\n Sua resposta: "
                mensagem2 = f"agora insira a cordenada LATEAL desejada. 1 - {tamanhoVertical}\n Sua resposta: "
            elif escolhaV == 2:
                mensagem = "Insira a cordenada SUPERIOR desejada: A - "+ alfabeto[tamanhoVertical -tamanhoCRU]+ "\n Sua resposta: "
                mensagem2 = f"agora insira a cordenada LATEAL desejada. 1 - {tamanhoHorizontal} \n Sua resposta: "
                V = 1
            else: 
                raise ValueError
            os.system("cls")
            jogoPlayer_.clear()
            monta_jogo2()
            monta_jogo_set_ph(escolhaX,escolhaY_,ph_v)
            monta_jogo_set_pa(pa_x,pa_y_,pa_y_v)
            monta_jogo_set_cru(0,tamanhoVertical - tamanhoCRU,V)
            mostrar_player()

        

            cor_x = input(f"{mensagem}").upper()
            cor_x = alfabeto.index(cor_x)
            os.system("cls")
            jogoPlayer_.clear()
            monta_jogo2()
            monta_jogo_set_ph(escolhaX,escolhaY_,ph_v)
            monta_jogo_set_pa(pa_x,pa_y_,pa_y_v)
            monta_jogo_set_cru(cor_x,cor_y - tamanhoCRU,V)
            mostrar_player()

       
            cor_y = int(input(f"{mensagem2}"))
            cor_y_ = cor_y - 1
            os.system("cls")
            jogoPlayer_.clear()
            monta_jogo2()
            monta_jogo_set_ph(escolhaX,escolhaY_,ph_v)
            monta_jogo_set_pa(pa_x,pa_y_,pa_y_v)
            monta_jogo_set_cru(cor_x,cor_y_,V)
            mostrar_player()
            if (V > 5 and cor_y_ > 17) or (V <= 5 and  cor_x > 17):
                raise ValueError
     
            menu = input("Confirma a posição selecionada? y / n ").upper()
            # verifica_colisao(escolhaX,escolhaY_,pa_x,pa_y_,0,0,0,0)
            if menu == "Y" or not menu:
                break
        except ValueError:
            os.system('cls')
            print("Valor inválido. ")
            time.sleep(2)
        except IndexError:
            print("Valor inválido. ")
            time.sleep(2)
            os.system('cls')
    return(cor_x,cor_y_,V)
def posiciona_fragata(escolhaX,escolhaY_,ph_v,pa_x,pa_y_,pa_y_v,cor_x,cor_y_,cor_y_v):
    while True:
        try:
            V = 0
        
            os.system("cls")
            jogoPlayer_.clear()
            monta_jogo2()
            monta_jogo_set_ph(escolhaX,escolhaY_,ph_v)
            monta_jogo_set_pa(pa_x,pa_y_,pa_y_v)
            monta_jogo_set_cru(cor_x,cor_y_,cor_y_v)
            monta_jogo_set_fra(5,5,V)
            mostrar_player()
            print("Este 🟣🟣🟣 é sua fragata, escolha se ele sera posicionado na horizontal ou vertical \n Obs: Deixe uma casa de distância entre os navios!")
            escolhaV = int(input(f" 1 - Para Vertical. \n 2 - Para Horizontal. \n Sua resposta: "))
            if escolhaV == 1:
                V = 6
                mensagem = "Insira a cordenada SUPERIOR desejada. A - " +alfabeto[tamanhoHorizontal - 1] + "\n Sua resposta: "
                mensagem2 = f"agora insira a cordenada LATEAL desejada. 1 - {tamanhoVertical}\n Sua resposta: "
            elif escolhaV == 2:
                mensagem = "Insira a cordenada SUPERIOR desejada: A - "+ alfabeto[tamanhoVertical -tamanhoCRU]+ "\n Sua resposta: "
                mensagem2 = f"agora insira a cordenada LATEAL desejada. 1 - {tamanhoHorizontal} \n Sua resposta: "
                V = 1
            else: 
                raise ValueError
            os.system("cls")
            jogoPlayer_.clear()
            monta_jogo2()
            monta_jogo_set_ph(escolhaX,escolhaY_,ph_v)
            monta_jogo_set_pa(pa_x,pa_y_,pa_y_v)
            monta_jogo_set_cru(cor_x,cor_y_,cor_y_v)
            monta_jogo_set_fra(5,5,V)
            mostrar_player()
        
            fra_x = input(mensagem).upper()
            fra_x = alfabeto.index(fra_x)
            os.system("cls")
            jogoPlayer_.clear()
            monta_jogo2()
            monta_jogo_set_ph(escolhaX,escolhaY_,ph_v)
            monta_jogo_set_pa(pa_x,pa_y_,pa_y_v)
            monta_jogo_set_cru(cor_x,cor_y_,cor_y_v)
            monta_jogo_set_fra(fra_x,5,V)
            mostrar_player()
        
            fra_y = int(input(mensagem2))
            fra_y_ = fra_y -1
            os.system("cls")
            jogoPlayer_.clear()
            monta_jogo2()
            monta_jogo_set_ph(escolhaX,escolhaY_,ph_v)
            monta_jogo_set_pa(pa_x,pa_y_,pa_y_v)
            monta_jogo_set_cru(cor_x,cor_y_,cor_y_v)
            monta_jogo_set_fra(fra_x,fra_y_,V)
            mostrar_player()
            if (V >5 and fra_y_ > tamanhoVertical -3) or (V <= 5 and  fra_x > tamanhoHorizontal -3):
                raise ValueError

            menu = input("Confirma a posição selecionada? y / n ").upper()
    
            if menu == "Y" or not menu:
                break
        except ValueError:
            os.system('cls')
            print("Valor inválido. ")
            time.sleep(2)
        except IndexError:
            print("Valor inválido. ")
            time.sleep(2)
            os.system('cls')
    return(fra_x,fra_y_,V)
def bot_afundar_navio(navio):
    global playerNavios
    global playerPontos
    lista = []
    if navio[0] == "ph":
        lista = BotAcertosPH
        playerPontos = playerPontos - 10 * tamanhoPH
    elif navio[0] == "pa":
        lista = BotAcertosPA
        playerPontos = playerPontos - 10 * tamanhoPA
    elif navio[0] == "cru":
        lista = BotAcertosCru
        playerPontos = playerPontos - 10 * tamanhoCRU
    elif navio[0] == "fra":
        lista = BotAcertosFra
        playerPontos = playerPontos - 10 * tamanhoFra
    for i_ in range(0, len(lista)):
                coordenadas = lista
                coordenadas2 = coordenadas[i_]
                x = coordenadas2[0]
                y = coordenadas2[1]
                jogoPlayer_[x][y] = "❌"   
    playerNavios -= 1
def bot_verifica_afundar(navio):
    mensagem = ""
    if navio == "ph":
        if len(BotAcertosPH) > tamanhoPH - 1:
            mensagem = "O inimigo afundou nosso Porta Helicopteros"
            return "ph", mensagem 
        else:
            return False  
    if navio == "pa":
        if len(BotAcertosPA) > tamanhoPA - 1:
            mensagem = "O inimigo afundou nosso Porta Aviões"
            return "pa", mensagem
        else:
            return False
    if navio == "cru":
        if len(BotAcertosCru) > tamanhoCRU - 1:
            mensagem = "O inimigo afundou nossa Corveta"
            return "cru", mensagem
        else:
            return False
    if navio == "fra":
        if len(BotAcertosFra) > tamanhoFra - 1:
            mensagem = "O inimigo afundou nossa Fragata"
            return "fra", mensagem
        else:
            return False
def bot_verifica_acerto(x,y):
    # print(f" x = {x} y = {y}")
    mensagem = ""
    afundou = ""
    try:
        if jogoPlayer_[x][y] != "🔵" and x <= tamanhoHorizontal - 1 and y <= tamanhoVertical -1:
            if jogoPlayer_[x][y]  == "🟠":
                jogoPlayer_[x][y]  = '🔴'
                BotAcertosPH.append([x,y])
                return "ph"
            elif jogoPlayer_[x][y]  == "🟡":
                jogoPlayer_[x][y]  = '🔴'
                BotAcertosPA.append([x,y])
                return "pa"
            elif jogoPlayer_[x][y]  == "🟢":
                jogoPlayer_[x][y]  = '🔴'
                BotAcertosCru.append([x,y])
                return "cru"
            elif jogoPlayer_[x][y]  == "🟣":
                jogoPlayer_[x][y]  = '🔴'
                BotAcertosFra.append([x,y])
                return "fra"
            BotAcertos.append([x,y])
        else:
            return False
    except IndexError:
        return False
def atirar(tabuleiro,acertou,x,y):
    jogo = ""
    try:
        if tabuleiro == "player":
            if acertou != False and acertou != None:
                jogoPlayer_[x][y] = '🔴'
            else:
                jogoPlayer_[x][y] = "⚫"
        else:
            if acertou != False:
                jogo[x][y] = '🔴'
            else:
                jogo[x][y] = "⚫"
    except IndexError:
        return
        

def bot_randomizador():
    while True:
        X = random.randint(0,tamanhoHorizontal - 1)
        Y = random.randint(0,tamanhoVertical- 1)

        coord = [X,Y]
        if coord not in BotCoordenadaTentada:
            return X,Y
def bot_set_proximo_tiro(X,Y,_x,_y):
    BotProximoTiro.clear()
    BotProximoTiro.append([X + _x,Y + _y])
def bot():
    mensagem = ""
    ultimoTiro = 0
    afundar_ = int(0)
    
    if BotInstruçõesEx == []:
           instrucoes = BotInstruções
           random.shuffle(instrucoes)
           BotInstruçõesEx.append(instrucoes[0])
           BotInstruçõesEx.append(instrucoes[1])
           BotInstruçõesEx.append(instrucoes[2])
           BotInstruçõesEx.append(instrucoes[3])

    instrucoes_x = BotInstruçõesEx[0][0]
    instrucoes_y = BotInstruçõesEx[0][1]


    if BotProximoTiro == []:
        coordenadas = bot_randomizador()
        X = coordenadas[0]
        Y = coordenadas[1]    
        acertou = bot_verifica_acerto(X,Y)
        if acertou:
            BotCheckPoint.append([X,Y])
            BotAcertos.append([X,Y])
            BotProximoTiro.append([X + instrucoes_x,Y + instrucoes_y])
            mensagem = " acertou um de nossos navios"
        else:
            BotProximoTiro.clear()
            mensagem = " errou"

                    
        BotCoordenadaTentada.append([X,Y])
        
    else:
        X = BotProximoTiro[0][0]
        Y = BotProximoTiro[0][1]
        acertou = bot_verifica_acerto(X,Y)
        afundou = bot_verifica_afundar(acertou)
        BotCoordenadaTentada.append([X,Y])

        check_point_x = BotCheckPoint[0][0]
        check_point_y = BotCheckPoint[0][1]

        if BotCoordenadaTentada != []:
            ultimoTiro = BotCoordenadaTentada[len(BotCoordenadaTentada) -1]
            ultimoTiroX = ultimoTiro[0]
            ultimoTiroY = ultimoTiro[1]       
        
        if acertou:
            BotAcertos.append([X,Y])
            bot_set_proximo_tiro(ultimoTiroX,ultimoTiroY,instrucoes_x,instrucoes_y)
            mensagem = " acertou um de nossos navios"

        if (ultimoTiroX == 0 and instrucoes_x == -1) or (ultimoTiroY == 0 and instrucoes_y == -1) or (ultimoTiroX == (tamanhoHorizontal - 1) and instrucoes_x == +1) or (ultimoTiroY == (tamanhoVertical - 1) and instrucoes_y == +1):
            bot_set_proximo_tiro(check_point_x,check_point_y,instrucoes_x,instrucoes_y)

        if afundou:
            afundar_ = int(1)


        if not acertou and BotInstruçõesEx != [] :
            BotInstruçõesEx.pop(0)
            instrucoes_x = BotInstruçõesEx[0][0]
            instrucoes_y = BotInstruçõesEx[0][1]
            
            bot_set_proximo_tiro(check_point_x,check_point_y,instrucoes_x,instrucoes_y)

        elif not acertou and BotInstruçõesEx == []:
            BotProximoTiro.clear()
            BotCheckPoint.clear()
            BotInstruçõesEx.clear()

    if not acertou:
        mensagem = "errou"
    print("Agora é vez do inimigo atacar.")
    time.sleep(2)
    atirar("player",acertou,X,Y)
    if afundar_ != 0:
        bot_afundar_navio(afundou)
        BotProximoTiro.clear()
        BotCheckPoint.clear()
        BotInstruçõesEx.clear()
        mensagem = "afundou um de nossos navios!!"
    os.system('cls')
    painel(mostrarResposta)
    print(f"O inimigo escolheu a coordenada {alfabeto[Y]} x {alfabeto[X]} e {mensagem}")

def painel(Resposta):
    espaco = math.floor(tamanhoHorizontal / 2.2)
    print(' '* espaco, Fore.CYAN + " Seu Tabuleiro",' '* espaco, Style.RESET_ALL,end="")
    print(' '* (math.floor(espaco * 3 - 5)) ,end="")
    print(' '* espaco, Fore.RED  + "Tabuleiro Inimigo", Style.RESET_ALL,)

    print("  ", end="")
    for x in range (0, tamanhoHorizontal):
        print(f" {alfabeto[x]}", end="")
    for m in range(0,espaco * 2):
        print(" ", end="")
    print("     ", end="")
    for x in range (0, tamanhoHorizontal):
        print(f" {alfabeto[x]}", end="")
    print()
    for i in range (0,tamanhoVertical):
        # print(alfabeto[i], end="")
        if i < 9:
            print(f" {i + 1}", end='')
        else:
            print(f"{i + 1}", end='')

        
        for j in range(0, tamanhoHorizontal):
            print(jogoPlayer_[i][j], end="")

        if i < 9:
            print(f"{i + 1} ", end='')
        else:
            print(f"{i + 1}", end='')
        m = 0
        while True:            
            print(" ", end="")
              
            m += 1            
            if m >= espaco * 2:
                break
        if i < 9:
            print(f"  {i + 1}", end='')
        else:
            print(f" {i + 1}", end='')

        if Resposta == 1:
            for j2 in range(0, tamanhoHorizontal):
                print(jogo[i][j2], end="")
        elif Resposta == 0:
            for j2 in range(0, tamanhoHorizontal):
                if jogo[i][j2] != "🔵":
                    if jogo[i][j2] == "❌":
                        print("❌", end="")
                    elif jogo[i][j2] == "⚫":
                        print("⚫", end="")
                    elif jogo[i][j2] == '🔴':
                        print("🔴", end="")
                    else:
                        print("🔵", end="")
                else:
                    print("🔵", end="")


        
        print(f"{i + 1}")
    print()
    print( f'  Pontos: {playerPontos}' + ' '* (math.floor(espaco * 3 - 6)) + f'Seus navios: {playerNavios}/4 '+  ' '* (math.floor(espaco * 3 - 6)) + f'Navios Inimigos:{botNavios}/4 ' )
    print()
        
    
def menu():
    global playerNome
    os.system("cls")
    n = tamanhoHorizontal * 2+ 8
    n2 = int(n /2)
    menu_ = "menu"
    while True:
        n = tamanhoHorizontal * 2+ 8
        n2 = int(n /2)
        i=0
        while i < tamanhoVertical:
            if i == 3:
                # os.system("cls")
                if menu_ == "ranking":
                    rank = ranking()                    
                    le = len(rank)
                    tam = 17 - le
                    lista = []
                    for x in rank:
                        a = x.replace("\n",'')
                        a2 = a.split(' ')
                        nome = a2[0]
                        pontos = int(a2[1])
                        lista.append((nome,pontos))
                        listaOrdenada = sorted(lista, key=lambda x:x[1], reverse=True)
                   
                    print()
                    print("  " * (n2 - 5),"   RANKING  ")
                    print()
                    print("  " * (n2 - 7),"Nome            Pontos")
                    print()
                    for item in listaOrdenada:
                        nome = item[0] 
                        pontos = item[1]                                        
                        print("  " * (n2 - 7), f'{nome:19s}{pontos:2}') 
                    for x in range(1,tam - 4):
                        if x == tam - 5:
                            print("  " * (n2 - 9),"Digite 0 para voltar ao menu")
                        else:
                            print()                 
                    print("")
                    i = 17
                elif menu_ == "menu":
                    print()
                    print("  " * (n2 - 5),"BATALHA NAVAL")
                    print()
                    print("  " * (n2 - 5),"1  Novo Jogo ")
                    print("  " * (n2 - 5),"2   Ranking  ")
                    print("  " * (n2 - 5),"3     Sair   ")
                    tam = 21 - 4
                    for x in range(1, tam - 4):
                        print()
                    i = 17            
            j = 0
            while j < n:
            
                print("🔵", end="")
                j += 1

            i += 1
            print()
        menu = int(input("Insira a opção desejada: "))
        if menu == 1:
            
            contador = 0
            mensagemTopMenu = "Nome do jogador"
            opcaoUm = ""
            opcaoDois = ""
            while True:
                i=0
                os.system("cls")                
                while i < tamanhoVertical:
                    if i == 3:
                        print()
                        print("  " * (n2 - 5),mensagemTopMenu)
                        print()
                        print("  " * (n2 - 22),opcaoUm)
                        print()
                        print("  " * (n2 - 22),opcaoDois)
                        print()
                        tam = 21 - 5
                        for x in range(1, tam - 4):
                            print()
                        i = 17
                    j = 0
                    while j < n:            
                        print("🔵", end="")
                        j += 1
                    i += 1
                    print()
                if contador == 1:
                    menuu = int(input("Insira a opção desejada: "))
                else:
                    menuu = input("Insira seu nome: ")
                    playerNome = menuu
                    mensagemTopMenu = "Modo de jogo"
                    opcaoUm = "1 - Aleatório. Seus navios serão distribuidos de maneira aleatória pelo tabuleiro"
                    opcaoDois = "2 - Manual. Você define a posição de cada navio"
                if menuu == 1:
                    return "aleatorio"
                elif menuu == 2:
                    return "manual"
                else:
                    contador +=1
                    
                
        elif menu == 2:
            menu_ = "ranking"
        elif menu == 0:
            menu_ = "menu"
        elif menu == 3:
            os._exit(1)
        os.system('cls')
        
def montar_jogo_player(ModoDeJogo):
    monta_jogo2()
    
    if ModoDeJogo == "manual":
        while True:
            exec = posiciona_portaHelicopteros()
            exec2 = posiciona_portaAvioes(*exec)
            exec3 = posiciona_corveta(*exec,*exec2)
            exec4 = posiciona_fragata(*exec,*exec2,*exec3)
            adiciona_zona_colisao()
            colidiu = verifica_colisao()
            colidiu2 = verifica_colisao2("player", *exec,*exec2,*exec3,*exec4)

            if colidiu == False and colidiu2 == False:
                break
            else:
                print("Posições inválidas")
                print("Parece que você colocou os navios muito perto e eles colidiram!!!")
                time.sleep(5)


    else:
        while True:
            monta_jogo2()
            ran = randomizador(0)
            monta_jogo_set_ph(ran[0],ran[1],ran[2])
            monta_jogo_set_pa(ran[3],ran[4],ran[5])
            monta_jogo_set_cru(ran[6],ran[7],ran[8])
            monta_jogo_set_fra(ran[9],ran[10],ran[11])
            adiciona_zona_colisao()
            colidiu = verifica_colisao()
            
            if colidiu == False:
                break

def verifica_status():

    if botNavios<= 0:
        return "vitoria"
    elif playerNavios<= 0:
        return "derrota"
    else:
        return False
def salvar_game():
    if os.path.isfile("ranking.txt"):
        arq = open("ranking.txt",'a')
        arq.write(f'\n{playerNome} {playerPontos}')
    else:
        return ""

def player():
    mensagem =""
    global mostrarResposta
    while True:
        try:
            if contaRodadas == 0:
                os.system('cls')
                painel(mostrarResposta)
                time.sleep(2)
            print(f"Qual coordenada devemos atacar capitão?")
            tiroX = input(f" insira a letra da coordenada superior. ex: A :").upper()
            tiroUmY = int(input(f" insira a coordenada lateral. ex: 1 :"))
            time.sleep(1)
            if tiroX == 'HACK' or tiroUmY == "HACK":
                mostrarResposta = int(1)
                tiroUmX = alfabeto.index("A")
                indexLetra = 2
            else:
                tiroUmX = alfabeto.index(tiroX)
                indexLetra = tiroUmY -1
            tiros = [tiroUmX,indexLetra]

            if tiros in coordenadaTentada:
                raise TypeError
            elif tiroX == "" : #or tiroUmX == "":
                    raise ValueError
            elif tiroUmX >= tamanhoHorizontal or indexLetra >= tamanhoVertical:
                raise ValueError
            else:
                coordenadaTentada.append(tiros)
                break            
               
        except ValueError:
            print("Valor inválido. ")
            time.sleep(2)
        except TypeError:
            print("Você já tentou essa coordenada!")
            time.sleep(2)            
    exec = verifica_acerto(indexLetra,tiroUmX)
    if exec:
        print(exec)
        mensagem = exec
    else:
        print("Não acertamos nada capitão.") 
    time.sleep(2)  
    os.system("cls")
    painel(mostrarResposta)
    print(mensagem)


#                                                            -> menu pre jogo <-                                                              #
mainMenu = menu()

while True:
    montarJogo = randomizador(0)
    montarJogo = monta_jogo(*montarJogo)

    if not montarJogo:
        jogo = []
    else:
        monta_jogo2()
        if mainMenu == "aleatorio":
            montar_jogo_player("aleatorio")
          
        else:
            montar_jogo_player("manual")
        # mostrar_dois()
        break
#                                                            -> Jogo Principal <-                                                              #
while True:
    player()     
    bot()
    contaRodadas += 1
    endGame = verifica_status()
    if endGame:
        if endGame == 'derrota':
            print("Derrota,Todos navios da nossa esquadra foram afundados ") 
        elif endGame == "vitoria":
            os.system('cls')
            i = 0
            while i < tamanhoVertical * 2 - 1:
                cor = random.randint(0, len(cores) - 1)
                cor2 = cores[cor]
                print(cor2 + "VITÓRIA", Style.RESET_ALL)
                time.sleep(0.3)
                if i == tamanhoVertical - 1:
                    os.system('cls')
                i += 1
            
        salvar_game()
        break
