import pygame
import random

# Константы
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
MINES_COUNT = 10

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Сапер")


# Класс для клетки
class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_opened = False
        self.is_flagged = False
        self.neighbor_mines = 0


def start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)  # Шрифт текста
    text = font.render("Сапер", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    screen.blit(text, text_rect)

    # Шрифт для кнопок
    button_font = pygame.font.Font(None, 30)  # Размер шрифта для кнопок

    # Кнопка старта игры
    start_button = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 20, 160, 40)
    pygame.draw.rect(screen, WHITE, start_button)
    start_text = button_font.render("Играть", True, BLACK)
    start_text_rect = start_text.get_rect(center=start_button.center)  # Центрируем текст
    screen.blit(start_text, start_text_rect)

    # Кнопка выхода из игры
    exit_button = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 70, 160, 40)
    pygame.draw.rect(screen, WHITE, exit_button)
    exit_text = button_font.render("Выход", True, BLACK)
    exit_text_rect = exit_text.get_rect(center=exit_button.center)  # Центрируем текст
    screen.blit(exit_text, exit_text_rect)
    return start_button, exit_button


# Создание игрового поля
def create_board(mined_cells=[]):
    board = [[Cell() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    mines = 0

    # Установка мин, исключая заранее определенные клетки
    while mines < MINES_COUNT:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if not board[y][x].is_mine and (x, y) not in mined_cells:
            board[y][x].is_mine = True
            mines += 1

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[y][x].is_mine:
                continue
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if 0 <= x + dx < GRID_SIZE and 0 <= y + dy < GRID_SIZE:
                        if board[y + dy][x + dx].is_mine:
                            board[y][x].neighbor_mines += 1

    return board


# Открытие клеток вокруг
def open_area(board, x, y):
    if board[y][x].is_opened or board[y][x].is_flagged:
        return
    board[y][x].is_opened = True
    if board[y][x].neighbor_mines == 0 and not board[y][x].is_mine:
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if 0 <= x + dx < GRID_SIZE and 0 <= y + dy < GRID_SIZE:
                    open_area(board, x + dx, y + dy)


# Отрисовка игрового поля
def draw_board(board):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cell = board[y][x]
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell.is_opened:
                pygame.draw.rect(screen, WHITE, rect)
                if cell.is_mine:
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
                elif cell.neighbor_mines > 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(cell.neighbor_mines), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)
                if cell.is_flagged:
                    pygame.draw.line(screen, BLACK, rect.topleft, rect.bottomright, 3)
                    pygame.draw.line(screen, BLACK, rect.topright, rect.bottomleft, 3)

            # Рисуем кант
            pygame.draw.rect(screen, BLACK, rect, 1)

    # Рисуем сетку
    for x in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
    for y in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))


# Отображение окон окончания игры
def display_end_screen(victory):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Победа!" if victory else "Проигрыш!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    screen.blit(text, text_rect)

    # Шрифт для кнопок
    button_font = pygame.font.Font(None, 30)  # Размер шрифта для кнопок

    # Кнопка "Начать заново"
    restart_button = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 20, 160, 40)
    pygame.draw.rect(screen, WHITE, restart_button)
    restart_text = button_font.render("Начать заново", True, BLACK)
    restart_text_rect = restart_text.get_rect(center=restart_button.center)  # Центрируем текст
    screen.blit(restart_text, restart_text_rect)

    # Кнопка "Выход"
    exit_button = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 70, 160, 40)
    pygame.draw.rect(screen, WHITE, exit_button)
    exit_text = button_font.render("Выход", True, BLACK)
    exit_text_rect = exit_text.get_rect(center=exit_button.center)  # Центрируем текст
    screen.blit(exit_text, exit_text_rect)
    return restart_button, exit_button


# Основной игровой цикл
def main():
    running = True
    board = None
    game_over = False
    victory = False
    first_click = True
    exit_button_active = True

    while running:
        start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                start_button, exit_button = start_screen()

                if start_button.collidepoint((mouse_x, mouse_y)):
                    exit_button_active = False  # Деактивируем кнопку выхода

                if exit_button_active and exit_button.collidepoint((mouse_x, mouse_y)):
                    running = False  # Выход из игры

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                x //= CELL_SIZE
                y //= CELL_SIZE

                if event.button == 1:  # Левый клик
                    if board:
                        if board[y][x].is_flagged:  # Проверка на флаг
                            continue
                    if first_click:
                        mined_cells = [(x, y)]
                        board = create_board(mined_cells)  # Создание доски с минами
                        first_click = False
                    open_area(board, x, y)

                    if board[y][x].is_mine:  # Игра окончена
                        game_over = True
                    elif all(cell.is_opened or cell.is_mine for row in board for cell in row):
                        victory = True
                        game_over = True
                elif event.button == 3:  # Правый клик
                    if board:  # Проверяем, что доска создана
                        board[y][x].is_flagged = not board[y][x].is_flagged  # Меняем состояние флага

            elif game_over and event.type == pygame.MOUSEBUTTONDOWN:  # Создание кнопок
                mouse_x, mouse_y = event.pos
                restart_button, exit_button = display_end_screen(victory)

                # Проверка нажатия кнопок на окончательном экране
                if restart_button.collidepoint((mouse_x, mouse_y)):
                    main()  # Рекурсивно запускаем новую игру
                elif exit_button.collidepoint((mouse_x, mouse_y)):
                    running = False  # Выход из игры

            # Отрисовка доски
        if board:
            draw_board(board)
            if game_over:
                display_end_screen(victory)

        pygame.display.flip()


# Запуск игры при старте
if __name__ == "__main__":
    main()
    pygame.quit()
