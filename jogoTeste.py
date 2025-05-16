import pygame
import sys
import random
import time
import src.settings as settings


pygame.init()

largura, altura = 1000, 1100
tela = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
pygame.display.set_caption("peixonauta matemático")

velocidade_inicial = 2
velocidade_maxima = 8
aceleracao = 0.35
velocidade_atual = {"x": 0, "y": 0}

turbo_ativo = False
carga_turbo = 100  # carga máxima
carga_maxima = 100
consumo_turbo = 50  # por segundo
recarga_turbo = 20  # por segundo
multiplicador_turbo = 2  # dobra a velocidade


modo_tela_cheia = False
fonte_grande = pygame.font.SysFont(None, 80)
fonte_media = pygame.font.SysFont(None, 40)

# Fundo
fundo = pygame.image.load("assets/images/fundo.png")
fundo = pygame.transform.scale(fundo, (largura, altura))

imagem_jogador = pygame.image.load("assets/images/submarino.png")
imagem_jogador = pygame.transform.scale(imagem_jogador, (settings.largura_jogador, settings.altura_jogador))

# Carregar imagens dos inimigos
imagens_inimigos = {
    "lento": pygame.image.load("assets/images/verde.png"),
    "medio": pygame.image.load("assets/images/laranja.png"),
    "rapido": pygame.image.load("assets/images/vermelho.png"),
    "rapidao": pygame.image.load("assets/images/azul.png"),
}

# Redimensionar as imagens
tamanho_inimigo = (50, 50)
for tipo in imagens_inimigos:
    imagens_inimigos[tipo] = pygame.transform.scale(imagens_inimigos[tipo], tamanho_inimigo)

# velocidades dos inimigos
velocidades = {
    "lento": 2,
    "medio": 5,
    "rapido": 8,
    "rapidao": 11
}



def criar_inimigo():
    tipo = random.choice(list(imagens_inimigos.keys()))
    return {
        "tipo": tipo,
        "x": largura + random.randint(0, 300),
        "y": random.randint(0, altura - 50),
        "vel": velocidades[tipo]
    }


def gerar_equacao():
    a = random.randint(1, 9)
    x = random.randint(0, 10)
    b = random.randint(0, 10)
    resultado = x + b
    equacao_str = f"x + {b} = {resultado}"
    return equacao_str, x


def criar_bloco(valor):
    return {
        "x": random.randint(0, largura - 30),
        "y": -30,
        "vel": random.randint(3, 5),
        "valor": valor,
        "ativo": True,
        "rect": pygame.Rect(0, 0, 30, 30)
    }


blocos = []  
inimigos_max = 5
blocos_por_rodada = 2
aumento_dificuldade_em = 2



def reiniciar_jogo():
    global equacoes_completadas
    global x, y, inimigos, morto, vidas, tempo_inicio, TEMPO_PROXIMO_BLOCO
    global equacao_atual, resposta_correta, blocos, pausado  
    global tempo_invulneravel
    global inimigos_max, blocos_por_rodada
    inimigos_max = 5
    blocos_por_rodada = 2
    tempo_invulneravel = 0
    x = 0
    y = 400
    equacoes_completadas = 0
    inimigos = [criar_inimigo() for _ in range(inimigos_max)]
    morto = False
    pausado = False
    vidas = 3
    tempo_inicio = time.time()
    blocos.clear()
    TEMPO_PROXIMO_BLOCO = time.time()
    equacao_atual, resposta_correta = gerar_equacao()

# Inicializa o jogo
reiniciar_jogo()
clock = pygame.time.Clock()

# Loop principal
while True:
    global tempo_invulneravel
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                pausado = not pausado  
            if evento.key == pygame.K_F11:
                modo_tela_cheia = not modo_tela_cheia
                if modo_tela_cheia:
                    tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    largura, altura = tela.get_size()
                else:
                    largura, altura = 800, 600
                    tela = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
                
                imagem_original_fundo = pygame.image.load("fundo.png").convert()
                fundo = pygame.transform.scale(imagem_original_fundo, (largura, altura))
                
            if morto and evento.key == pygame.K_r:
                reiniciar_jogo()

    delta_time = clock.get_time() / 1000  # para cálculo por segundo

    teclas = pygame.key.get_pressed()
    turbo_ativo = teclas[pygame.K_SPACE] and carga_turbo > 0

    # Ativa ou desativa o turbo e atualiza a carga
    if turbo_ativo:
        carga_turbo -= consumo_turbo * delta_time
        if carga_turbo < 0:
            carga_turbo = 0
    else:
        carga_turbo += recarga_turbo * delta_time
        if carga_turbo > carga_maxima:
            carga_turbo = carga_maxima

    # Movimentação
    if not morto and not pausado:
        teclas = pygame.key.get_pressed()

        # Direção X
        if teclas[pygame.K_LEFT]:
            if velocidade_atual["x"] > -velocidade_maxima:
                velocidade_atual["x"] -= aceleracao
        else:
            if velocidade_atual["x"] < 0:
                velocidade_atual["x"] += aceleracao
            if abs(velocidade_atual["x"]) < aceleracao:
                velocidade_atual["x"] = 0

        if teclas[pygame.K_RIGHT]:
            if velocidade_atual["x"] < velocidade_maxima:
                velocidade_atual["x"] += aceleracao
        else:
            if velocidade_atual["x"] > 0:
                velocidade_atual["x"] -= aceleracao
            if abs(velocidade_atual["x"]) < aceleracao:
                velocidade_atual["x"] = 0

        # Direção Y
        if teclas[pygame.K_UP]:
            if velocidade_atual["y"] > -velocidade_maxima:
                velocidade_atual["y"] -= aceleracao
        else:
            if velocidade_atual["y"] < 0:
                velocidade_atual["y"] += aceleracao
            if abs(velocidade_atual["y"]) < aceleracao:
                velocidade_atual["y"] = 0

        if teclas[pygame.K_DOWN]:
            if velocidade_atual["y"] < velocidade_maxima:
                velocidade_atual["y"] += aceleracao
        else:
            if velocidade_atual["y"] > 0:
                velocidade_atual["y"] -= aceleracao
            if abs(velocidade_atual["y"]) < aceleracao:
                velocidade_atual["y"] = 0

       
        # Verifica se o turbo está ativo (tecla espaço pressionada e carga disponível)
        turbo_ativo = teclas[pygame.K_SPACE] and carga_turbo > 0
        multiplicador = multiplicador_turbo if turbo_ativo else 1

        # Aplica movimentação com turbo (se ativo)
        x += velocidade_atual["x"] * multiplicador
        y += velocidade_atual["y"] * multiplicador

        # Limita aos limites da tela
        x = max(0, min(x, largura - settings.largura_jogador))
        y = max(0, min(y, altura - settings.altura_jogador))


    # Fundo
    tela.blit(fundo, (0, 0))
    # Recarrega o turbo automaticamente (0.5 por frame, por exemplo)
    if not teclas[pygame.K_SPACE] and carga_turbo < carga_maxima:
        carga_turbo += 0.5

    # Diminui a carga quando em uso
    elif teclas[pygame.K_SPACE] and carga_turbo > 0:
        carga_turbo -= 1

    # Jogador
    jogador_rect = pygame.Rect(x, y, settings.largura_jogador, settings.altura_jogador)
    if not morto:
        if not morto:
            if time.time() < tempo_invulneravel:
                if int(time.time() * 5) % 2 == 0:  
                    tela.blit(imagem_jogador, (x, y))
            else:
                tela.blit(imagem_jogador, (x, y))


    # Inimigos
    for inimigo in inimigos:
        if not morto and not pausado:
            inimigo["x"] -= inimigo["vel"]
            if inimigo["x"] < -50:
                novo = criar_inimigo()
                inimigo.update(novo)

        inimigo_rect = pygame.Rect(inimigo["x"], inimigo["y"], 50, 50)
        if not morto and jogador_rect.colliderect(inimigo_rect) and time.time() > tempo_invulneravel:
            vidas -= 1
            tempo_invulneravel = time.time() + 2
            if vidas <= 0:
                morto = True
            
            
            break


        tela.blit(imagens_inimigos[inimigo["tipo"]], (inimigo["x"], inimigo["y"]))

    # Criar blocos com números
    if not morto and not pausado and time.time() > TEMPO_PROXIMO_BLOCO:
        valores = list(set(random.sample(range(0, 15), blocos_por_rodada + 1)))
        if resposta_correta not in valores:
            valores[0] = resposta_correta
        for valor in valores:
            blocos.append(criar_bloco(valor))
        TEMPO_PROXIMO_BLOCO = time.time() + 1.5

    # Atualizar e desenhar blocos
    for bloco in blocos:
        if bloco["ativo"]:
            if not morto and not pausado:
                bloco["y"] += bloco["vel"]
                bloco["rect"].update(bloco["x"], bloco["y"], 30, 30)

                if jogador_rect.colliderect(bloco["rect"]):
                    if bloco["valor"] == resposta_correta:
                        equacoes_completadas += 1 
                        equacao_atual, resposta_correta = gerar_equacao()
                        blocos.clear()
                        if equacoes_completadas % aumento_dificuldade_em == 0:
                            inimigos_max = min(inimigos_max + 1, 15)
                            blocos_por_rodada = min(blocos_por_rodada + 1, 4)
                            for inimigo in inimigos:
                                inimigo["vel"] += 0.1  # acelera inimigos existentes
                            inimigos.append(criar_inimigo())

                    else:
                        if time.time() > tempo_invulneravel:
                            vidas -= 1
                            tempo_invulneravel = time.time() + 2
                            if vidas <= 0:
                                morto = True
                    bloco["ativo"] = False

            if bloco["ativo"]:  
                pygame.draw.rect(tela, settings.AZUL_CLARO, bloco["rect"])
                valor_texto = fonte_media.render(str(bloco["valor"]), True, settings.BRANCO)
                tela.blit(valor_texto, (bloco["x"] + 5, bloco["y"]))


    # HUD
    vidas_texto = fonte_media.render(f"Vidas: {vidas}", True, settings.BRANCO)
    tela.blit(vidas_texto, (10, 10))
    equacao_texto = fonte_media.render(f"Equação: {equacao_atual}", True, settings.BRANCO)
    tela.blit(equacao_texto, (largura // 2 - equacao_texto.get_width() // 2, 10))
    equacoes_texto = fonte_media.render(f"Equações: {equacoes_completadas}", True, settings.BRANCO)
    tela.blit(equacoes_texto, (10, 90))

    # Desenhar barra de turbo
    barra_largura = 200
    barra_altura = 20
    barra_x = largura - barra_largura - 10
    barra_y = 10

    # Contorno
    pygame.draw.rect(tela, settings.BRANCO, (barra_x, barra_y, barra_largura, barra_altura), 2)

    # Barra preenchida
    largura_preenchida = int((carga_turbo / carga_maxima) * barra_largura)
    pygame.draw.rect(tela, (0, 200, 255), (barra_x, barra_y, largura_preenchida, barra_altura))

    # Texto da barra
    turbo_texto = fonte_media.render("Turbo", True, settings.BRANCO)
    tela.blit(turbo_texto, (barra_x, barra_y - 25))


    
    if pausado:
        texto_pausa = fonte_grande.render("JOGO PAUSADO", True, settings.BRANCO)
        tela.blit(texto_pausa, ((largura - texto_pausa.get_width()) // 2, altura // 2))


    if not morto and not pausado:
        tempo_atual = int(time.time() - tempo_inicio)
    tempo_texto = fonte_media.render(f"Tempo: {tempo_atual}s", True, settings.BRANCO)
    tela.blit(tempo_texto, (10, 50))

    # Tela de morte
    if morto:
        texto = fonte_grande.render("VOCÊ MORREU", True, settings.BRANCO)
        reiniciar_texto = fonte_media.render("Pressione R para reiniciar", True, settings.BRANCO)
        tela.blit(texto, ((largura - texto.get_width()) // 2, altura // 2 - 50))
        tela.blit(reiniciar_texto, ((largura - reiniciar_texto.get_width()) // 2, altura // 2 + 20))

    pygame.display.update()
