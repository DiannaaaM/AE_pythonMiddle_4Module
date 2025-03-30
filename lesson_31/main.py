import pygame


# Определяет класс питомеца
class Pet:
    """
    Класс, описывающий питомеца.
    """
    def __init__(self, x, y, health, max_health, happiness, max_happiness):
        """
        Инициализирует объект питомеца.
        """
        self.x = x
        self.y = y
        # Здоровье питомеца - это радиус окружности
        self.health = health
        self.max_health = max_health
        # Счастье питомеца - это зеленый цвет цвета
        self.happiness = happiness
        self.max_happiness = max_happiness
        self.colour = pygame.Color(0, happiness, 0)

    # Возвращает координаты центра окружности и прямоугольник, ограничивающий окружность
    def get_pos(self):
        """
        Возвращает координаты центра окружности и прямоугольник, ограничивающий окружность.
        """
        return pygame.Vector2(self.x, self.y)

    def get_rect(self):
        return pygame.Rect(self.x - self.health, self.y - self.health, self.health * 2, self.health * 2)
    # Изменяет координаты питомеца
    def move(self, x_amount, y_amount):
        """
        Изменяет координаты питомеца.
        """
        self.x += x_amount
        self.y += y_amount

    # Обновляет здоровье и счастье питомеца, потребляя предмет
    def consume_item(self, item):
        """
        Обновляет здоровье и счастье питомеца, потребляя предмет.
        """
        self.update_health(item.health)
        self.update_happiness(item.happiness)

    # Обновляет здоровье и счастье питомеца
    def update_health(self, d_h):
        """
        Обновляет здоровье и счастье питомеца.
        """
        self.health += d_h
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health < 0:
            self.health = 0

    # Обновляет счастье питомеца
    def update_happiness(self, d_h):
        """
        Обновляет счастье питомеца.
        """
        self.happiness += d_h
        if self.happiness > self.max_happiness:
            self.happiness = self.max_happiness
        elif self.happiness < 0:
            self.happiness = 0
        self.colour = pygame.Color(0, self.happiness, 0)

    # Проверяет, жив ли питомец
    def check_if_dead(self):
        """
        Проверяет, жив ли питомец.
        """
        return self.health <= 0 or self.happiness <= 0


# Определяет класс предмета
class Item:
    """
    Класс, описывающий предмет.
    """
    def __init__(self, x, y, health, happiness, image_name):
        """
        Инициализирует объект предмета.
        """
        self.x = x
        self.y = y
        self.health = health
        self.happiness = happiness
        # Загружает и сохраняет изображение по имени файла
        self.image = pygame.image.load(image_name)
        # Сдвигает изображение так, чтобы координаты x и y были в центре, а не в верхнем левом углу
        rect = self.image.get_rect()
        self.image_rect = pygame.Rect(x - rect.width / 2, y - rect.height / 2, rect.width, rect.height)


# Определяет класс игры
class Game:
    """
    Класс, описывающий игру.
    """
    def __init__(self):
        """
        Инициализирует объект игры.
        """
        # Размеры окна
        self.width = 500
        self.height = 500
        # Цвет фона
        self.background_colour = "white"
        # Высота полосы кнопок
        self.buttons_bar_height = 100
        # Цвет полосы кнопок
        self.buttons_bar_colour = "orange"
        # Переменные, связанные с Pygame
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Pet")
        self.clock_tick = 60
        self.clock = pygame.time.Clock()
        # Переменные, связанные с предметами
        self.image_names = ["apple.png", "icecream.png", "toy.png"]
        self.item_mode_index = 0
        self.item = None
        # Переменные, связанные с питомецем
        self.apple_button = Item(self.width / 4, self.buttons_bar_height / 2, 0, 0, self.image_names[0])
        self.ice_cream_button = Item(self.width / 2, self.buttons_bar_height / 2, 0, 0, self.image_names[1])
        self.toy_button = Item(self.width * (3 / 4), self.buttons_bar_height / 2, 0, 0, self.image_names[2])
        # Pet variables
        self.pet = Pet(self.width / 2, self.height / 2, 50, 100, 180, 255)
        self.speed = 2
        self.d_x = 0
        self.d_y = 0
        self.decay_rate = -1
        self.current_tick = 0
        self.size_update_rate = self.clock_tick / 3
        self.colour_update_rate = self.clock_tick / 10

    # Выбирает предмет или создает предмет, если подходящая область нажата
    def handle_mouse_click(self):
        """
        Выбирает предмет или создает предмет, если подходящая область нажата.
        """
        pos = pygame.mouse.get_pos()
        # Проверяет, был ли нажат кнопка в области кнопок
        if self.apple_button.image_rect.collidepoint(pos):
            self.item_mode_index = 0
        elif self.ice_cream_button.image_rect.collidepoint(pos):
            self.item_mode_index = 1
        elif self.toy_button.image_rect.collidepoint(pos):
            self.item_mode_index = 2
        # Не делает ничего, если пользователь нажал кнопку вне области кнопок
        elif pos[1] < self.buttons_bar_height:
            return
        # Создает предмет в выбранной позиции
        else:
            self.create_item(pos)

    # Создает предмет в выбранной позиции
    def create_item(self, pos):
        """
        Создает предмет в выбранной позиции.
        """
        # Загружает имя нового предмета
        image_name = self.image_names[self.item_mode_index]
        # Создает предмет в выбранной позиции
        if self.item_mode_index == 0:
            self.item = Item(pos[0], pos[1], 20, 0, image_name)
        elif self.item_mode_index == 1:
            self.item = Item(pos[0], pos[1], -10, 60, image_name)
        elif self.item_mode_index == 2:
            self.item = Item(pos[0], pos[1], 0, 40, image_name)
        # Начинает двигать питомец
        self.set_speed()

    # Устанавливает скорость и направление движения питомеца
    def set_speed(self):
        """
        Устанавливает скорость и направление движения питомеца.
        """
        # Вычисляет разницу в x и y координатах питомеца и предмета
        d_x = abs(self.pet.x - self.item.x)
        d_y = abs(self.pet.y - self.item.y)
        # Проверяет, больше ли разница в x координатах, чем в y координатах
        if d_x >= d_y:
            self.d_x = self.speed
            # Снижает скорость y движения в соответствии с разницей в x координатах
            self.d_y = self.speed * (d_y / d_x)
        else:
            # Снижает скорость x движения в соответствии с разницей в y координатах
            self.d_x = self.speed * (d_x / d_y)
            self.d_y = self.speed
        # Если питомец находится левее предмета, устанавливает скорость x в отрицательную сторону
        if self.pet.x > self.item.x:
            self.d_x = -self.d_x
        # Если питомец находится выше предмета, устанавливает скорость y в отрицательную сторону
        if self.pet.y > self.item.y:
            self.d_y = -self.d_y

    # Проверяет столкновение питомеца и предмета
    def handle_item_collision(self):
        """
        Проверяет столкновение питомеца и предмета.
        """
        # Если предмет существует и область предмета пересекается с областью питомеца, произошло столкновение
        if self.item != None and self.item.image_rect.colliderect(self.pet.get_rect()):
            # Убирает предмет и делает питомеца неподвижным
            self.pet.consume_item(self.item)
            self.item = None
            self.d_x = 0
            self.d_y = 0

    # Обновляет координаты, здоровье и счастье питомеца
    def update_pet(self):
        """
        Обновляет координаты, здоровье и счастье питомеца.
        """
        # Обновляет координаты питомеца
        self.pet.move(self.d_x, self.d_y)
        # Обновляет здоровье и счастье питомеца
        self.current_tick += 1
        # Уменьшает здоровье питомеца на 3 раза в секунду
        if self.current_tick % self.size_update_rate == 0:
            self.pet.update_health(self.decay_rate)
        # Уменьшает счастье питомеца на 10 раз в секунду
        if self.current_tick % self.colour_update_rate == 0:
            self.pet.update_happiness(self.decay_rate)
        # Сбрасывает текущий таймер, чтобы он не стал слишком большим
        if self.current_tick == 60:
            self.current_tick = 0

    # Рисует окно, полосу кнопок, кнопки, предмет, питомец
    def draw_everything(self):
        """
        Рисует окно, полосу кнопок, кнопки, предмет, питомец.
        """
        # Очищает окно
        self.screen.fill(self.background_colour)
        # Рисует предмет, если он существует
        if self.item != None:
            self.screen.blit(self.item.image, self.item.image_rect)
        # Рисует питомец
        pygame.draw.circle(self.screen, self.pet.colour, self.pet.get_pos(), self.pet.health)
        # Рисует полосу кнопок
        pygame.draw.rect(self.screen, self.buttons_bar_colour, pygame.Rect(0, 0, self.width, self.buttons_bar_height))
        # Рисует кнопки
        self.screen.blit(self.apple_button.image, self.apple_button.image_rect)
        self.screen.blit(self.ice_cream_button.image, self.ice_cream_button.image_rect)
        self.screen.blit(self.toy_button.image, self.toy_button.image_rect)
        # Обновляет окно
        pygame.display.update()

    # Запускает игру
    def run(self):
        """
        Запускает игру.
        """
        while True:
            # Обрабатывает входящие события
            for event in pygame.event.get():
                # Если произошло закрытие окна, завершает работу программы
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click()
            # Проверяет столкновение питомеца и предмета
            self.handle_item_collision()
            # Проверяет, жив ли питомец и завершает работу программы, если он мерт
            if self.pet.check_if_dead():
                pygame.quit()
                return
            # Обновляет состояние питомеца
            self.update_pet()

            # Рисует все элементы на экране
            self.draw_everything()

            # Обновляет кадр
            self.clock.tick(self.clock_tick)


# Initialize Pygame and start running game
pygame.init()
game = Game()
game.run()