import pygame
import sys
import pymunk
import pymunk.pygame_util
import random
import math
import time


def create_ball(mass, radius, x, y):  # 输入质量、半径和横坐标
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))  # 惯性
    body = pymunk.Body(mass, inertia)  # 刚体
    body.position = x, y
    shape = pymunk.Circle(body, radius, (0, 0))  # 形状
    shape.elasticity = 0.4
    shape.friction = 0.2
    space.add(body, shape)
    globals()['balls_' + str(radius)].append(shape)


def remove_ball(ball, balls):
    space.remove(ball, ball.body)
    balls.remove(ball)


def update_screen(level, x):
    global last
    global time_start
    global game_continue
    global warn
    global gif
    highest = 130

    screen.blit(background, (0, 0))
    screen.blit(warn_line, (0, 120))
    time_now = time.time()
    score_now = score_get()
    cqu_num = cqu_get()
    score = font.render('score:' + str(int(score_now)), True, (150, 150, 150))
    num = font.render('how many CQU are synthesized:' + str(cqu_num), True, (150, 150, 150))
    the_time = font.render('time:' + str(round(time_now - time_begin, 2)), True, (150, 150, 150))
    # 读取最高分
    with open('highest_score', 'r') as f:
        highest_before = f.readlines()
        highest_score = font.render('highest_score:' + highest_before[0].replace('\n', ''), True, (150, 150, 150))
        most_cqu = font.render('most_cqu:' + highest_before[1], True, (150, 150, 150))

    if warn:
        screen.blit(warning, (0, 0))
    screen.blit(score, (0, -5))
    screen.blit(num, (0, 25))
    screen.blit(highest_score, (0, 55))
    screen.blit(most_cqu, (0, 85))
    gif_2 = gif // 4
    screen.blit(globals()['rua_' + str(gif_2)], (450, 7))
    screen.blit(the_time, (400, -5))
    if gif < 19:
        gif += 1
    else:
        gif = 1

    img_1 = globals()['cqu_' + str(level)]
    img_radius = img_1.get_width() / 2
    screen.blit(img_1, (x - img_radius, 60 - img_radius))
    space.debug_draw(draw_options)
    for i in level_radius[1:11]:
        balls = globals()['balls_' + str(i)]
        for ball in balls:
            level_str = level_radius_list[str(int(ball.radius))]
            img_2 = pygame.transform.rotate(globals()['cqu_' + level_str], -math.degrees(ball.body.angle))
            screen.blit(img_2, (ball.body.position.x - img_2.get_width() / 2, ball.body.position.y - img_2.get_height() / 2))

            if ball.body.position.y - ball.radius < highest:
                highest = ball.body.position.y - ball.radius

            for ball_2 in balls:
                det_x = ball_2.body.position.x - ball.body.position.x
                det_y = ball_2.body.position.y - ball.body.position.y
                if ball_2 != ball and math.pow(det_x, 2) + math.pow(det_y, 2) < math.pow(ball_2.radius + ball.radius + 3, 2):
                    sound.play()
                    create_ball(level_mass[int(level_str) + 1], level_radius[int(level_str) + 1], (ball_2.body.position.x + ball.body.position.x) / 2, (ball_2.body.position.y + ball.body.position.y) / 2)
                    remove_ball(ball, balls)
                    remove_ball(ball_2, balls)

    if highest < 120 and not last:
        time_start = time.time()
        last = True
    elif highest < 120 and last:
        time_end = time.time()
        if time_end - time_start > 2:
            warn = True
        if time_end - time_start > 5:
            game_continue = False
    else:
        last = False
        warn = False

    flag = False  # 判断是否需要更新最高分数据
    if score_now > int(highest_before[0]):
        highest_before[0] = str(int(score_now))
        flag = True
    if cqu_num > int(highest_before[1]):
        highest_before[1] = str(int(cqu_num))
        flag = True
    if flag:
        with open('highest_score', 'w') as f:
            f.write('\n'.join(highest_before))

    pygame.display.update()


def the_event(level):
    x, y = pygame.mouse.get_pos()

    # 防止球刷到外面去的bug
    if x < 10:
        x = 10
    if x > 590:
        x = 590

    update_screen(level, x)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            create_ball(level_mass[level], level_radius[level], x, 60)
            return True
    return False


def score_get():
    score = 0
    for i in range(1, 12):
        balls = globals()['balls_' + str(level_radius[i])]
        for ball in balls:
            score += math.pow(2, i - 1)
    return score


def cqu_get():
    num = 0
    for ball in balls_148:
        num += 0
    return num


if __name__ == '__main__':
    # pygame初始化
    pygame.init()
    screen = pygame.display.set_mode((600, 1000))
    clock = pygame.time.Clock()
    cqu_1 = pygame.image.load('balls/cqu1.png')
    cqu_2 = pygame.image.load('balls/cqu2.png')
    cqu_3 = pygame.image.load('balls/cqu3.png')
    cqu_4 = pygame.image.load('balls/cqu4.png')
    cqu_5 = pygame.image.load('balls/cqu5.png')
    cqu_6 = pygame.image.load('balls/cqu6.png')
    cqu_7 = pygame.image.load('balls/cqu7.png')
    cqu_8 = pygame.image.load('balls/cqu8.png')
    cqu_9 = pygame.image.load('balls/cqu9.png')
    cqu_10 = pygame.image.load('balls/cqu10.png')
    cqu_11 = pygame.image.load('balls/cqu11.png')
    background = pygame.image.load('back_mask/background.png')
    warning = pygame.image.load('back_mask/warning.png')
    over = pygame.image.load('back_mask/game_over.png')
    warn_line = pygame.image.load('back_mask/line.png')
    rua_0 = pygame.image.load('rua_cqu/rua_1.png')
    rua_1 = pygame.image.load('rua_cqu/rua_2.png')
    rua_2 = pygame.image.load('rua_cqu/rua_3.png')
    rua_3 = pygame.image.load('rua_cqu/rua_4.png')
    rua_4 = pygame.image.load('rua_cqu/rua_5.png')
    sound = pygame.mixer.Sound('sound/sound.wav')
    sound.set_volume(0.3)
    pygame.mixer.music.load('sound/moemoesweeper.mp3')
    pygame.mixer.music.set_volume(0.1)
    # pymunk初始化
    space = pymunk.Space()
    space.gravity = (0, 10)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    # 窗口边框
    static_lines = [
        pymunk.Segment(space.static_body, (0, 0), (0, 1000), 0.0),
        pymunk.Segment(space.static_body, (600, 0), (600, 1000), 0.0),
        pymunk.Segment(space.static_body, (0, 1000), (600, 1000), 0.0)
    ]
    for line in static_lines:
        line.elasticity = 0.4  # 弹性系数
        line.friction = 0.2  # 摩擦系数
        space.add(line)
    # level对应的碰撞半径
    level_radius = [0, 24, 34, 56, 63, 73, 103, 113, 123, 136, 147, 148]
    # 所有的ball
    for i in level_radius[1:]:
        globals()['balls_' + str(i)] = []
    # 碰撞半径对应的level
    level_radius_list = {
        '24': '1',
        '34': '2',
        '56': '3',
        '63': '4',
        '73': '5',
        '103': '6',
        '113': '7',
        '123': '8',
        '136': '9',
        '147': '10',
        '148': '11',
    }
    # level对应的质量
    level_mass = [0, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    # 字体
    font = pygame.font.Font('ARIALN.TTF', 30)

    pygame.mixer.music.play(-1)
    time_start = time.time()
    time_begin = time.time()
    choose = True
    game_continue = True
    last = False
    warn = False
    gif = 0
    while game_continue:
        for i in range(5):
            space.step(0.04)
        if choose:
            level = random.randint(1, 3)
            choose = False
        choose = the_event(level)
        clock.tick(60)

    screen.blit(over, (0, 0))
    game_over = font.render('GAME OVER YOU ARE LOST', True, (0, 0, 0))
    screen.blit(game_over, (300 - game_over.get_width() / 2, 500 - game_over.get_height() / 2))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
