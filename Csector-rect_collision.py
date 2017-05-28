import pygame as pg
import os
import sys
vec = pg.math.Vector2
os.environ["SDL_VIDEO_CENTERED"] = "1"

width = 1000
height = 800
thickness = 2

pg.init()
screen = pg.display.set_mode((width, height))
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
rect = pg.Rect(0,0,64,64)
radius = 200
center = (width/2, height/2)
vec_center = vec(center)
clock = pg.time.Clock()

def collision(rect, center, line1, line2, radius):
    test1 = False
    test2 = False
    if not ((rect.center[0]-center[0])**2 + (rect.center[1]-center[1])**2) <= radius**2:
        point = flat_intersection(rect, center, 0)
        test1 = in_sector(center, line1, line2, radius, point)
    test2 = in_sector(center, line1, line2, radius, vec(rect.center))
    test3 = (line1, line2)
    for line in test3:
        coll = flat_intersection(rect, center, line)
        if coll:
            test3 = True
    if test3 != True:
        test3 = False
    if test1 or test2 or test3:
        return True
    else:
        return False
        
def flat_intersection(rect, center, line1):
    if not line1:
        line1 = vec(rect.center)
    veccenter = line1 - center
    a = rect.top
    b = rect.bottom
    c = rect.left
    d = rect.right
    x = 0
    y = 0
    t = 0
    hor = (a,b)
    ver = (c,d)
    for line in hor:
        if veccenter.y:
            t = (line-center.y)/veccenter.y
            x = center.x + t*veccenter.x
        else:
            if line == a:
                a = False
            else:
                b = False
        if line and 0 <= t <= 1 and rect.left <= x <= rect.right:
            if line == a:
                a = vec(x, line)
            else:
                b = vec(x, line)
        else:
            if line == a:
                a = False
            else:
                b = False
    for line in ver:
        if veccenter.x:
            t = (line-center.x)/veccenter.x
            y = center.y + t*veccenter.y
        else:
            if line == c:
                c = False
            else:
                d = False
        if line and 0 <= t <= 1 and rect.top <= y <= rect.bottom:
            if line == c:
                c = vec(line, y)
            else:
                d = vec(line, y)
        else:
            if line == c:
                c = False
            else:
                d = False
    z = (a,b,c,d)
    try:
        z = [i for i in z if i is not False][0]
    except IndexError:
        z = False
    return z

def intersection(p1, p2, center1, line1, center2, line2):
    pvec = p2 - p1
    l1vec = line1 - center
    p_l1_u = (pvec.x*(center1.y-p1.y) + pvec.y*(p1.x-center1.x)) \
           /(l1vec.x*pvec.y - l1vec.y*pvec.x)
    p_l1_t = (l1vec.x*(p1.y-center1.y) + l1vec.y*(center1.x-p1.x)) \
           /(l1vec.y*pvec.x - l1vec.x*pvec.y)
    if 0 <= p_l1_u <= 1 and 0 <= p_l1_t <= 1:
        print "collide red"
    l2vec = line2 - center
    p_l2_u = (pvec.x*(center2.y-p1.y) + pvec.y*(p1.x-center2.x)) \
           /(l2vec.x*pvec.y - l2vec.y*pvec.x)
    p_l2_t = (l2vec.x*(p1.y-center2.y) + l2vec.y*(center2.x-p1.x)) \
           /(l2vec.y*pvec.x - l2vec.x*pvec.y)
    if 0 <= p_l2_u <= 1 and 0 <= p_l2_t <= 1:
        print "collide green" 

def end_line(center, radius, pos):
    mouse_dist = pos - center
    rot = mouse_dist.angle_to(vec(1,0)) % 360
    center_rotate = vec(radius, 0).rotate(-rot)
    circle_edge = center_rotate + center
    return circle_edge

def in_sector(center, line_1, line_2, radius, pos):
    if ((pos[0]-center[0])**2 + (pos[1]-center[1])**2) <= radius**2:
        pos_1 = line_1 - center
        rot_1 = pos_1.angle_to(vec(1,0)) % 360
        pos_2 = line_2 - center
        rot_2 = pos_2.angle_to(vec(1,0)) % 360
        angle = (pos - center).angle_to(vec(1,0)) % 360
        difference_0 = rot_1 - rot_2
        difference_1 = rot_1 - angle
        if difference_0 < 0:
            difference_0 += 360
        if difference_1 < 0:
            difference_1 += 360
        if difference_0 >= difference_1:
            return True
    return False

def run():
    running = True
    line_1 = 0
    line_2 = 0
    point_1 = 0
    point_2 = 0
    while running:
        clock.tick(0)
        mouse_pos = vec(pg.mouse.get_pos())
        rect.center = mouse_pos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_r:
                    line_1 = 0
                    line_2 = 0
                    point_1 = 0
                    point_2 = 0
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pressed()
                if mouse[2] == 1:
                    collided = collision(rect, vec_center, line_1, line_2, radius)
                if mouse[0] == 1:
                    if line_1 and not line_2:
                        line_2 = edge
                    if not line_1:
                        line_1 = edge
        pg.display.set_caption("{:.2f}".format(clock.get_fps()))
        screen.fill(white)
        pg.draw.circle(screen, black, center, radius, thickness)
        edge = end_line(center, radius, mouse_pos)
        if not line_2:
            pg.draw.line(screen, green, center, (edge[0], edge[1]), thickness)
        else:
            pg.draw.line(screen, green, center, (line_2[0], line_2[1]), thickness)
        if not line_1:
            pg.draw.line(screen, red, center, (edge[0], edge[1]), thickness)
        else:
            pg.draw.line(screen, red, center, (line_1[0], line_1[1]), thickness)
        if line_1 and line_2:
            collided = collision(rect, vec_center, line_1, line_2, radius)
            if collided:
                filled = 0
            else:
                filled = thickness
            pg.draw.rect(screen, black, rect, filled)
            line_1 = (line_1 - vec_center).rotate(0.1) + vec_center
            line_2 = (line_2 - vec_center).rotate(0.1) + vec_center
        pg.display.flip()

run()
