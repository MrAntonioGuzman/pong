import pygame, sys, time, random
from pygame.locals import *


pygame.init()

# COLORS USED
BACKGROUND_COLOR = (105,105,105)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN = (0,128,0)

# SCREEN DIMENSIONS
WINDOWWIDTH = 800
WINDOWHEIGHT = 500


# SOUND EFFECTS
hitSound = pygame.mixer.Sound('slimeball.wav')
pygame.mixer.music.load('background.mid')
pygame.mixer.music.play(-1, 0.0)

class Paddle:
    def __init__(self, surface, rect, speed, color):
        self.rect = rect
        self.y_orig = pygame.Rect((20, 200), (5, 70))
        self.x_orig_b = pygame.Rect((165, 400), (70, 5))
        self.x_orig_t = pygame.Rect((165, 20), (70, 5))
        self.p_right = pygame.Rect((780, 200), (5, 70))
        self.p_top = pygame.Rect((565, 20), (70, 5))
        self.p_bottom = pygame.Rect((565, 400), (70, 5))
        self.surface = surface
        self.color = color
        self.speed = speed


    def reset(self, pos, user):
        if user == 'c':
            if pos == 'l':
                self.rect.center = self.y_orig.center
            elif pos == 't':
                self.rect.center = self.x_orig_t.center
            else:
                self.rect.center = self.x_orig_b.center
        else:
            if pos == 'r':
                self.rect.center = self.p_right.center
            elif pos == 't':
                self.rect.center = self.p_top.center
            else:
                self.rect.center = self.p_bottom.center

    def get_rect(self):
        return self.rect

    def move_left(self):
        self.rect.move_ip(self.speed * -1, 0)
    
    def move_right(self):
        self.rect.move_ip(self.speed, 0)
    
    def move_up(self):
        self.rect.move_ip(0, self.speed * -1)
    
    def move_down(self):
        self.rect.move_ip(0, self.speed)
        
    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
    


class Ball:
    def __init__(self, surface, x_start, y_start, vector, color):
        self.surface = surface
        self.x_start = x_start
        self.y_start = y_start
        self.x = x_start
        self.y = y_start
        self.vector = vector
        self.color = color
        self.rect = None
        self.speed = random.randint(2, 4)
    
    def get_vector(self):
        return self.vector

    def get_r(self):
        return self.rect

    def reset(self, v):
        x = [2, -2]
        self.speed = random.randint(2, 4)
        self.vector = pygame.Vector2(random.choice(x), random.choice(x)) * self.speed
        self.x = self.x_start
        self.y = self.y_start
        self.rect = pygame.draw.circle(self.surface, self.color, (int(self.x_start), int(self.y_start)), 15)
    
    def change_x(self):
        speed = random.randint(2, 4)
        self.vector[0] *= -1
    
    def change_y(self):
        speed = random.randint(2, 4)
        self.vector[1] *= -1

    def move(self):
        self.x += self.vector[0]
        self.y += self.vector[1]
        self.draw()

    def draw(self):
        self.rect = pygame.draw.circle(self.surface, self.color, (int(self.x), int(self.y)), 15)



class Text:
    def __init__(self, surface, text_obj, pos_x, pos_y):
        self.text_obj = text_obj
        self.text_rect = self.text_obj.get_rect()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text_rect.topleft = (pos_x, pos_y)
        self.surface = surface
    
    def get_text_obj(self):
        return self.text_obj

    def get_text_rect(self):
        return self.text_rect

    def update(self, text):
        self.text_obj = text
        self.text_rect = self.text_obj.get_rect()
        self.text_rect.topleft = (self.pos_x, self.pos_y)
        self.draw()
    
    def draw(self):
        self.surface.blit(self.text_obj, self.text_rect)


def draw_dashed_line(surface):
    surface_rect = surface.get_rect()
    DASH_WIDTH = 5
    DASH_HEIGHT = 30
    X_POSITION = int(surface_rect.width / 2)
    Y_POSITION = 10
    Y_OFFSET = 20
    for _ in range(int(surface_rect.height / 50)):
        pygame.draw.line(surface, (255, 255, 255), (X_POSITION, Y_POSITION), (X_POSITION, Y_POSITION+DASH_HEIGHT), DASH_WIDTH)
        Y_POSITION += Y_OFFSET + DASH_HEIGHT
        

def handle_player_keys(right_rect, top_rect, bottom_rect, boundary_rect, velocity):
    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT]:
        top_rect.move_left()
        bottom_rect.move_left()

    if key[pygame.K_RIGHT]:
        top_rect.move_right()
        bottom_rect.move_right()

    if key[pygame.K_UP]:
        right_rect.move_up()

    if key[pygame.K_DOWN]:
        right_rect.move_down()

    right_rect.get_rect().clamp_ip(boundary_rect)
    top_rect.get_rect().clamp_ip(boundary_rect)
    bottom_rect.get_rect().clamp_ip(boundary_rect)



def handle_computer_control(bottom_rect, top_rect, left_rect, circle_rect, boundary_rect, v, velocity):
    velocity = r_velocity = 4
    b_center = circle_rect.center
    bc = bottom_rect.get_rect().center
    tc = top_rect.get_rect().center
    cx = top_rect.get_rect().center[0]
    
    # LEFT PADDLE
    lc = left_rect.get_rect().center
    ly = lc[1]
    
    if cx > b_center[0]:
        cx -= velocity

    if cx < b_center[0]:
        cx += velocity

    if ly > b_center[1]:
        ly -= r_velocity

    if ly < b_center[1]:
        ly += r_velocity
    
    
    top_rect.get_rect().center = (cx, tc[1])
    bottom_rect.get_rect().center = (cx, bc[1])
    left_rect.get_rect().center = (lc[0], ly)
    
    left_rect.get_rect().clamp_ip(boundary_rect)
    top_rect.get_rect().clamp_ip(boundary_rect)
    bottom_rect.get_rect().clamp_ip(boundary_rect)



def draw_scores(c_text, p_text, g_text, w_text):
    c_text.draw()
    p_text.draw()
    g_text.draw()
    w_text.draw()


def draw_paddles(p_top, p_right, p_bottom, c_top, c_left, c_bottom):
    p_top.draw()
    p_right.draw()
    p_bottom.draw()

    c_top.draw()
    c_left.draw()
    c_bottom.draw()


def handle_winner(p_game, c_game):
    if p_game > 3:
        return 'You Won!'
    elif c_game > 3:
        return 'You Lost!'
    else:
        return 'No Winner'
    


def reset(c_top, c_left, c_bottom, p_top, p_right, p_bottom):
    c_top.reset('t', 'c')
    c_left.reset('l', 'c')
    c_bottom.reset('b', 'c')
    p_top.reset('t', 'p')
    p_right.reset('r', 'p')
    p_bottom.reset('b', 'p')


def reset_comp(c_top, c_left, c_bottom):
    c_top.reset('t', 'c')
    c_left.reset('l', 'c')
    c_bottom.reset('b', 'c')



screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
font = pygame.font.SysFont(None, 48)
s_font = pygame.font.SysFont(None, 28)

GAME_BOUNDARY = pygame.Rect((0, 0), (800, 420))
player_boundary_rect = pygame.Rect(400, 20, 380, 380)
comp_boundary_rect = pygame.Rect(20, 20, 380, 380)

player_rect_right = pygame.Rect((780, 200), (5, 70))
player_rect_top = pygame.Rect((565, 20), (70, 5))
player_rect_bottom = pygame.Rect((565, 400), (70, 5))

comp_rect_left = pygame.Rect((20, 200), (5, 70))
comp_rect_top = pygame.Rect((165, 20), (70, 5))
comp_rect_bottom = pygame.Rect((165, 400), (70, 5))

VELOCITY = 10
p_right = Paddle(screen, player_rect_right, VELOCITY, WHITE)
p_top = Paddle(screen, player_rect_top, VELOCITY, WHITE)
p_bottom = Paddle( screen, player_rect_bottom, VELOCITY, WHITE)

c_left = Paddle(screen, comp_rect_left, VELOCITY, WHITE)
c_top = Paddle(screen, comp_rect_top, VELOCITY, WHITE)
c_bottom = Paddle(screen, comp_rect_bottom, VELOCITY, WHITE)

speed = 2
x, y = 400, 250
v = pygame.Vector2(2, 2) * speed
ball = Ball(screen, x, y, v, WHITE)

computer_text = s_font.render('COMPUTER: 0', 1, WHITE)
player_text = s_font.render('PLAYER: 0', 1, WHITE)
game_text = s_font.render('GAME: 0', 1, WHITE)
win_game_text = s_font.render('WIN GAME: 3', 1, WHITE)

WINNING_SCORE = 11
clock = pygame.time.Clock()
random_dir = [0, 1]

while True:
    
    p_score = 0
    c_score = 0
    outcome = ''
    game = 0
    p_game = 0
    c_game = 0
    winner = None
    w_game = 3
    score_reached = False
    reset(c_top, c_left, c_bottom, p_top, p_right, p_bottom)
    ball.reset(v)
    g_text = Text(screen, game_text, 40, 450)
    c_text = Text(screen, computer_text, 240, 450)
    p_text = Text(screen, player_text, 440, 450)
    w_text = Text(screen, win_game_text, 640, 450 )

    while not score_reached:
        for event in pygame.event.get():  # quit?
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BACKGROUND_COLOR)
        draw_dashed_line(screen)
        p_text.update(s_font.render('PLAYER: ' + str(p_score), 1, WHITE))
        c_text.update(s_font.render('COMPUTER: ' + str(c_score), 1, WHITE))
        w_text.update(s_font.render('WIN GAME: ' + str(w_game), 1, WHITE))
        g_text.update(s_font.render('GAME: ' + str(game), 1, WHITE))
        draw_scores(c_text, p_text, g_text, w_text)
        draw_paddles(p_top, p_right, p_bottom, c_top, c_left, c_bottom)
        handle_player_keys(p_right, p_top, p_bottom, player_boundary_rect, VELOCITY)
        if ball.x < 380:
            handle_computer_control(c_bottom, c_top, c_left, ball.get_r(), comp_boundary_rect, ball.get_vector(), VELOCITY)
        else:
            reset_comp(c_top, c_left, c_bottom)

        ball.move()
        # LEFT AND RIGHT SITUATIONS
        if ball.x < GAME_BOUNDARY.left:
            ball.reset(v)
            p_score += 1
        
        if ball.x > GAME_BOUNDARY.right:
            ball.reset(v)
            c_score += 1            

        # UP AND DOWN SITUATIONS
        if (ball.x < GAME_BOUNDARY.width / 2) and (ball.y not in range(GAME_BOUNDARY.top, GAME_BOUNDARY.bottom)):
            ball.reset(v)
            p_score += 1
            
        if (ball.x > GAME_BOUNDARY.width / 2) and (ball.y not in range(GAME_BOUNDARY.top, GAME_BOUNDARY.bottom)):
            ball.reset(v)
            c_score += 1
            
        
        paddle_list = [
            p_right.get_rect(),
            c_left.get_rect(),
            p_top.get_rect(),
            p_bottom.get_rect(),
            c_top.get_rect(),
            c_bottom.get_rect()
        ]
        
        hit = ball.get_r().collidelist(paddle_list)
        if hit != -1:
            hitSound.play()
            if hit in range(0, 2):
                ball.change_x()
            if hit in range(2, 6):
                ball.change_y()
                r = random.choice(random_dir)

        pygame.display.update()   # blit all updates to screen at once

        if p_score == 11 or c_score == 11:
            remainder = abs(p_score - c_score)
            if remainder >= 2:
                game += 1
                if p_score > c_score:
                    p_game += 1
                    w_game = 3 - p_game
                else:
                    c_game += 1
                if p_game == 3 or c_game == 3:
                    winner = 'You Won!' if p_game == 3 else 'You Lost!'
                    score_reached = True
            p_score = 0
            c_score = 0

    dialogue_box = pygame.Rect((200, 100), (400, 300))
    message_rect = pygame.Rect((220, 150), (200, 50))
    message_text = font.render(winner+' Play Again?', 1, (0, 0, 0))

    yes_rect = pygame.Rect((250, 250), (100, 100))
    yes_text = font.render('YES', 1, GREEN)
    yes_rect = yes_text.get_rect()
    yes_rect.topleft = (275, 300)

    no_rect = pygame.Rect((450, 250), (100, 100))
    no_text = font.render('NO', 1, RED)
    no_rect = yes_text.get_rect()
    no_rect.topleft = (475, 300)

    btn_clicked = False

    while not btn_clicked:
        for event in pygame.event.get():  # quit?
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if yes_rect.collidepoint(pos):
                    btn_clicked = True

                if no_rect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
        
        screen.fill(Color('#303030'))
        pygame.draw.rect(screen,(255,255,255), dialogue_box)
        screen.blit(message_text, message_rect)
        screen.blit(yes_text, yes_rect)
        screen.blit(no_text, no_rect)
        pygame.display.update()
    




