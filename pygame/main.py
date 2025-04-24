# 셋업
import os,pygame,sys,random, time
from pygame.locals import *

'''
뭐만들지
k_down 일정 시간 동안 무적이 됨 o
k_up 일정 시간 미사일이 많이 나감 o
ai 예측 알고리즘/미사일 클래스
점수 두 배 정예 몬스터 o
보스몹 o 보스 패턴 탄막 레이저 양쪽 움직임/보스1 패턴 작은 레이저 o
스테이지 구조(보스1-보스2-무한 모드) o

'''


# 현재 파일의 디렉토리로 작업 디렉토리 설정
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Space Defence")
screen = pygame.display.set_mode((1040, 650))

score = 0
shots =0
hits = 0
misses = 0

subfireact = False
subfirestart = 0 
lastsubfire= 0
lastsubfirekey=0

shieldact=False
shieldstart=0
lastshieldkey=0

gamestart=time.time()
b1spn=False
b2spn=False

ctime=0
ctimetg=False

mlpt = False
mlstart = 0 
lastml= 0
lastmlpt=0

lpt = False
lstart = 0 
lastl= 0
lastlpt=0

bulpt = False
bulpt2 = False
bulstart = 0 
lastbul= 0
lastbulpt=0

bstime1=0
bstime2=0
bstime3=0

font = pygame.font.Font(None, 20) # 기본 폰트, 크기:20
font2 = pygame.font.Font(None, 70)
last_badguys_spawm_time = 0    # 악당이 마지막에 나온 시각을 기록
last_sbadguys_spawm_time=0

badguy_iamge = pygame.image.load("img/rbadguy.png").convert()
badguy_iamge.set_colorkey((0,0,0))
sbadguy_img=pygame.image.load("img/sbadguy.png").convert()
sbadguy_img.set_colorkey((0,0,0))

boss1_img=pygame.image.load("img/miniboss.png").convert()
boss2_img=pygame.image.load("img/boss.png").convert()

laser_img=pygame.image.load("img/laser.png").convert()
laser_img.set_colorkey((255,255,255))
mlaser_img=pygame.image.load("img/mlaser.png").convert()
mlaser_img.set_colorkey((255,255,255))
bullet_img=pygame.image.load("img/bullet.png").convert()


fighter_image = pygame.image.load("img/rfighter.png").convert()
fighter_image.set_colorkey((255,255,255))

missile_image = pygame.image.load("img/rmissile.png").convert()
missile_image.set_colorkey((255,255,255))

skil1t_img= pygame.image.load("img/skil1t.png").convert()
skil1f_img=pygame.image.load("img/skil1f.png").convert()

skil2t_img=pygame.image.load("img/skil2t.png").convert()
skil2f_img=pygame.image.load("img/skil2f.png").convert()

shield_img=pygame.image.load("img/shield.png").convert()
shield_img.set_colorkey((255,255,255))

item_img=pygame.image.load("img/item.png").convert()
uitem_img=pygame.image.load("img/itemuse.png").convert()

GAME_OVER = pygame.image.load("img/rgameover.png").convert()

# 클래스 
class Badguy:
    def __init__ (self) :
        self.x = random.randint(0,960)
        self.y = -100
        self.dy = random.randint(2,6)
        self.dx = random.choice((-1, 1))*self.dy
    def move(self) :
        if self.x < 0 or self.x > 960 :
            self.dx *= -1
        self.x += self.dx
        self.dy += 0.1
        self.y += self.dy
    def draw(self) :
        screen.blit(badguy_iamge, (self.x, self.y))
    def sdraw(self):
        screen.blit(sbadguy_img, (self.x, self.y))
    def off_screen(self) :
        return self.y > 640
    def touching(self, missile) :
        return (self.x+35-missile.x)**2 + (self.y+22-missile.y)**2 < 1225
    def score(self):
        global score
        score += 100
    def sscore(self):
        global score
        score+=200

class Fighter :
    def __init__(self) :
        self.x = 320
        self.shieldacted=False
        self.restart=False
        self.itemon=False
    def move(self) :
        if pressed_keys[K_LEFT] and self.x > 3 :
            self.x -= 7
        if pressed_keys[K_RIGHT] and self.x < 930 :
            self.x += 7
    def draw(self):
        screen.blit(fighter_image, (self.x, 591))
    def fire(self) :
        global shots
        shots += 1
        missiles.append(Missile(self.x+50))
    def subfire(self):
        global shots
        shots+=3
        tmissiles.extend([Tmissile(self.x,591),Tmissile(self.x+50,591),Tmissile(self.x+100,591)])
    def shield(self):
        screen.blit(shield_img, (self.x-30, 570))
    def hit_by(self, badguy):
        if self.shieldacted:
            return False
        else:
            return (badguy.y > 585 and badguy.x > self.x - 55 and badguy.x < self.x + 85)
    def hits_by(self, sbadguy):
        if self.shieldacted:
            return False
        else:
            return (sbadguy.y > 585 and sbadguy.x > self.x - 55 and sbadguy.x < self.x + 85)
    def hit_ml(self, mlaser):
        if self.shieldacted:
            return False
        else:
            return (mlaser.y > 585 and mlaser.x > self.x - 15 and mlaser.x < self.x + 65)
    def hit_l(self, laser):
        if self.shieldacted:
            return False
        else:
            return (laser.y > 585 and laser.x > self.x - 15 and laser.x < self.x + 65)
    def hit_bul(self, bullet):
        if self.shieldacted:
            return False
        else:
            return (bullet.y > 585 and bullet.x > self.x - 45 and bullet.x < self.x + 45)
    def use_item(self):
        if self.itemon and not self.restart:
            screen.blit(uitem_img, (240, 12))
            screen.blit(font.render("used", True, (255, 255, 255)), (245, 60))
        else:
            screen.blit(item_img, (240, 12))
            screen.blit(font.render("Item", True, (255, 255, 255)), (247, 60))
                
class Missile :
    def __init__(self, x) :
        self.x = x
        self.y = 591
    def move(self) :
        self.y -= 5
    def off_screen(self) :
        return self.y < -8
    def draw(self) :
        screen.blit(missile_image, (self.x-4, self.y))

class Boss :
    def __init__(self):
        self.x=380
        self.y=100
        self.dx=5
        self.health = 80
        self.health2 = 160
        self.bosskill1=False
        self.bosskill2=False
        self.scored=False
        self.scored2=False
    def move(self):
        if self.x < 0 or self.x > 760 :
            self.dx *= -1
        self.x += self.dx
    def draw(self):
        screen.blit(boss1_img, (self.x, self.y))
    def draw2(self):
        screen.blit(boss2_img, (self.x, self.y))
    def score(self):
        if self.bosskill1 and not self.scored:
            global score
            score+=800
            self.scored=True
    def score2(self):
        if self.bosskill2 and not self.scored2:
            global score
            score+=1600
            self.scored2=True
    def hp(self, missile):
        return (self.x + 140 - missile.x) ** 2 + (self.y + 52 - missile.y) ** 2 < 6000
    def ptl(self):
        patternl.extend([Pattern(self.x,200), Pattern(self.x+260,200)])
    def ptml(self):
        patternml.extend([Pattern(self.x+random.randint(0,260),200), Pattern(self.x+random.randint(0,260),200)])
    def ptb(self):
        patternb.extend([Pattern(self.x-50,150), Pattern(self.x+50,250), Pattern(self.x+150,350)])
        patternb.extend([Pattern(self.x-50,200), Pattern(self.x+50,300), Pattern(self.x+150,400)])
    def ptb2(self):
        patternb2.extend([Pattern(self.x+100,300), Pattern(self.x+200,200), Pattern(self.x+300,100)])
        patternb2.extend([Pattern(self.x+100,350), Pattern(self.x+200,250), Pattern(self.x+300,150)])

class Pattern :
    def __init__(self, x, y):
        self.x=x
        self.y=y
    def mlaser(self):
        screen.blit(mlaser_img, (self.x, self.y))
    def laser(self):
        screen.blit(laser_img, (self.x, self.y))
    def bullet(self):
        screen.blit(bullet_img, (self.x, self.y))
    def move1(self):
        self.y += 8
    def move2(self):
        self.x += 5
    def move3(self):
        self.x-=5
    def off_screen(self):
        return self.y > 600
    
class Tmissile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 8
        self.target_pos = None
    def find_target(self, targets, locked_targets):
        if self.target_pos:
            return
        available_targets = [t for t in targets if t not in locked_targets]
        if not available_targets:
            return
        target = min(available_targets, key=lambda t: ((t.x - self.x) + (t.y - self.y)))
        self.target_pos = (target.x, target.y)
        if b1spn:
            self.target_pos = (target.x+150, target.y+100)
        if b2spn:
            self.target_pos = (target.x-50, target.y)
        locked_targets.add(target)
    def move(self):
        if self.target_pos and self.target_pos[1]<=self.y:
            dx = self.target_pos[0] - self.x
            dy = self.target_pos[1] - self.y
            distance = max((dx ** 2 + dy ** 2) ** 0.5, 0.1)
            self.x += self.speed * dx*2 / distance
            # self.y += self.speed * dy*2 / distance
            self.y -= self.speed
        else:
            self.y -= self.speed
    def off_screen(self):
        return self.y < -10 or self.y > 650
    def draw(self):
        screen.blit(missile_image, (self.x - 4, self.y))

def show_lobby():
    screen.fill((0, 0, 0))  # 배경색

    title_text = font2.render("SPACE DEFENCE", True, (255, 255, 255))
    press_text = font.render("Press any key to start", True, (255, 255, 255))

    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 200))
    screen.blit(badguy_iamge, (screen.get_width() // 2 - title_text.get_width() // 10, 300))
    screen.blit(press_text, (screen.get_width() // 2 - press_text.get_width() // 2, 400))

    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                waiting = False


def gameover():
    screen.blit(GAME_OVER, (370,150))

    screen.blit(font.render(str(shots), True, (255, 255, 255)), (580, 242))
    screen.blit(font.render(str(score), True, (255, 255, 255)), (580, 302))
    screen.blit(font.render(str(hits), True, (255, 255, 255)), (580, 262))
    screen.blit(font.render(str(misses), True, (255, 255, 255)), (580, 282))
    if shots == 0:
        screen.blit(font.render("--", True, (255, 255, 255)), (580, 322))
    else :
        screen.blit(font.render("{:.1f}%".format(100*hits/shots), True, (255, 255, 255)), (580, 322))

    pygame.display.update()
    pygame.time.wait(2000)  # 2초간 대기
    # 키 입력 대기
    waiting_for_keypress = True
    while waiting_for_keypress:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (not fighter.restart or fighter.itemon):
                waiting_for_keypress = False
                reset_game()  # 게임을 다시 초기화
            elif event.type == KEYDOWN and fighter.restart :
                waiting_for_keypress = False
                restart_game()

# def endc():

def restart_game() :
    global badguys,sbadguys,patternl,patternml,patternb,patternb2
    fighter.itemon=True
    fighter.restart=False
    badguys = []
    sbadguys = []
    patternl= []
    patternml= []
    patternb= []
    patternb2= []

def reset_game() : # 게임을 다시 초기화
    global badguys, gamestart, sbadguys, missiles, tmissiles,fighter, boss, b1spn, b2spn, ctime, ctimetg, patternl, patternml,patternb,patternb2, score, shots, hits, misses, subfireact, subfirestart, lastsubfire, lastsubfirekey, shieldact, shieldstart, lastshieldkey,mlpt,mlstart,lastml,lastmlpt,lpt,lstart,lastl,lastlpt,bulpt,bulstart,lastbul,lastbulpt
    badguys = []
    sbadguys = []
    missiles = []
    fighter = Fighter()
    boss=Boss()
    b1spn=False
    b2spn=False
    ctimetg=False
    gamestart=time.time()
    ctime=0
    patternl= []
    patternml= []
    patternb= []
    patternb2= []
    tmissiles = []
    score = 0
    hits = 0
    misses = 0
    shots = 0 
    subfireact = False
    subfirestart = 0 
    lastsubfire= 0
    lastsubfirekey=0
    shieldact=False
    shieldstart=0
    lastshieldkey=0
    mlpt = False
    mlstart = 0 
    lastml= 0
    lastmlpt=0
    lpt = False
    lstart = 0 
    lastl= 0
    lastlpt=0
    bulpt = False
    bulpt2 = False
    bulstart = 0 
    lastbul= 0
    lastbulpt=0

# 리스트
badguys = []
sbadguys = []
fighter = Fighter()
missiles = []
boss=Boss()
patternl= []
patternml= []
patternb= []
patternb2= []
tmissiles = []

show_lobby()
# 게임루프
while 1 :
    clock.tick(60)

    pressed_keys = pygame.key.get_pressed()
    screen.fill((0,0,0))
    fighter.move()
    fighter.draw()
    
    if time.time()-lastsubfirekey> 3:
        screen.blit(skil1t_img, (100, 12))
    else:
        screen.blit(skil1f_img, (100, 12))

    if time.time()-lastshieldkey> 3:
        screen.blit(skil2t_img, (170, 12))
    else:
        screen.blit(skil2f_img, (170, 12))

    for event in pygame.event.get():
        if event.type == QUIT :
            sys.exit()
        if event.type == KEYDOWN and event.key == K_UP and time.time()-lastsubfirekey> 3:
                subfireact = True
                subfirestart = time.time()
                fighter.subfire()
        elif event.type==KEYDOWN and event.key==K_DOWN and time.time()-lastshieldkey>3:
                shieldact = True
                shieldstart = time.time()
        else:
            if event.type == KEYDOWN and event.key == K_SPACE :
                fighter.fire()   

    if not b1spn and not b2spn and not boss.bosskill1 and time.time() - gamestart >= 15:
        b1spn=True
    
    if not b2spn and boss.bosskill1 and not boss.bosskill2 and time.time() - ctime >= 15:
        b2spn=True

    if b1spn:
        boss.draw()
        i=0
        while i < len(missiles):
            if boss.hp(missiles[i]):
                boss.health-=1
                del missiles[i]
                hits += 1
                i-=1
            i+=1
        i = 0
        while i < len(tmissiles):
            if boss.hp(tmissiles[i]):
                boss.health -= 1
                del tmissiles[i]
                hits += 1
                i -= 1
            i += 1

    if b1spn :
        mlpt=True

    if b2spn :
        lpt=True
        bulpt=True
        bulpt2=True

    if b2spn:
        boss.move()
        boss.draw2()
        i=0
        while i < len(missiles):
            if boss.hp(missiles[i]):
                boss.health2-=1
                del missiles[i]
                hits += 1
                i-=1
            i+=1
        i = 0
        while i < len(tmissiles):
            if boss.hp(tmissiles[i]):
                boss.health2 -= 1
                del tmissiles[i]
                hits += 1
                i -= 1
            i += 1

    if boss.health<=0 and not fighter.itemon:
        b1spn=False
        boss.bosskill1=True
        fighter.restart=True
        boss.score()
        if not ctimetg:
            ctime=time.time()
            ctimetg=True

    if boss.health2<=0: 
        b2spn=False
        boss.bosskill2=True
        boss.score2()
        if not ctimetg:
            ctime=time.time()
            ctimetg=True
    
    if boss.bosskill1:
        fighter.use_item()

    if shieldact:
        if time.time() - shieldstart < 3:
            fighter.shield()
            fighter.shieldacted=True
        else:
            lastshieldkey=time.time()
            shieldact = False
            fighter.shieldacted = False

    if subfireact:
        if time.time() - subfirestart < 3: 
            if time.time() - lastsubfire >= 0.1:
                fighter.subfire()
                lastsubfire = time.time() 
        else:
            lastsubfirekey=time.time()
            subfireact = False

    if mlpt:
        if time.time() - lastml >= 0.5:
            boss.ptml()
            lastml = time.time()
        if b1spn==False:
            mlpt=False

    if lpt:
        if time.time() - lastl >=1:
            boss.ptl()
            lastl = time.time() 
        if b2spn==False:
            lpt = False

    if bulpt:
        if time.time() - lastbul >=1 and boss.x < 0:
            boss.ptb2()
            lastbul = time.time() 
        if b2spn==False:
            bulpt = False

    if bulpt2:
        if time.time() - lastbul >=1 and boss.x > 760:
            boss.ptb()
            lastbul = time.time() 
        if b2spn==False:
            bulpt2 = False

    if time.time() - last_badguys_spawm_time > 0.5 and not b1spn and not b2spn :
        badguys.append(Badguy())
        last_badguys_spawm_time = time.time()    

    if time.time() - last_sbadguys_spawm_time > 3 and not b1spn and not b2spn:
        sbadguys.append(Badguy())
        last_sbadguys_spawm_time = time.time()    

    i=0
    while i < len(patternml) and mlpt: 
        patternml[i].move1()
        patternml[i].mlaser()
        if patternml[i].off_screen():
            del patternml[i]
            i -= 1
        i += 1
    i=0

    while i < len(patternb) and bulpt:
        patternb[i].move1()
        patternb[i].move3()
        patternb[i].bullet()
        if patternb[i].off_screen():
            del patternb[i]
            i -= 1
        i += 1

    i=0
    while i < len(patternb2) and bulpt2:
        patternb2[i].move1()
        patternb2[i].move2()
        patternb2[i].bullet()
        if patternb2[i].off_screen():
            del patternb2[i]
            i -= 1
        i += 1

    i=0
    while i < len(patternl) and lpt: 
        patternl[i].move1()
        patternl[i].laser()
        if patternl[i].off_screen():
            del patternl[i]
            i -= 1
        i += 1

    i = 0
    while i < len(badguys):
        badguys[i].move()
        badguys[i].draw()
        if badguys[i].off_screen():
            del badguys[i]
            i -= 1
        i += 1

    k = 0
    while k < len(sbadguys):
        sbadguys[k].move()
        sbadguys[k].sdraw()
        if sbadguys[k].off_screen():
            del sbadguys[k]
            k -= 1
        k += 1
        
    i = 0
    while i < len(missiles): 
        missiles[i].move()
        missiles[i].draw()
        if missiles[i].off_screen():
            del missiles[i]
            misses += 1
            i -= 1
        i += 1
        
    i = 0
    while i < len(tmissiles):
        locked_targets = set()
        all_targets = badguys + sbadguys
        if b1spn or b2spn:
            all_targets.append(boss)
        for tmissile in tmissiles:
            tmissile.find_target(all_targets, locked_targets)
        tmissiles[i].move()
        tmissiles[i].draw()
        if tmissiles[i].off_screen():
            del tmissiles[i]
            misses += 1
            i -= 1
        i += 1

    i = 0
    while i < len(badguys):
        j = 0
        while j < len(missiles):
            if badguys[i].touching(missiles[j]):
                badguys[i].score()
                hits += 1
                del badguys[i]
                del missiles[j]
                i -= 1
                break
            j += 1
        i += 1
    i = 0

    while i < len(sbadguys):
        j = 0
        while j < len(missiles):
            if sbadguys[i].touching(missiles[j]):
                sbadguys[i].sscore()
                hits += 1
                del sbadguys[i]
                del missiles[j]
                i -= 1
                break
            j += 1
        i += 1

    i = 0
    while i < len(tmissiles):
        j = 0
        while j < len(badguys):
            if badguys[j].touching(tmissiles[i]):
                badguys[j].score()
                hits += 1
                del badguys[j]
                del tmissiles[i]
                i -= 1
                break
            j += 1
        i += 1

    i = 0
    while i < len(tmissiles):
        j = 0
        while j < len(sbadguys):
            if sbadguys[j].touching(tmissiles[i]):
                sbadguys[j].sscore()
                hits += 1
                del sbadguys[j]
                del tmissiles[i]
                i -= 1
                break
            j += 1
        i += 1

        
    screen.blit(font.render("Score: "+ str(score), True, (255,255,255)), (5,5))
    screen.blit(font.render("Up", True, (255,255,255)), (115,60))
    screen.blit(font.render("Down", True, (255,255,255)), (175,60))

    if boss.bosskill1:
        screen.blit(font.render("1 stage clear ", True, (255,255,255)), (5,25))
    if boss.bosskill2:
        screen.blit(font.render("2 stage clear", True, (255,255,255)), (5,40))

    for badguy in badguys:
        if fighter.hit_by(badguy):
            gameover()
    for sbadguy in sbadguys:
        if fighter.hits_by(sbadguy) :
            gameover()
    for patternls in patternl:
        if fighter.hit_l(patternls):
            gameover()
    for patternmls in patternml:
        if fighter.hit_ml(patternmls) :
            gameover()
    for patternbs in patternb:
        if fighter.hit_bul(patternbs) :
            gameover()
    pygame.display.update()