import pygame

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


    # Draw the screen, bar, buttons, item, pet
    def draw_everything(self):
        # Screen
        self.screen.fill(self.background_colour)
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