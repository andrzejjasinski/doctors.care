import os
from sys import *
import shlex
import subprocess
from time import strftime #imprt time module

os.system('cls' if os.name == 'nt' else 'clear')  
if platform == "linux" or platform == "linux2":            
    osversion = 'Linux'  
else:
    osversion = 'MS Windows'     
print ('==================================')
print ('OS = '+osversion)
game = 'start' 
try:
    import mysql.connector
    from mysql.connector import errorcode     
    print ('MySQL connector OK')    
except:    
    print ('MySQL connector is not installed!!')
    game = 'stop' 
try:    
    import pygame  
    print ("Pygame Version Number = "+str(pygame.version.vernum))  
except:    
    game = ('stop') 
    print ("Pygame not installed")    
print ('==================================\n')

if osversion != 'MS Windows': 
    home_folder = os.getenv('HOME')  
    clock_tick = 30
if osversion == 'MS Windows': 
    home_folder = 'c:/'
    clock_tick = 30

if game == 'start':
    
    if osversion == ('Linux') :
	logo_os1 = (home_folder+'/doctors_care/graphics/linux.png') 
    else:
	logo_os1 = (home_folder+'/doctors_care/graphics/windows.png') 
    
    font_1_file = (home_folder+'/doctors_care/fonts/font_1.ttf')     
    font_2_file = (home_folder+'/doctors_care/fonts/font_2.ttf')     
    full_screen = 'false'
    program_DC = 'run'
    print ('Graphics initialization...')
    pygame.init()     
    pygame.font.init()
    pygame.mouse.set_visible(True)
    clock = pygame.time.Clock()
        
    scale_a = ''
    scale_b = ''
    scroll_pos = ['0', '0', '1366', '768', '1366', '0']
    window_size_factor = 0.88
    
   
    
    
    print ('completed...')    
    def screen_resolution_display (a,b,logo_os):	   
	print ('Resolution detected: '+str(a)+'x'+str(b))     
	scale_a = a / 1366.0 * 1
	scale_b = b / 768.0  * 1
	
	print ('Resolution descaled: '+str(scale_a)+'x'+str(scale_b)) 
	print ('Resolution after: '+str(scale_a*a)+'x'+str(scale_b*b)) 
	if osversion == 'MS Windows': 
	    background_5a = pygame.transform.scale(logo_os,(int(70*scale_a), int(70*scale_b)))
	if osversion != 'MS Windows': 
	    background_5a = pygame.transform.scale(logo_os,(int(70*scale_a), int(90*scale_b)))
	font_1 = pygame.font.Font(font_1_file, int(30*scale_a)) 
	font_2 = pygame.font.Font(font_2_file, int(40*scale_a)) 
	
	return(scale_a, scale_b, background_5a, font_1, font_2)
        
    screen_resolution = (pygame.display.list_modes()[0])          
    a = int ((screen_resolution[0]))    
    b = int ((screen_resolution[1]))    
    scroll_pos[0] = (a)
    scroll_pos[1] = (b)   
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    logo_os = pygame.image.load(logo_os1).convert_alpha() 
    scale_a, scale_b, background_5a, font_1, font_2 = screen_resolution_display(a,b,logo_os)
   
    
    display_nominal_x = a
    display_nominal_y = b
    pygame.display.flip() 
    user_name = ''  
    user_password = ''
    user_password_secu = ''
    font_color_user_name = (0, 0, 0)
    font_color = (0,0,0) 
    black = (0,0,0)
    white = (253,253,253)
    gray = (211,211,211)  
    login_stage = ['start', '1', '0', '0', 'sql_ok']
    scrolling_txt = ("Doctors Care Medical System for "+osversion+". MSc in Software Engineering - Athlone Institute of Technology 2016/2017." )
        
    while program_DC == 'run':
	
	screen.fill((55,55,50))
	
	for event in pygame.event.get():	    
	    if event.type == pygame.QUIT:                                
		pygame.quit()            
		exit()  
	    
	    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
		mousex, mousey = pygame.mouse.get_pos() 
		print (mousex, mousey)
		if login_stage[4] == 'sql_password_error' or login_stage[4] == 'sql_error':
		    
		    login_stage[1] = '1'
		    login_stage[2] = '0'
		    login_stage[3] = '0'
		    login_stage[4] = 'sql_ok'
		    user_name = ''
		    user_password = ''
		    user_password_secu = ''
		    font_color_user_name = (0,0,0)
		    
			    
	    if login_stage[1] == '1' and login_stage[2] == '0':
		if event.type == pygame.KEYDOWN:  
		    login_stage[3] = '0'
		    if event.key == pygame.K_BACKSPACE: 
			user_name = user_name[:-1] 
		    elif event.unicode and event.key != pygame.K_RETURN and event.key != pygame.K_ESCAPE:
			if len(user_name) <= 14:
			    user_name += event.unicode 
		    elif event.key == pygame.K_RETURN: 	
			if len(user_name) >= 6:
			    login_stage[2] = '1'
			    mysql_ip_user_name = user_name
			    
	    if login_stage[1] == '1' and login_stage[2] == '1':			    
		if event.type == pygame.KEYDOWN: 
		    if event.key == pygame.K_BACKSPACE: 
			user_password = user_password[:-1] 
			user_password_secu = user_password_secu[:-1] 
			user_ip_controller_password = ''
		    elif event.unicode and event.key != pygame.K_RETURN and event.key != pygame.K_ESCAPE:
			if len(user_password) <= 10:
			    user_ip_controller_password = ''
			    user_password += event.unicode
			    user_password_secu += '*' 
		    elif event.key == pygame.K_RETURN: 
			if len(user_password) > 7:
			    mysql_password = user_password
			    print ('Connecting...')
			    login_stage[3] = '1'
			    	
	    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2 or event.type == pygame.KEYDOWN:
		windows_screen = 'true'
		if event.key == pygame.K_ESCAPE:
                  
		    if full_screen == 'false':
			full_screen = 'true'
		    else:
			full_screen = 'false'
		    if full_screen == 'true':
			pygame.display.quit()
			pygame.display.init()
			
			a = int(a *window_size_factor)
			b = int(b * window_size_factor)
			scroll_pos[0] = int(scroll_pos[0] * window_size_factor) 
			scroll_pos[1] = int(scroll_pos[0] * window_size_factor)   			
			screen = pygame.display.set_mode((a,b), pygame.RESIZABLE)
			scale_a, scale_b, background_5a, font_1, font_2 = screen_resolution_display(a,b,logo_os)
			pygame.display.set_caption("Doctors Care Medical System for "+osversion+". MSc in Software Engineering - Athlone Institute of Technology 2016/2017.")
			
		    if full_screen == 'false':
			pygame.display.quit()
			pygame.display.init()
			screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
			screen_resolution = (pygame.display.list_modes()[0])          
			a = int ((screen_resolution[0]))    
			b = int ((screen_resolution[1]))		    
			scale_a, scale_b, background_5a, font_1, font_2 = screen_resolution_display (a,b,logo_os)
		
	background_color = (55,55,50)		
	    
	pygame.draw.rect(screen,white,(39*scale_a,19*scale_b,1292*scale_a,62*scale_b))	
	
	pygame.draw.rect(screen,white,(39*scale_a,89*scale_b,1292*scale_a,552*scale_b))
	pygame.draw.rect(screen,black,(38*scale_a,88*scale_b,1294*scale_a,554*scale_b),2)
	
	pygame.draw.rect(screen,white,(39*scale_a,649*scale_b,1292*scale_a,82*scale_b))
	pygame.draw.rect(screen,black,(38*scale_a,648*scale_b,1294*scale_a,84*scale_b),2)
	
	#scrolling txt
	font_color_scroll = (5,5,5)
	font_1_display = font_2.render((scrolling_txt), True,font_color_scroll)		    
	screen.blit(font_1_display, [((int(scroll_pos[4])*scale_a)),(int(23*scale_b))]) 
	scroll_pos[4] = ( int(scroll_pos[4]) - 1)
	
	
	if scroll_pos[4] < (int(- int(scroll_pos[2]) - (len(scrolling_txt)+1120))*scale_a):
	    scroll_pos[4] = ((int(scroll_pos[2]) + 300) * scale_a)
	
	pygame.draw.rect(screen,background_color,(0*scale_a,0*scale_b,40*scale_a,85*scale_b))	
	pygame.draw.rect(screen,background_color,(1333*scale_a,0*scale_b,40*scale_a,85*scale_b))
	pygame.draw.rect(screen,black,(38*scale_a,18*scale_b,1294*scale_a,64*scale_b),2)	
	if login_stage[1] == '1':
	    
	    pygame.draw.rect(screen,gray,(389*scale_a,109*scale_b,592*scale_a,582*scale_b))	
	    pygame.draw.rect(screen,black,(388*scale_a,108*scale_b,594*scale_a,584*scale_b),2)
	    if osversion == 'MS Windows':
		screen.blit(background_5a,(int(850*scale_a),int(590*scale_b))) #os logo
	    else:
		screen.blit(background_5a,(int(900*scale_a),int(580*scale_b))) #os logo
		
	    pygame.draw.rect(screen,white,(489*scale_a,269*scale_b,392*scale_a,42*scale_b))	
	    pygame.draw.rect(screen,black,(488*scale_a,268*scale_b,394*scale_a,44*scale_b),1)
	    
		    
	    font_1_display = font_1.render("Login",True,font_color)
	    screen.blit(font_1_display, [int(489*scale_a),int(200*scale_b)]) 
	    font_1_display = font_1.render(">> ",True,font_color)
	    screen.blit(font_1_display, [int(500*scale_a),int(265*scale_b)]) 
	    if login_stage[2] == '1':
		font_color_user_name = (20,205,0)			
	    font_1_display = font_1.render((user_name), True,font_color_user_name)
	    screen.blit(font_1_display, [int(530*scale_a),int(268*scale_b)]) 
	    
	if login_stage[1] == '1' and login_stage[2] == '1': 
	    
	    pygame.draw.rect(screen,white,(489*scale_a,399*scale_b,392*scale_a,42*scale_b))	
	    pygame.draw.rect(screen,black,(488*scale_a,398*scale_b,394*scale_a,44*scale_b),1)
	    
	    font_1_display = font_1.render("Password",True,font_color)
	    screen.blit(font_1_display, [int(489*scale_a),int(330*scale_b)]) 
	    font_1_display = font_1.render(">> ",True,font_color)
	    screen.blit(font_1_display, [int(500*scale_a),int(395*scale_b)]) 
	    font_color_password = (0,0,0)
	    font_1_display = font_1.render((user_password_secu), True,font_color_password)
	    screen.blit(font_1_display, [int(530*scale_a),int(405*scale_b)]) 		    
	    user_password_secu
	    
	if login_stage[1] == '1' and login_stage[2] == '1' and login_stage[3] == '1' and login_stage[4] != 'sql_error' and login_stage[4] != 'sql_password_error': 
	
	    try: 
		mysql_ip = '79.97.123.177'
		mysql_port = '3306'
		print ('\n>> Connecting to MySQL... ')
		cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
		print ('>> Connected...\n') 
		login_stage[1] = '0'
		login_stage[2] = '0'
		login_stage[3] = '0'
		login_stage[4] = 'sql_ok'
		user_name = ''
		user_password = ''		    
		
	    except mysql.connector.Error as err:
		login_stage[4] = 'sql_error'
		
		print ('>> MySQL database error...\n')
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		    login_stage[4] = 'sql_password_error'	
		    print(">> Something is wrong with your user name or password\n")
		else:
		    print(err)
		print ('>> Program will be terminated\n')
    
	if login_stage[4] == 'sql_error': 
		
	    font_1_display = font_1.render("Database is not accessible",True,font_color)
	    screen.blit(font_1_display, [int(415*scale_a),int(480*scale_b)])
	    font_1_display = font_1.render("Mouse click to continue...",True,font_color)
	    screen.blit(font_1_display, [int(415*scale_a),int(540*scale_b)])		    
	    
	    
	elif login_stage[4] == 'sql_password_error':
	    font_1_display = font_1.render("Something is wrong with User_Name or Password",True,font_color)
	    screen.blit(font_1_display, [int(415*scale_a),int(480*scale_b)])	
	    font_1_display = font_1.render("Mouse click to continue...",True,font_color)
	    screen.blit(font_1_display, [int(415*scale_a),int(540*scale_b)])		    
       
       
	
	    
	pygame.display.flip()      
	clock.tick(clock_tick)	
	