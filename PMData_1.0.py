print("PMData loading")
from tkinter import *
import json

def sep(template):
    r = 1440
    p = 0
    list = []
    for i in template:
        r = r - 1
        if r >= 0:
            p = p + float(i.get("value"))
        else:
            d = p
            list.append(d)
            r = 1440
            p = 0
    return list
def personsList(num):
    persons_list = []
    for i in range(1,num + 1):
        if i <= 9 :
            persons_list.append("p0"+str(i))
        else:
            persons_list.append("p"+str(i))
    return persons_list
def personsDict(persons_list):
    persons_dict = {}
    for i in persons_list:
        with open("pmdata/" + i + "/fitbit/calories.json")as calories_file:
            template = json.load(calories_file)
        calories_list = sep(template)

        with open("pmdata/" + i + "/fitbit/steps.json")as steps_file:
            steps_dict = json.load(steps_file)
        steps_list = sep(steps_dict)

        with open("pmdata/" + i + "/fitbit/distance.json")as distance_file:
            distance_dict = json.load(distance_file)
        distance_list = sep(distance_dict)
        dict = {'calories_list':calories_list, 'steps_list': steps_list, 'distance_list':distance_list}
        persons_dict.update({i:dict})
    return persons_dict
def line(list, cof, stepY, stepX, min_it, fill_color):
    x0 = 20 + stepX; y0 = 470 - stepY;
    xf = 20 + stepX; yf = 470 - stepY;
    step = 7.5
    for i in range(0, min_it):
        k = (list[i])/int(cof)
        yfk = yf - k
        x0 = x0 + step
        xf = x0 + step
        xa = xf
        xb = xa
        canv.create_line(x0, y0, xf, yfk, fill=fill_color)
        canv.create_line(xa, 475, xb, 460, fill="black")
        y0 = yfk
def drow(dict, min_it, stepX):
    coord(stepX)
    for i in dict:
        t = dict.get(i)
        line(t.get("calories_list"), 50, 0, stepX, min_it, "red")
        line(t.get("steps_list"), 420, 130, stepX, min_it,"blue")
        line(t.get("distance_list"), 35000, 280, stepX, min_it, "green")
def coord(stepX):
    canv.create_line(27 + stepX, 470, 1180, 470, fill="black", arrow=LAST)
    canv.create_line(27 + stepX, 470, 27 + stepX, 27, fill="black", arrow=LAST)
def lenLists(dict):
    mas = {}
    for i in dict:
        t = dict.get(i)
        mas.update({i:{'calories_list':len(t.get("calories_list")), 'steps_list':len(t.get("steps_list")), "distance_list":len(t.get("distance_list"))}})
    return mas
def minInLen(dict):
    min_len = []
    for i in dict:
        t = dict.get(i)
        for k in t:
            min_len.append(t.get(k))
    return min_len
def average(dict, min_it):
    average_calories_list = [0 for i in range(0, min_it)]
    average_steps_list = [0 for i in range(0, min_it)]
    average_distance_list = [0 for i in range(0, min_it)]
    for i in dict:
        t = dict.get(i)
        for k in range(0, min_it ):
            average_calories_list[k] = average_calories_list[k] + t.get("calories_list")[k]
            average_steps_list[k] = average_steps_list[k] + t.get("steps_list")[k]
            average_distance_list[k] = average_distance_list[k] + t.get("distance_list")[k]
    for i in range(0, min_it ):
        average_calories_list[i] = (average_calories_list[i]) / len(dict)
        average_steps_list[i] = (average_steps_list[i]) / len(dict)
        average_distance_list[i] = (average_distance_list[i]) / len(dict)
    average_person_dict = {}
    average_person_dict.update({'average_person':{'calories_list':average_calories_list, 'steps_list': average_steps_list,"distance_list": average_distance_list }})
    return average_person_dict
def steps_calories(dict, min_it, stepX):
    coord(stepX)



window = Tk()
window.title("PMData")
canv = Canvas(window, width=1200, height=500)
canv.pack()


persons_dict = personsDict(personsList(16))
persons_len_lists = lenLists(persons_dict)
min_it = min(minInLen(persons_len_lists))
drow(persons_dict, min_it, 0)
average_pd = average(persons_dict, min_it)
drow(average_pd, min_it, 280)
window.mainloop()