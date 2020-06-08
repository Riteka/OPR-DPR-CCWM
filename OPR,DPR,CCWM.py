
import csv
import numpy as np
np.set_printoptions(edgeitems=200)


#got the .csv file from https://github.com/the-blue-alliance/the-blue-alliance-data/
#removed the playoff data from the .csv file in order to replicate OPR calculations given on Blue Alliance Website

def preparation(csv_f):
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

def initmatrix(prepresults, OPR_or_DPR):
	num_alliances = prepresults[0]
	num_teams = prepresults[1]
	teams = prepresults[2]
	csv_list = prepresults[3]
	M_array = np.zeros( (num_alliances, num_teams), dtype = int ) #initializing a matrix of 0's with num_alliances rows and num_alliance columns
	s_array = np.zeros( (num_alliances, 1) ) #initializing the alliance score matrix
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

	return([M_array, s_array, teams])


def isSquare (matrix): #just for debugging
	return all (len(row)==len(matrix) for row in matrix) #this function is just to check if the matrix is square or not

def OPRCalc(initmatrixresults): 
#since the number of matches (represents the number of equations) is greater than the number of teams in the event (represents the variables), overdetermined
	M_array = initmatrixresults[0]		#since the initmatrix() function is being passed in, the individual parts of the list that initmatrix() returns, represents M_array and the s_array
	s_array = initmatrixresults[1]
	teams = initmatrixresults[2]

	
	transposed = M_array.transpose()
	transposed_copy = transposed
	left_side = transposed.dot(M_array)
	#print(isSquare(left_side))
	#print(np.linalg.det(left_side))			#this just gives the determinant of the matrix for debugging
	#inverse_M = np.linalg.inv(M_array)
	inverse_left = np.linalg.inv(left_side)
	inverse_left_copy = inverse_left

	right_side = transposed_copy.dot(s_array)
	final_right_side = inverse_left_copy.dot(right_side)
	return ([teams, final_right_side])
 
def DPRCalc(initmatrixresults):	
#since the number of matches (represents the number of equations) is greater than the number of teams in the event (represents the variables), overdetermined

	M_array = initmatrixresults[0]
	#since the initmatrix() function is being passed in, the individual parts of the list that initmatrix() returns, represents M_array and the s_array
	s_array = initmatrixresults[1]
	teams = initmatrixresults[2]

	transposed = M_array.transpose()
	transposed_copy = transposed
	left_side = transposed.dot(M_array)
	#print(isSquare(left_side))
	#print(np.linalg.det(left_side))			#this just gives the determinant of the matrix for debugging
	#inverse_M = np.linalg.inv(M_array)
	inverse_left = np.linalg.inv(left_side)
	inverse_left_copy = inverse_left

	right_side = transposed_copy.dot(s_array)
	final_right_side = inverse_left_copy.dot(right_side)
	return (final_right_side)


def display(OPRResults, DPRResults):
	teams = OPRResults[0]
	OPR_final_right_side = OPRResults[1]
	DPR_final_right_side = DPRResults

	count = 0
	for OPR in OPR_final_right_side:
		OPR = OPR[0]
		DPR = float(DPR_final_right_side[count])
		CCWM = OPR - DPR
		print teams[count], "			", "OPR: ", OPR, "			", "DPR: ", DPR, "			", "CCWM: ", CCWM
		count += 1
	print
	#print "(Rows,Columns)", "			", final_right_side.shape					#to verify 


def main():
	f = open('2019.csv')		#.csv file
	csv_f = csv.reader(f)		
	
	Prep = preparation(csv_f)
	print"Num of Alliances ", Prep[0] #number of alliances
	print"Num of Teams     ", Prep[1] #number of teams
	print
	OPR_Results = OPRCalc(initmatrix(Prep, "OPR"))
	DPR_Results = DPRCalc(initmatrix(Prep, "DPR"))
	display(OPR_Results, DPR_Results)

main()













