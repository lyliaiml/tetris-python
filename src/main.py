import pygame
from tetris import Tetris
from config import *

pygame.init()



WIDTH, HEIGHT = 500, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

base_fps = 25




while True:

    

    game1 = Tetris(20, 10)
    game2 = Tetris(20, 10)

    game1.zoom = 20
    game2.zoom = 20

    grid_width = game1.width * game1.zoom
    space_between = 40

    total_width = grid_width * 2 + space_between
    start_x = (WIDTH - total_width) // 2

    game1.x = start_x
    game2.x = start_x + grid_width + space_between

    game1.y = 80
    game2.y = 80

    counter = 0
    done = False
    menu = True
    mode = 2

    

    while menu:

        # fond dégradé
        for y in range(HEIGHT):

            color = (20,min(255, y // 4),min(255, 60 + y // 3))

            pygame.draw.line(screen,color,(0, y),(WIDTH, y) )

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # polices
        font_title = pygame.font.SysFont('Calibri',80,True)

        font = pygame.font.SysFont('Calibri',40,True )

        # glow titre
        for i in range(6):

            glow = font_title.render("TETRIS",True,(0, 255, 180) )

            screen.blit(glow,(WIDTH // 2 - 150 - i, 100 - i))

        # titre principal
        title = font_title.render("TETRIS",True,(255, 255, 255))

        screen.blit(title,(WIDTH // 2 - 150, 100))

        # boutons
        btn1 = pygame.Rect(WIDTH // 2 - 150,280,300,70)

        btn2 = pygame.Rect( WIDTH // 2 - 150,370,300,70)

        # bouton 1 joueur
        if btn1.collidepoint(mouse):

            pygame.draw.rect(screen,(180, 0, 255),btn1,border_radius=25 )

            if click[0]:
                mode = 1
                menu = False

        else:
            pygame.draw.rect(screen,(90, 0, 150),btn1,border_radius=25)

        # bouton 2 joueurs
        if btn2.collidepoint(mouse):

            pygame.draw.rect( screen,(255, 50, 150),btn2,border_radius=25)

            if click[0]:
                mode = 2
                menu = False

        else:

            pygame.draw.rect(screen,(150, 0, 80),btn2,border_radius=25 )

        # texte boutons
        text1 = font.render("1 JOUEUR",True,(255, 255, 255))

        text2 = font.render( "2 JOUEURS",True,(255, 255, 255))

        screen.blit(text1, (WIDTH // 2 - 90, 300))
        screen.blit(text2, (WIDTH // 2 - 100, 390))

        # quitter
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()

    #  JEU

    while not done:

        counter += 1

        # vitesse augmente avec score
        fps = min(60, base_fps + game1.score // 5)

        if counter > 100000:
            counter = 0

        screen.fill(BLACK)

        # nouvelles pièces
        if game1.figure is None:
            game1.new_figure()

        if game2.figure is None:
            game2.new_figure()

        # descente automatique
        if counter % (fps // 2) == 0:

            if game1.state == "start":
                game1.go_down()

            if game2.state == "start":
                game2.go_down()

        #  ÉVÉNEMENTS

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                

                if event.key == pygame.K_ESCAPE:

                    pause = True

                    while pause:

                        # fond sombre
                        overlay = pygame.Surface((WIDTH, HEIGHT))
                        overlay.set_alpha(180)
                        overlay.fill((0, 0, 0))
                        screen.blit(overlay, (0, 0))

                        font_pause = pygame.font.SysFont( 'Calibri',True)

                        font_btn = pygame.font.SysFont('Calibri',35,True)

                        # titre pause
                        txt_pause = font_pause.render("PAUSE",True,WHITE)

                        screen.blit( txt_pause,(WIDTH // 2 - 80, 150))

                        mouse = pygame.mouse.get_pos()
                        click = pygame.mouse.get_pressed()

                        # boutons
                        btn_continue = pygame.Rect(WIDTH // 2 - 120,260,240,60)

                        btn_quit = pygame.Rect(WIDTH // 2 - 120,350,240,60)

                        pygame.draw.rect(screen,(120, 0, 200), btn_continue, border_radius=20)

                        pygame.draw.rect( screen,(200, 50, 50),btn_quit,border_radius=20 )

                        txt1 = font_btn.render ("CONTINUER",True,WHITE)

                        txt2 = font_btn.render("QUITTER",True, WHITE)

                        screen.blit(txt1, (WIDTH // 2 - 95, 275))
                        screen.blit(txt2, (WIDTH // 2 - 70, 365))

                        # continuer
                        if btn_continue.collidepoint(mouse) and click[0]:
                            pause = False

                        # quitter
                        if btn_quit.collidepoint(mouse) and click[0]:
                         pygame.quit()
                         exit()

                        for pause_event in pygame.event.get():

                            if pause_event.type == pygame.QUIT:
                                pygame.quit()
                                exit()

                        pygame.display.flip()

             

                if event.key == pygame.K_LEFT:
                    game1.go_side(-1)

                if event.key == pygame.K_RIGHT:
                    game1.go_side(1)

                if event.key == pygame.K_UP:
                    game1.rotate()

                if event.key == pygame.K_DOWN:
                    game1.go_down()

                # descente instantanée
                if event.key == pygame.K_SPACE:
                    game1.go_space()

                # JOUEUR 2

                if mode == 2:

                    if event.key == pygame.K_q:
                        game2.go_side(-1)

                    if event.key == pygame.K_d:
                        game2.go_side(1)

                    if event.key == pygame.K_z:
                        game2.rotate()

                    if event.key == pygame.K_s:
                        game2.go_down()

        # jeux affichés
        games = [game1] if mode == 1 else [game1, game2]

        # DESSIN 

        for game in games:

            # grille
            for i in range(game.height):

                for j in range(game.width):

                    pygame.draw.rect(
                        screen,
                        (40, 40, 40),
                        [
                            game.x + game.zoom * j,
                            game.y + game.zoom * i,
                            game.zoom,
                            game.zoom
                        ],
                        1
                    )

                    # blocs placés
                    if game.field[i][j] > 0:

                        pygame.draw.rect(
                            screen,
                            colors[game.field[i][j]],
                            [
                                game.x + game.zoom * j + 1,
                                game.y + game.zoom * i + 1,
                                game.zoom - 2,
                                game.zoom - 2
                            ]
                        )

            # pièce actuelle
            if game.figure:

                for i in range(4):

                    for j in range(4):

                        p = i * 4 + j

                        if p in game.figure.image():

                            pygame.draw.rect(
                                screen,
                                colors[game.figure.color],
                                [
                                    game.x + game.zoom * (j + game.figure.x) + 1,
                                    game.y + game.zoom * (i + game.figure.y) + 1,
                                    game.zoom - 2,
                                    game.zoom - 2
                                ]
                            )

        # SCORES 

        font_info = pygame.font.SysFont('Calibri',22,True)

        # joueur 1
        score1 = font_info.render("Score J1 : " + str(game1.score),True,WHITE)

        screen.blit(score1, [game1.x, 40])

        # joueur 2
        if mode == 2:

            score2 = font_info.render("Score J2 : " + str(game2.score),True,WHITE)

            screen.blit(score2, [game2.x, 40])

        # GAME OVER

        if game1.state == "gameover":

            game_over = font_info.render("GAME OVER J1",True,(255, 50, 50))

            screen.blit(game_over, (game1.x - 10, 250))

        if mode == 2 and game2.state == "gameover":

            game_over2 = font_info.render("GAME OVER J2",True,(255, 50, 50))

            screen.blit(game_over2, (game2.x - 10, 250))

        pygame.display.flip()

        clock.tick(fps)
