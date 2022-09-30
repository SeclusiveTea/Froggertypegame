#PyGame development 1
#Start the basic game set up
#set up the display

#PyGame development 2
#set up the game loop
#use game loop to render graphics

#PyGame development 3
#Draw objects to the screen
#Load images into objects 

#PyGame development 4
#Focus on making code object orientated
#Introduce classes and objects into our code

#PyGame development 5
#implement game classes
#implement generic game object class

#PyGame development 6
#implement game classes
#implement player character class and movement

#PyGame development 7
#Implement game classes
#Implement enemy character class and bounds checking

#PyGame development 8
#Implement collision detection
#detect collisions with treasure and enemies

#PyGame development 9
#Add true end game conditions
#Implement specific win and lose conditions

#PyGame development 10
#Make game more interesting
#add more enemies and make them move faster

#Gain access to the pygame library
import pygame

#Size of the screen
SCREEN_TITLE = "Frogger"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
#Colours according to RGB codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
#clock used to update game events and frames
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('comicsans', 75)

class Game:

    #typical rate of 60, equivalent to FPS
    TICK_RATE = 60
    

    #initializer for the game class to set up the width, height and title
    def __init__(self, imagePath, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        #Create a window of specified size in white to display the game
        self.gameScreen = pygame.display.set_mode((width, height))
        #set game window colour to white
        self.gameScreen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

        backgroundImage = pygame.image.load(imagePath)
        self.image = pygame.transform.scale(backgroundImage, (width, height))
    
    def runGameLoop(self, level):
        isGameOver = False
        didWin = False
        direction = 0

        playerCharacter = PlayerCharacter('player.png', 375, 700, 50, 50)
        enemyCharacter1 = EnemyCharacter ('enemy.png', 20, 400, 50, 50)
        enemyCharacter1.SPEED += level
        enemyCharacter2 = EnemyCharacter ('enemy.png', self.width - 50, 200, 50, 50)
        enemyCharacter2.SPEED += level
        enemyCharacter3 = EnemyCharacter ('enemy.png', 300, 600, 50, 50)
        enemyCharacter3.SPEED += level
        
        treasure = Treasure('treasure.png', 375, 20, 50, 50)

        #Main game loop, used to update all game play such as movement, checks and graphics
        #runs until isGameOver is equal to true
        while not isGameOver:

            #a loop to get all of the events occuring at a given time
            #events are most often mouse movement, mouse and button clicks or exit events
            for event in pygame.event.get():
                #if we have a quit type event (exit out) then exit out of the game loop
                if event.type == pygame.QUIT:
                    isGameOver = True
                #detect when key is pressed down
                elif event.type == pygame.KEYDOWN:
                    #move up if up key is pressed
                    if event.key == pygame.K_UP:
                        direction = 1
                    #move down if down key is pressed
                    elif event.key == pygame.K_DOWN:
                        direction = -1
                #detect when key is released
                elif event.type == pygame.KEYUP:
                    #stop movement when key is no longer pressed
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction = 0
            
            self.gameScreen.fill(WHITE_COLOR)
            self.gameScreen.blit(self.image, (0, 0))

            treasure.draw(self.gameScreen)
            
            #update the player position
            playerCharacter.move(direction, self.height)
            #draw the player at the new position
            playerCharacter.draw(self.gameScreen)

            enemyCharacter1.move(self.width)
            enemyCharacter1.draw(self.gameScreen)

            if level >= 4:
                enemyCharacter2.move(self.width)
                enemyCharacter2.draw(self.gameScreen)
            
            if level >= 6:
                enemyCharacter3.move(self.width)
                enemyCharacter3.draw(self.gameScreen)

            if playerCharacter.detectCollision(enemyCharacter1):
                isGameOver = True
                didWin = False
                text = font.render(f'You lost on level {level}', True, BLACK_COLOR)
                self.gameScreen.blit(text, (150, 350))
                pygame.display.update()
                clock.tick(2)
                break
            elif playerCharacter.detectCollision(enemyCharacter2):
                isGameOver = True
                didWin = False
                text = font.render(f'You lost on level {level}', True, BLACK_COLOR)
                self.gameScreen.blit(text, (150, 350))
                pygame.display.update()
                clock.tick(2)
                break
            elif playerCharacter.detectCollision(enemyCharacter3):
                isGameOver = True
                didWin = False
                text = font.render(f'You lost on level {level}', True, BLACK_COLOR)
                self.gameScreen.blit(text, (150, 350))
                pygame.display.update()
                clock.tick(2)
                break
            elif playerCharacter.detectCollision(treasure):
                isGameOver = True
                didWin = True
                text = font.render('Congratulations you win!', True, BLACK_COLOR)
                self.gameScreen.blit(text, (50, 350))
                pygame.display.update()
                clock.tick(2)
                break

            

            #update all game graphics
            pygame.display.update()
            #Tick the clock to update everything within the game.
            clock.tick(self.TICK_RATE)

        if didWin:
            self.runGameLoop(level + 1)
        else:
            return

class GameObject:

    def __init__(self, imagePath, x, y, width, height):
        #load the image from the file directory
        objectImage = pygame.image.load(imagePath)
        #scale the image up
        self.image = pygame.transform.scale(objectImage, (width, height))

        self.xPos = x
        self.yPos = y

        self.width = width
        self.height = height

    #draw the object by blitting it onto the background (game screen)
    def draw(self, background):
        background.blit(self.image, (self.xPos, self.yPos))

#Class to represent the character controlled by the player
class PlayerCharacter(GameObject):
    
    #How many tiles the character moves per second
    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    #Move function will move character up if direction is > 0 and down if direction < 0
    def move(self, direction, maxHeight):
        if direction > 0:
            self.yPos -= self.SPEED
        elif direction < 0:
            self.yPos += self.SPEED
        
        if self.yPos >= maxHeight - 50:
            self.yPos = maxHeight - 50
        elif self.yPos <= 20:
            self.yPos = 20
    
    def detectCollision(self, otherBody):
        if self.yPos > otherBody.yPos + otherBody.height:
            return False
        elif self.yPos + self.height < otherBody.yPos:
            return False

        if self.xPos > otherBody.xPos + otherBody.width:
            return False
        elif self.xPos + self.width < otherBody.xPos:
            return False
        
        return True


#Class to represent the enemy character
class EnemyCharacter(GameObject):
    
    #How many tiles the character moves per second
    SPEED = 5

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, maxWidth):
        if self.xPos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self. xPos >= maxWidth - 50:
            self.SPEED = -abs(self.SPEED)
        self.xPos += self.SPEED

class Treasure(GameObject):
    
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    
pygame.init()

newGame = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
newGame.runGameLoop(1)

#Quit pygame and the program
pygame.quit()
quit()





