import pygame
import pytmx
import pyscroll
from player import Player


class Game:

    def __init__(self):
        # fenêtre
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("pygame")

        # charge la carte tmx
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # generer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # liste des collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # definir le rectangle pour entrer dans la maison
        enter_house1 = tmx_data.get_object_by_name('enter_house1')
        self.enter_house1_rect = pygame.Rect(enter_house1.x, enter_house1.y, enter_house1.width, enter_house1.height)

        enter_house2 = tmx_data.get_object_by_name('enter_house2')
        self.enter_house2_rect = pygame.Rect(enter_house2.x, enter_house2.y, enter_house2.width, enter_house2.height)

        self.map = 'world'
        self.house = None

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def switch_house(self):
        # charge la carte tmx
        tmx_data = pytmx.util_pygame.load_pygame('house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # liste des collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # definir le rectangle pour sortir dans la maison
        exit_house = tmx_data.get_object_by_name('exit_house')
        self.exit_house_rect = pygame.Rect(exit_house.x, exit_house.y, exit_house.width, exit_house.height)

        # recuperer le point de spawn dans la maison
        spawn_house_point = tmx_data.get_object_by_name('spawn_house')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y

    def switch_world(self, enter_house_exit):
        # charge la carte tmx
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # liste des collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # definir le rectangle pour entrer dans la maison
        enter_house1 = tmx_data.get_object_by_name('enter_house1')
        self.enter_house1_rect = pygame.Rect(enter_house1.x, enter_house1.y, enter_house1.width, enter_house1.height)

        enter_house2 = tmx_data.get_object_by_name('enter_house2')
        self.enter_house2_rect = pygame.Rect(enter_house2.x, enter_house2.y, enter_house2.width, enter_house2.height)

        # recuperer le point de spawn devant la maison
        enter_house_point = tmx_data.get_object_by_name(enter_house_exit)
        self.player.position[0] = enter_house_point.x
        self.player.position[1] = enter_house_point.y

    def update(self):
        self.group.update()

        # verifier entrée dans la maison
        if self.map == 'world':
            if self.player.feet.colliderect(self.enter_house1_rect):
                self.switch_house()
                self.house = 1
                self.map = 'house'

            elif self.player.feet.colliderect(self.enter_house2_rect):
                self.switch_house()
                self.house = 2
                self.map = 'house'

        # verifier sortie de la maison
        if self.map == 'house':
            if self.player.feet.colliderect(self.exit_house_rect):
                self.switch_world('enter_house' + str(self.house) + '_exit')
                self.map = 'world'

        # collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):
        clock = pygame.time.Clock()

        running = True
        while running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()
