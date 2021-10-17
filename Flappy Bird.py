#My Second Python game: Flappy Bird
#Kai Wang, August 14, 2019
import random
import pygame
import sys

class FlappyBird():

    def __init__(self):
        
        #environment parameters
        self.screenWidth = 1200
        self.screenHeight = 700
        pygame.init()
        self.gameWindow = pygame.display.set_mode( (self.screenWidth, self.screenHeight) ) 
        pygame.display.set_caption("Flappy Bird by Kai Wang")

        #game parameters
        self.gravityValue = 1
        self.gameSpeed = 10
        self.score = 0
        self.death = False
        self.clock = pygame.time.Clock()
        self.bird = Bird()
        self.pipes = []
        self.frame = 0
        
        #begin running the game
        self.runGame()

    def gravity(self):
        self.bird.ySpeed += self.gravityValue

    def generatePipe(self, minHeight, maxHeight):
        height = random.randint(minHeight, maxHeight)
        top = random.randint(0,self.screenHeight - height)
        
        self.pipes.append(Pipe(self.screenWidth + 10, top, 80, height, self.screenHeight))
    
    def drawPipes(self):
        for pipe in self.pipes:
            pipe.move(self.gameSpeed)
            self.gameWindow.blit(pipe.pipe1Image, pipe.pipe1Rect)
            self.gameWindow.blit(pipe.pipe2Image, pipe.pipe2Rect)

        if self.pipes[0].left + self.pipes[0].width < 0:
            self.pipes.pop(0)

    def checkCollision(self):
        if self.bird.birdRect.colliderect(self.pipes[0].pipe1Rect) or self.bird.birdRect.colliderect(self.pipes[0].pipe2Rect):
            self.gameSpeed = 0
            
    def runGame(self):
        self.generatePipe(100,400)
        while True:
            for event in pygame.event.get():
                #checks for the quit event
                if event.type == pygame.QUIT:
                    #quit the program
                    pygame.quit()
                    sys.exit()

            self.frame += 1
        
            self.bird.flap()
            self.gravity()
            self.bird.updatePosition()

            if(self.frame % 100 * self.gameSpeed == 0):
                self.generatePipe(100,300)

            self.gameWindow.fill((100,150,200))
            self.gameWindow.blit(self.bird.birdImage, self.bird.birdRect)

            self.drawPipes()
            self.checkCollision()
            
            pygame.display.update()
            
            self.clock.tick(30)

class Bird():
    def __init__(self):
        self.size = 80
        self.xPos = 40
        self.yPos = 300
        self.ySpeed = 0
        self.xSpeed = 0
        self.thrust = 2.5
        
        self.birdImage = pygame.image.load("goldfishSprite.png")
        self.birdImage = pygame.transform.scale(self.birdImage, (self.size+60, self.size))
        self.birdRect = self.birdImage.get_rect()
        self.birdRect = self.birdRect.move((self.xPos, self.yPos))

    def flap(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.ySpeed -= self.thrust
        elif pressed[pygame.K_DOWN]:
            self.ySpeed += self.thrust

        if pressed[pygame.K_LEFT]:
            self.xSpeed -= self.thrust
        elif pressed[pygame.K_RIGHT]:
            self.xSpeed += self.thrust

    def updatePosition(self):
        self.yPos += self.ySpeed
        self.xPos += self.xSpeed
        
        if(self.yPos <= 0):
            self.yPos = 0
            self.ySpeed = 0
        elif(self.yPos + self.size >= 700):
            self.yPos = 700 - self.size
            self.ySpeed = 0

        if(self.xPos <= 0):
            self.xPos = 0
            self.xSpeed = 0
            self.birdRect.left = self.xPos
        elif(self.xPos + self.size >= 1200):
            self.xPos = 1200 - self.size
            self.xSpeed = 0
            self.birdRect.left = self.xPos
            
        self.birdRect = self.birdRect.move(self.xSpeed,self.ySpeed)
                                    
class Pipe():
    def __init__(self, left, top, width, height, screenHeight):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.pipe1Image = pygame.image.load("pipe1.png")
        self.pipe1Image = pygame.transform.scale(self.pipe1Image, (self.width, self.top))
        self.pipe1Image = pygame.transform.flip(self.pipe1Image, False, True)
        self.pipe1Rect = pygame.Rect(self.left, 0, self.width, self.height)

        self.pipe2Image = pygame.image.load("pipe1.png")
        self.pipe2Image = pygame.transform.scale(self.pipe2Image, (self.width, screenHeight - self.top - self.height))
        self.pipe2Rect = pygame.Rect(self.left, self.top + self.height, self.width, screenHeight - self.top - self.height)

    def move(self, gameSpeed):
        self.left -= gameSpeed
        self.pipe1Rect.left = self.left
        self.pipe2Rect.left = self.left
        
theGame = FlappyBird()
