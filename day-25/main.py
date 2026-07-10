# with open("weather_data.csv") as csv_file:
# 	data = csv_file.readlines()

# import csv
#
# with open("weather_data.csv") as data_file:
# 	data = csv.reader(data_file)
# 	next(data)
# 	temperatures =  []
# 	for row in data:
# 		temperatures.append(int(row[1]))
#


# data = pandas.read_csv("weather_data.csv")
# #
# # temp_list = data["temp"].to_list()
# # def average_temp():
# # 	sum = 0
# # 	for temp in temp_list:
# # 		sum += temp
# # 	average = sum / len(temp_list)
# # 	rounded_average = round(average, 2)
# # 	print(rounded_average)
# # average_temp()


# #
# # print(data["temp"].max())
#
#
# monday = data[data.day == "Monday"]
# temp_mon = monday.temp[0]
# farenheit_temp = (temp_mon * 9/5) + 32
# print(farenheit_temp)

import pandas

df = pandas.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
grey_squirrels_count = len(df[df["Primary Fur Color"] == "Gray"])
red_squirrels_count = len(df[df["Primary Fur Color"] == "Cinnamon"])
black_squirrels_count = len(df[df["Primary Fur Color"] == "Black"])\

squirrel_table = {
	"Fur Color": ["Gray", "Cinnamon", "Black"],
	"Count": [grey_squirrels_count, red_squirrels_count, black_squirrels_count]
}

new_df = pandas.DataFrame(squirrel_table)

new_df.to_csv("squirrel_table.csv")