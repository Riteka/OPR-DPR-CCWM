"""import csv
import numpy as np

f = open('2019abca.csv')
csv_f = csv.reader(f)

frcteams = []	#raw teams
num_teams = 0
num_alliances=0

csv_list = []


for row in csv_f:
	csv_list.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]])
	frcteams.append(int(row[1][3:]))
	frcteams.append(int(row[2][3:]))
	frcteams.append(int(row[3][3:]))
	frcteams.append(int(row[4][3:]))
	frcteams.append(int(row[5][3:]))
	frcteams.append(int(row[6][3:]))
	num_alliances+=2

print(num_teams) #number of matches
print(num_alliances) #number of alliances

teams = list(set(frcteams)) #just team numbers as int
num_teams = (len(teams)) #number of teams
print(num_teams)

teams.sort()
print(teams)

#print(csv_list)

def initmatrix():
	M_array = np.zeros( (num_alliances, num_teams) ) #initializing a matrix of 0's with num_alliances rows and num_teams columns
	s_array = np.zeros( (num_alliances, 1) ) #initializing the alliance score matrix
	row_num = 0
	#M_array[0][1]=1 

	for row in csv_list:
		for x in range(1, 4): 								#for red team
			index = teams.index(int(row[x][3:]))
			M_array[row_num][index] = 1
		s_array[row_num] = int(row[7])
		row_num += 1

		for x in range(4, 7):									#for blue team
			index = teams.index(int(row[x][3:]))
			M_array[row_num][index] = 1
		s_array[row_num] = int(row[8])
		row_num += 1

		return(M_array, s_array)

#print(M_array[33])
#print(s_array)
print ("Hello")
prac = np.array([[1,1,0,0],[1,0,1,0],[0,1,1,0],[1,0,0,1],[0,1,0,1]])
prac1 = np.array([10,13,7,15,10])
transposed = prac.transpose()
left_side = transposed.dot(prac)
print("left side", left_side)
left_side_transverse = np.linalg.inv(left_side)
right_side = transposed.dot(prac1)
final_right_side = left_side_transverse.dot(right_side)
print(final_right_side)


def OPRCalc(initmatrixresults): #since the number of matches (represents the number of equations) is greater than the number of teams in the event (represents the variables), overtdetermined
	M_array = initmatrixresults[0]
	print(M_array)
	s_array = initmatrixresults[1]
	transposed = M_array.transpose()
	left_side = transposed.dot(M_array)
	print(M_array)
	print("left side", left_side)
	print(np.linalg.det(left_side))
	left_side_tranverse = np.linalg.inv(left_side)
	right_side = transposed.dot(s_array)
	#final_right_side = left_side_transverse.dot(right_side)
	#print (final_right_side)

OPRCalc(initmatrix())
"""
import csv
import numpy as np
np.set_printoptions(edgeitems=200)

f = open('2019.csv')
csv_f = csv.reader(f)

frcteams = []	#raw teams
num_teams = 0
num_alliances=0

csv_list = []


for row in csv_f:
	csv_list.append([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]])
	frcteams.append(int(row[1][3:]))
	frcteams.append(int(row[2][3:]))
	frcteams.append(int(row[3][3:]))
	frcteams.append(int(row[4][3:]))
	frcteams.append(int(row[5][3:]))
	frcteams.append(int(row[6][3:]))
	num_alliances+=2

#print("num_teams", num_teams) #number of matches
print("Num of alliances ", num_alliances) #number of alliances

teams = list(set(frcteams)) #just team numbers as int
num_teams = (len(teams)) #number of teams
print("Num of teams ", num_teams)

teams.sort()
print(teams)

#print(csv_list)

def initmatrix():
	M_array = np.zeros( (num_alliances, num_teams), dtype = int ) #initializing a matrix of 0's with num_alliances rows and num_alliance columns
	s_array = np.zeros( (num_alliances, 1) ) #initializing the alliance score matrix
	row_num = 0
	#M_array[0][1]=1 

	#M_array: Since each match in the csv file contains 6 teams, there needs to be two rows created in the matrix for each alliance. One row is for the three red teams. The second row is for the three blue teams. There's a specific column for each team based on ascending order (smallest team number to the largest team number.) So for each team that plays in a match on an alliance, its corresponding column in that row (alliance) will be replaced with a 1. 
	#s_array: this is just the matrix with the scores that each alliance makes in a match. Each match would have two scores, one for the red, and one for the blue, and similar to the M_array, they will be placed in separate rows. 
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

	return([M_array, s_array])

"""#print(M_array[33])
#print(s_array)
print ("Hello")
prac = np.array([[1,1,0,0],[1,0,1,0],[0,1,1,0],[1,0,0,1],[0,1,0,1]])
prac1 = np.array([10,13,7,15,10])
transposed = prac.transpose()
left_side = transposed.dot(prac)
print("left side", left_side)
left_side_transverse = np.linalg.inv(left_side)
right_side = transposed.dot(prac1)
final_right_side = left_side_transverse.dot(right_side)
print(final_right_side)"""

def isSquare (matrix): 
	return all (len(row)==len(matrix) for row in matrix) #this function is just to check if the matrix is square or not

def OPRCalc(initmatrixresults): #since the number of matches (represents the number of equations) is greater than the number of teams in the event (represents the variables), overdetermined
	M_array = initmatrixresults[0]		#since the initmatrix() function is being passed in, the individual parts of the list that initmatrix() returns, represents M_array and the s_array
	print (M_array)
	s_array = initmatrixresults[1]

	"""

	M_array_transposed = initmatrixresults[0]
	M_array_transposed = M_array_transposed.transpose()
	M_array_transposed_copy = M_array_transposed

	left_side = M_array_transposed_copy.dot(M_array)
	print(isSquare(left_side))
	print(np.linalg.det(left_side))
	
	"""


	
	transposed = M_array.transpose()
	transposed_copy = transposed
	left_side = transposed.dot(M_array)
	print(isSquare(left_side))
	print(np.linalg.det(left_side))			#this just gives the determinant of the matrix for debugging
	#inverse_M = np.linalg.inv(M_array)
	inverse_left = np.linalg.inv(left_side)
	inverse_left_copy = inverse_left

	right_side = transposed_copy.dot(s_array)
	final_right_side = inverse_left_copy.dot(right_side)
	print(final_right_side)
	print ("Number of rows and columns")
	print(final_right_side.shape)					#to verify 



	"""

	s_array = initmatrixresults[1]
	transposed = M_array.transpose()
	left_side = transposed.dot(M_array)
	#left_side = M_array.dot(transposed)
	print(isSquare(left_side))
	#print(M_array)
	#print("left side", left_side)
	print(np.linalg.det(left_side))
	left_side_tranverse = np.linalg.inv(left_side)
	right_side = transposed.dot(s_array)
	#final_right_side = left_side_transverse.dot(right_side)
	#print (final_right_side)

	"""

OPRCalc(initmatrix())
prac = np.array([[1,1,0,0],[1,0,1,0],[0,1,1,0],[1,0,0,1],[0,1,0,1]])
prac1 = np.array([[10],[13],[7],[15],[10]])
OPRCalc([prac, prac1])












