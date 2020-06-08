
import requests
import json
import csv
import numpy as np
np.set_printoptions(edgeitems=200)


headers = {"User-Agent": "Mozilla/5.0", "X-TBA-Auth-Key": "fzQY0pv6qwfwuII5Xx2bmP57BBSuE0maxKailYlrI0e1EdfKCq6F3Th9FFDqpW7f"}
def fetch_json(link):
	return requests.get(link, headers=headers).json()

"""
x=fetch_json('https://www.thebluealliance.com/api/v3/event/2019abca/matches')
#x.decode(encoding='UTF-8')					using event/2016nytr/matches
print ("hello")
print(x[0]["alliances"]["red"]["team_keys"][0][3:]) #2013
print(x[0]["alliances"]["red"]["score"])						#157
print(x[0]["alliances"]["blue"]["team_keys"])				#keys

y=fetch_json("https://www.thebluealliance.com/api/v3/event/2019abca/teams")
teamcount = 0
for team in y:
	teamcount +=1
print(teamcount)	#37
"""

def find_num_of_teams(json_file): 	#takes in /event/2019abca/matches
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
	#return(teamcount)
#print("new")
#print(find_num_of_teams(x))



def find_num_of_alliances(json_file): #takes in /event/2019abca/matches
	matchcount=0
	for match in json_file:
		matchcount += 1
	alliancecount = (matchcount) * 2
	return(alliancecount)
#print("new1")
#print(find_num_of_alliances(x))		#156



def teams_least_to_greatest(json_file): #takes in /event/2019abca/matches
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
	


def initmatrixnew(num_of_teams, num_of_alliances, json_file, teams):
	M_array = np.zeros( ((num_of_alliances), num_of_teams), dtype = int ) #initializing a matrix of 0's with num_alliances rows and num_alliance columns
	s_array = np.zeros( (num_of_alliances, 1) ) #initializing the alliance score matrix
	row_num = 0
	
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
	

	"""
	for q in range(0,(num_of_alliances-31)):
		for x in range(0,3):
			z = int(json_file[q]["alliances"]["red"]["team_keys"][x][3:])
			index = teams.index(z)
			M_array[row_num][index] = 1
		s_array[row_num] = json_file[q]["alliances"]["red"]["score"]
		row_num += 1

		for y in range(0,3):
			r = int(json_file[q]["alliances"]["blue"]["team_keys"][x][3:])
			index = teams.index(r)
			M_array[row_num][index] = 1
		s_array[row_num] = json_file[q]["alliances"]["blue"]["score"]
		row_num += 1
	"""

	#for q in range(125,num_of_alliances+1):
	#M_array = np.delete(M_array,slice(148,None),0)
	#s_array = np.delete(s_array,slice(148,None),0)


	#M_array = np.delete(M_array,slice(148,156),0)
	#s_array = np.delete(s_array,slice(148,156),0) #got rid of semi
	#M_array = np.delete(M_array,slice(0,24),0)
	#s_array = np.delete(s_array,slice(0,24),0)


	#M_array = np.delete(M_array,slice(0,24),0)
	#s_array = np.delete(s_array,slice(0,24),0)
	
	#print(M_array.shape)
	return([M_array, s_array])



def isSquare (matrix): 
	return all (len(row)==len(matrix) for row in matrix) #this function is just to check if the matrix is square or not




def OPRCalc(initmatrixresults): #since the number of matches (represents the number of equations) is greater than the number of teams in the event (represents the variables), overdetermined
	M_array = initmatrixresults[0]		#since the initmatrix() function is being passed in, the individual parts of the list that initmatrix() returns, represents M_array and the s_array
	#print (M_array)
	print ("Rows, Columns      " + str(M_array.shape))
	s_array = initmatrixresults[1]
	
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

	#print(final_right_side)
	#print ("Answer (Rows, Columns) " + str(final_right_side.shape) )
	#print(final_right_side.shape)					#to verify 

	return(final_right_side)



def main():
	matches_json = fetch_json('https://www.thebluealliance.com/api/v3/event/2019abca/matches')
	num_of_teams = find_num_of_teams(matches_json)
	print "Number of Teams:   ", num_of_teams
	num_of_alliances = find_num_of_alliances(matches_json)
	print "Num of Alliances: ", num_of_alliances
	
	teams = teams_least_to_greatest(matches_json)
	#print(teams)
	matrix = initmatrixnew(num_of_teams, num_of_alliances, matches_json, teams)
	results = OPRCalc(matrix)
	final_list = []
	counting = 0
	for e in results:
		final_list.append([teams[counting], e]) 
		counting+=1
	
	print
	print ("Highest to Lowest OPR")
	resultscopy = []
	for i in results:
		resultscopy.append(i[0])
	#print (resultscopy)
	resultscopy.sort(reverse = True)
	#print (resultscopy)
	for f in resultscopy: 
		index = list(results).index(f)
		print final_list[index][0], "				", "OPR: ", float(final_list[index][1])


main()
x=fetch_json('https://www.thebluealliance.com/api/v3/event/2019abca/oprs')
print x









