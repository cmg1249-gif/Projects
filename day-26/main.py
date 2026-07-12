# numbers = [1,2,3]
#
# # new_list=[]
# #
# # for n in numbers:
# #     add_1 = n  + 1
# #     new_list.append(add_1)
#
# new_list = [n +1 for n in numbers]
#
# new_range = [i * 2 for i in range(1,5)]
# print(new_range)
#
#
# import random
# names = ["Alex", "Beth", "Caroline", "Dave", "Eleanor", "Freddie"]
#
# student_scores = {name:random.randint(1,101) for name in names}
#
# passed_students = {
#     key:value for (key, value) in student_scores.items() if value > 60
# }
# print(passed_students)

# string = "This is a string"
# print(string)
# split = string.split()
# print(split)

# student_dict = {
#     "student": ["Angela", "James", "Lily"],
#     "score": [56, 76 ,98]
#     }
#
# # for (key, value) in student_dict.items():
# #     print (value)
#
# import pandas
#
# student_data_frame = pandas.DataFrame(student_dict)
#
#
# # for (key, value) in student_data_frame.items():
# #     print(key)
# #     print(value)
#
# for (index, row) in student_data_frame.iterrows():
#     print(row.score


           )
