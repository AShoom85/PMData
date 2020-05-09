print("PMData loading")
from tkinter import *
import json

class BuildGraph:
    """name - str, point_zero - [x,y], values_x - [], values_y - [], factor - [x, y], color - str """
    def __init__(self, name, point_zero, values_x, values_y, factor, canvas, color):
        self.name = name
        self.point_zero = point_zero
        self.values_x = values_x
        self.values_y = values_y
        self.factor = factor
        self.canvas = canvas
        self.color = color

    def draw_graph(self):
        x0 = self.point_zero[0]
        y0 = self.point_zero[1]
        xf = x0
        yf = y0
        for i in range(len(self.values_x)):
            self.canvas.create_line(x0, y0, xf, yf, fill=self.color)
            xf = x0
            yf = y0
            x0 = self.point_zero[0] + int(self.values_x[i])/int(self.factor[0])
            y0 = self.point_zero[1] - int(self.values_y[i])/int(self.factor[1])

    def draw_coord_sys(self):
        if (self.point_zero[0] + int(min(self.values_x)) / int(self.factor[0])) < self.point_zero[0]:
            self.point_zero[0] = (self.point_zero[0] + int(min(self.values_x)) / int(self.factor[0])) + 40
            self.canvas.create_line(self.point_zero[0], self.point_zero[1], (
                             self.point_zero[0] + int(min(self.values_x)) / int(self.factor[0])) + 40,
                             self.point_zero[1], fill="black")
            self.canvas.create_line(self.point_zero[0], self.point_zero[1], (
                             self.point_zero[0] + int(max(self.values_x)) / int(self.factor[0])) + 40,
                             self.point_zero[1], fill="black")
        else:
            self.canvas.create_line(self.point_zero[0], self.point_zero[1], (
                             self.point_zero[0] + int(max(self.values_x)) / int(self.factor[0])) + 40,
                             self.point_zero[1], fill="black")
        if (self.point_zero[1] - int(min(self.values_y)) / int(self.factor[1])) > self.point_zero[1]:
            self.point_zero[1] = (self.point_zero[1] - int(min(self.values_y)) / int(self.factor[1])) - 40
            self.canvas.create_line(self.point_zero[0], self.point_zero[1], self.point_zero[0], (
                                 self.point_zero[1] - int(min(self.values_y)) / int(self.factor[1])) - 40,
                                 fill="black")
            self.canvas.create_line(self.point_zero[0], self.point_zero[1], self.point_zero[0], (
                    self.point_zero[1] - int(max(self.values_y)) / int(self.factor[1])) - 40,
                                    fill="black")
        else:
            self.canvas.create_line(self.point_zero[0], self.point_zero[1], self.point_zero[0], (
                    self.point_zero[1] - int(max(self.values_y)) / int(self.factor[1])) - 40,
                                    fill="black")
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
    for i in range(1, num + 1):
        if i <= 9:
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
        persons_dict.update({i: {'calories_list': calories_list,
                                 'steps_list': steps_list, 'distance_list': distance_list}})
    return persons_dict
def lenLists(dict):
    mas = {}
    for i in dict:
        t = dict.get(i)
        mas.update({i: {'calories_list': len(t.get("calories_list")),
                        'steps_list': len(t.get("steps_list")),
                        'distance_list': len(t.get("distance_list"))}})
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
        for k in range(0, min_it):
            average_calories_list[k] = average_calories_list[k] + t.get("calories_list")[k]
            average_steps_list[k] = average_steps_list[k] + t.get("steps_list")[k]
            average_distance_list[k] = average_distance_list[k] + t.get("distance_list")[k]
    for i in range(0, min_it):
        average_calories_list[i] = (average_calories_list[i]) / len(dict)
        average_steps_list[i] = (average_steps_list[i]) / len(dict)
        average_distance_list[i] = (average_distance_list[i]) / len(dict)
    average_person_dict = {}
    average_person_dict.update({'average_person': {'calories_list': average_calories_list,
                                                   'steps_list': average_steps_list,
                                                   'distance_list': average_distance_list}})
    return average_person_dict
def build_all_graph(dict, range_graph, name_taxt, can):

    for i in dict:
        t = dict.get(i)
        if range_graph == 1:
            calories_range = len(t.get('calories_list'))
        else:
            calories_range = range_graph
        person = BuildGraph(i, [30, 470], [i * 7.5 for i in range(calories_range)],
                            t.get('calories_list'), [1, 64], can, "red")
        person.draw_graph()
        can.create_text(200, 480, text=name_taxt + " calories graph", fill="black")
        person.draw_coord_sys()

    for i in dict:
        t = dict.get(i)
        if range_graph == 1:
            steps_range = len(t.get('steps_list'))
        else:
            steps_range = range_graph
        person = BuildGraph(i, [30, 330], [i * 7.5 for i in range(steps_range)],
                            t.get('steps_list'), [1, 540], can, "blue")
        person.draw_graph()
        can.create_text(200, 340, text=name_taxt + " steps graph", fill="black")
        person.draw_coord_sys()

    for i in dict:
        t = dict.get(i)
        if range_graph == 1:
            distance_range = len(t.get('distance_list'))
        else:
            distance_range = range_graph
        person = BuildGraph(i, [30, 180], [i * 7.5 for i in range(distance_range)],
                            t.get('distance_list'), [1, 42000], can, "green")
        person.draw_graph()
        can.create_text(200, 190, text=name_taxt + " distance graph", fill="black")
        person.draw_coord_sys()
def draw_text(can, x, y, z, path ):
    with open(path, 'r', encoding='utf-8') as t:
        Text_read = t.read()
    can.create_text(x, y, text=Text_read, justify= z, fill="black")

def run(can):
    global num
    if num >= 4:
        can.delete("all")
        draw_text(can, 600, 250, CENTER, "Text0.txt")
        num = 0
    elif num == 0:
        can.delete("all")
        build_all_graph(persons_dict, 1, "All persons", can)
        num = 1
    elif num == 1:
        can.delete("all")
        build_all_graph(persons_dict, min_it, "All persons", can)
        draw_text(can, 780, 280, LEFT, "Text1.txt")
        num = 2
    elif num == 2:
        can.delete("all")
        build_all_graph(average_pd, min_it, "Average", can)
        draw_text(can, 780, 280, LEFT, "Text2.txt")
        num = 3
    elif num == 3:
        can.delete("all")
        steps_calories_graph = BuildGraph('AveragePD', [30, 470],
                                          average_pd.get('average_person').get('calories_list'),
                                          average_pd.get('average_person').get('steps_list'),
                                          [8, 90], can, "blue")
        steps_calories_graph.draw_graph()
        steps_calories_graph.draw_coord_sys()
        draw_text(can, 850, 250, LEFT, "Text3.txt")
        num = 4


num = 0
window = Tk()
window.title("PMData")
Button_next = Button(window, text="NEXT", width=170,
                     height=3, bg="white", fg="black",
                     activebackground="#555555", activeforeground="#ffffff")
can = Canvas(window, width=1200, height=500)
can.pack()
Button_next.bind("<Button-1>", lambda event: run(can))
Button_next.pack(side='bottom')

persons_dict = personsDict(personsList(16))
persons_len_lists = lenLists(persons_dict)
min_it = min(minInLen(persons_len_lists))
average_pd = average(persons_dict, min_it)

draw_text(can, 600, 250, CENTER, "Text0.txt")

window.mainloop()


