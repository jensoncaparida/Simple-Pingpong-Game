
import pygame, sys

pygame.init()

Width = 1000
Height = 600

black = (0, 0, 0)
brown = (150, 75, 0)
red = (204, 0, 0)
gray = (105, 105, 105)
blue = (0, 0, 255)
springgreen = (0, 255, 127)
white = (255, 255, 255)
clock = pygame.time.Clock()
opacity = (255, 255, 255, 0.3)
myFont = pygame.font.SysFont("Times New Roman", 30)
myFont1 = pygame.font.SysFont("Times New Roman", 50)
myFont2 = pygame.font.SysFont("Times New Roman", 40)
myFont3 = pygame.font.SysFont("Times New Roman", 70)
font = pygame.font.SysFont('Times New Roman', 80, bold=True)

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Ping Pong')
pingpong = pygame.image.load('thumbnails/pingpong-logo.png')
pygame.display.set_icon(pingpong)

class Ball:
    def __init__(self, screen, color, posX, posY, radius):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.dx = 0
        self.dy = 0
        self.show()

    def show(self):
        pygame.draw.circle(self.screen, self.color, (self.posX, self.posY), self.radius)

    def start(self):
        self.dx = 20
        self.dy = 10

    def move(self):
        self.posX += self.dx
        self.posY += self.dy

    def paddle_collision(self):
        self.dx = -self.dx

    def wall_collision(self):
        self.dy = -self.dy

    def restart_pos(self):
        self.posX = Width//2
        self.posY = Height//2
        self.dx = 0
        self.dy = 0
        self.show()


class Paddle:
    def __init__(self, screen, color, posX, posY, width, height):
        self.screen = screen
        self.color = color
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.state = "stopped"
        self.show()

    def show(self):
        pygame.draw.rect(self.screen, self.color, (self.posX, self.posY, self.width, self.height))

    def move(self):
        if self.state == "up":
            self.posY -= 10
        elif self.state == "down":
            self.posY += 10

    def limit(self):
        if self.posY <= 0:
            self.posY = 0

        if self.posY + self.height >= Height:
            self.posY = Height - self.height

    def restart_pos(self):
        self.posY = Height//2 - self.height//2
        self.state = 'Stopped'
        self.show()

class Score:
    def __init__(self, screen, points, posX, posY):
        self.screen = screen
        self.points = points
        self.posX = posX
        self.posY = posY
        self.font = pygame.font.SysFont("Times New Roman", 80, bold=True)
        self.label = self.font.render(self.points, 0, white)
        self.show()

    def show(self):
        self.screen.blit(self.label, (self.posX - self.label.get_rect().width//2, self.posY))

    def increase(self):
        points = int(self.points) + 1
        self.points = str(points)
        self.label = self.font.render(self.points, 0, springgreen)

    def restart(self):
        self.points = '0'
        self.label = self.font.render(self.points, 0, white)


class Collision:
    def ball_and_paddle1(self, ball, paddle1):
        if ball.posY + ball.radius > paddle1.posY and ball.posY - ball.radius < paddle1.posY + paddle1.height:
            if ball.posX - ball.radius <= paddle1.posX + paddle1.width:
                return True

        return False


    def ball_and_paddle2(self, ball, paddle2):
        if ball.posY + ball.radius > paddle2.posY and ball.posY - ball.radius < paddle2.posY + paddle2.height:
            if ball.posX + ball.radius >= paddle2.posX:
                return True

        return False

    def ball_and_walls(self, ball):
        if ball.posY - ball.radius <= 0:
            return True
        if ball.posY + ball.radius >= Height:
            return True

        return False

    def goal_player1(self, ball):
        return ball.posX - ball.radius >= Width

    def goal_player2(self, ball):
        return ball.posX + ball.radius <= 0

def back():
    screen.fill(gray)
    pygame.draw.line(screen, black, (Width//2, 0), (Width//2, Height), 5)
def line():
    pygame.draw.line(screen, black, (Width // 2, 0), (Width // 2, Height), 5)

def restart():
    back()
    score1.restart()
    score2.restart()
    ball.restart_pos()
    paddle1.restart_pos()
    paddle2.restart_pos()
    gaming()

def create_button(x, y, width, height, hovercolor, defaultcolor):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hovercolor, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, defaultcolor, (x, y, width, height))

def mainMenu():
    screen.fill(gray)
    pingpong = pygame.image.load('thumbnails/pingpong.png')
    screen.blit(pingpong, (Width // 2 - 225, Height // 2 - 250))
    Play = myFont1.render("Play", 1, red)
    Howtoplay = myFont1.render("How to Play", 1, red)
    Credits = myFont1.render("Credits", 1, red)
    Exit = myFont1.render("Exit", 1, red)
    About = pygame.image.load('thumbnails/about.png')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    mainscreen()


        p1 = create_button(Width//2 - 75, 160, 90, 60, opacity, gray)
        screen.blit(Play, (Width//2 - 75, 160))
        if p1:
            gaming()

        h1 = create_button(Width//2 - 150, 250, 250, 60, opacity, gray)
        screen.blit(Howtoplay, (Width//2 - 150, 250))
        if h1:
            howtoplayscreen()

        c1 = create_button(Width // 2 - 100, 350, 150, 60, opacity, gray)
        screen.blit(Credits, (Width // 2 - 100, 350))
        if c1:
            credits()


        e1 = create_button(Width // 2 - 75, 450, 90, 60, opacity, gray)
        screen.blit(Exit, (Width // 2 - 75, 450))
        if e1:
            pygame.quit()
            sys.exit()

        a1 = create_button(15, 500, 60, 60, opacity, gray)
        screen.blit(About, (10, 500))
        if a1:
            about()


        pygame.display.update()
        clock.tick(30)

def howtoplayscreen():
    screen.fill(gray)
    Howtoplay = myFont2.render("How to Play", 1, springgreen)
    P1 = myFont.render("Player 1", 1, white)
    W = myFont.render("Press W", 1, white)
    Wpic = pygame.image.load('thumbnails/up.png')
    S = myFont.render("Press S", 1, white)
    Spic = pygame.image.load('thumbnails/down.png')
    P2 = myFont.render("Player 2", 1, white)
    Up = pygame.image.load('thumbnails/Keyup.png')
    Pup = myFont.render("Press", 1, white)
    Uppic = pygame.image.load('thumbnails/up.png')
    Down = pygame.image.load('thumbnails/Keydown.png')
    Pdown = myFont.render("Press", 1, white)
    Downpic = pygame.image.load('thumbnails/down.png')
    next = myFont.render("Press Right arrow key to Guide", 1, white)

    while True:
        screen.blit(Howtoplay, (Width // 2 - 100, Height // 2 - 250))
        screen.blit(P1, (200, 100))
        screen.blit(W, (50, 200))
        screen.blit(Wpic, (50, 150))
        screen.blit(S, (55, 350))
        screen.blit(Spic, (50, 400))
        screen.blit(P2, (700, 100))
        screen.blit(Up, (930, 200))
        screen.blit(Pup, (850, 200))
        screen.blit(Uppic, (930, 150))
        screen.blit(Down, (930, 350))
        screen.blit(Pdown, (850, 350))
        screen.blit(Downpic, (930, 400))
        screen.blit(next, (550, 500))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    mainMenu()
                if event.key == pygame.K_RIGHT:
                    Guide()


        line()
        paddle1.show()
        paddle2.show()
        ball.show()

        pygame.display.update()
        clock.tick(30)

def Guide():
    while True:
        screen.fill(gray)
        Guide = myFont1.render("Guides", 1, springgreen)
        screen.blit(Guide, (Width // 2 - 60, Height // 2 - 200))
        Grestart = myFont.render("Press R to restart the game score", 1, white)
        screen.blit(Grestart, (Width // 2 - 200, Height // 2 - 100))
        esc = myFont.render("Press ESC to Main Menu", 1, white)
        screen.blit(esc, (Width // 2 - 150, Height//2))
        backspace = myFont.render("Press Backspace to Back", 1, white)
        screen.blit(backspace, (Width // 2 - 150, 400))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    howtoplayscreen()
                if event.key == pygame.K_ESCAPE:
                    mainMenu()


        pygame.display.update()
        clock.tick(30)


def credits():
    while True:
        screen.fill(gray)
        cs = pygame.image.load('thumbnails/credits.png')
        textscreen = myFont.render("Thanks to", 1, white)
        screen.blit(cs, (Width // 2 - 80, Height // 2 - 50))
        screen.blit(textscreen, (Width // 2 - 60, Height // 2 - 100))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or pygame.K_ESCAPE:
                    mainMenu()

def about():
    while True:
        screen.fill(gray)

        info = pygame.image.load('thumbnails/info.png')
        screen.blit(info, (1, 1))

        aboutscreen = myFont2.render("About", 1, springgreen)
        screen.blit(aboutscreen, (Width // 2 - 70, Height // 2 - 200))

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or pygame.K_ESCAPE:
                    mainMenu()

def mainscreen():
        screen.fill(gray)
        pingponglogo = pygame.image.load('thumbnails/pingpong-logo.png')
        screen.blit(pingponglogo, (Width // 2 - 150, Height // 2 - 150))
        pingpong = pygame.image.load('thumbnails/pingpong.png')
        screen.blit(pingpong, (Width // 2 - 225, Height // 2 - 50))
        guide = myFont.render("Press anywhere to Continue", 1, white)
        screen.blit(guide, (Width // 2 - 175, 500))


        pygame.display.update()
        clock.tick(30)



back()
# objects
score1 = Score(screen, '0', Width//4, 15)
score2 = Score(screen, '0', Width - Width//4, 15)
ball = Ball(screen, white, Width//2, Height//2, 20)
paddle1 = Paddle(screen, red, 10, Height//2 - 70, 20, 140)
paddle2 = Paddle(screen, blue, Width - 20 - 10, Height//2 - 70, 20, 140)
collision = Collision()
playing = False
bounce = pygame.mixer.Sound('thumbnails/bounce.wav')
warning = pygame.mixer.Sound('thumbnails/warning.wav')
nplaying = True

def gaming():
    back()
    # objects
    score1 = Score(screen, '0', Width // 4, 15)
    score2 = Score(screen, '0', Width - Width // 4, 15)
    ball = Ball(screen, white, Width // 2, Height // 2, 20)
    paddle1 = Paddle(screen, red, 10, Height // 2 - 70, 20, 140)
    paddle2 = Paddle(screen, blue, Width - 20 - 10, Height // 2 - 70, 20, 140)
    collision = Collision()
    playing = False
    bounce = pygame.mixer.Sound('thumbnails/bounce.wav')
    warning = pygame.mixer.Sound('thumbnails/warning.wav')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    playing = False

                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    mainMenu()

                if event.key == pygame.K_SPACE:
                    ball.start()
                    playing = True

                if event.key == pygame.K_w:
                    paddle1.state = 'up'
                if event.key == pygame.K_s:
                    paddle1.state = 'down'
                if event.key == pygame.K_UP:
                    paddle2.state = 'up'
                if event.key == pygame.K_DOWN:
                    paddle2.state = 'down'
            if event.type == pygame.KEYUP:
                paddle1.state = 'stopped'
                paddle2.state = 'stopped'



        if playing:
            back()

            ball.move()
            ball.show()

            paddle1.move()
            paddle1.limit()
            paddle1.show()

            paddle2.move()
            paddle2.limit()
            paddle2.show()

            if collision.ball_and_paddle1(ball, paddle1):
                ball.paddle_collision()
                if True:
                    bounce.play()
            if collision.ball_and_paddle2(ball, paddle2):
                ball.paddle_collision()
                if True:
                    bounce.play()

            if collision.ball_and_walls(ball):
                ball.wall_collision()

            if collision.goal_player1(ball):
                back()
                score1.increase()
                ball.restart_pos()
                paddle1.restart_pos()
                paddle2.restart_pos()
                playing = False
                if True:
                    warning.play()

            if collision.goal_player2(ball):
                back()
                score2.increase()
                ball.restart_pos()
                paddle1.restart_pos()
                paddle2.restart_pos()
                playing = False
                if True:
                    warning.play()

        score1.show()
        score2.show()

        pygame.display.update()
        clock.tick(30)


while True:
    mainscreen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mainMenu()








    pygame.display.update()
    clock.tick(30)

