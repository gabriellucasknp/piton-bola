import sys
import random 
import pygame

# Configurações da grade
CELL_SIZE = 24  # Tamanho das células
COLS = 30       # Número de colunas (largura)
ROWS = 20       # Número de linhas (altura)
MARGIN_TOP = 36 # Espaço superior para o placar

# Cores (nomes em inglês seguindo convenções)
BG_COLOR = (0, 24, 0)        # Cor de fundo
GRID_COLOR = (12, 36, 18)    # Cor da grade
SNAKE_COLOR = (12, 36, 18)   # Cor da cobra
HEAD_COLOR = (200, 255, 200) # Cor da cabeça
FOOD_COLOR = (110, 200, 110) # Cor da comida
TEXT_COLOR = (180, 255, 180) # Cor do texto

# Inicialização do Pygame
pygame.init()
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + MARGIN_TOP  # Ajuste para incluir a margem superior
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Píton Bola")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 18, bold=True)

# Estado do jogo
score = 0
game_over = False

# Criando a cobra
snake = [
    (COLS // 2, ROWS // 2),
    (COLS // 2 - 1, ROWS // 2),
    (COLS // 2 - 2, ROWS // 2)
]
direction = (1, 0)  # Começa movendo para a direita

# Comida
def place_food():
    while True:
        pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if pos not in snake:
            return pos

food = place_food()

# Funções de desenho
def draw_cell(pos, color):
    x, y = pos
    rect = pygame.Rect(
        x * CELL_SIZE, 
        y * CELL_SIZE + MARGIN_TOP, 
        CELL_SIZE - 2, 
        CELL_SIZE - 2
    )
    pygame.draw.rect(screen, color, rect, border_radius=4)

def draw_snake():
    # Desenha a cabeça
    draw_cell(snake[0], HEAD_COLOR)
    # Desenha o corpo
    for segment in snake[1:]:
        draw_cell(segment, SNAKE_COLOR)

def draw_food():
    draw_cell(food, FOOD_COLOR)

def draw_score():
    text = font.render(f"SCORE: {score}", True, TEXT_COLOR)
    screen.blit(text, (8, 8))

def draw_game_over():
    game_over_font = pygame.font.SysFont("monospace", 32, bold=True)
    text = game_over_font.render("GAME OVER", True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    
    restart_font = pygame.font.SysFont("monospace", 18, bold=True)
    restart_text = restart_font.render("Press R to restart", True, TEXT_COLOR)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    screen.blit(restart_text, restart_rect)

# Movimento da cobra
def move_snake():
    global food, score, game_over
    
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    # Verifica colisão com as paredes
    if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
        game_over = True
        return

    # Verifica colisão com o próprio corpo
    if new_head in snake:
        game_over = True
        return

    # Move a cobra
    snake.insert(0, new_head)

    # Verifica se comeu a comida
    if new_head == food:
        score += 1
        food = place_food()
    else:
        snake.pop()

# Reinicia o jogo
def reset_game():
    global snake, direction, food, score, game_over
    snake = [
        (COLS // 2, ROWS // 2),
        (COLS // 2 - 1, ROWS // 2),
        (COLS // 2 - 2, ROWS // 2)
    ]
    direction = (1, 0)
    food = place_food()
    score = 0
    game_over = False

# Loop principal do jogo
running = True
while running:
    # Processamento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset_game()
            elif not game_over:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

    # Atualização do jogo
    if not game_over:
        move_snake()

    # Renderização
    screen.fill(BG_COLOR)
    
    # Desenha a grade
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, MARGIN_TOP), (x, HEIGHT))
    for y in range(MARGIN_TOP, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))
    
    # Desenha os elementos do jogo
    draw_snake()
    draw_food()
    draw_score()
    
    if game_over:
        draw_game_over()

    # Atualiza a tela
    pygame.display.flip()
    
    # Controla a velocidade do jogo
    clock.tick(10 + score * 0.5)

# Encerra o pygame
pygame.quit()
sys.exit()
