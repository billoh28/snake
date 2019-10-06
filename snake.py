import pygame
import random
global screen
global screen_size
global background_colour
global fruit
global score

# Snake head class and snake movement
class Snake:
    def __init__(self, size=10, colour=(110, 235, 52)):
        self.size = size
        self.length = size
        self.snake = None
        self.pos = [0, 0]
        self.colour = colour
        self.oldpos = [0, 0]
        self.child = None
        self.fc = 0
        self.endCond = False

    def starter(self):
        self.snake = pygame.draw.rect(screen, self.colour, pygame.Rect(self.pos[0], self.pos[1], self.length, self.size)) # x, y, width_x, height_y

    def move(self):
        self.oldpos = self.pos[:]  # Remember last move
        pygame.draw.rect(screen, background_colour, pygame.Rect(self.pos[0], self.pos[1], self.length, self.size)) # x, y, width_x, height_y

        key_dict = pygame.key.get_pressed()
        if key_dict[pygame.K_DOWN] == 1: # If down position pressed
            self.pos[1] = (self.pos[1] + 10) % screen_size # Stop snake going off screen

        elif key_dict[pygame.K_UP] == 1: # If up position pressed
            self.pos[1] = (self.pos[1] - 10) % screen_size

        elif key_dict[pygame.K_LEFT] == 1: # If left position pressed
            self.pos[0] = (self.pos[0] - 10) % screen_size

        elif key_dict[pygame.K_RIGHT] == 1: # If down position pressed
            self.pos[0] = (self.pos[0] + 10) % screen_size
        
        if fruit == self.pos: # If snake gets a fruit
            self.fc -= 1
            self.spawn_child()

        # Move head
        self.starter()

        # Move body
        if self.child != None:
            self.move_child()

        return self.endCond
        

    def spawn_child(self):
        if self.child == None:  # If no child already the spawn one
            self.child = SnakeChild(self, self, self.oldpos[:])   # SnakeChild(root, parent, child_position)

        else:
            self.child.spawn_child()

    def move_child(self):
        self.child.moveBody()   # return result for collision test

    def end(self): # End game condition
        self.endCond = True

# Snake body
class SnakeChild:
    def __init__(self, root, parent, pos):
        self.root = root     # Instance of the Snake class
        self.parent = parent # Instance of SnakeChild class unless pointing to root
        self.size = 10
        self.colour = (110, 235, 52)
        self.child = None
        self.pos = pos
        self.oldpos = None
        self.starter()

    def starter(self):
        self.snake = pygame.draw.rect(screen, self.colour, pygame.Rect(self.pos[0], self.pos[1], self.size, self.size))

    def moveBody(self):
        self.oldpos = self.pos[:] # Remember old position
        # Remove old body position
        pygame.draw.rect(screen, background_colour, pygame.Rect(self.pos[0], self.pos[1], self.size, self.size))
        # Draw new body
        self.pos = self.parent.oldpos[:]
        pygame.draw.rect(screen, self.colour, pygame.Rect(self.pos[0], self.pos[1], self.size, self.size))

        if self.child != None:
            self.child.moveBody()  # Move body piece behind current one

        if self.check_collision():
            # return back to Snake class and then to main() function so to stop the game
            self.root.end()


    def spawn_child(self):
        if self.child == None:
            self.child = SnakeChild(self.root, self, self.oldpos[:])

        else:
            self.child.spawn_child()

    # Check for collision of the body and the head
    def check_collision(self):
        return self.pos[:] == self.root.pos[:]  # Collision has occurred: return to moveBody
 
# Fruit
class Fruit:
    def __init__(self, size=10):
        self.size = size
        self.x = None
        self.y = None
        self.fruit = None

    def set_fruit(self):
        rand1 = random.randint(0, 400)  # Random position of fruit on screen
        rand2 = random.randint(0, 400)
        self.x = rand1 - (rand1%self.size)  # So fruit position will always be a multiple of ten to stop partial overlap
        self.y = rand2 - (rand2%self.size)
        self.fruit = pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x, self.y, 10, 10))
        return [self.x, self.y] # return fruit position


# Event Loop, Fruit and Snake handling
def main():
    global fruit
    global score
    done = False # event loop end condition

    s = Snake()
    s.starter()
    fruit_counter = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if trying to close window
                done = True # End condition
        
            elif fruit_counter == 0: # If no fruit then spawn fruit
                f = Fruit()
                fruit = f.set_fruit()
                fruit_counter += 1
                s.fc += 1
                score += 1
            
            elif event.type == pygame.KEYDOWN:
                # Code for wasd movement
                done = s.move()   # Collision check
                fruit_counter = s.fc
            
            # print(fruit_counter, s.fruit_counter)
        pygame.display.flip() # required in order for any updates that you make to the game screen to become visible
    print("Your score was: {:}".format(score))

if __name__ == '__main__':
    score = 0
    screen_size = 400
    background_colour = [0,0,0]
    pygame.init() # initializes all the modules required for PyGame
    screen = pygame.display.set_mode((screen_size, screen_size + 30)) # Display screen size setting, width : height
    screen.fill(background_colour)  # Set background colour
    scoreboard = pygame.draw.rect(screen, (255,255,255), pygame.Rect(0, screen_size, 400, 30))
    main()