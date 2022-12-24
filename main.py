import os
import sys
import pygame

pygame.init()
pygame.key.set_repeat(200, 70)
FPS = 50
SIZE = WIDTH, HEIGHT = 650, 600
STEP = 50
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Перемещение героя')
clock = pygame.time.Clock()
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image

# Функция выхода из игры!
def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = [" Моя супер игра!",
                  "",
                  "",
                  "",
                  "          Правила игры",
                  "Если в правилах несколько строк",
                  "приходится выводить их построчно"]
    fon = pygame.transform.scale(load_image('fon.jpeg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    # выводим текст два раза со сдвигом в 1 пиксель для красоты
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color("black"))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord  # координаты у
        intro_rect.x = 11
        screen.blit(string_rendered, intro_rect)
        text_coord += intro_rect.height + 10
    # Ждем пока игрок нажмет кнопку для продолжения игры.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

start_screen()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return [line.ljust(max_width, '.') for line in level_map]

# проверка уровня
# print(load_level('level1.txt'))

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(pos_x * tile_width + 16, pos_y * tile_height + 5)

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
    return new_player, x, y

player, level_x, level_y = generate_level(load_level("level1.txt"))


# class Camera:
#     def __init__(self):
#         self.dx = 0
#         self.dy = 0
#     def apply(self, obj):
#         obj.rect.x += self.dx
#         obj.rect.y += self.dy
#     def update(self, target):
#         self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
#         self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)
#
#
#
# camera = Camera()

# Главный Игровой цикл
while True:
    WIDTH, HEIGHT = pygame.display.get_window_size()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            with open("data/level1.txt") as f:
                if event.key == pygame.K_LEFT:
                    if f.readlines()[player.rect.y // 50][(player.rect.x - 16) // 50 - 1] != "#" and player.rect.x > -50:
                        player.rect.x -= STEP
                if event.key == pygame.K_RIGHT:
                    if f.readlines()[player.rect.y // 50][(player.rect.x - 16) // 50 + 1] != "#" and player.rect.x < 600:
                        player.rect.x += STEP
                if event.key == pygame.K_UP:
                    if f.readlines()[player.rect.y // 50 - 1][(player.rect.x - 16) // 50] != "#" and player.rect.y > -50:
                        player.rect.y -= STEP
                if event.key == pygame.K_DOWN:
                    if f.readlines()[player.rect.y // 50 + 1][(player.rect.x - 16) // 50] != "#" and player.rect.y < 550:
                        player.rect.y += STEP
    # camera.update(player)
    # for sprite in all_sprites:
    #     camera.apply(sprite)
    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
