#!/usr/bin/python 

from __future__ import print_function
from sys import *
import time 
import subprocess
from socket import *
import re
import os #find home folder universal link
from random import randint
import datetime #import time for milisecond time stamp
import sys #import linux sys module

sql_DB_name = "dcare"
TABLES = {} #mysql
os_version = []
home_folder = os.getenv('HOME')    
if platform == "linux" or platform == "linux2":            
    osversion = 'Linux'  
    import lsb_release
    os_ver = lsb_release.get_lsb_information()
    a,b = ("os_ver['DESCRIPTION']: ",  os_ver['DESCRIPTION'])
    os_version.append(b)
    c,d = ("os_ver['CODENAME']: ", os_ver['CODENAME'])
    os_version.append(d)    
else:
    osversion = 'MS Windows' 
    if str(sys.getwindowsversion()[0]) == '6':
	print (sys.getwindowsversion()[0])
	os_version.append("8 or 8.1 or 10")    
	os_version.append("32/64 Bit")
    else:
	os_version.append("XP or Vista or 7")    
	os_version.append("32/64 Bit")	
	
    import platform
    print (platform.platform())    
try:
    import mysql.connector
    from mysql.connector import errorcode     
    print ('MySQL connector OK\n')  
    program = 'start'
except:    
    print ('MySQL connector is not installed!!')
    program = 'stop'    

def init_setup():
    os.system('cls' if os.name == 'nt' else 'clear')  
    def get_ip():
        s = socket(AF_INET, SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 0))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    ip_discover = get_ip()
    
       
    print ('----------------------------------------------')  
    print (">> MSc Doctors Care System\n>> MySQL Admin Pannel, AIT 2016/2017")
    print (">> Machine IP Addr "+ip_discover)
    print ('>> OS = '+osversion+' '+os_version[0]+' - '+os_version[1])
    print ('----------------------------------------------\n')  

   
def test_module(program):
    
    if program == "start":
	mysql_ip = raw_input ("Input MySQL Server IP Address (remote = 79.97.123.177): ")
	if mysql_ip == "":
	    mysql_ip = "192.168.100.10"
	    print ("Go with default IP Address: "+mysql_ip)
	mysql_port = raw_input ("Input MySQL Server Port Number (3306): ")
	if mysql_port == "":
		mysql_port = "3306"  
		print ("Go with default Port Number")
	mysql_ip_user_name_action = "true"
	while mysql_ip_user_name_action == "true":
	    mysql_ip_user_name = raw_input ("Input MySQL Server User Name: ")
	    if mysql_ip_user_name == "":
			mysql_ip_user_name = "Doctors_Care"   
	    if len(mysql_ip_user_name) < 6:
		print ("Server User Name is to short")
	    else:
		mysql_ip_user_name_action = "false"
	mysql_password_action = "true"
	while  mysql_password_action == "true":
	    mysql_password = raw_input ("Input MySQL Server Password: ") 
	    if mysql_password == "":
		mysql_password = "MSc_2017" 	    
	    if len(mysql_password) < 6:
		print ("Server Password is to short must be greater than 6")
	    else:
		mysql_password_action = "false"
		
	print ("\n-> User Name: "+mysql_ip_user_name)
	print ("-> Password: "+mysql_password)
	print ("-> IP Address: "+mysql_ip)
	print ("-> Server Port: "+mysql_port)
		
	try: 
	    print ('\n>> Connecting to MySQL... ')
	    cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	    print ('>> Connected...\n')        
	except mysql.connector.Error as err:
	    print ('>> MySQL database error...\n')
	    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print(">> Something is wrong with your user name or password\n")
	    else:
		print(err)
	    print ('>> Program will be terminated\n')
	    exit()	    
	else:	    
	    def backup_sql_users():
		
		DB_NAME_Backup = 'Database_User_Name_Backup'		
		TABLES['mysql_user_list_backup'] = (
		    "CREATE TABLE `mysql_user_list_backup` ("
		    "  `user_backup_id` int(2) NOT NULL AUTO_INCREMENT,"
		    "  `user_backup_name` Varchar(40) NOT NULL,"
		    "  `info_1` varchar(20) NOT NULL,"
		    "  `info_2` varchar(20) NOT NULL,"
		    "  PRIMARY KEY (`user_backup_id`)"
                    ") ENGINE=InnoDB")  
		
		cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
		try:
		    cursor = cnx.cursor()	    
		    cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME_Backup))
		    print (">> Database '"+DB_NAME_Backup+"' created")
		    cnx.database = DB_NAME_Backup  
		    for name, ddl in TABLES.iteritems():
			try:
			    print(">> Creating table '{}': ".format(name), end='')
			    cursor.execute(ddl)
			except mysql.connector.Error as err:
			    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
				print(">> already exists.")
			    else:
				print(err.msg) 		    
			else:
			    print ('>>  OK!')   
			    
		    cursor.execute("""SELECT * from information_schema.user_privileges GROUP BY GRANTEE HAVING COUNT(*) >=1""")		
		    rows = cursor.fetchall()
		    for row in rows:
			print (row[0])
			info_1 = '---empty---'
			info_2 = '---empty---'
			user_backup_name = (row[0])
			
			add_log = ("INSERT INTO Database_User_Name_Backup.mysql_user_list_backup"
			        "(user_backup_name, info_1, info_2)"
			        "VALUES (%s, %s, %s)")	
			add_log_1 = ((user_backup_name, info_1, info_2))
			cursor.execute(add_log, add_log_1)
			rule_mac_id = cursor.lastrowid            
			cnx.commit()				
			
		except:
		    pass
		    
	    def create_database():
		cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
		cursor = cnx.cursor()
		DB_NAME = (sql_DB_name)
		TABLES['GP_list'] = (
                    "CREATE TABLE `GP_list` ("
                    "  `GP_ID` int(2) NOT NULL AUTO_INCREMENT,"
                    "  `GP_name` varchar(20) NOT NULL,"
                    "  `GP_DOB` varchar(20) NOT NULL,"
                    "  `GP_Address` varchar(36) NOT NULL,"
                    "  `GP_user_name` varchar(20) NOT NULL,"
                    "  `GP_Password` varchar(20) NOT NULL,"
                    "  `GP_email` varchar(30) NOT NULL,"
                    "  `GP_phone` varchar(36) NOT NULL,"
                    "  `GP_Specialisation` varchar(16) NOT NULL,"
                    "  PRIMARY KEY (`GP_ID`)"
                    ") ENGINE=InnoDB")  
		
		TABLES['Pharmacist_list'] = (
                    "CREATE TABLE `Pharmacist_list` ("
                    "  `Pharmacist_ID` int(2) NOT NULL AUTO_INCREMENT,"
                    "  `Pharmacist_name` varchar(20) NOT NULL,"
                    "  `Pharmacist_DOB` varchar(20) NOT NULL,"
                    "  `Pharmacist_Address` varchar(36) NOT NULL,"
                    "  `Pharmacist_user_name` varchar(20) NOT NULL,"
                    "  `Pharmacist_Password` varchar(20) NOT NULL,"
                    "  `Pharmacist_email` varchar(30) NOT NULL,"
                    "  `Pharmacist_phone` varchar(36) NOT NULL,"
                    "  `Pharmacist_Specialisation` varchar(16) NOT NULL,"
                    "  PRIMARY KEY (`Pharmacist_ID`)"
                    ") ENGINE=InnoDB")    
		
		TABLES['OMS_list'] = (
                    "CREATE TABLE `OMS_list` ("
                    "  `OMS_ID` int(2) NOT NULL AUTO_INCREMENT,"
                    "  `OMS_name` varchar(20) NOT NULL,"
                    "  `OMS_DOB` varchar(20) NOT NULL,"
                    "  `OMS_Address` varchar(36) NOT NULL,"
                    "  `OMS_user_name` varchar(20) NOT NULL,"
                    "  `OMS_Password` varchar(20) NOT NULL,"
                    "  `OMS_email` varchar(30) NOT NULL,"
                    "  `OMS_phone` varchar(36) NOT NULL,"
                    "  `OMS_Specialisation` varchar(16) NOT NULL,"
                    "  PRIMARY KEY (`OMS_ID`)"
                    ") ENGINE=InnoDB")  
		
		TABLES['Patients_list'] = (
                    "CREATE TABLE `Patients_list` ("
                    "  `patient_ID` int(2) NOT NULL AUTO_INCREMENT,"
                    "  `patient_name` Varchar(20) NOT NULL,"
                    "  `patient_DOB` Varchar(20) NOT NULL,"
                    "  `patient_address` Varchar(40) NOT NULL,"
                    "  `patient_phone` Varchar(20) NOT NULL,"
                    "  `patient_user_name` Varchar(20) NOT NULL,"
                    "  `patient_password` varchar(20) NOT NULL,"
                    "  `patient_emergency_id` varchar(20) NOT NULL,"
                    "  `info_1` varchar(20) NOT NULL,"
                    "  `info_2` varchar(20) NOT NULL,"
                    "  PRIMARY KEY (`patient_id`)"
                    ") ENGINE=InnoDB")  
		
		cursor = cnx.cursor()
		cursor.execute ("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'Doctors_Care_database_Test'") 
		rows = cursor.fetchall()
		database_empty = (len(rows))
		if database_empty != 0:
		    decission_msql_delete = raw_input ("Would You like to delete default Database: '"+DB_NAME+"' (y/n) ")
		    if decission_msql_delete == "y" or decission_msql_delete == "Y":
			confirmation_msql_delete = raw_input ("Are You sure?, All data will be lost (y/n) ")
			if confirmation_msql_delete == "y" or confirmation_msql_delete == "Y":
			    decission_msql_delete_password = raw_input ("Input Admin password: ")
			    if mysql_password == decission_msql_delete_password:
				
				try:
				    cursor.execute("DROP DATABASE IF EXISTS "+DB_NAME)
				    print ('>> Deleted...')
				    
				    cursor.execute("""SELECT * from information_schema.user_privileges GROUP BY GRANTEE HAVING COUNT(*) >=1""")		
				    rows = cursor.fetchall()
				    for row in rows:
					info_1 = '---empty---'
					info_2 = '---empty---'
					user_backup_name_list = (row[0])	
					
					cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
					cursor = cnx.cursor()	
					cursor.execute("""SELECT count(Database_User_Name_Backup.mysql_user_list_backup.user_backup_name)
					from Database_User_Name_Backup.mysql_user_list_backup
					WHERE Database_User_Name_Backup.mysql_user_list_backup.user_backup_name=%s""",(user_backup_name_list, ))		
					rows = cursor.fetchall()
					for row in rows:
					    user_names_in_DB = row[0]	
					if user_names_in_DB == 1:
					    pass
					else:
					    command_sql = ("DROP USER "+ (user_backup_name_list))
					    cursor.execute(command_sql)
				except:
				    pass
			    else:
				print ("wrong password -> delete procedure terminated...")		    
		try:
		    cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
		    print (">> Database '"+DB_NAME+"' created")
		except:
		    print ("\n>> Database name: '"+DB_NAME+"' exist, continue...")
		    
		cnx.database = DB_NAME   
		for name, ddl in TABLES.iteritems():
		    try:
			print(">> Creating table '{}': ".format(name), end='')
			cursor.execute(ddl)
		    except mysql.connector.Error as err:
			if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
			    print(">> already exists.")
			else:
			    print(err.msg) 		    
		    else:
			print ('>>  OK!')    	
		
	    backup_sql_users()	    
	    create_database()
	    
    print("\n")
    time.sleep(5) 
    return(mysql_ip_user_name, mysql_password, mysql_ip, mysql_port)
    
def input_admin_gp(program):
    
    print ("\n-----------------------\nGP options\n")
    print ("1. Add new GP")
    print ("2. Delete existing GP")
    print ("3. Info about GP")
    print ("4. Exit to main menu\n------------------------")
    admin_decission = raw_input ("\nYours Choice (1 - 4)? ")
    if admin_decission == "1":	
	print ('\n>>> Add New GP <<<\n')
	gp_name = raw_input ("Enter GP full name ")
	gp_DOB = raw_input ("Enter GP Date of Birth ")
	gp_address = raw_input ("Enter GP Address ")
	enter_user_name_DB = 'true'
	while enter_user_name_DB == 'true':
	    gp_user_name = raw_input ("Enter GP user_name ")
	    cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	    cursor = cnx.cursor()	
	    cursor.execute("""SELECT count(doctors_care_database_test.gp_list.GP_user_name)
		            from doctors_care_database_test.gp_list
		            WHERE doctors_care_database_test.gp_list.GP_user_name=%s""",(gp_user_name, ))		
	    rows = cursor.fetchall()
	    for row in rows:
		user_names_in_DB = row[0]	
	    if user_names_in_DB == 0:
		print ("User_name Unique -> Ok!")
		enter_user_name_DB = 'false'
	    else:
		print ("User_name exist in the Doctors Care system!!")	
	gp_password = raw_input ("Enter GP password ")
	gp_email = raw_input ("Enter GP e-mail ")
	gp_phone_num = raw_input ("Enter GP phone number ")	
	gp_specialisation = raw_input ("Enter GP specialisation ")
	add_log = ("INSERT INTO doctors_care_database_test.gp_list"
	           "(GP_name, GP_DOB, GP_Address, GP_user_name, GP_Password, GP_email, GP_phone, GP_Specialisation)"
	           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")	
	add_log_1 = ((gp_name), (gp_DOB), (gp_address), (gp_user_name), (gp_password), (gp_email),(gp_phone_num ), (gp_specialisation) )
	print ('Adding to database...')
	cursor.execute(add_log, add_log_1)
	rule_mac_id = cursor.lastrowid            
	cnx.commit()
	
	part_B = str('%')
	part_A = ("GRANT ALL PRIVILEGES ON doctors_care_database_test.patients_list TO '"+gp_user_name+"'@'"+ part_B+"' IDENTIFIED BY '"+gp_password+"'")
	print ('Added a grant to accesss to patient table')
	cursor.execute(part_A)
	cursor.execute("FLUSH PRIVILEGES")	
	
	part_B = str('%')
	part_A = ("GRANT ALL PRIVILEGES ON doctors_care_database_test.GP_list TO '"+gp_user_name+"'@'"+ part_B+"' IDENTIFIED BY '"+gp_password+"'")
	print ('Add a grant to accesss to GP table')
	cursor.execute(part_A)
	cursor.execute("FLUSH PRIVILEGES")	
	gp_confirm = raw_input ("Completed. Enter to continue... ")
	
    elif admin_decission == "2":
	print ('\n>>> Delete Existing GP <<<\n')
	gp_user_name = raw_input ("Enter GP user_name ")
	cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	cursor = cnx.cursor()	
	cursor.execute("""SELECT count(doctors_care_database_test.gp_list.GP_user_name)
                                from doctors_care_database_test.gp_list
                                WHERE doctors_care_database_test.gp_list.GP_user_name=%s""",(gp_user_name, ))		
	rows = cursor.fetchall()
	for row in rows:
	    user_names_in_DB = row[0]	
	if user_names_in_DB == 1:
	    gp_name = raw_input ("Enter GP full name ")
	    
	    cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	    cursor = cnx.cursor()	
	    cursor.execute("""SELECT count(doctors_care_database_test.gp_list.GP_name)
                                    from doctors_care_database_test.gp_list
                                    WHERE doctors_care_database_test.gp_list.GP_name=%s""",(gp_name, ))		
	    rows = cursor.fetchall()
	    for row in rows:
		user_names_in_DB = row[0]
		
	    if user_names_in_DB > 0:		
		decission_GP_delete_password = raw_input ("Input Admin password: ")
		if mysql_password == decission_GP_delete_password:
		    cursor.execute("""delete from doctors_care_database_test.gp_list where doctors_care_database_test.gp_list.GP_user_name=%s""",(gp_user_name, ))
		    cnx.commit()
		    aaa = raw_input (gp_user_name+" Deleted... Enter ")
		    
		    command_sql = ("DROP USER "+ (gp_user_name))
		    cursor.execute(command_sql)		    
		else:
		    aaa = raw_input ("Password problem - action terminated... ")
	    else:
		aaa = raw_input ("Wrong Full name - process terminated... Enter ")
	else:
	    aaa = raw_input  ("User_name non exist in the Doctors Care system!!")
	
    elif admin_decission == "3":
	gp_name = raw_input ("Enter GP full name or user_name ")
	cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	cursor = cnx.cursor()	
	cursor.execute("""SELECT count(doctors_care_database_test.gp_list.GP_name)
                                        from doctors_care_database_test.gp_list
                                        WHERE doctors_care_database_test.gp_list.GP_name=%s""",(gp_name, ))	
	rows = cursor.fetchall()
	for row in rows:
	    user_names_in_DB = row[0]	    
	if user_names_in_DB > 0:
	    print ('')	    
	    cursor.execute("""SELECT *
	                    from doctors_care_database_test.gp_list
	                    WHERE doctors_care_database_test.gp_list.GP_name=%s""",(gp_name, ))
	    rows = cursor.fetchall()
	    cursor.close()
	    cnx.close()	      
	     
	    log_row_1 = rows   	    
	    for x in range(len(log_row_1)):		
		print (log_row_1[x])	    
	    admin_decission = raw_input ('\n(Enter to continue...)')
	elif user_names_in_DB == 0: 
	    cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	    cursor = cnx.cursor()	
	    cursor.execute("""SELECT count(doctors_care_database_test.gp_list.GP_user_name)
	                    from doctors_care_database_test.gp_list
	                    WHERE doctors_care_database_test.gp_list.GP_user_name=%s""",(gp_name, ))	
	    rows = cursor.fetchall()
	    for row in rows:
		user_names_in_DB = row[0]	    
	    if user_names_in_DB == 1:
		print ('')	    
		cursor.execute("""SELECT *
	                        from doctors_care_database_test.gp_list
	                        WHERE doctors_care_database_test.gp_list.GP_user_name=%s""",(gp_name, ))
		rows = cursor.fetchall()
		cursor.close()
		cnx.close()
		log_row_1 = rows[0] 
		print (log_row_1)
		admin_decission = raw_input ('\n(Enter to continue...)')
	    else:
		admin_decission = raw_input ('\nno in the system '+gp_name)
		admin_decission = raw_input ("\nCan't find "+gp_name+" in the system. ")
    elif admin_decission == "4":
	program = 'stop'	
    else:
	admin_decission = raw_input ('\nWrong choice!, Try again!! (Enter to continue...)')
    return (program)

def input_admin_pharmacist(program):
    
    print ("\n-----------------------\nPharmacist options\n")
    print ("1. Add new Pharmacist")
    print ("2. Delete existing Pharmacist")
    print ("3. Info about Pharmacist")
    print ("4. Exit to main menu\n------------------------")
    admin_decission = raw_input ("\nYours Choice (1 - 4)? ")
    if admin_decission == "1":	
	print ('\n>>> Add New Pharmacist <<<\n')
	Pharmacist_name = raw_input ("Enter Pharmacist full name ")
	Pharmacist_DoB = raw_input ("Enter Pharmacist date of birth ")
	Pharmacist_address = raw_input ("Enter Pharmacist Address ")
	enter_user_name_DB = 'true'
	while enter_user_name_DB == 'true':
	    Pharmacist_user_name = raw_input ("Enter Pharmacist user_name ")
	    cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	    cursor = cnx.cursor()	
	    cursor.execute("""SELECT count(doctors_care_database_test.Pharmacist_list.Pharmacist_user_name)
		            from doctors_care_database_test.Pharmacist_list
		            WHERE doctors_care_database_test.Pharmacist_list.Pharmacist_user_name=%s""",(Pharmacist_user_name, ))		
	    rows = cursor.fetchall()
	    for row in rows:
		user_names_in_DB = row[0]	
	    if user_names_in_DB == 0:
		print ("User_name Unique -> Ok!")
		enter_user_name_DB = 'false'
	    else:
		print ("User_name exist in the Doctors Care system!!")	
	Pharmacist_password = raw_input ("Enter Pharmacist password ")
	Pharmacist_email = raw_input ("Enter Pharmacist e-mail ")
	Pharmacist_phone_num = raw_input ("Enter Pharmacist phone number ")	
	Pharmacist_specialisation = raw_input ("Enter Pharmacist specialisation ")
	add_log = ("INSERT INTO doctors_care_database_test.Pharmacist_list"
	           "(Pharmacist_name, Pharmacist_DOB, Pharmacist_Address, Pharmacist_user_name, Pharmacist_Password, Pharmacist_email, Pharmacist_phone, Pharmacist_Specialisation)"
	           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")	
	add_log_1 = ((Pharmacist_name), (Pharmacist_DoB), (Pharmacist_address), (Pharmacist_user_name), (Pharmacist_password), (Pharmacist_email), (Pharmacist_phone_num ), (Pharmacist_specialisation) )
	print ('Adding...')
	cursor.execute(add_log, add_log_1)
	rule_mac_id = cursor.lastrowid            
	cnx.commit()	
	
	part_B = str('%')
	part_A = ("GRANT ALL PRIVILEGES ON doctors_care_database_test.patients_list TO '"+Pharmacist_user_name+"'@'"+ part_B+"' IDENTIFIED BY '"+Pharmacist_password+"'")
	print ('Added a grant to accesss to patient table')
	cursor.execute(part_A)
	cursor.execute("FLUSH PRIVILEGES")	
	Pharmacist_confirm = raw_input ("Completed... Enter to continue... ")
	
    elif admin_decission == "2":
	print ('\n>>> Delete Existing Pharmacist <<<\n')
	Pharmacist_user_name = raw_input ("Enter Pharmacist user_name ")
	cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	cursor = cnx.cursor()	
	cursor.execute("""SELECT count(doctors_care_database_test.Pharmacist_list.Pharmacist_user_name)
                                from doctors_care_database_test.Pharmacist_list
                                WHERE doctors_care_database_test.Pharmacist_list.Pharmacist_user_name=%s""",(Pharmacist_user_name, ))		
	rows = cursor.fetchall()
	for row in rows:
	    user_names_in_DB = row[0]	
	if user_names_in_DB == 1:
	    Pharmacist_name = raw_input ("Enter Pharmacist full name ")
	    
	    cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	    cursor = cnx.cursor()	
	    cursor.execute("""SELECT count(doctors_care_database_test.Pharmacist_list.Pharmacist_name)
                                    from doctors_care_database_test.Pharmacist_list
                                    WHERE doctors_care_database_test.Pharmacist_list.Pharmacist_name=%s""",(Pharmacist_name, ))		
	    rows = cursor.fetchall()
	    for row in rows:
		user_names_in_DB = row[0]
	    if user_names_in_DB > 0:		
		decission_Pharmacist_delete_password = raw_input ("Input Admin password: ")
		if mysql_password == decission_Pharmacist_delete_password:
		    cursor.execute("""delete from doctors_care_database_test.Pharmacist_list where doctors_care_database_test.Pharmacist_list.Pharmacist_user_name=%s""",(Pharmacist_user_name, ))
		    cnx.commit()
		    aaa = raw_input (Pharmacist_user_name+" Deleted... Enter ")
		else:
		    aaa = raw_input ("Password problem - action terminated... ")
	    else:
		aaa = raw_input ("Wrong Full name - process terminated... Enter ")
	else:
	    aaa = raw_input  ("User_name non exist in the Doctors Care system!!")
	
    elif admin_decission == "3":
	Pharmacist_name = raw_input ("Enter Pharmacist full name or user_name ")
	cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	cursor = cnx.cursor()	
	cursor.execute("""SELECT count(doctors_care_database_test.Pharmacist_list.Pharmacist_name)
                                        from doctors_care_database_test.Pharmacist_list
                                        WHERE doctors_care_database_test.Pharmacist_list.Pharmacist_name=%s""",(Pharmacist_name, ))	
	rows = cursor.fetchall()
	for row in rows:
	    user_names_in_DB = row[0]	    
	if user_names_in_DB > 0:
	    print ('')	    
	    cursor.execute("""SELECT *
	                    from doctors_care_database_test.Pharmacist_list
	                    WHERE doctors_care_database_test.Pharmacist_list.Pharmacist_name=%s""",(Pharmacist_name, ))
	    rows = cursor.fetchall()
	    cursor.close()
	    cnx.close()	      
	     
	    log_row_1 = rows   	    
	    for x in range(len(log_row_1)):		
		print (log_row_1[x])	    
	    admin_decission = raw_input ('\n(Enter to continue...)')
	elif user_names_in_DB == 0: 
	    cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	    cursor = cnx.cursor()	
	    cursor.execute("""SELECT count(doctors_care_database_test.Pharmacist_list.Pharmacist_user_name)
	                    from doctors_care_database_test.Pharmacist_list
	                    WHERE doctors_care_database_test.Pharmacist_list.Pharmacist_user_name=%s""",(Pharmacist_name, ))	
	    rows = cursor.fetchall()
	    for row in rows:
		user_names_in_DB = row[0]	    
	    if user_names_in_DB == 1:
		print ('')	    
		cursor.execute("""SELECT *
	                        from doctors_care_database_test.Pharmacist_list
	                        WHERE doctors_care_database_test.Pharmacist_list.Pharmacist_user_name=%s""",(Pharmacist_name, ))
		rows = cursor.fetchall()
		cursor.close()
		cnx.close()
		log_row_1 = rows[0] 
		print (log_row_1)
		admin_decission = raw_input ('\n(Enter to continue...)')
	    else:
		admin_decission = raw_input ("\nCan't find "+Pharmacist_name+" in the system. ")
    elif admin_decission == "4":
	program = 'stop'	
    else:
	admin_decission = raw_input ('\nWrong choice!, Try again!! (Enter to continue...)')
    return (program)

def input_admin_oms(program):
    
    print ("\n-----------------------\nOther Medical Staff (OMS) options\n")
    print ("1. Add new OMS")
    print ("2. Delete existing OMS")
    print ("3. Info about OMS")
    print ("4. Exit to main menu\n------------------------")
    admin_decission = raw_input ("\nYours Choice (1 - 4)? ")
    if admin_decission == "1":	
	print ('\n>>> Add New OMS <<<\n')
	OMS_name = raw_input ("Enter OMS full name ")
	OMS_DOB = raw_input ("Enter OMS date of birth ")
	OMS_address = raw_input ("Enter OMS Address ")
	enter_user_name_DB = 'true'
	while enter_user_name_DB == 'true':
	    OMS_user_name = raw_input ("Enter OMS user_name ")
	    cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	    cursor = cnx.cursor()	
	    cursor.execute("""SELECT count(doctors_care_database_test.OMS_list.OMS_user_name)
		            from doctors_care_database_test.OMS_list
		            WHERE doctors_care_database_test.OMS_list.OMS_user_name=%s""",(OMS_user_name, ))		
	    rows = cursor.fetchall()
	    for row in rows:
		user_names_in_DB = row[0]	
	    if user_names_in_DB == 0:
		print ("User_name Unique -> Ok!")
		enter_user_name_DB = 'false'
	    else:
		print ("User_name exist in the Doctors Care system!!")	
	OMS_password = raw_input ("Enter OMS password ")
	OMS_email = raw_input ("Enter OMS e-mail ")
	OMS_phone_num = raw_input ("Enter OMS phone number ")	
	OMS_specialisation = raw_input ("Enter OMS specialisation ")	
	print ('Adding...')
	add_log = ("INSERT INTO doctors_care_database_test.OMS_list"
	           "(OMS_name, OMS_DOB, OMS_Address, OMS_user_name, OMS_Password, OMS_email, OMS_phone, OMS_Specialisation)"
	           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")	
	add_log_1 = ((OMS_name), (OMS_DOB), (OMS_address), (OMS_user_name), (OMS_password), (OMS_email),(OMS_phone_num ), (OMS_specialisation) )	   
	cursor.execute(add_log, add_log_1)
	rule_mac_id = cursor.lastrowid            
	cnx.commit()	
	OMS_confirm = raw_input ("Completed... Enter to continue... ")	
    elif admin_decission == "2":
	print ('\n>>> Delete Existing OMS <<<\n')
	OMS_user_name = raw_input ("Enter OMS user_name ")
	cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	cursor = cnx.cursor()	
	cursor.execute("""SELECT count(doctors_care_database_test.OMS_list.OMS_user_name)
                                from doctors_care_database_test.OMS_list
                                WHERE doctors_care_database_test.OMS_list.OMS_user_name=%s""",(OMS_user_name, ))		
	rows = cursor.fetchall()
	for row in rows:
	    user_names_in_DB = row[0]	
	if user_names_in_DB == 1:
	    OMS_name = raw_input ("Enter OMS full name ")
	    
	    cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	    cursor = cnx.cursor()	
	    cursor.execute("""SELECT count(doctors_care_database_test.OMS_list.OMS_name)
                                    from doctors_care_database_test.OMS_list
                                    WHERE doctors_care_database_test.OMS_list.OMS_name=%s""",(OMS_name, ))		
	    rows = cursor.fetchall()
	    for row in rows:
		user_names_in_DB = row[0]
	    if user_names_in_DB > 0:		
		decission_OMS_delete_password = raw_input ("Input Admin password: ")
		if mysql_password == decission_OMS_delete_password:
		    cursor.execute("""delete from doctors_care_database_test.OMS_list where doctors_care_database_test.OMS_list.OMS_user_name=%s""",(OMS_user_name, ))
		    cnx.commit()
		    aaa = raw_input (OMS_user_name+" Deleted... Enter ")
		else:
		    aaa = raw_input ("Password problem - action terminated... ")
	    else:
		aaa = raw_input ("Wrong Full name - process terminated... Enter ")
	else:
	    aaa = raw_input  ("User_name non exist in the Doctors Care system!!")
	
    elif admin_decission == "3":
	OMS_name = raw_input ("Enter OMS full name or user_name ")
	cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	cursor = cnx.cursor()	
	cursor.execute("""SELECT count(doctors_care_database_test.OMS_list.OMS_name)
                                        from doctors_care_database_test.OMS_list
                                        WHERE doctors_care_database_test.OMS_list.OMS_name=%s""",(OMS_name, ))	
	rows = cursor.fetchall()
	for row in rows:
	    user_names_in_DB = row[0]	    
	if user_names_in_DB > 0:
	    print ('')	    
	    cursor.execute("""SELECT *
	                    from doctors_care_database_test.OMS_list
	                    WHERE doctors_care_database_test.OMS_list.OMS_name=%s""",(OMS_name, ))
	    rows = cursor.fetchall()
	    cursor.close()
	    cnx.close()	   
	    log_row_1 = rows   	    
	    for x in range(len(log_row_1)):		
		print (log_row_1[x])	    
	    admin_decission = raw_input ('\n(Enter to continue...)')
	elif user_names_in_DB == 0: 
	    cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	    cursor = cnx.cursor()	
	    cursor.execute("""SELECT count(doctors_care_database_test.OMS_list.OMS_user_name)
	                    from doctors_care_database_test.OMS_list
	                    WHERE doctors_care_database_test.OMS_list.OMS_user_name=%s""",(OMS_name, ))	
	    rows = cursor.fetchall()
	    #giving a number /0 when mac not exist in host mac table, or 1 otherwise
	    for row in rows:
		user_names_in_DB = row[0]	    
	    if user_names_in_DB == 1:
		print ('')	    
		cursor.execute("""SELECT *
	                        from doctors_care_database_test.OMS_list
	                        WHERE doctors_care_database_test.OMS_list.OMS_user_name=%s""",(OMS_name, ))
		rows = cursor.fetchall()
		cursor.close()
		cnx.close()
		log_row_1 = rows[0] 
		print (log_row_1)
		admin_decission = raw_input ('\n(Enter to continue...)')
	    else:
		admin_decission = raw_input ("\nCan't find "+OMS_name+" in the system. ")
    elif admin_decission == "4":
	program = 'stop'	
    else:
	admin_decission = raw_input ('\nWrong choice!, Try again!! (Enter to continue...)')
    return (program)

def input_admin_options(program):
    
    print ("\n-----------------------\nAdministration options\n")
    print ("1. Display all users")
    print ("2. Display tables")
    print ("3. Other functions")
    print ("4. Exit to main menu\n------------------------")
    admin_decission = raw_input ("\nYours Choice (1 - 4)? ")
    if admin_decission == "1":	
	print ('\n>>> Database User names <<<\n')
	
	cnx = mysql.connector.connect(user=(mysql_ip_user_name), password=(mysql_password), host=(mysql_ip), port=(mysql_port))
	cursor = cnx.cursor()	
	cursor.execute("""SELECT * from information_schema.user_privileges GROUP BY GRANTEE HAVING COUNT(*) >=1""")		
	rows = cursor.fetchall()
	for row in rows:
	    print (row[0])
	admin_decission = raw_input ("\nEnter ")	
def input_admin(program):    
    print ("-----------------------\nAdmin options\n")
    print ("1. GP -> add, del, disp")
    print ("2. Pharmacist -> add, del, disp")
    print ("3. Other Medical Staff")
    print ("4. Administration options")
    print ("5. Exit from Doctors Care admin panel\n\n------------------------")
    admin_decission = raw_input ("\nYours Choice (1 - 5)? ")
    if admin_decission == "1":
	program = input_admin_gp(program)
    elif admin_decission == "2":
	program = input_admin_pharmacist(program)   
    elif admin_decission == "3":
	program = input_admin_oms(program)   	
    elif admin_decission == "4":
	    program = input_admin_options(program)
    elif admin_decission == "5":
	program = 'stop'
	return (program)
	    
if program != 'stop':
    init_setup()
    mysql_ip_user_name, mysql_password, mysql_ip, mysql_port = test_module(program)
    while program != 'stop':
	init_setup()
	program = input_admin(program)
else:
    Pharmacist_confirm = raw_input ("Terminating... Enter to continue... ")	
print ('\n')