import pyxel
import random

largeur = 256
hauteur = 138
pyxel.init(largeur, hauteur, title="Space Invador")
X = largeur / 2
Y = hauteur
tirs = []
ennemis = []
vies = 5
gameover = False
score = 0
color = 11
bestscore = 0


def est_en_collision(x, y):
    if x >= X and x <= X + 20 and y >= hauteur - 30 and y <= hauteur - 5:
        return True
    return False

def collision_tir_ennemi(tir_x, tir_y, ennemi_x, ennemi_y):
    if tir_x >= ennemi_x and tir_x <= ennemi_x + 8 and tir_y >= ennemi_y and tir_y <= ennemi_y + 8:
        return True
    return False

def cheatcode():
    global score, vies
    if pyxel.btnp(pyxel.KEY_V) and pyxel.btnp(pyxel.KEY_A) and pyxel.btnp(pyxel.KEY_L):
        score += 10
    if pyxel.btnp(pyxel.KEY_V) and pyxel.btnp(pyxel.KEY_I) and pyxel.btnp(pyxel.KEY_E):
        vies += 10

def update():
    global X, vies, gameover, score, color, bestscore

    cheatcode()

    if vies == 0:
        gameover = True

    color = 11 # pour que la couleur redevienne bleue

    if pyxel.btnp(pyxel.KEY_Q) and gameover == False:
        pyxel.quit()

    if pyxel.btn(pyxel.KEY_LEFT) and gameover == False:
        if X > 0:
            X -= 3

    if pyxel.btn(pyxel.KEY_RIGHT) and gameover == False:
        if X < pyxel.width - 20:
            X += 3

    if pyxel.btnr(pyxel.KEY_SPACE) and len(tirs) < 20 and gameover == False:
        tirs.append([X + 7, hauteur - 25])


    for tir in tirs:
        tir[1] -= 2
        if tir[1] < 0:
            tirs.remove(tir)

        for ennemi in ennemis:
            if collision_tir_ennemi(tir[0], tir[1], ennemi[0], ennemi[1]) and ennemi in ennemis:
                ennemis.remove(ennemi)
                score += 1
    # génération des ennemis
    if score < 5:
        if pyxel.frame_count % 60 == 0:  # toute les 2s
            ennemis.append([random.randint(0, largeur - 20), 0])
    if 5 <= score < 15:
        if pyxel.frame_count % 30 == 0:  # toute les 1s
            ennemis.append([random.randint(0, largeur - 20), 0])

    if 15 <= score:
        if pyxel.frame_count % 15 == 0:  # toute les 0.5s
            ennemis.append([random.randint(0, largeur - 20), 0])


    # while True: #NE FONCTIONNE PAS pourquoi ? -> pyxel ?
    #     ennemis.append([random.randint(0, largeur), 0])
    #     time.sleep(2)

    # création des ennemis

    for ennemi in ennemis:

        ennemi[1] += 1

        if ennemi[1] > hauteur and gameover == False:
            score -= 1
            ennemis.remove(ennemi)
        if pyxel.frame_count % 60 == 0:
            if est_en_collision(ennemi[0], ennemi[1]):
                if vies > 0:
                    vies -= 1
                    color = 9
                    print("Collision")
                else:
                    if score > bestscore:
                        bestscore = score
                    gameover = True
                    ennemis.remove(ennemi)
                    print("game over")



        if gameover == True:
            break



    if pyxel.btnr(pyxel.KEY_SPACE) and gameover == True:

        score = 0
        vies = 5
        gameover = False


def draw():
    pyxel.cls(0)


    pyxel.text(largeur - 50, 10, f"score : {str(score)}", 2)
    for tir in tirs:
        pyxel.rect(tir[0], tir[1], 1, 5, 7)

    for ennemi in ennemis:
        pyxel.rect(ennemi[0], ennemi[1], 8, 8, 8)
    pyxel.text(10, 10, f"vies restantes : {str(vies)}", 2)

    # deplacement lateral
    pyxel.rect(X, hauteur - 20, 15, 15, color)


    if gameover == True:
        pyxel.text(largeur / 2 - 18, hauteur/2, "GAME OVER", 2)
        pyxel.text(largeur / 2 - 25, hauteur / 2 + 10, f"meilleur score : {bestscore}", 2)
        pyxel.text(largeur / 2 - 34, hauteur - 10, "ESPACE POUR REJOUER", 2)


pyxel.run(update, draw)
