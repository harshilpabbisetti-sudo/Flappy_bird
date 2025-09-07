import pygame
from sys import exit
import mysql.connector as sqltor


def login(database):
    mycon = sqltor.connect(host='localhost', user='root', passwd='12345678', database=database)
    if mycon.is_connected():

        def message(text):
            text_surf = error_font.render(text, False, (255, 0, 0))
            text_rect = text_surf.get_rect(midbottom=(630, 365))
            screen.blit(text_surf, text_rect)

        cursor = mycon.cursor()
        to_break = False
        pygame.init()                                   # initializes pygame (No need to repeat it in other codes)
        screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption(database)
        clock = pygame.time.Clock()

        font = pygame.font.Font('font/Pixeltype.ttf', 50)
        error_font = pygame.font.Font('font/Pixeltype.ttf', 30)

        color_active = pygame.Color('lightskyblue3')
        color_passive = pygame.Color('gray15')

        username_surf = font.render('Username', False, (0, 0, 102))
        username_rect = username_surf.get_rect(bottomleft=(30, 120))

        username_text = ''
        username_text_rect = pygame.Rect(25, 130, 500, 50)
        username_text_rect_color = color_passive

        password_surf = font.render('Password', False, (0, 0, 102))
        password_rect = username_surf.get_rect(bottomleft=(30, 240))

        password_text = ''
        password_text_rect = pygame.Rect(25, 250, 500, 50)
        password_text_rect_color = color_passive

        submit_surf = font.render('Submit', False, (0, 0, 102))
        submit_rect = submit_surf.get_rect(midbottom=(400, 370))

        username_active, password_active, wrong_input, register, blank_input = False, False, False, False, False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if username_text_rect.collidepoint(event.pos):
                        username_active = True
                    else:
                        username_active = False
                    if password_text_rect.collidepoint(event.pos):
                        password_active = True
                    else:
                        password_active = False

                    if submit_rect.collidepoint(event.pos):
                        cursor.execute('select * from login_credentials')
                        data = cursor.fetchall()
                        if register:
                            if username_text != '' and password_text != '':                     # adds new login credentials to game
                                if not data:
                                    data = [[0]]
                                cursor.execute(f"insert into login_credentials values ({data[-1][0] + 1}, '{username_text}', '{password_text}', 0, 0, 0);")
                                mycon.commit()
                                register = False
                            else:
                                blank_input = True
                        else:                                                                   # checks if given login credentials are correct
                            for row in data:
                                if row[1] == username_text and row[2] == password_text:
                                    to_break = True
                                    return username_text
                            else:
                                username_text, password_text = '', ''
                                wrong_input = True
                            if to_break:
                                break

                    if register_login_rect.collidepoint(event.pos):
                        if register:
                            register = False
                        else:
                            register = True

                if event.type == pygame.KEYDOWN:
                    if username_active:
                        if event.key != pygame.K_RETURN:
                            if event.key == pygame.K_BACKSPACE:
                                username_text = username_text[:-1]
                            else:
                                username_text += event.unicode
                    if password_active:
                        if event.key != pygame.K_RETURN:
                            if event.key == pygame.K_BACKSPACE:
                                password_text = password_text[:-1]
                            else:
                                password_text += event.unicode

                    if event.key == pygame.K_RETURN:
                        cursor.execute('select * from login_credentials')
                        data = cursor.fetchall()
                        if register:
                            if username_text != '' and password_text != '':
                                if not data:
                                    data = [[0]]
                                cursor.execute(f"insert into login_credentials values ({data[-1][0]+1}, '{username_text}', '{password_text}', 0);")
                                mycon.commit()
                                register = False
                            else:
                                blank_input = True
                        else:
                            for row in data:
                                if row[1] == username_text and row[2] == password_text:
                                    to_break = True
                                    return username_text
                            else:
                                username_text, password_text = '', ''
                                wrong_input = True
                            if to_break:
                                break
            if to_break:
                break

            screen.fill((51, 153, 255))
            pygame.draw.rect(screen, (192, 192, 192), (342, 325, 109, 50), 0, 20)
            pygame.draw.rect(screen, (192, 192, 192), (635, 7, 152, 43), 0, 20)
            font = pygame.font.Font('font/Pixeltype.ttf', 50)
            if register:
                title_surf = font.render(f'Registration Page', False, (0, 0, 102))
                register_login_surf = font.render('login', False, (0, 0, 102))
                wrong_input = False
            else:
                title_surf = font.render(f'Login Page', False, (0, 0, 102))
                register_login_surf = font.render('Register', False, (0, 0, 102))
                blank_input = False

            title_rect = title_surf.get_rect(midbottom=(400, 50))
            screen.blit(title_surf, title_rect)
            register_login_rect = register_login_surf.get_rect(midbottom=(718, 50))
            screen.blit(register_login_surf, register_login_rect)

            mouse_pos = pygame.mouse.get_pos()
            submit_surf = font.render('Submit', False, (0, 0, 102))
            submit_rect = submit_surf.get_rect(midbottom=(400, 370))
            if submit_rect.collidepoint(mouse_pos):
                font = pygame.font.Font('font/Pixeltype.ttf', 60)
                submit_surf = font.render('Submit', False, (0, 0, 102))
                submit_rect = submit_surf.get_rect(midbottom=(397, 375))
                pygame.draw.rect(screen, (192, 192, 192), (333, 322, 125, 57), 0, 20)

            if register_login_rect.collidepoint(mouse_pos):
                font = pygame.font.Font('font/Pixeltype.ttf', 60)
                pygame.draw.rect(screen, (192, 192, 192), (625, 7, 172, 53), 0, 20)
                if register:
                    register_login_surf = font.render('login', False, (0, 0, 102))
                else:
                    register_login_surf = font.render('Register', False, (0, 0, 102))
                register_login_rect = register_login_surf.get_rect(midbottom=(718, 55))
                screen.blit(register_login_surf, register_login_rect)

            screen.blit(username_surf, username_rect)
            screen.blit(password_surf, password_rect)
            screen.blit(submit_surf, submit_rect)

            if username_active:
                username_text_rect_color = color_active
            else:
                username_text_rect_color = color_passive

            if password_active:
                password_text_rect_color = color_active
            else:
                password_text_rect_color = color_passive

            pygame.draw.rect(screen, username_text_rect_color, username_text_rect, 0, 20)
            pygame.draw.rect(screen, password_text_rect_color, password_text_rect, 0, 20)

            username_text_surf = font.render(username_text, True, (255, 255, 255))
            screen.blit(username_text_surf, (username_text_rect.x + 10, username_text_rect.y + 10))
            username_text_rect.w = max(username_text_surf.get_width() + 10, 500)

            password_text_surf = font.render(len(password_text)*'* ', True, (255, 255, 255))
            screen.blit(password_text_surf, (password_text_rect.x + 10, password_text_rect.y + 15))
            password_text_rect.w = max(password_text_surf.get_width() + 10, 500)

            if wrong_input:
                message('Wrong username or password')
            if blank_input:
                message("Username or Password can't be blank")

            pygame.display.update()
            clock.tick(60)
        return username_text
    else:
        print('\nproblem occurred in backend connection\n')
