
import requests
import json
import csv
import numpy as np
import sqlite3
from decimal import Decimal
np.set_printoptions(edgeitems=200)

conn = sqlite3.connect(':memory:')
c = conn.cursor()



c.execute("""CREATE TABLE OPR_DPR_CCWM_Calculations (
						team_number integer,
						OPR real,
						DPR real,
						CCWM real
						)""")




def insert_values_into_table(team_number,OPR,DPR,CCWM):
	with conn: #executing the statement from this context manager means that we don't have to commit after each execution
		c.execute("INSERT INTO OPR_DPR_CCWM_Calculations VALUES (:team_number, :OPR, :DPR, :CCWM)", {'team_number': team_number, 'OPR': OPR, 'DPR': DPR, 'CCWM': CCWM})

#_____________________________________________________ CSV Functions___________________________________________________
#got the .csv file from https://github.com/the-blue-alliance/the-blue-alliance-data/
#removed the playoff data from the .csv file in order to replicate OPR calculations given on Blue Alliance Website

def preparationCSV(csv_f):
	num_alliances = 0
	csv_list = []
	frcteams = []
	for row in csv_f:
		csv_list.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]])
		frcteams.append(int(row[1][3:]))
		frcteams.append(int(row[2][3:]))
		frcteams.append(int(row[3][3:]))
		frcteams.append(int(row[4][3:]))
		frcteams.append(int(row[5][3:]))
		frcteams.append(int(row[6][3:]))

		num_alliances += 2

	teams = list(set(frcteams)) #just team numbers as int
	num_teams = (len(teams)) #number of teams

	teams.sort()
	#print(teams)
	#print(csv_list)
	return ([num_alliances, num_teams, teams, csv_list])




def initmatrixCSV(num_of_teams, num_of_alliances, csv_list, teams, OPR_or_DPR):
	
	M_array = np.zeros( (num_of_alliances, num_of_teams), dtype = int ) #initializing a matrix of 0's with num_alliances rows and num_alliance columns
	s_array = np.zeros( (num_of_alliances, 1) ) #initializing the alliance score matrix
	row_num = 0
	#M_array[0][1]=1 

	#M_array: Since each match in the csv file contains 6 teams, there needs to be two rows created in the matrix for each alliance. One row is for the three red teams. The second row is for the three blue teams. There's a specific column for each team based on ascending order (smallest team number to the largest team number.) So for each team that plays in a match on an alliance, its corresponding column in that row (alliance) will be replaced with a 1. 
	#s_array: this is just the matrix with the scores that each alliance makes in a match. Each match would have two scores, one for the red, and one for the blue, and similar to the M_array, they will be placed in separate rows. 

	if (OPR_or_DPR == "OPR"):
		for row in csv_list:
			for x in range(1, 4): 								#for red team
				index = teams.index(int(row[x][3:]))
				M_array[row_num][index] = 1
			s_array[row_num] = int(row[7])				#red team score being added into s_array
			row_num += 1

			for x in range(4, 7):									#for blue team; 
				index = teams.index(int(row[x][3:]))
				M_array[row_num][index] = 1
			s_array[row_num] = int(row[8])				#blue team score
			row_num += 1

	#different from OPRCalc since the scores for are switched within each match
	if (OPR_or_DPR == "DPR"):
		for row in csv_list:
			for x in range(1,4):
				index = teams.index(int(row[x][3:]))
				M_array[row_num][index] = 1
			s_array[row_num] = int(row[8])
			row_num += 1

			for x in range(4,7):
				index = teams.index(int(row[x][3:]))
				M_array[row_num][index] = 1
			s_array[row_num] = int(row[7])
			row_num += 1

	return([M_array, s_array])

#__________________________________________________API Functions_______________________________________________________

headers = {"User-Agent": "Mozilla/5.0", "X-TBA-Auth-Key": "fzQY0pv6qwfwuII5Xx2bmP57BBSuE0maxKailYlrI0e1EdfKCq6F3Th9FFDqpW7f"}
def fetch_json(link):
	return requests.get(link, headers=headers).json()


def find_num_of_teams(json_file): 	
	allteams = []
	for match in json_file:
		#teamcount += 1
		for x in range(0,3):
			allteams.append(match["alliances"]["red"]["team_keys"][x][3:])
		for y in range(0,3):
			allteams.append(match["alliances"]["blue"]["team_keys"][y][3:])
	teams = list(set(allteams))
	teams.sort()
	return (len(teams))
	



def find_num_of_alliances(json_file): 
	matchcount=0
	for match in json_file:
		if (match["comp_level"]=="qm"):
			matchcount += 1
	alliancecount = (matchcount) * 2
	return(alliancecount)




def teams_least_to_greatest(json_file): 
	allteams = []
	for match in json_file:
		#teamcount += 1
		for x in range(0,3):
			allteams.append(int(match["alliances"]["red"]["team_keys"][x][3:]))
		for y in range(0,3):
			allteams.append(int(match["alliances"]["blue"]["team_keys"][y][3:]))
	teams = list(set(allteams))
	teams.sort()
	return (teams)
	


def initmatrix(num_of_teams, num_of_alliances, json_file, teams, OPR_DPR):
	M_array = np.zeros( ((num_of_alliances), num_of_teams), dtype = int ) #initializing a matrix of 0's with num_alliances rows and num_alliance columns
	s_array = np.zeros( (num_of_alliances, 1) ) #initializing the alliance score matrix
	row_num = 0
	
	if (OPR_DPR == 'OPR'):
		for match in json_file:
			if (match["comp_level"]=="qm"):
				for x in range(0,3):			#x is to access the different teams within the red alliance in the specific match
					z = int(match["alliances"]["red"]["team_keys"][x][3:])
					index = teams.index(z)
					M_array[row_num][index] = 1
				s_array[row_num] = match["alliances"]["red"]["score"]
				row_num += 1

				for y in range(0,3):		#y is to access the different teams within the blue alliance in the specific match
					r = int(match["alliances"]["blue"]["team_keys"][y][3:])
					index = teams.index(r)
					M_array[row_num][index] = 1
				s_array[row_num] = match["alliances"]["blue"]["score"]
				row_num += 1

	if (OPR_DPR == "DPR"):
		for match in json_file:
			if (match["comp_level"]=="qm"):
				for x in range(0,3):			#x is to access the different teams within the red alliance in the specific match
					z = int(match["alliances"]["red"]["team_keys"][x][3:])
					index = teams.index(z)
					M_array[row_num][index] = 1
				s_array[row_num] = match["alliances"]["blue"]["score"]
				row_num += 1

				for y in range(0,3):		#y is to access the different teams within the blue alliance in the specific match
					r = int(match["alliances"]["blue"]["team_keys"][y][3:])
					index = teams.index(r)
					M_array[row_num][index] = 1
				s_array[row_num] = match["alliances"]["red"]["score"]
				row_num += 1

	return([M_array, s_array])

	
#__________________________________________________Common for Both_______________________________________________________

def OPR_or_DPR_Calc(initmatrixresults): 
#since the number of matches (represents the number of equations) is greater than the number of teams in the event (represents the variables), overdetermined
	M_array = initmatrixresults[0]		#since the initmatrix() function is being passed in, the individual parts of the list that initmatrix() returns, represents M_array and the s_array
	s_array = initmatrixresults[1]
	
	transposed = M_array.transpose()
	transposed_copy = transposed
	left_side = transposed.dot(M_array)
	#print(isSquare(left_side))
	#print(np.linalg.det(left_side))			#this just gives the determinant of the matrix for debugging
	inverse_left = np.linalg.inv(left_side)
	inverse_left_copy = inverse_left

	right_side = transposed_copy.dot(s_array)
	final_right_side = inverse_left_copy.dot(right_side)

	return(final_right_side)

def CCWM_Calc(OPR, DPR):
	CCWM = OPR - DPR
	return (CCWM)

def display(OPR_Results, DPR_Results, teams):
	"""
	#Version Without Database
	count = 0
	for OPR in OPR_Results:
		OPR = float(OPR[0])
		DPR = float(DPR_Results[count])
		CCWM = float(CCWM_Calc(OPR, DPR_Results[count]))

		#insert_values_into_table(teams[count],OPR,DPR,CCWM)

		print teams[count], "			", "OPR: ", OPR, "			", "DPR: ", DPR, "			", "CCWM: ", CCWM
		count += 1
	"""
	#Version With Database
	count = 0
	for OPR in OPR_Results:
		OPR = float(OPR[0])
		DPR = float(DPR_Results[count])
		CCWM = float(CCWM_Calc(OPR, DPR_Results[count]))

		insert_values_into_table(teams[count], OPR, DPR, CCWM)
	
		c.execute("SELECT * FROM OPR_DPR_CCWM_Calculations WHERE team_number=?", (teams[count], ))

		print(c.fetchall())
		count+=1
	print

#_________________________________________________________________________________________________________
def main():
	#filename = '2019.csv'

	filename = '' #************************************ NEED TO PUT A FILENAME******************************** OR
	APILink = 'https://www.thebluealliance.com/api/v3/event/2019abca/matches' #*********** Need to Put An API Link

	if (len(filename)>0):
		#f = open('2019.csv')		#.csv file
		f = open(filename)
		csv_f = csv.reader(f)		
		
		print'CSV'
		Prep = preparationCSV(csv_f)
		num_of_teams = Prep[1]
		num_of_alliances = Prep[0]
		teams = Prep[2]
		csv_list = Prep[3]
		print"Num of Teams     ", Prep[1] #number of teams
		print"Num of Alliances ", Prep[0] #number of alliances
		print
		OPR_Results = OPR_or_DPR_Calc(initmatrixCSV(num_of_teams, num_of_alliances, csv_list, teams, "OPR"))
		DPR_Results = OPR_or_DPR_Calc(initmatrixCSV(num_of_teams, num_of_alliances, csv_list, teams, "DPR"))
		display(OPR_Results, DPR_Results, teams)


	elif (filename=='') and (len(APILink)>0):
		matches_json = fetch_json(APILink)
		num_of_teams = find_num_of_teams(matches_json)
		print'API'
		print "Number of Teams:   ", num_of_teams
		num_of_alliances = find_num_of_alliances(matches_json)
		print "Num of Alliances: ", num_of_alliances
		print
	
		teams = teams_least_to_greatest(matches_json)
		#print(teams)
		OPR_matrix = initmatrix(num_of_teams, num_of_alliances, matches_json, teams, "OPR")
		OPR_results = OPR_or_DPR_Calc(OPR_matrix)
		DPR_matrix = initmatrix(num_of_teams, num_of_alliances, matches_json, teams, "DPR")
		DPR_results = OPR_or_DPR_Calc(DPR_matrix)
		display(OPR_results, DPR_results, teams)

main()
#x=fetch_json('https://www.thebluealliance.com/api/v3/event/2019abca/oprs')
#print x









