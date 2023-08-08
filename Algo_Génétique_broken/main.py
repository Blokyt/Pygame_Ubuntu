gitimport pygame
from random import randint

resolution = (1000,600)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("algo génétique")

size = 10
sizelevel = 5*size
speedx = 5
speedy = 5
moves = 100
count = 0

class Particule():

    def __init__(self):
        self.rect = pygame.Rect(start_pos[0]+size,start_pos[1]+size, size, size)
        self.color = (randint(0,255),randint(0,255),randint(0,255))
        self.moves = [(randint(-speedx, speedx),randint(-speedy, speedy)) for i in range(moves)]
        self.score = 0

    def collide(self,other):
        return self.rect.colliderect(other)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self):
        self.rect.x += self.moves[count][0]
        self.rect.y += self.moves[count][1]

def genParticules(n):
    for i in range(n):
        particules.append(Particule())

def moveParticules():
    for element in particules:
        element.move()

def draw():
    for tile in level.tiles:
        pygame.draw.rect(screen, (255,0,0), tile)
    pygame.draw.rect(screen, (0, 255, 0), level.start_tile)
    pygame.draw.rect(screen, (0, 255, 0), level.end_tile)

    for element in particules:
        element.draw()

def check_collide_reward():
    for element in particules:
        for tile in level.tiles:
            if element.collide(tile):
                element.score += 1
        if element.collide(level.end_tile):
            element.score += 5

class Level():

    def __init__(self, fichier):
        self.fichier = fichier
        self.tiles = []
        self.start_tile = None
        self.end_tile = None
        self.start_pos = (0,0)
        self.end_pos = (0,0)

    def generate(self):
        fichier_texte = open(self.fichier, 'r')
        contenu = fichier_texte.read()
        j = 0
        k = 0
        for element in contenu:
            if element == "\n":
                k += 1
                j = 0
            elif element == "#":
                self.tiles.append(pygame.Rect(sizelevel*j,sizelevel*k, sizelevel, sizelevel))
            elif element == "*":
                self.start_tile = pygame.Rect(sizelevel*j,sizelevel*k, sizelevel, sizelevel)
                self.start_pos = (sizelevel*j,sizelevel*k)
            elif element == "+":
                self.end_tile = pygame.Rect(sizelevel*j,sizelevel*k, sizelevel, sizelevel)
                self.end_pos = (sizelevel * j, sizelevel * k)
            j += 1
        fichier_texte.close()

level = Level("level.txt")
level.generate()
start_pos = level.start_pos

particules = []
genParticules(1000)

mutation_rate = 20 #1 chance sur mutation rate

def newGen(best_particule):
    genParticules(1000)
    for element in particules:
        for i in range(moves):
            element.moves[i] = best_particule.moves[i]
            if randint(1, mutation_rate) == 1:
                element.moves[i] = randint(-speedx, speedx), randint(-speedy, speedy)



def find_best_particule():
    i = 0
    max1 = 0
    part1 = particules[0]
    while i < len(particules):
        if particules[i].score >= max1:
            max2 = max1
            part2 = part1
            max1 = particules[i].score
            part1 = particules[i]
        i += 1
    return part1

generation = 1
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            best_particule = find_best_particule()
            print("generation", generation)
            print(best_particule.score)
            generation += 1

            for element in particules:
                element.rect = None
            particules = []
            newGen(best_particule)


    screen.fill((0,0,0))

    draw()
    moveParticules()
    check_collide_reward()
    if count == moves-1:
        count = 0
    else:
        count += 1


    pygame.display.update()

pygame.quit()




