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
import random
names = ["Alex", "Beth", "Caroline", "Dave", "Eleanor", "Freddie"]

student_scores = {name:random.randint(1,101) for name in names}

passed_students = {
    new_key:score for score in student_scores if student_score[]
}