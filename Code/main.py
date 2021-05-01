import numpy as np 
import pygame
import math 
import sys
import os 
from ship import *
from roid import *
from bullet import * 
from testBlock import * 
from population import * 
from vision import * 

DISPLAY_W = 700
DISPLAY_H = 500
BORDER_BOX = (100, 100, 500, 300) 
AST_LIMIT = 10
FIRERATE = 200 # Milliseconds 

def clearSavedGens(): 
    DIR = "SavedGenerations"
    numGens = (len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))
    
    if numGens != 0:  
        for i in range(1, numGens+1): 
            fileName = "gen" + str(i) + ".txt"
            os.remove("SavedGenerations/"+fileName) 
            
def saveBest(net, num): 
    name = "gen" + str(num) +".txt" 
    file = open("SavedGenerations/"+name, "w") 
    for i in np.nditer(net.weight_input_h1): 
        file.write(str(i)+"\n") 
    for i in np.nditer(net.weight_input_h2): 
        file.write(str(i)+"\n") 
    for i in np.nditer(net.weight_output): 
        file.write(str(i)+"\n") 
    file.close() 

def genPopulations(populations, count, surface): 
    populations.clear() 
    for i in range(0, count): 
        newPopulation = Population() 
        newPopulation.genVision(surface) 
        populations.append(newPopulation) 

def resetPopulations(populations): 
    for p in populations: 
        p.gameOver = False 
        p.timeAlive = 0 
        p.score = 0 
        p.fitness = 0 
        p.usedLeft = False 
        p.usedRight = False
        p.usedShoot = False 
    
def matePopulations(pop1, pop2): 
    new_net = Network(9, 9, 6, 3) 
    new_net.create_mixed_weights(pop1, pop2) 
    
    return new_net 
    
def evolvePopulations(populations): 
    mutation_cutoff = 0.4 
    mutation_bad_keep = 0.2 
    mutation_chance_lim = 0.4 
    
    cutoff = int(len(populations) * mutation_cutoff) 
    good_pop = populations[0:cutoff] 
    bad_pop = populations[cutoff:] 
    num_bad_take = int(len(populations) * mutation_bad_keep) 
    #print("Cutoff: ", cutoff) 
    #print("bad_pop: ", len(bad_pop)) 
    #print("Num_bad_take ", num_bad_take) 
    
    for p in bad_pop: 
        p.network.modify_weights() 
    
    new_pops = []
    
    sel_bad_take = np.random.choice(np.arange(len(bad_pop)), num_bad_take, replace=False) 
    
    for index in sel_bad_take: 
        new_pops.append(bad_pop[index]) 
    
    new_pops.extend(good_pop) 
    
    pops_needed = len(populations) - len(new_pops) 
    
    while len(new_pops) < len(populations): 
        sel_to_breed = np.random.choice(np.arange(len(good_pop)), 2, replace=False) 
        if sel_to_breed[0] != sel_to_breed[1]: 
            new_pop = Population() 
            new_pop.network = matePopulations(good_pop[sel_to_breed[0]], good_pop[sel_to_breed[1]]) 
            if np.random.random() < mutation_chance_lim: 
                new_pop.network.modify_weights() 
            new_pops.append(new_pop) 
    
        

def spawn_asteroid(asteroid_list): 
    
    side = np.random.randint(0, 4) # Left = 0, Right = 1, Top = 2, Bottom = 3
    if side == 0: 
        xPos = 0
        yPos = np.random.randint(0, 501) 
    elif side == 1: 
        xPos = 700
        yPos = np.random.randint(0, 501) 
    elif side == 2: 
        xPos = np.random.randint(0, 701) 
        yPos = 0 
    elif side == 3: 
        xPos = np.random.randint(0, 701) 
        yPos = 500 

    speed = np.random.randint(1, 3)
    
    asteroid = Asteroid(xPos, yPos, speed) 
    asteroid_list.add(asteroid) 
    
    print("New asteroid") 
    

def fire(bullet_list, playerShip): 
    
    center = playerShip.getORect().center 
    top = (playerShip.getORect()).top
    
    radius = center[1] - top 
    
    posX = center[0]
    posY = center[1]
    
    angle = playerShip.getAngle() 
    
    # Trig is weird because of how pygame percieves the grid space 
    dx = radius * math.sin(math.radians(angle)) 
    dy = radius * math.cos(math.radians(angle)) 
    
    posX += dx   
    posY -= dy 
    
    bullet = Bullet(posX, posY, angle) 
    bullet_list.add(bullet)
    



def run_game():
    # SETUP -----------------------------------
    
    # Initialize game space 
    pygame.init()

    # Set window size and caption
    screen = pygame.display.set_mode([DISPLAY_W, DISPLAY_H])
    pygame.display.set_caption("Start Menu")
    
    font = pygame.font.SysFont("Bahnschrift", 20) # Font 
    
    start = True 
    progPlay = False 
    progTrain = False 
    progTest = False 
    
    # START MENU ------------------------------
    
    while start: 
        
        PLAY_BOX = ((DISPLAY_W/2) - 100, DISPLAY_H/3, 200, 50)
        TRAIN_BOX = ((DISPLAY_W/2) - 100, (DISPLAY_H/3) + 70, 200, 50)
        TEST_BOX = ((DISPLAY_W/2) - 100, (DISPLAY_H/3) + 140, 200, 50) 
        
        events = pygame.event.get() 
        for event in events: 
            if event.type == pygame.QUIT: 
                start = False 
            if event.type == pygame.MOUSEBUTTONDOWN: 
                mouse = pygame.mouse.get_pos() 
                if mouse[0] >= PLAY_BOX[0] and mouse[0] <= (PLAY_BOX[0] + PLAY_BOX[2]) and mouse[1] >= PLAY_BOX[1] and mouse[1] <= (PLAY_BOX[1] + PLAY_BOX[3]): 
                    start = False 
                    progPlay = True 
                    pygame.display.set_caption("Solo play") 
                elif mouse[0] >= TRAIN_BOX[0] and mouse[0] <= (TRAIN_BOX[0] + TRAIN_BOX[2]) and mouse[1] >= TRAIN_BOX[1] and mouse[1] <= (TRAIN_BOX[1] + TRAIN_BOX[3]): 
                    start = False 
                    progTrain = True 
                    pygame.display.set_caption("Training") 
                elif mouse[0] >= TEST_BOX[0] and mouse[0] <= (TEST_BOX[0] + TEST_BOX[2]) and mouse[1] >= TEST_BOX[1] and mouse[1] <= (TEST_BOX[1] + TEST_BOX[3]): 
                    start = False 
                    progTest = True 
                    pygame.display.set_caption("Testing") 
                
        screen.fill((0, 0, 0))
        
        pygame.draw.rect(screen, WHITE, PLAY_BOX, 2)
        pygame.draw.rect(screen, WHITE, TRAIN_BOX, 2) 
        pygame.draw.rect(screen, WHITE, TEST_BOX, 2) 
        
        play_text = font.render("PLAY", True, WHITE)
        play_textRect = play_text.get_rect(center=(DISPLAY_W/2, DISPLAY_H/3+25))
        train_text = font.render("TRAIN", True, WHITE) 
        train_textRect = train_text.get_rect(center=(DISPLAY_W/2, (DISPLAY_H/3) +95))
        test_text = font.render("TEST", True, WHITE) 
        test_textRect = test_text.get_rect(center=(DISPLAY_W/2, (DISPLAY_H/3) +165))
        
        screen.blit(play_text, play_textRect)
        screen.blit(train_text, train_textRect)
        screen.blit(test_text, test_textRect) 
        
        pygame.display.flip() 
        
    # -----------------------------------------
        
    # SOLO PLAY -------------------------------
    if progPlay == True: 
        
        playerShip = Ship()
        ship_list = pygame.sprite.Group() 
        ship_list.add(playerShip)
        
        asteroid_list = pygame.sprite.Group() 
        bullet_list = pygame.sprite.Group() 
        
        gameOver = False 
        score = 0
        last_shot = 0 
        spawnBox = False # For testing 

        # Create game time, FPS
        clock = pygame.time.Clock()
        startTime = pygame.time.get_ticks() 
        
        # Timed events
        SPAWN_AST = pygame.USEREVENT 
        pygame.time.set_timer(SPAWN_AST, 1000) # Trigger SPAWN_AST every 1s 
        
        while progPlay:

            events = pygame.event.get()
            for event in events: 
                if event.type == pygame.QUIT:
                    progPlay = False
                if event.type == SPAWN_AST: 
                    if len(asteroid_list) < AST_LIMIT: 
                        spawn_asteroid(asteroid_list) 
                if event.type == pygame.KEYDOWN and gameOver == False: 
                    if event.key == pygame.K_SPACE: 
                        if(pygame.time.get_ticks() >= last_shot+FIRERATE or last_shot == 0):
                            last_shot = pygame.time.get_ticks() 
                            fire(bullet_list, playerShip) 

            if gameOver == False: 
                keys = pygame.key.get_pressed() 
                if keys[pygame.K_LEFT]: 
                    playerShip.rotate("left")
                if keys[pygame.K_RIGHT]:
                    playerShip.rotate("right") 

            # UPDATES ----------------------------
            # Placements
            screen.fill((0, 0, 0))  # Black screen
            
            # Timer, might move this to another class 
            milliseconds = pygame.time.get_ticks() - startTime 
            seconds = format(int((milliseconds / 1000) % 60), "02") 
            minutes = format(int((milliseconds / 1000) / 60), "02") 
            time = str(minutes + " : " + seconds) 
            
            time_text = font.render(time, True, WHITE) 
            # time_textRect = time_text.get_rect(center=(655, 20))
            time_textRect = time_text.get_rect(right=690, top=5) 
            
            # Score text, might move this to another class 
            score_text = font.render(str(format(score, "08")), True, WHITE)
            score_textRect = score_text.get_rect(left=10, top=5)
            
            
            # Move asteroids based on their trajectories 
            for ast in asteroid_list:
                ast.move() 
                ast.killCheck() 
            for blt in bullet_list: 
                blt.move() 
                blt.killCheck() 
                
            # Check to see if any asteroids have collided with the player 
            collision = pygame.sprite.spritecollide(playerShip, asteroid_list, False) 
            for plr in ship_list: 
                for ast in collision: 
                    ast.destroy() 
                    playerShip.destroy() 
                    gameOver = True 

            # Check to see if any bullets have collided with an asteroid 
            for blt in bullet_list: 
                bullet_x_ast = pygame.sprite.spritecollide(blt, asteroid_list, False) 
                for ast in bullet_x_ast: 
                    ast.destroy() 
                    blt.destroy() 
                    score += 20
            
            
            # Update screen
            screen.blit(time_text, time_textRect) 
            screen.blit(score_text, score_textRect)
            for plr in ship_list: 
                screen.blit(playerShip.getImg(), playerShip.getRect()) 
            for ast in asteroid_list: 
                screen.blit(ast.getImg(), ast.getRect())
            for blt in bullet_list: 
                screen.blit(blt.getImg(), blt.getRect())
            
            # Testing 
            if spawnBox == True: 
                pygame.draw.rect(screen, WHITE, BORDER_BOX, 2) 
            
            pygame.display.flip()
            clock.tick(60) # 60FPS
    
    # -----------------------------------------
    
    # TRAIN DATA SET --------------------------
    
    if progTrain == True: 
        
        clearSavedGens() 
        
        clock = pygame.time.Clock() 
        timeStart = pygame.time.get_ticks() 
        
        invinsible = False 
        showLos = False 
        
        populations = []
        
        SPAWN_AST = pygame.USEREVENT 
        pygame.time.set_timer(SPAWN_AST, 1000) # Spawn asteroid every 1s 
        
        genStartTime = pygame.time.get_ticks() 
        
        # Generate populations 
        populationCount = 200
        genNum = 1
        genPopulations(populations, populationCount, screen) 
        print("Starting generation", genNum) 
        
        
        while progTrain:
            
            # Check status of populations 
            popAlive = 0 
            for p in populations: 
                if p.getStatus() == False: 
                    popAlive += 1
            if popAlive == 0: 
                for p in populations:
                    p.updateFitness() 
                populations.sort(key=lambda x: x.fitness, reverse=True) 
                saveBest(populations[0].network, genNum) 
                print("Best fitness: ", populations[0].fitness) 
                print("Time to complete: ", pygame.time.get_ticks()-genStartTime)
                print("")  
                evolvePopulations(populations) 
                resetPopulations(populations) 
                genNum += 1
                print("Starting generation", genNum) 
                genStartTime = pygame.time.get_ticks() 
                timeStart = pygame.time.get_ticks() 
                
                
            # Check for in-game events 
            events = pygame.event.get() 
            for event in events: 
                if event.type == pygame.QUIT: 
                    progTrain = False 
                if event.type == SPAWN_AST: 
                    for p in populations: 
                        if p.getStatus() == False: 
                            if len(p.getAstList()) < AST_LIMIT: 
                                p.spawnAsteroid() 
                        
            # Test if all populations are present and movement
            net_inputs = [] 
            
            for p in populations: 
                net_inputs = []
                if p.getStatus() == False: 
                    
                    # Fitness 
                    p.timeAlive = pygame.time.get_ticks() - timeStart 
                    #p.updateFitness() 
                                        
                    # Collisions 
                    for blt in p.getBltList(): 
                        bullet_x_ast = pygame.sprite.spritecollide(blt, p.getAstList(), False)
                        for ast in bullet_x_ast: 
                            ast.destroy() 
                            blt.destroy() 
                            p.score += 20 
                    
                    if invinsible == False: 
                        plr_x_ast = pygame.sprite.spritecollide(p.getShip(), p.getAstList(), False) 
                        if len(plr_x_ast) == 1: 
                            p.nuke() 
                            p.gameOver = True 
                    
                    # Vision reactions 
                    los = p.getLos()
                    for i in range(0, len(los)): 
                        astDistance = 0 
                        vision_x_ast = pygame.sprite.spritecollide(los[i], p.getAstList(), False) 
                        if len(vision_x_ast) > 0: 
                            astDistance = p.astDistance(vision_x_ast) 
                        net_inputs.append(astDistance) 
                    
                    net_inputs.append(p.getShip().getAngle())
                    
                    # Calculate moves from neural net 
                    net_moves = p.runNetwork(net_inputs) 
                            
                    # Movement 
                    # [0] is rotation left; [1] is rotation right; [2] is shoot 
                    
                    # Random moving 
                    #move = np.random.randint(0,2) # 0 = Left, 1 = Right 
                    #p.shipMove(move)  
                    if net_moves[0] >= 0.7: 
                        p.shipMove(0)
                    if net_moves[1] >= 0.7: 
                        p.shipMove(1) 
                    
                    #if(np.random.randint(0,2) == 1): 
                    if net_moves[2] >= 0.7:
                        p.fire(pygame.time.get_ticks()) 
                    
                    for ast in p.getAstList(): 
                        ast.move() 
                        ast.killCheck() 
                    for blt in p.getBltList(): 
                        blt.move() 
                        blt.killCheck() 
            
            
            # UPDATES 
            screen.fill((0, 0, 0)) # Black 
            
            for p in populations: 
                if p.getStatus() == False: 
                    screen.blit(p.getShipImg(), p.getShipRect()) 
                    for ast in p.getAstList(): 
                        screen.blit(ast.getImg(), ast.getRect()) 
                    for blt in p.getBltList(): 
                        screen.blit(blt.getImg(), blt.getRect()) 
                    if showLos == True: 
                        for los in p.getLos(): 
                            screen.blit(los.getImg(), los.getRect())
                    
            
            pygame.display.flip() 
            clock.tick(60) 
    
    # -----------------------------------------
    
    # TEST DATA SET ---------------------------
    
    if progTest == True: 
        
        GEN_TO_TEST = 1 
        
        showLos = False 
        
        p = Population() 
        p.genVision(screen) 
        
        name = "gen" + str(GEN_TO_TEST) + ".txt" 
        file = open("SavedGenerations/"+name, "r") 
        p.network.fillArray(file) 
        file.close() 
        
        clock = pygame.time.Clock() 
        timeStart = pygame.time.get_ticks() 
        finalTime = 0 
        
        SPAWN_AST = pygame.USEREVENT 
        pygame.time.set_timer(SPAWN_AST, 1000) # Spawn asteroid every 1s 
        
        
        while progTest: 
            
            events = pygame.event.get() 
            for event in events: 
                if event.type == pygame.QUIT: 
                    progTest = False 
                if event.type == SPAWN_AST: 
                    if len(p.getAstList()) < AST_LIMIT: 
                        p.spawnAsteroid() 
            
            # On-screen timer 
            if p.getStatus() == False: 
                milliseconds = pygame.time.get_ticks() - timeStart 
                seconds = format(int((milliseconds / 1000) % 60), "02") 
                minutes = format(int((milliseconds / 1000) / 60), "02") 
                time = str(minutes + " : " + seconds) 
            finalTime = time 
            
            time_text = font.render(finalTime, True, WHITE) 
            time_textRect = time_text.get_rect(right=690, top=5) 
            
            # Score text, might move this to another class 
            score_text = font.render(str(format(p.score, "08")), True, WHITE)
            score_textRect = score_text.get_rect(left=10, top=5)
            
            net_inputs = []
            
            if p.getStatus() == False: 
                                    
                # Collisions 
                for blt in p.getBltList(): 
                    bullet_x_ast = pygame.sprite.spritecollide(blt, p.getAstList(), False)
                    for ast in bullet_x_ast: 
                        ast.destroy() 
                        blt.destroy() 
                        p.score += 20 
                
                plr_x_ast = pygame.sprite.spritecollide(p.getShip(), p.getAstList(), False) 
                if len(plr_x_ast) == 1: 
                    p.nuke() 
                    p.gameOver = True 
                
                # Vision reactions 
                los = p.getLos()
                for i in range(0, len(los)): 
                    astDistance = 0 
                    vision_x_ast = pygame.sprite.spritecollide(los[i], p.getAstList(), False) 
                    if len(vision_x_ast) > 0: 
                        astDistance = p.astDistance(vision_x_ast) 
                    net_inputs.append(astDistance) 
                
                net_inputs.append(p.getShip().getAngle())
                
                # Calculate moves from neural net 
                net_moves = p.runNetwork(net_inputs) 
                        
                # Movement 
                # [0] is rotation left; [1] is rotation right; [2] is shoot 
                if net_moves[0] >= 0.7: 
                    p.shipMove(0)
                if net_moves[1] >= 0.7: 
                    p.shipMove(1) 
                
                if net_moves[2] >= 0.7:
                    p.fire(pygame.time.get_ticks()) 
                
                for ast in p.getAstList(): 
                    ast.move() 
                    ast.killCheck() 
                for blt in p.getBltList(): 
                    blt.move() 
                    blt.killCheck() 
            
            # UPDATES 
            screen.fill((0, 0, 0)) # Black 
            
            screen.blit(time_text, time_textRect) 
            screen.blit(score_text, score_textRect)
            
            if p.getStatus() == False: 
                screen.blit(p.getShipImg(), p.getShipRect()) 
                for ast in p.getAstList(): 
                    screen.blit(ast.getImg(), ast.getRect()) 
                for blt in p.getBltList(): 
                    screen.blit(blt.getImg(), blt.getRect()) 
                if showLos == True: 
                    for los in p.getLos(): 
                        screen.blit(los.getImg(), los.getRect())
                    
            
            pygame.display.flip() 
            clock.tick(60) 
            
                        
    # ----------------------------------------- 

    # EXIT HANDLING 
    pygame.display.quit()
    pygame.quit()
    
    
    
    

if __name__ == "__main__":
    print("Running game")
    run_game()
    print("Game closed")
