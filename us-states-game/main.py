import turtle
import pandas

#Winning message
GAME_WINNER_TEXT = "YOU WON!"
exit = "exit"
EXIT = exit.title()
#Creating the drawing turtle
drawer = turtle.Turtle()
drawer.hideturtle()
drawer.penup()

#Setting up the screen
screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

#Importing data from csv file
df_states = pandas.read_csv("50_states.csv")
state_col = df_states.state

# Game logic
game_is_on = True
score = 0
guessed_states = []
while game_is_on:

	#Get user's answer and convert it to Title Case
	answer_state = screen.textinput(title=f"{score}/50 States Correct", prompt="Enter a state's name")
	answer_state = answer_state.title()

	for state in state_col.to_list():
		if state == answer_state:
			row = df_states[df_states.state == answer_state]
			x_coor = row.x.item()
			y_coor = row.y.item()

			drawer.goto(x_coor, y_coor)
			drawer.write(answer_state, font=("Arial", 7, "normal"))

			# Update score and add state to list
			score += 1
			guessed_states.append(answer_state)
			#Checking if the game is over
			if score == 50:
				drawer.goto(-200,0)
				drawer.write(GAME_WINNER_TEXT, font=("Arial", 50, "bold"))
				game_is_on = False
	if answer_state == EXIT:
		game_is_on = False

not_guessed_states = [state for state in state_col.to_list() if state not in guessed_states]

missing_states = {
	"Missing States": not_guessed_states,
}


missed_df = pandas.DataFrame(missing_states)

missed_df.to_csv("missed_states.csv")