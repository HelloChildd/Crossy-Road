import pygame
import os
import sys
import time
import math
import random

from review import *

WIDTH = 600
HEIGHT = 600

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))  # create screen
pygame.display.set_caption('CROSSY ROAD')  # set the caption

# Load images
PURPLE_CAR = pygame.image.load("purplecar.png")
PURPLE_CAR = pygame.transform.scale(PURPLE_CAR, (PURPLE_CAR.get_width() / 8, PURPLE_CAR.get_height() / 8))

RED_TRUCK = pygame.image.load("Red_Truck.png")
RED_TRUCK = pygame.transform.scale(RED_TRUCK, (RED_TRUCK.get_width() / 7, RED_TRUCK.get_height() / 7))

POLICE_CAR = pygame.image.load("policecar.png")
POLICE_CAR = pygame.transform.scale(POLICE_CAR, (POLICE_CAR.get_width() / 6, POLICE_CAR.get_height() / 6))

ROAD = pygame.image.load("road1.png")
ROAD = pygame.transform.rotate(ROAD, -14)

DUCK = pygame.image.load("duck1.png")
DUCK = pygame.transform.scale(DUCK, (DUCK.get_width() / 6, DUCK.get_height() / 6))

RACECAR = pygame.image.load("racecar.png")
RACECAR = pygame.transform.scale(RACECAR, (RACECAR.get_width() / 6, RACECAR.get_height() / 6))

BLUE_TRUCK = pygame.image.load("Blue_Truck_PNG.png")
BLUE_TRUCK = pygame.transform.scale(BLUE_TRUCK, (BLUE_TRUCK.get_width() / 6, BLUE_TRUCK.get_height() / 6))

GREEN_CAR = pygame.image.load("Green_Car.png")
GREEN_CAR = pygame.transform.scale(GREEN_CAR, (GREEN_CAR.get_width() / 6, GREEN_CAR.get_height() / 6))

CAM_ANGLE = -14  # degrees

IMAGES = [PURPLE_CAR, RED_TRUCK, POLICE_CAR, RACECAR, BLUE_TRUCK, GREEN_CAR]

pygame.font.init()
GAME_FONT = pygame.font.Font("8bitwonder.TTF", 40)
SMALL_FONT = pygame.font.Font("8bitwonder.TTF", 20)
SUPER_SMALL_FONT = pygame.font.Font("8bitwonder.TTF", 10)

class Duck:
    def __init__(self):
        self.img = DUCK
        self.x = 200
        self.y = 200
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self):
        SCREEN.blit(self.img, (self.x, self.y))

class Vehicle:
    def __init__(self, img):
        self.spawn_x = -150
        self.spawn_y = 50
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.speed = 3
        self.dx = math.cos(math.radians(CAM_ANGLE))
        self.dy = -1 * math.sin(math.radians(CAM_ANGLE))
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self):
        SCREEN.blit(self.img, (self.x, self.y))

    def drive(self):
        self.x += self.speed * self.dx
        self.y += self.speed * self.dy

        if self.x >= WIDTH:
            self.respawn_car()

    def respawn_car(self):
        self.x = self.spawn_x
        self.y = self.spawn_y

class Traffic:
    def __init__(self, y, vehicle_img, num_vehicles):
        self.y = y
        self.vehicle_img = vehicle_img
        self.num_vehicles = num_vehicles
        self.vehicles = []
        self.crossed = False
        self.create_vehicles()

    def draw(self):
        SCREEN.blit(ROAD, (-110, self.y - 130))
        for vehicle in self.vehicles:
            vehicle.draw()

    def create_vehicles(self):
        for i in range(self.num_vehicles):
            vehicle = Vehicle(self.vehicle_img)
            vehicle.spawn_y = self.y
            spacing = random.randint(200, 230)
            vehicle.x = vehicle.spawn_x - (spacing * vehicle.dx) * i
            vehicle.y = vehicle.spawn_y - (spacing * vehicle.dy) * i
            self.vehicles.append(vehicle)

    def move_down(self):
        self.y += 5
        for vehicle in self.vehicles:
            vehicle.y += 5
            vehicle.spawn_y += 5

    def drive(self):
        for vehicle in self.vehicles:
            vehicle.drive()
            vehicle.speed = 5

    def road_crossed(self):
        if self.y >= 190 and self.crossed == False:
            self.crossed = True
            return True
        else:
            return False

def get_collision(obj1, obj2):
    obj2_width = obj2.img.get_width()
    obj2_height = obj2.img.get_height()
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y))

def start_screen():
    SCREEN.fill((0, 0, 0))
    title = GAME_FONT.render("CROSSY ROAD", True, (255, 255, 0))
    prompt = SMALL_FONT.render("Press any key to start", True, (255, 255, 255))
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))
    SCREEN.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def main():
    clock = pygame.time.Clock()
    FPS = 60
    duck = Duck()
    traffic_objs = [
        Traffic(20, PURPLE_CAR, 3),
        Traffic(-120, PURPLE_CAR, 4),
        Traffic(-260, RED_TRUCK, 4),
        Traffic(-400, POLICE_CAR, 4)
    ]
    score = 0
    game_over_flag = False
    movement = False

    def redraw_window():
        SCREEN.fill((0, 255, 50))
        for traffic in traffic_objs:
            traffic.draw()
        duck.draw()

        score_label = GAME_FONT.render(str(score), True, (255, 255, 255))
        SCREEN.blit(score_label, (520, 20))

        ins_label1 = SUPER_SMALL_FONT.render("Welcome to Crossy Road", True, (60, 60, 60))
        ins_label2 = SUPER_SMALL_FONT.render("Press the up arrow to move forward", True, (60, 60, 60))
        ins_label3 = SUPER_SMALL_FONT.render("Avoid the cars and cross the roads!", True, (60, 60, 60))

        if not movement:
            SCREEN.blit(ins_label1, (10, 300))
            SCREEN.blit(ins_label2, (10, 320))
            SCREEN.blit(ins_label3, (10, 340))
        pygame.display.update()

    while True:
        keys = pygame.key.get_pressed()
        clock.tick(FPS)
        redraw_window()

        if game_over_flag == False and keys[pygame.K_UP]:
            movement = True
            for traffic in traffic_objs:
                traffic.move_down()
                if traffic.road_crossed():
                    score += 1

            if traffic_objs[0].y > 550:
                traffic_objs.pop(0)
            last_traffic = traffic_objs[-1]
            if last_traffic.y > 0:
                new_traffic = Traffic(last_traffic.y - 140, random.choice(IMAGES), 3)
                traffic_objs.append(new_traffic)

        if not game_over_flag:
            for traffic in traffic_objs:
                traffic.drive()

        for traffic in traffic_objs:
            for vehicle in traffic.vehicles:
                if get_collision(duck, vehicle):
                    game_over_flag = True
                    return score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def game_over(score):
    clock = pygame.time.Clock()
    FPS = 60

    def redraw_window():
        SCREEN.fill((0, 0, 0))
        game_over_label = GAME_FONT.render("GAME OVER", True, (255, 0, 0))
        score_label = GAME_FONT.render("SCORE WAS " + str(score), True, (255, 0, 0))
        restart_label = SMALL_FONT.render("Press any key to restart", True, (255, 255, 255))
        game_over_x = WIDTH / 2 - game_over_label.get_width() / 2
        score_x = WIDTH / 2 - score_label.get_width() / 2
        restart_x = WIDTH / 2 - restart_label.get_width() / 2
        SCREEN.blit(game_over_label, (game_over_x, 200))
        SCREEN.blit(score_label, (score_x, 250))
        SCREEN.blit(restart_label, (restart_x, 300))
        pygame.display.update()

    while True:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

# ⬇️ Start Screen + Game Loop
start_screen()

while True:
    score = main()
    game_over(score)
