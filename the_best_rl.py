#!/usr/bin/python
#-*- encoding: utf-8 -*-

import libtcodpy as libtcod

# 실제 창 크기
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

LIMIT_FPS = 20 # 20 프레임이 최고

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
        playery -= 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        playery += 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        playerx -= 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        playerx += 1

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
npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', libtcod. yellow)

# 위 두 객체를 포함하는 리스트
objects = [npc, player]

while not libtcod.console_is_window_closed():
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_put_char(0, playerx, playery, '@', libtcod.BKGND_NONE)

    libtcod.console_flush()

    libtcod.console_put_char(0, playerx, playery, ' ', libtcod.BKGND_NONE)

    #핸들링 키들 그리고 원한다면 게임 종료하는 기능
    exit = handle_keys()
    if exit:
        break
