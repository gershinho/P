import pygame

pygame.init()



Width,Height = 700,500
win = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("Pong")

FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)




PADDLE_WIDTH,PADDLE_HEIGHT = 20,100
BAll_RADIUS = 7

SCORE_FONT = pygame.font.SysFont('comicsans', 50)
WINNING_SCORE = 1


class Paddle:
    COLOR = WHITE
    VEL = 7
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self,win):
        pygame.draw.rect(win, self.COLOR, (self.x,self.y,self.width,self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = 8
    COLOR = WHITE
    def __init__(self,x,y,radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win,self.COLOR,(self.x,self.y),self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1









def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(right_score_text, (Width * (3/4) - right_score_text.get_width() // 2, 20))
    win.blit(left_score_text, (Width//4 - left_score_text.get_width()//2, 20))
    for paddle in paddles:
        paddle.draw(win)

    Line = True
    for i in range(10,Height, Height//20):
       if Line:
           if i%2 == 1:
               continue
           pygame.draw.rect(win, WHITE, (Width // 2 - 5, i, 10, Height // 20))


    ball.draw(win)
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= Height:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys,left_paddle,right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= Height:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= Height:
        right_paddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, Height // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(Width - 10 - PADDLE_WIDTH, Height//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(Width // 2, Height//2, BAll_RADIUS)
    left_score = 0
    right_score = 0
    while run:
        clock.tick(FPS)
        draw(win, [left_paddle, right_paddle], ball, left_score, right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1

            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

        elif ball.x > Width:
            left_score += 1

            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

        won = False
        if left_score >= WINNING_SCORE:
           won = True
           win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            win_text = "Right player Won!"
            won = True

        if won:
            Line = False
            text = SCORE_FONT.render(win_text,1,WHITE)
            win.blit(text, (Width//2 - text.get_width()//2,Height//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(1000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()

def home_screen():
    font = pygame.font.Font('freesansbold.ttf', 40)
    home_text = font.render('First to 5 wins!', True, WHITE)
    begin_text = font.render('Press SPACE to start!', True, WHITE)
    run = True
    while run:
        win.fill(BLACK)
        home_text_rect = home_text.get_rect(center=(Width / 2, Height / 2))
        win.blit(home_text, home_text_rect)  
        begin_text_rect = begin_text.get_rect(center=(Width / 2, home_text_rect.bottom + 20))  # Place begin text below home text
        win.blit(begin_text, begin_text_rect)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()  # Make sure to exit if the window is closed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False  # Exit the loop to start the main game

    main()  # Start the main game loop after the space bar is pressed


if __name__ == "__main__":
    home_screen()




