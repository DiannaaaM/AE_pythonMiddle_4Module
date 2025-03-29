import pygame


class Item:
    def __init__(self, x, y, health, happiness, image_name):
        # Set up basic fields
        self.x = x
        self.y = y
        self.health = health
        self.happiness = happiness
        # Load and store the image based on the filepath
        self.image = pygame.image.load(image_name)
        # Shift the image rect so that the x and y are at the center rather than top left
        rect = self.image.get_rect()
        self.image_rect = pygame.Rect(x - rect.width / 2, y - rect.height / 2, rect.width, rect.height)


class Game:
    def __init__(self):
        # Display variables
        self.width = 500
        self.height = 500
        self.background_colour = "white"
        self.buttons_bar_height = 100
        self.buttons_bar_colour = "orange"
        # Pygame specific variables
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Pet")
        self.clock_tick = 60
        self.clock = pygame.time.Clock()
        # Item variables
        self.image_names = ["apple.png", "icecream.png", "toy.png"]
        self.item_mode_index = 0
        self.item = None
        # Button variables
        self.apple_button = Item(self.width / 4, self.buttons_bar_height / 2, 0, 0, self.image_names[0])
        self.ice_cream_button = Item(self.width / 2, self.buttons_bar_height / 2, 0, 0, self.image_names[1])
        self.toy_button = Item(self.width * (3 / 4), self.buttons_bar_height / 2, 0, 0, self.image_names[2])

        # Select an item or place an item if appropriate area is clicked

    def handle_mouse_click(self):
        pos = pygame.mouse.get_pos()
        # Check for button press
        if self.apple_button.image_rect.collidepoint(pos):
            self.item_mode_index = 0
        elif self.ice_cream_button.image_rect.collidepoint(pos):
            self.item_mode_index = 1
        elif self.toy_button.image_rect.collidepoint(pos):
            self.item_mode_index = 2
        # Do nothing if user clicks button bar outside of buttons
        elif pos[1] < self.buttons_bar_height:
            return
        # Create an item at the mouse position
        else:
            self.create_item(pos)

        # Spawn an item at the position

    def create_item(self, pos):
        # Get current image name
        image_name = self.image_names[self.item_mode_index]
        # Create an item at the position
        if self.item_mode_index == 0:
            self.item = Item(pos[0], pos[1], 20, 0, image_name)
        elif self.item_mode_index == 1:
            self.item = Item(pos[0], pos[1], -10, 60, image_name)
        elif self.item_mode_index == 2:
            self.item = Item(pos[0], pos[1], 0, 40, image_name)
        # Start moving the pet
        self.set_speed()

    # Draw the screen, bar, buttons, item, pet
    def draw_everything(self):
        # Screen
        self.screen.fill(self.background_colour)
        # Item
        if self.item != None:
            self.screen.blit(self.item.image, self.item.image_rect)
        # Buttons bar
        pygame.draw.rect(self.screen, self.buttons_bar_colour, pygame.Rect(0, 0, self.width, self.buttons_bar_height))
        # Buttons
        self.screen.blit(self.apple_button.image, self.apple_button.image_rect)
        self.screen.blit(self.ice_cream_button.image, self.ice_cream_button.image_rect)
        self.screen.blit(self.toy_button.image, self.toy_button.image_rect)
        # Update
        pygame.display.update()

    # Run the game loop
    def run(self):
        while True:
            # Handle incoming events
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click()
            # Draw
            self.draw_everything()

            # Tick clock
            self.clock.tick(self.clock_tick)


# Initialize Pygame and start running game
pygame.init()
game = Game()
game.run()