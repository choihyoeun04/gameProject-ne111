import pygame, sys, random
 


class GameState():
    def __init__(self):
        self.state = 'intro'

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = 'main_game'  

        #drawing
        screen.blit(background,(0,0))
        screen.blit(ready_text,(screen_width/2 - 115, screen_height/2 - 33))
        player_group.draw(screen)
        player_group.update()
 
        pygame.display.flip()

    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                sys.exit()

        #Drawing
        screen.blit(background,(0,0))
        player_group.draw(screen)
        player_group.update()

    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()

        
#General Setup

pygame.init()
clock = pygame.time.Clock()
game_state = GameState()



        

#Game Screen
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Hi")
background = pygame.image.load("background.jpg")
ready_text = pygame.image.load("ready.jpg")

player_group = pygame.sprite.Group()

while True:
    game_state.intro()