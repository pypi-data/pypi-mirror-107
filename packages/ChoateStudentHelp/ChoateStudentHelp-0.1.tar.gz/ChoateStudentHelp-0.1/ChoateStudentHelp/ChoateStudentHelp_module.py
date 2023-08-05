'''
Brian Harder
5/24/2021

Description: This is a Python module that has 6 functions that I thought would be useful in my own life as a Choate student. There is are 6 math help functions, 2 standardized test simulation functions, a
function for stock prices, a fortunte teller game, a function for walking time between Choate buildings, and a randomized visual design creator. In terms of my process, I think the coding was pretty smooth
overall. The infinite_limit and Pascal_triangle functions in the mathClass were a little more difficult to execute due to the various possibilites of negative coefficients. However, the other funtions were 
pretty doable in conjunction with some code that I got from various sources. Also, getting the module onto PyPI for PIP installation was more difficult than I anticipated given that the first method I tried, 
based on a website I found, did not work. Given that this is the largest project we have done so far, I'd say my time management was pretty good overall. I did fall behind at one point during the process 
but was able to get back on schedule within a few days. If I were to do this again, I would try to create more cohesion in the project since the functions in the module are not very related to one another 
beyond the fact that I would find them all useful.


Sources:

I used several functions from the sympy library in the infiniteLimit function, including converting strings to sympy equations and getting coefficients:

https://docs.sympy.org/latest/modules/parsing.html

I used this website to figure out how to remove the extra + sign at the end of expanded_string in the Pascal function; the rstrip function was what I found:

https://geekflare.com/python-remove-last-character/

I uesd the findOccurences function from this website in the Pascal function:

https://stackoverflow.com/questions/13009675/find-all-the-occurrences-of-a-character-in-a-string

I used these websites to get the data points for the SAT and ACT linear regression:

https://www.albert.io/blog/sat-score-calculator/
https://www.albert.io/blog/act-score-calculator/

I used these functions to stop the yfinance.download function from printing to the console:

https://stackoverflow.com/questions/8447185/to-prevent-a-function-from-printing-in-the-batch-console-in-python

I used this website to make sure all the colors were different in the visual_design function's last option:

https://www.geeksforgeeks.org/check-if-all-array-elements-are-distinct/


OMH
'''
import math, sympy, cmath, random
from sympy import *
import yfinance, stockquotes
import matplotlib.pyplot as plt
import sys, os
import geopy.distance
from PIL import Image, ImageDraw


#This class organizes all the math related functions.
class mathClass:

	#This function evaluates limits to infinity by using the rules with the highest power in the numerator and denominator. Lists of the exponents and the sympy library are the main methods used here.
	def infinite_limit(self, numerator, denominator):

		numerator_powers, denominator_powers = [], []

		#every time a "**" is found, the next term is recorded in powers since the double asterisk indicates an exponent
		for i in range(0, len(numerator)):

			if numerator[i] == "*" and numerator[i+1] == "*":

				numerator_powers.append(int(numerator[i+2]))

			if numerator[i] == "x": 

				if i == len(numerator)-1:

					numerator_powers.append(1)

				elif numerator[i+1] != "*":

					numerator_powers.append(1)

		for i in range(0, len(denominator)):

			if denominator[i] == "*" and denominator[i+1] == "*":

				denominator_powers.append(int(denominator[i+2]))

			if denominator[i] == "x": 

				if i == len(denominator)-1:

					denominator_powers.append(1)

				elif denominator[i+1] != "*":

					denominator_powers.append(1)

		highest_numerator, highest_denominator = max(numerator_powers), max(denominator_powers)

		x = symbols("x")

		#the coeff function in sympy is used to get the coefficients of the terms with the highest powers ; sympy.parsing.sympy_parser.parse_expr is used to convert the inputted strings to sympy expressions
		numerator_coefficient, denominator_coefficient = sympy.parsing.sympy_parser.parse_expr(numerator).coeff(x, highest_numerator), sympy.parsing.sympy_parser.parse_expr(denominator).coeff(x, highest_denominator)

		if highest_numerator < highest_denominator:

			return 0

		elif highest_numerator > highest_denominator:

			if numerator_coefficient > 0:

				return math.inf

			else:

				return -math.inf

		else:

			return numerator_coefficient / denominator_coefficient
			

	#This function returns the value of a limit using direct substitution by substituting in the given x value. Try/except is used to deal with situations where direct substitution cannot be used (sqrt(neg), etc)
	def substitution_limit(self, numerator, denominator, x_val):

		numerator = numerator.replace("x", x_val)
		denominator = denominator.replace("x", x_val)

		try:

			return eval("(" + numerator + ")" + "/" + "(" + denominator + ")")

		except:

			return "Direct substitution cannot be used to evaluate this limit."

	
	#This function takes the 3 coefficients of a quadratic equation and uses the quadratic formula to return the solutions.
	def quadratic_formula(self, a, b, c):

		discriminant = (b**2) - (4*a*c)

		try:

			sqrt_d = math.sqrt(discriminant)

		except:

			#cmath is used to allow for complex numbers when the discriminant is negative
			sqrt_d = cmath.sqrt(discriminant)

		root_1 = (-b + sqrt_d) / (2*a)
		root_2 = (-b - sqrt_d) / (2*a)

		return [root_1, root_2]


	#This function returns an expression expanded to a given power via binomial theorem and increasing/decreasing exponents. Sympy is used for the math operations.
	def Pascal_triangle(self, power, expression):

		def C(n, r):

			return int(math.factorial(n) / (math.factorial(n-r)*math.factorial(r)))

		def find_occurrences(s, ch):

			return [i for i, letter in enumerate(s) if letter == ch]

		negatives = find_occurrences(expression, "-")

		neg_x, neg_y = False, False

		#whether or not the two terms of the binomial are negative is found by checking if there is a negative at index 0 (x) or somewhere else (y)
		if 0 in negatives:

			neg_x = True

		for element in negatives:

			if element != 0:

				neg_y = True

		coefficients = []

		#the coefficients are created with binomial theorem, which uses combinations for each coefficient (0C0, 1C0, 1C1, 2C0, 2C1, 2C2, etc)
		for i in range(0, power+1):

			coefficients.append(C(power, i))

		x_exponents, y_exponents = [], []

		#the first term's exponents go from high to low, and the second term's are opposite
		for i in range(power, -1, -1):

			x_exponents.append(i)

		for i in range(0, power+1):

			y_exponents.append(i)

		expanded = []

		#the expanded strings are x and y raised to the respective powers in order with negatives being included based on the boolean variables
		for i in range(0, len(coefficients)):

			if not neg_x and not neg_y:

				expanded_string = "x**" + str(x_exponents[i]) + " * " + expression[len(expression)-1] + "**" + str(y_exponents[i])

			elif neg_x and not neg_y:

				#the negative coefficients are applied to odd powers
				if x_exponents[i] % 2 != 0:

					expanded_string = "-1 * x**" + str(x_exponents[i]) + " * " + expression[len(expression)-1] + "**" + str(y_exponents[i])

				else:

					expanded_string = "x**" + str(x_exponents[i]) + " * " + expression[len(expression)-1] + "**" + str(y_exponents[i])

			elif not neg_x and neg_y:

				if y_exponents[i] % 2 != 0:

					expanded_string = "x**" + str(x_exponents[i]) + " * -1 * " + expression[len(expression)-1] + "**" + str(y_exponents[i])

				else:

					expanded_string = "x**" + str(x_exponents[i]) + " * " + expression[len(expression)-1] + "**" + str(y_exponents[i])

			else:

				if x_exponents[i] % 2 != 0 and  y_exponents[i] % 2 == 0:

					expanded_string = "-1 * x**" + str(x_exponents[i]) + " * " + expression[len(expression)-1] + "**" + str(y_exponents[i])

				elif x_exponents[i] % 2 == 0 and  y_exponents[i] % 2 != 0:

					expanded_string = "x**" + str(x_exponents[i]) + " * -1 * " + expression[len(expression)-1] + "**" + str(y_exponents[i])

				elif x_exponents[i] % 2 != 0 and  y_exponents[i] % 2 != 0:

					expanded_string = "-1 * x**" + str(x_exponents[i]) + " * -1 * " + expression[len(expression)-1] + "**" + str(y_exponents[i])

				else:

					expanded_string = "x**" + str(x_exponents[i]) + " * " + expression[len(expression)-1] + "**" + str(y_exponents[i])

			expanded.append(expanded_string)

		#the expanded strings are then multiplied by the coefficients that were found with Pascal's triangle
		for i in range(0, len(expanded)):

			sympy_expanded = sympy.parsing.sympy_parser.parse_expr(expanded[i])

			element = expand(sympy_expanded * coefficients[i])

			expanded[i] = element

		expanded_string = ""

		for element in expanded:

			expanded_string += str(element)

			expanded_string += " + "

		for i in range(-3, 0):

			expanded_string = expanded_string.rstrip(expanded_string[i])

		return expanded_string


	#This function returns the nth term of an arithmetic or geometric series, denoted by the arithmetic boolean variable, using the t of n formulas. 	
	def sequences(self, t1, r, n, arithmetic):

		if arithmetic:

			return t1 + (r*(n-1))

		else:

			return t1 * (r**(n-1))


	'''
	This function returns the sum of the first n terms of an arithmetic or geometric series, once again using the boolean arithmetic, with the s of n formulas. This function has another boolean infinite; when 
	True, the function will return the infinite sum of a geometric series, using the formula t1 / 1-r.
	'''
	def series(self, t1, tn, r, n, arithmetic, infinite):

		if arithmetic:

			return (n*(t1 + tn)) / 2

		elif not arithmetic and not infinite:

			return (t1*(1-r**n)) / (1-r)

		elif not arithmetic and infinite:

			return t1 / (1-r)

		else:

			return "Only geometric sequences can be infinite."


#This class organizes the SAT and ACT score simulation functions.
class standardizedTestClass:

	#The SAT function returns the average score one would get, based on 10,000 trials, if they guessed every question on the SAT. The user can choose to input the same answer every time or have it be randomized.
	def SAT(self, same_answer, answer):

		trials, score = 10000, 0

		def SAT_trial():

			key, answers, count = [], [], 0

			for i in range(154):

				key.append(random.randint(1, 4))

			if same_answer:

				for i in range(154):

					answers.append(answer)
			else:

				for i in range(154):

					answers.append(random.randint(1, 4))

			for i in range(154):

				if key[i] == answers[i]:

					count += 1

			return count

		for i in range(trials):

			score += SAT_trial()

		average_raw = score / trials

		'''
		I looked at a website that calculates SAT scaled scores based on raw scores, used that to get a bunch of data points, and used linear regression to get an equation for scaled score based on raw score. 
		The r value was 0.994745175, so I think the regression model fit the SAT score data pretty well.
		'''
		score_calculation = 417.835052 + (average_raw*7.68870819)

		if average_raw == 0:

			return 400

		elif average_raw == 154:

			return 1600

		else:

			return int(score_calculation)
			

	#This function serves the same purpose as the SAT function but for the ACT. An addition had to be made to account for the ACT math section having 5 answer choices.
	def ACT(self, same_answer, math_answer, other_answer):

		trials, score = 10000, 0

		def ACT_trial():

			#the correct and given answers are put in lists just like in the SAT function based on the same_answer boolean, but the math section is done separately to account for A-E answer choices, not A-D
			math_key, math_answers, count = [], [], 0

			for i in range(60):

				math_key.append(random.randint(1, 5))

			if same_answer:

				for i in range(60):

					math_answers.append(math_answer)

			else:

				for i in range(60):

					math_answers.append(random.randint(1, 5))

			for i in range(60):

				if math_key[i] == math_answers[i]:

					count += 1

			key, answers = [], []

			for i in range(155):

				key.append(random.randint(1, 4))

			if same_answer:

				for i in range(155):

					answers.append(other_answer)
			else:

				for i in range(155):

					answers.append(random.randint(1, 4))

			for i in range(155):

				if key[i] == answers[i]:

					count += 1

			return count

		for i in range(trials):

			score += ACT_trial()

		average_raw = score / trials

		#I did linear regression again for this ACT function. The r value was 0.9998002744, so once again I had a pretty good model.
		score_calculation = 0.195352576 + (average_raw*0.1653997383)

		if average_raw == 0:

			return 1

		elif average_raw == 215:

			return 36

		else:

			return int(score_calculation)


#The stocks function displays a graph of the stocks's price over a given interval and returns the current share price.
def stocks(ticker, start, end):

	stock = stockquotes.Stock(ticker)

	#If the user chooses to print the output of this function - share price -, a confirmation message for the yfinance.download function is also printed to the console. 
	#To prevent this, I blocked printing for when the yfinance function is called.
	old_stdout = sys.stdout 
	sys.stdout = open(os.devnull, "w")

	chart_data = yfinance.download(ticker, start, end)

	sys.stdout = old_stdout

	plt.plot(chart_data["Close"])
	plt.show()

	return stock.current_price


#This function is a fortunte teller game that I thought might be fun to play now and then, like the foldable paper ones. Lists are used instead of lots of nested if statements, which was my main goal here.
def fortune_teller():

	question1 = ["red", "blue"]

	#each question is a list of all the possible answer choices based on the previous response
	question2 = [

	  ["A", "B"],
	  ["C", "D"],
	]

	question3 = [

  		[
		    ["green", "purple"],
		    ["magenta", "yellow"],
  		],

  		[

		    ["grey", "black"],
		    ["indigo", "maroon"],
  		],
	]

	question4 = [

		[
			[

				["1", "2"],
				["3", "4"],

			],

			[

				["5", "6"],
				["7", "8"],

			],

		],

		[
			[

				["9", "10"],
				["11", "12"],

			],

			[

				["13", "14"],
				["15", "16"],

			],

		],
	]

	answers = [

		"Each day, compel yourself to do something you would rather not do.",
		"Every wise man started out by asking many questions.",
		"From now on your kindness will lead you to success.",
		"Get your mind set – confidence will lead you on.",
		"If you think you can do a thing or think you can’t do a thing, you’re right.",
		"Every flower blooms in its own sweet time.",
		"The greatest achievement in life is to stand up again after falling.",
		"The only people who never fail are those who never try.",
		"There is no wisdom greater than kindness.",
		"A smile is your personal welcome mat.",
		"Accept something that you cannot change, and you will feel better.",
		"Miles are covered one step at a time.",
		"Put your mind into planning today. Look into the future.",
		"The sure way to predict the future is to invent it.",
		"If you want the rainbow, you have to tolerate the rain."
		"The fortune you seek is in another index."

	]

	def question(options):

	  while True:

	    try:

	      response = int(input("Pick 1) " + options[0] + " or 2) " + options[1] + ": ")) - 1

	      if response < len(options):

	        return response

	    except:

	      pass


	#the questions are gone through one at a time with the previous responses as inputs
	first = question(question1)
	second = question(question2[first])
	third = question(question3[first][second])
	fourth = question(question4[first][second][third])

	print(answers[int(question4[first][second][third][fourth]) - 1])


#This function will return how long it takes to walk from one building to another on the Choate campus using the distance between 2 points defined by latitude and longitude.
def walking_time(building1, building2, seconds):

	choate_buildings = {

		"Memorial House" : (41.459799130887546, -72.81253950970536),
		"Hill House" : (41.45813565561544, -72.81336797843655),
		"Squire Stanley" : (41.45995268009463, -72.81315530337368),
		"Sally Hart Lodge" : (41.45775075458777, -72.81223178769596),
		"Chapel" : (41.456854743438235, -72.81316049021501),
		"WJAC" : (41.45465878917236, -72.80958048559658),
		"Colony Hall" : (41.45777834343251, -72.80732027781659),
		"PMAC" : (41.45790261089875, -72.80811321340957),
		"Steele Hall" : (41.45888279615266, -72.81400813253074),
		"Lanphier Center" : (41.45918845037742, -72.80975433000114),
		"Carl Icahn Science Center" : (41.459491535335864, -72.80853419325018),
		"Humanities Building" : (41.459386516160265, -72.81310335516075),
		"Andrew Mellon Library" : (41.45853003456271, -72.81341308415308),
		"St. John Hall" : (41.457511329055556, -72.81349263538527),
		"Tenney/Bernhard" : (41.45603055473527, -72.81274745557317),
		"Archbold" : (41.45871173929997, -72.80978442310364),
		"CK/McCook" : (41.458404856495854, -72.81037853238148),
		"Pratt Health Center" : (41.45833282443969, -72.81515393077808),
		"Pierce" : (41.45993804491732, -72.81093804141835),
		"Woodhouse/Combination" : (41.45725788267579, -72.81401686529755),
		"Logan Munroe" : (41.460507817639375, -72.81173217823357),
		"Hunt Tennis Center" : (41.46113232348608, -72.8120426847346),
		"Atwater/Mead" : (41.4588347173473, -72.81168353576032),
		"Spencer" : (41.456616116479665, -72.81182642820936),
	}

	coordinates_1, coordinates_2 = choate_buildings[building1], choate_buildings[building2]

	#the geopy library will return the distance between two lat/long coordinates
	distance = geopy.distance.distance(coordinates_1, coordinates_2).mi

	#I figured 3.5 mi/hr is a pretty reasonable average walking pace
	time = (distance / 3.5) * 60

	#the user can choose to have a 2 digit decimal or a formatted string returned for the time in minutes and seconds
	if seconds:

		time_tuple = math.modf(time)

		seconds, minutes = time_tuple[0], int(time_tuple[1])
		seconds = int(seconds*60)

		return str(minutes) + " minutes and " + str(seconds) + " seconds"

	else:

		return round(time, 2)


#This function creates an appealing visual design based on a couple parameters and some randomness; there are 3 different options for the type of image created.
def visual_design(vertices, layers, colors, option):

	img, img2 = Image.new("RGB", (1000, 1000), (255, 255, 255)), Image.new("RGB", (1000, 1000), (255, 255, 255))
	image, image2 = ImageDraw.Draw(img), ImageDraw.Draw(img2)

	#option #1 uses the number of vertices to create regular polygons that spiral outwards with the rotation parameter
	if option == 1:

		color = random.choice(colors)

		for i in range(450):

			if i % layers == 0:

				color = random.choice(colors)

			image.regular_polygon((500, 500, 50+i), vertices, rotation = i*4, fill = color, outline = "black")

	#option #2 creates a bunch of circles in random positions and of random colors throughout the canvas
	elif option == 2:

		for i in range(layers):

			x, y, radius = random.randint(0, 1000), random.randint(0, 1000), 75

			image.ellipse([x, y, x+radius, y+radius], fill = random.choice(colors), outline = "black")

	#option 3 uses rows and columsn of rectangles that slowly change in length from top to bottom and left to right to create 4 colored zones that are joined in an interesting way
	else:

		def distinct(arr) :
  
		    n = len(arr)
		    s = set()

		    for i in range(0, n): 

		        s.add(arr[i])
		      
		    return (len(s) == len(arr))


		global color_list 
		color_list = []

		for i in range(4):

			color_list.append(random.choice(colors))

		while not distinct(color_list):

			color_list.clear()

			for i in range(4):

				color_list.append(random.choice(colors))

		def create_image(picture, iteration):

			dist = 1000/layers
			
			x_values, y_values = [], []

			for i in range(0, int(1001-dist), int(dist)):

				x_values.append(i)

			for i in range(0, int(1001-dist), int(dist)):

				y_values.append(i/2)

			for i in range(0, len(y_values)):

					y_values[i] += random.randint(y_values[i]-1, y_values[i]+dist-1)

			for i in range(0, len(x_values)):

				if i == len(x_values) - 1:

					if iteration == 1:

						picture.rectangle([x_values[i], 1000, x_values[i] + dist, 0], fill = color_list[0])

					else:

						picture.rectangle([x_values[i], 1000, x_values[i] + dist, 0], fill = color_list[2])

				else:

					if iteration == 1:

						picture.rectangle([x_values[i], 1000, x_values[i] + dist, 1000-y_values[i]], fill = color_list[0])
						picture.rectangle([x_values[i], 0, x_values[i] + dist, 1000-y_values[i]], fill = color_list[1])

					else:

						picture.rectangle([x_values[i], 1000, x_values[i] + dist, 1000-y_values[i]], fill = color_list[2])
						picture.rectangle([x_values[i], 0, x_values[i] + dist, 1000-y_values[i]], fill = color_list[3])


		create_image(image, 1)
		create_image(image2, 2)

		#the horizontal rectangles are less bright
		img2 = img2.rotate(90)
		img2.putalpha(100)

		img.paste(img2, (0, 0), img2)

	img.show()
	

#The two sets of functions that are organized into classes are defined here, and these are what the user would import to use either the math or SAT/ACT functions.
Math = mathClass()
standardizedTest = standardizedTestClass()


'''
Peer Feedback:

Enzo, 5/13 - Try putting in a bunch of data points with the SAT and ACT websites and using regression to come up with an equation instead of having 2 super long dictionaries.
'''