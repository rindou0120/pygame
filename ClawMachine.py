import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Set screen size
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Claw Machine")

# Set application icon
icon = pygame.image.load("C:\introduce\pygame_clawer\img\icon.png")  # 請確認 icon.png 的路徑
pygame.display.set_icon(icon)

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Load and scale images
claw_image = pygame.image.load("C:\introduce\pygame_clawer\img\claw.png")
claw_image = pygame.transform.scale(claw_image, (50, 50))  # Adjust size

toy_image = pygame.image.load("C:\introduce\pygame_clawer\img\duck.png")
toy_image = pygame.transform.scale(toy_image, (50, 50))  # Adjust size

# Load fonts
font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 18)  # Smaller font for controls

# Clock for controlling game speed
clock = pygame.time.Clock()

class Claw:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 50
        self.speed = 5
        self.dropping = False
        self.holding = False
        self.retracting = False

    def move(self, direction):
        if direction == 'left' and self.x > 20:
            self.x -= self.speed
        if direction == 'right' and self.x < WIDTH - 20:
            self.x += self.speed

    def drop(self):
        if not self.dropping and not self.retracting:
            self.dropping = True

    def update(self, toy):
        if self.dropping:
            self.y += 5
            if self.y >= HEIGHT - 50:
                self.dropping = False
                self.retracting = True
                self.try_grab(toy)
        
        elif self.retracting:
            if self.holding:
                toy.x = self.x
                toy.y = self.y + 20
            self.y -= 5
            if self.y <= 50:
                self.retracting = False
                return True  # Determine result upon returning to the top
        return False

    def try_grab(self, toy):
        if abs(self.x - toy.x) < toy_image.get_width() // 2 and random.random() > 0.5:
            self.holding = True

    def draw(self):
        screen.blit(claw_image, (self.x - claw_image.get_width() // 2, self.y))

class Toy:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = HEIGHT - 50

    def reset_position(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = HEIGHT - 50

    def draw(self):
        screen.blit(toy_image, (self.x - toy_image.get_width() // 2, self.y - toy_image.get_height() // 2))

def show_message(text):
    screen.fill(WHITE)
    message = font.render(text, True, BLACK)
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

def draw_controls():
    controls = [
        "Controls:",
        "Left Arrow - Move Left",
        "Right Arrow - Move Right",
        "Down Arrow - Drop Claw"
    ]
    y_offset = 10
    for line in controls:
        text = small_font.render(line, True, BLACK)  # Use smaller font
        screen.blit(text, (10, y_offset))
        y_offset += 15  # Reduced line spacing

def draw_button(text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = GRAY if x < mouse[0] < x + width and y < mouse[1] < y + height else WHITE
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
    label = font.render(text, True, BLACK)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))
    if x < mouse[0] < x + width and y < mouse[1] < y + height and click[0] == 1:
        pygame.time.delay(200)
        if action:
            return action()
    return None

def ask_replay():
    screen.fill(WHITE)
    message = font.render("Play again?", True, BLACK)
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 3))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        replay = draw_button("Yes", WIDTH // 3 - 50, HEIGHT // 2, 100, 50, lambda: True)
        quit_game = draw_button("No", WIDTH * 2 // 3 - 50, HEIGHT // 2, 100, 50, lambda: False)
        
        if replay is not None:
            return replay
        if quit_game is not None:
            return quit_game
        
        pygame.display.flip()
    return False

running = True
while running:
    claw = Claw()
    toy = Toy()
    success = False
    grabbed = False
    
    while not success:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    claw.drop()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            claw.move('left')
        if keys[pygame.K_RIGHT]:
            claw.move('right')
        
        success = claw.update(toy)
        
        claw.draw()
        toy.draw()
        draw_controls()
        
        pygame.display.flip()
        clock.tick(30)
    
    show_message("Success!" if claw.holding else "Fail!")
    
    if not ask_replay():
        running = False

pygame.quit()
sys.exit()
