import random
import pygame
from sys import exit
import login_page
import mysql.connector as sqltor


class Owl(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        owl_paths = [('graphics/owl/owl1.png', 0.15),
                     ('graphics/owl/owl2.png', 0.15),
                     ('graphics/owl/owl3.png', 0.1425),
                     ('graphics/owl/owl2.png', 0.15)]

        self.owl_fly = [self._load_and_scale(path, scale) for path, scale in owl_paths]
        self.owl_fly.append(self.owl_fly[1])  # creates a list of all animation images of owl

        self.owl_index = 0
        self.image = self.owl_fly[self.owl_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.velocity = -7

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.25)

    def _load_and_scale(self, path, scale):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.rotozoom(img, 0, scale)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w] == 1 or event.type == pygame.MOUSEBUTTONDOWN:
            self.velocity = -7  # flies
            self.jump_sound.play()

    def apply_gravity(self):  # for realistic parabolic curve
        self.velocity += 0.5
        self.rect.y += self.velocity

    def animation(self):
        self.owl_index += 0.1  # for flying effect
        if self.owl_index >= len(self.owl_fly):
            self.owl_index = 0
        self.image = self.owl_fly[int(self.owl_index)]

    def update(self):
        global game_phase, transparency, invincibility, lives, start_time
        if self.rect.y < 0 or self.rect.y > 350:  # checks for death
            self.rect = self.image.get_rect(midbottom=(80, 200))  # repositions it
            self.velocity = 0
            if lives > 1:
                lives -= 1
                transparency = 255
                invincibility = True  # short invincibility
                start_time = pygame.time.get_ticks()
            else:
                obstacle_group.empty()
                buff_group.empty()
                game_phase = 0
        self.player_input()
        self.apply_gravity()
        self.animation()


class Wave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.waves_list = []
        for i in range(1, 5):  # creates a nested list for every set of wave animation
            self.waves_list.append(
                [pygame.image.load(f'graphics/waves/Waves-set-{i}/{i}{j}.png').convert_alpha() for j in range(1, 7)])

        self.wave_index = 0
        self.waves = 0
        self.image = self.waves_list[self.waves][self.wave_index]
        self.rect = self.image.get_rect(bottomleft=(0, 410))

    def _load(self, path):
        return pygame.image.load(path).convert_alpha()

    def animation(self):
        self.wave_index += 0.1
        if self.wave_index >= len(self.waves_list[self.waves]):
            self.waves = random.randint(0, len(self.waves_list) - 1)  # to determine which wave set to use
            self.wave_index = 0
        self.image = self.waves_list[self.waves][int(self.wave_index)]

    def update(self):
        self.animation()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load('graphics/pillar.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))

    def destroy(self):
        global score, x2
        if self.rect.right < 0:  # destroys itself when out of screen
            self.kill()
            if x2:
                score += 1
            else:
                score += 0.5

    def update(self):
        global score
        self.rect.x -= 7.5 + (score // 10)  # increases speed with score
        self.destroy()


class Buffs(pygame.sprite.Sprite):
    def __init__(self, buff_type):
        super().__init__()

        self.image = self._icon(buff_type)
        self.rect = self.image.get_rect(center=(900, 200))
        self.speed = 2 * random.choice([-1, 1])

    def _icon(self, buff):
        img = pygame.image.load(f'graphics/buffs/{buff}.png').convert_alpha()
        return pygame.transform.rotozoom(img, 0, 0.2)

    def destroy(self):
        if self.rect.x < -10:  # destroys itself when out of screen
            self.kill()

    def update(self):
        self.destroy()
        self.rect.x -= 5
        self.rect.y += self.speed
        if self.rect.y >= 200 or self.rect.y <= 50:  # reverses direction when buff goes out of range
            self.speed *= -1


def display_score():
    global score
    score_surf = font.render(f'Score: {int(score)}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(midbottom=(400, 50))
    screen.blit(score_surf, score_rect)


def display_high_score():
    global score
    high_score_surf = font.render(f'High Score: {int(max(high_score, score))}', False, (111, 196, 169))
    high_score_rect = high_score_surf.get_rect(bottomright=(775, 50))
    screen.blit(high_score_surf, high_score_rect)


def end_score():
    end_score_surf = font.render(f'Final Score: {int(score)}', False, (64, 64, 64))
    end_score_rect = end_score_surf.get_rect(center=(400, 330))
    screen.blit(end_score_surf, end_score_rect)


def collision():
    global invincibility, lives, start_time, transparency, game_phase
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False) and not invincibility:
        if lives > 1:
            lives -= 1
            transparency = 255
            invincibility = True
            start_time = pygame.time.get_ticks()
            return game_phase  # for game_phase variable
        else:
            obstacle_group.empty()
            buff_group.empty()
            return 0  # for game_phase variable
    else:
        return game_phase  # if collision does not occur game_phase remains the same


def buff_collision():
    global invincibility, invincibility_check, plus_five_check, score, x2, x2_check, start_time, lives, heart_check, transparency
    if pygame.sprite.spritecollide(player.sprite, buff_group, False):
        transparency = 255
        buff_group.empty()
        start_time = pygame.time.get_ticks()
        if invincibility_check:  # checks which buff was sent and which buff to activate
            invincibility_check = False
            invincibility = True
        elif plus_five_check:
            score += 5
            plus_five_check = False
        elif heart_check:
            if lives < 3:
                lives += 1
            heart_check = False
        elif x2_check:
            x2 = True
            x2_check = False


def instructions():
    screen.blit(menu_icon_surf, menu_icon_rect)
    if menu_icon_rect.collidepoint(pygame.mouse.get_pos()):
        screen.blit(instruction_surf, instruction_rect)


def buff_status(buff):
    global transparency
    status = pygame.image.load(f'graphics/buffs/{buff}.png').convert_alpha()
    status = pygame.transform.rotozoom(status, 0, 0.1)
    status.set_alpha(int(transparency))
    status_rect = status.get_rect(bottomleft=(0, 400))
    screen.blit(status, status_rect)

    transparency -= 0.425  # 0.425 = (transparency max limit) / ((no of sec of timer) X fps)
    if transparency <= 0:
        transparency = 0


user = login_page.login('Flappy_Bird')

mycon = sqltor.connect(host='localhost', user='root', passwd='12345678', database='Flappy_Bird')
if mycon.is_connected():
    cursor = mycon.cursor()
    cursor.execute(f"select high_score from login_credentials where username = '{user}'")
    data = cursor.fetchone()
    high_score = data[0]

    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption('Flappy Bird')
    clock = pygame.time.Clock()
    font = pygame.font.Font('font/Pixeltype.ttf', 50)

    '''
    0 - end/start screen
    1 - mode settings
    2 - easy (powerups and hearts)
    3 - moderate (hearts)
    4 - hard (no powerups or hearts)
    '''
    game_phase = 0
    game_start = False
    score = 0

    bg_music = pygame.mixer.Sound('audio/music.wav')
    bg_music.set_volume(0.5)
    bg_music.play(loops=-1)

    player = pygame.sprite.GroupSingle()  # creates a group for single object
    player.add(Owl())

    obstacle_group = pygame.sprite.Group()  # creates a grp for multiple objects(obstacles)

    wave = pygame.sprite.GroupSingle()  # creates a grp for single object
    wave.add(Wave())

    buff_group = pygame.sprite.GroupSingle()  # creates a grp for multiple objects(buff)

    sky_surface = pygame.image.load('graphics/sky.png').convert_alpha()
    sky_surface_x_pos = 0

    owl_stand = pygame.image.load('graphics/owl/owl1.png').convert_alpha()
    owl_stand = pygame.transform.rotozoom(owl_stand, 0, 0.6)
    owl_stand_rect = owl_stand.get_rect(center=(400, 200))
    pygame.display.set_icon(owl_stand)  # sets game icon to owl

    game_name = font.render('Flappy Bird', False, (111, 196, 169))
    game_name_rect = game_name.get_rect(center=(400, 70))
    game_message = font.render('Press space to fly', False, (111, 196, 169))
    game_message_rect = game_message.get_rect(center=(400, 320))

    menu_icon_surf = pygame.image.load('graphics/menu_icon.webp').convert_alpha()
    menu_icon_surf = pygame.transform.rotozoom(menu_icon_surf, 0, 0.4)
    menu_icon_rect = menu_icon_surf.get_rect(topright=(810, -10))
    instruction_surf = pygame.image.load('graphics/instructions.png').convert_alpha()
    instruction_surf = pygame.transform.rotozoom(instruction_surf, 0, 0.75)
    instruction_rect = instruction_surf.get_rect(topright=(800, 25))

    username_surf = font.render(f'{user.upper()}', False, (111, 196, 169))
    username_rect = username_surf.get_rect(bottomleft=(25, 50))

    heart_surf = pygame.image.load('graphics/heart.png').convert_alpha()
    heart_surf = pygame.transform.rotozoom(heart_surf, 0, 0.1)
    lives = 3

    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1500)

    buff_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(buff_timer, 20000)

    start_time = 0  # for stopping the buff effect after set period of time
    duration = 10000

    debuff_timer = None
    transparency = 255

    easy_surf = font.render('Easy', False, (0, 0, 102))
    easy_rect = username_surf.get_rect(topleft=(190, 310))

    moderate_surf = font.render('Moderate', False, (0, 0, 102))
    moderate_rect = username_surf.get_rect(topleft=(325, 310))

    hard_surf = font.render('Hard', False, (0, 0, 102))
    hard_rect = username_surf.get_rect(topleft=(515, 310))

    invincibility, invincibility_check, plus_five_check, x2_check, x2, heart_check = False, False, False, False, False, False

    while True:
        print(game_phase, lives)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_phase == 0:
                    score = 0
                    game_phase = 1

            if event.type == obstacle_timer and game_phase in [2, 3, 4]:  # creation of pillars
                height = random.randint(50, 175)  # for random heights
                pillar_xpos = random.randint(900, 1100)  # for random spacing bw pillars
                obstacle_group.add(Obstacle(pillar_xpos, height))
                obstacle_group.add(
                    Obstacle(pillar_xpos, height + 350))  # 350 - height of pillar is the set space bw pillars

            if event.type == buff_timer and game_phase == 2:
                Type = random.choice(['invincibility', '+5', 'X2', 'heart', '', ''])  # for random buff or no buff
                if Type == 'invincibility':  # tell the buff_collide fn about which buff was sent
                    invincibility_check = True
                elif Type == '+5':
                    plus_five_check = True
                elif Type == 'X2':
                    x2_check = True
                elif Type == 'heart':
                    heart_check = True
                if Type != '':
                    buff_group.add(Buffs(Type))

        if (pygame.time.get_ticks() - start_time > duration) and game_phase in [2, 3]:
            invincibility = False
            x2 = False

        key = pygame.key.get_pressed()
        if (key[pygame.K_SPACE] or key[pygame.K_UP] or key[pygame.K_w] == 1) and game_phase == 0:
            score = 0
            game_phase = 1

        if game_phase in [2, 3, 4]:
            if game_phase == 4:
                lives = 0
            game_start = True

            screen.fill('#d0f4f7')
            screen.blit(sky_surface, (sky_surface_x_pos, 50))
            screen.blit(sky_surface, (sky_surface_x_pos + sky_surface.get_width(), 50))
            sky_surface_x_pos -= 1
            if sky_surface_x_pos <= -sky_surface.get_width():
                sky_surface_x_pos = 0  # loops the sky behind

            display_score()
            display_high_score()
            screen.blit(username_surf, username_rect)

            for i in range(lives):
                screen.blit(heart_surf, heart_surf.get_rect(bottomleft=(15 + i * 50, 100)))

            game_phase = collision()
            buff_collision()

            player.draw(screen)
            player.update()

            obstacle_group.draw(screen)
            obstacle_group.update()

            buff_group.draw(screen)
            buff_group.update()

            wave.draw(screen)
            wave.update()

            if invincibility:
                buff_status('invincibility')
            elif x2:
                buff_status('X2')

        elif game_phase in [1, 0]:
            screen.fill((94, 129, 162))
            screen.blit(owl_stand, owl_stand_rect)
            screen.blit(game_name, game_name_rect)

            if game_phase == 0:
                invincibility, invincibility_check, x2_check, x2 = False, False, False, False
                lives = 3
                transparency = 255
                if game_start:
                    end_score()
                    if high_score < score:
                        cursor.execute(
                            f"update login_credentials set high_score = {int(score)} where username = '{user}'")
                        mycon.commit()
                        high_score = score
                else:
                    screen.blit(game_message, game_message_rect)

            elif game_phase == 1:
                pygame.draw.rect(screen, (192, 192, 192), (175, 300, 105, 45), 0, 20)
                screen.blit(easy_surf, easy_rect)
                pygame.draw.rect(screen, (192, 192, 192), (310, 300, 165, 45), 0, 20)
                screen.blit(moderate_surf, moderate_rect)
                pygame.draw.rect(screen, (192, 192, 192), (500, 300, 105, 45), 0, 20)
                screen.blit(hard_surf, hard_rect)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_rect.collidepoint(event.pos):
                        game_phase = 2
                    if moderate_rect.collidepoint(event.pos):
                        game_phase = 3
                    if hard_rect.collidepoint(event.pos):
                        game_phase = 4
            instructions()

        pygame.display.update()
        clock.tick(60)
else:
    print('mysql backend connection problem')
