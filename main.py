import csv
import datetime
import os
import shutil
import tkinter as tk
from collections import Counter
from tkinter import filedialog
from tkinter import font

from matplotlib import pyplot as plt

import glob
from PIL import Image, ImageTk


class LocationPieChartStatistics(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        bigfont = font.Font(size=20)

        self.stats_label = tk.Label(self, text="Статистика", font=bigfont)
        self.stats_label.grid(row=0, column=0, padx=5, pady=5)

        self.update_stats()

    def update_stats(self):
        with open('observations.csv', 'r', newline='') as csvfile:
            fieldnames = ['text', 'photo_path', 'coordinates']
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)

            location_counter = Counter()

            for row in reader:
                location_counter[row['coordinates']] += 1

            locations = list(location_counter.keys())
            counts = list(location_counter.values())
            plt.pie(counts, labels=locations, autopct='%1.1f%%')
            plt.title('Статистика по местам наблюдений')
            plt.show()


class PieChartStatistics(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        bigfont = font.Font(size=20)

        self.stats_label = tk.Label(self, text="Статистика", font=bigfont)
        self.stats_label.grid(row=0, column=0, padx=5, pady=5)

        self.update_stats()

    def update_stats(self):
        with open('observations.csv', 'r', newline='') as csvfile:
            fieldnames = ['text', 'photo_path', 'coordinates']
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)

            bird_counter = Counter()

            for row in reader:
                bird_counter[row['text']] += 1

            birds = list(bird_counter.keys())
            counts = list(bird_counter.values())
            plt.pie(counts, labels=birds, autopct='%1.1f%%')
            plt.title('Статистика по видам птиц')
            plt.show()


class Gallery(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        self.images = glob.glob('app_photos/*')
        self.current_image = 0
        self.master.geometry("465x380")

        self.prev_button = tk.Button(self, text="Предыдущее", command=self.prev_image)
        self.prev_button.grid(row=2, column=0, padx=5, pady=5)

        self.display_image()

        self.next_button = tk.Button(self, text="Следующее", command=self.next_image)
        self.next_button.grid(row=2, column=2, padx=5, pady=5)

    def display_image(self):
        pil_image = Image.open(self.images[self.current_image])
        pil_image = pil_image.resize((250, 250), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(pil_image)
        if hasattr(self, 'image_label'):
            self.image_label.destroy()
        self.image_label = tk.Label(self, image=tk_image)
        self.image_label.image = tk_image
        self.image_label.grid(row=0, column=1, padx=5, pady=5)

        bird_name = os.path.basename(self.images[self.current_image]).split('.')[0]
        if hasattr(self, 'name_label'):
            self.name_label.destroy()
        self.name_label = tk.Label(self, text=bird_name)
        self.name_label.grid(row=1, column=1, padx=5, pady=5)

    def prev_image(self):
        self.current_image = (self.current_image - 1) % len(self.images)
        self.display_image()

    def next_image(self):
        self.current_image = (self.current_image + 1) % len(self.images)
        self.display_image()


class BirdObservation:
    def __init__(self, text, photo_path, coordinates):
        self.text = text
        self.photo_path = photo_path
        self.coordinates = coordinates


class Statistics(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        bigfont = font.Font(size=20)

        self.stats_label = tk.Label(self, text="Статистика", font=bigfont)
        self.stats_label.grid(row=0, column=0, padx=5, pady=5)

        self.update_stats()

    def update_stats(self):
        with open('observations.csv', 'r', newline='') as csvfile:
            fieldnames = ['text', 'photo_path', 'coordinates']
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)

            bird_counter = Counter()

            for row in reader:
                bird_counter[row['text']] += 1

            birds = list(bird_counter.keys())
            counts = list(bird_counter.values())
            plt.bar(birds, counts)
            plt.title('Статистика по видам птиц')
            plt.xlabel('Виды птиц')
            plt.ylabel('Количество наблюдений')
            plt.show()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("440x620")
        self.grid(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        bigfont = font.Font(size=20)

        my_width = 25

        self.text_entry = tk.Entry(self, width=my_width)
        self.text_entry['font'] = bigfont
        self.text_entry.insert(0, "вид птицы")
        self.text_entry.bind("<FocusIn>",
                             lambda args: self.text_entry.delete('0', 'end'))
        self.text_entry.grid(row=0, column=0, padx=5, pady=5)

        self.photo_button = tk.Button(self, text="Выберите фото",
                                      command=self.select_photo,
                                      font=bigfont, width=my_width)
        self.photo_button.grid(row=1, column=0, padx=5, pady=5)

        self.coordinates_entry = tk.Entry(self, width=my_width)
        self.coordinates_entry['font'] = bigfont
        self.coordinates_entry.insert(0, "парк/место")
        self.coordinates_entry.bind("<FocusIn>", lambda args: self.coordinates_entry.delete('0', 'end'))
        self.coordinates_entry.grid(row=2, column=0, padx=5, pady=5)

        self.save_button = tk.Button(self, text="Сохранить наблюдение", command=self.save_observation,
                                     font=bigfont, width=20)
        self.save_button.grid(row=3, column=0, padx=5, pady=5)

        self.space_label = tk.Label(self, text="", height=3)
        self.space_label.grid(row=4, column=0)

        self.gallary_button = tk.Button(self, text="Галлерея",
                                        command=self.show_gallary,
                                        font=bigfont, width=my_width)
        self.gallary_button.grid(row=5, column=0, padx=5, pady=5)

        self.stats_button = tk.Button(self, text="Стобчатая диаграмма (птицы)",
                                      command=self.show_stats,
                                      font=bigfont, width=my_width)
        self.stats_button.grid(row=6, column=0, padx=5, pady=5)

        self.pie_chart_stats_button = tk.Button(self, text="Круговая диаграмма (птицы)",
                                                command=self.show_pie_chart_stats,
                                                font=bigfont, width=my_width)
        self.pie_chart_stats_button.grid(row=7, column=0, padx=5, pady=5)

        self.location_pie_chart_stats_button = tk.Button(self, text="Круговая диаграмма (места)",
                                                         command=self.show_location_pie_chart_stats,
                                                         font=bigfont, width=my_width)
        self.location_pie_chart_stats_button.grid(row=8, column=0, padx=5, pady=5)

        self.import_button = tk.Button(self, text="Импорт статистики в txt файл",
                                       command=self.import_observations,
                                       font=bigfont, width=my_width)
        self.import_button.grid(row=9, column=0, padx=5, pady=5)

        self.quit = tk.Button(self, text="ВЫХОД", fg="red",
                              command=self.master.destroy,
                              font=bigfont, width=my_width)
        self.quit.grid(row=10, column=0, padx=5, pady=5)

    def select_photo(self):
        self.photo_path = filedialog.askopenfilename()

    def save_observation(self):
        text = self.text_entry.get()
        coordinates = self.coordinates_entry.get()
        new_photo_path = os.path.join('app_photos', os.path.basename(self.photo_path))
        if not os.path.exists('app_photos'):
            os.makedirs('app_photos')
        shutil.copy(self.photo_path, new_photo_path)
        observation = BirdObservation(text, new_photo_path, coordinates)
        with open('observations.csv', 'a', newline='') as csvfile:
            fieldnames = ['text', 'photo_path', 'coordinates']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'text': observation.text, 'photo_path': observation.photo_path,
                             'coordinates': observation.coordinates})

    def show_stats(self):
        self.stats_screen = tk.Toplevel(self)
        self.stats_app = Statistics(master=self.stats_screen)

    def show_gallary(self):
        self.gallary_screen = tk.Toplevel(self)
        self.gallary_app = Gallery(master=self.gallary_screen)

    def show_pie_chart_stats(self):
        self.pie_chart_stats_screen = tk.Toplevel(self)
        self.pie_chart_stats_app = PieChartStatistics(master=self.pie_chart_stats_screen)

    def show_location_pie_chart_stats(self):
        self.location_pie_chart_stats_screen = tk.Toplevel(self)
        self.location_pie_chart_stats_app = LocationPieChartStatistics(master=self.location_pie_chart_stats_screen)

    def import_observations(csv_file):
        with open('observations.csv', 'r', newline='') as csvfile:
            fieldnames = ['text', 'photo_path', 'coordinates']
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            observations = [row for row in reader]

        print(observations)
        places = dict()
        for o in observations:
            if o['coordinates'] not in places:
                places[o['coordinates']] = dict()
                places[o['coordinates']][o['text']] = 1
            else:
                if o['text'] in places[o['coordinates']]:
                    places[o['coordinates']][o['text']] += 1
                else:
                    places[o['coordinates']][o['text']] = 1

        print(places)

        txt_file = f"{datetime.date.today()}_observations.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            for p in places.items():
                f.write(f"{str(p[0]).capitalize()}\n")
                for b in p[1].items():
                    f.write(f"\t{b[0]} x {b[1]}\n")
                    f.write(os.linesep)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
