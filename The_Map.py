#!/usr/bin/python
#-*- encoding: utf-8 -*-

import libtcodpy as libtcod

# 실제 창 크기
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# 맵 크기
MAP_WIDTH = 80
MAP_HEIGHT = 45

LIMIT_FPS = 20 # 20 프레임이 최고

color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)

class Tile:
    # 맵의 타일과 값
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        # 기본적으로 타일이 막혀있으면 시야도 막는다
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

class Object:
    """
    그래픽 오브젝트 : 플레이어, 몬스터, 아이템, 계단 등등...
    해당 클레스는 항상 화면에 하나의 캐릭터를 표현한다.
    """
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        # 주어진 수치만큼 이동
        self.x += dx
        self.y += dy

    def draw(self):
        # 색깔을 지정하고 해당 객체가 위치한 곳에 캐릭터를 그린다
        #set the color and then draw the character that represents this object at its position
        libtcod.console_set_default_foreground(con, self.color)
        libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        # 해당 객체가 표현하고 있는 캐릭터를 지운다
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

def make_map():
    global map

    # 막히지 않은 타일들로 맵을 채운다
    map = [[ Tile(False) for y in range(MAP_HEIGHT) ] for x in range(MAP_WIDTH) ]

    # 맵을 테스트하기위해 두 기둥을 위치시킨다
    map[30][22].blocked = True
    map[30][22].block_sight = True
    map[30][22].blocked = True
    map[30][22].block_sight = True

def render_all():
    global color_light_wall
    global color_light_ground

    # 모든 타일들에 대해 지나가게되면 그 배경색이 결정되도록 한다.
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = map[x][y].block_sight
            if wall:
                libtcod.console_set_char_background(con, x, y, color_dard_wall, libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET)

    # 리스트의 모든 객체를 그려준다
    for object in objects:
        object.draw()

    # 루트 콘솔에 "con"의 내용물들을 블럭 전송(blit)한다
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def handle_keys():
    global playerx, playery
    #key = libtcod.console_check_for_keypress()  # 실시간
    key = libtcod.console_wait_for_keypress(True) # 턴제 방식
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # 알트+엔터 : 전체화면
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
        return True #게임 종료

    #이동키들
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0, -1)
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0, 1)
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0)
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1, 0)

#############################################
# 초기화 & 메인 루프
#############################################

libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

# 플레이어를 표현하는 객체를 생성한다
player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)

# NPC를 생성한다
npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', libtcod.yellow)

# 위 두 객체를 포함하는 리스트
objects = [npc, player]

while not libtcod.console_is_window_closed():

    # 리스트에 포함된 모든 객체를 그린다
    for object in objects:
        object.draw()

    # "con" 변수의 내용물들을 루트 콘솔에 블럭 전송(blit)하고 표현한다
    # blit : 따로 영역을 지정해서 부분부분 드로잉이 가능하게 만드는 함수
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()

    # 객체들이 이동하기 전에 이전 위치에 존재하던 모든 객체들을 지워준다
    for object in objects:
        object.clear()

    #핸들링 키들 그리고 원한다면 게임 종료하는 기능
    exit = handle_keys()
    if exit:
        break
