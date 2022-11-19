import random
import tkinter as tk
import cProfile
import re


class Game(tk.Frame):
    
    doors = ('a', 'b', 'c')

    def __init__(self, parent):
        """Инициализировать рамку"""
        super(Game, self).__init__(parent)  # родитель будет корневым окном
        self.parent = parent  
        self.img_file = 'all_closed.png'  # текущее изображение дверей
        self.choice = ''  # вариант двери, выбранный игроком
        self.winner = ''  # выйгрышная дверь
        self.reveal = ''  # раскрытая дверь
        self.first_choice_wins = 0  # счётчик для статистики
        self.pick_change_wins = 0  # счётчик для статистики
        self.create_widgets()

    def create_widgets(self):
        # создать надпись с изображением дверей
        img = tk.PhotoImage(file='all_closed.png')
        self.photo_lbl = tk.Label(self.parent, image=img, text='', borderwidth=0)
        self.photo_lbl.grid(row=0, column=0, columnspan=10, sticky='W')
        self.photo_lbl.image = img

        # создать надпись с инструкциями по игре
        instr_input = [
            ('За одной из дверей линчик', 1, 0, 5, 'W'),
            ('За остальными негр с автоматом', 2, 0, 5, 'W'),
            ('Выбрать дверку:', 1, 3, 1, 'E')
            ]
        for text, row, column, columnspan, sticky in instr_input:
            instr_lbl = tk.Label(self.parent, text=text)
            instr_lbl.grid(row=row, column=column, columnspan=columnspan,
                           sticky=sticky, ipadx=30)

        # создать радиокнопки для получения выбираемого пользователем начального варианта
        self.door_choice = tk.StringVar()
        self.door_choice.set(None)

        a = tk.Radiobutton(self.parent, text='A', variable=self.door_choice,
                           value='a', command=self.win_reveal)
        b = tk.Radiobutton(self.parent, text='B', variable=self.door_choice,
                           value='b', command=self.win_reveal)
        c = tk.Radiobutton(self.parent, text='C', variable=self.door_choice,
                           value='c', command=self.win_reveal)

        # создать виджеты для изменения вариантов выбора дверей
        self.change_door = tk.StringVar()
        self.change_door.set(None)
        
        instr_lbl = tk.Label(self.parent, text='Поменять дверки')
        instr_lbl.grid(row=2, column=3, columnspan=1, sticky='E')

        self.yes = tk.Radiobutton(self.parent, state='disabled', text='Y',
                                  variable=self.change_door, value='y',
                                  command=self.show_final)
        self.no = tk.Radiobutton(self.parent, state='disabled', text='N',
                                 variable=self.change_door, value='n',
                                 command=self.show_final)

        # создать текстовые виджеты для статистики выйгрышей
        defaultbg = self.parent.cget('bg')
        self.unchanged_wins_txt = tk.Text(self.parent, width=20,
                                          height=1, wrap=tk.WORD, bg=defaultbg,
                                          fg='black', borderwidth=0)
        self.changed_wins_txt = tk.Text(self.parent, width=20,
                                        height=1, wrap=tk.WORD, bg=defaultbg,
                                        fg='black', borderwidth=0)
        
        # поместить виджеты в рамку
        a.grid(row=1, column=4, sticky='W', padx=20)
        b.grid(row=1, column=4, sticky='N', padx=20)
        c.grid(row=1, column=4, sticky='E', padx=20)
        self.yes.grid(row=2, column=4, sticky='W', padx=20)
        self.no.grid(row=2, column=4, sticky='N', padx=20)
        self.unchanged_wins_txt.grid(row=1, column=5, columnspan=5)
        self.changed_wins_txt.grid(row=2, column=5, columnspan=5)

    def update_image(self):
        """обновить текущее изображение двери"""
        img = tk.PhotoImage(file=self.img_file)
        self.photo_lbl.configure(image=img)
        self.photo_lbl.image = img

    def win_reveal(self):
        """случайно выбрать выйгрышную дверь и раскрыть невыбранную дверь за которой спрятан нигер"""
        door_list = list(self.doors)
        self.choice = self.door_choice.get()
        self.winner = random.choice(door_list)

        door_list.remove(self.winner)

        if self.choice in door_list:
            door_list.remove(self.choice)
            self.reveal = door_list[0]
        else:
            self.reveal = random.choice(door_list)

        self.img_file = ('reveal_{}.png'.format(self.reveal))
        self.update_image()

        # активировать и очистить кнопки да\нет
        self.yes.config(state='normal')
        self.no.config(state='normal')
        self.change_door.set(None)

        # закрывать двери через 4 секунды после открытия
        self.img_file = 'all_closed.png'
        self.parent.after(4000, self.update_image)

    def show_final(self):
        """Раскрыть изображение за окончательно выбранной дверью и подсчитать выйгрыши"""
        door_list = list(self.doors)

        switch_doors = self.change_door.get()

        if switch_doors == 'y':
            door_list.remove(self.choice)
            door_list.remove(self.reveal)
            new_pick = door_list[0]
            if new_pick == self.winner:
                self.img_file = 'money_{}.png'.format(new_pick)
                self.pick_change_wins += 1
            else:
                self.img_file = 'goat_{}.png'.format(new_pick)
                self.first_choice_wins += 1
        elif switch_doors == 'n':
            if self.choice == self.winner:
                self.img_file = 'money_{}.png'.format(self.choice)
                self.first_choice_wins += 1
            else:
                self.img_file = 'goat_{}.png'.format(self.choice)
                self.pick_change_wins += 1

        # обновить изображение двери
        self.update_image()

        # обновить выводимую на экран статистику
        self.unchanged_wins_txt.delete(1.0, 'end')
        self.unchanged_wins_txt.insert(1.0, 'Unchanged wins = {:d}'
                                       .format(self.first_choice_wins))
        self.changed_wins_txt.delete(1.0, 'end')
        self.changed_wins_txt.insert(1.0, 'Changed wins = {:d}'
                                     .format(self.pick_change_wins))
        
        # деактивировать кнопки да\нет и очистить кнопки выбора дверей
        self.yes.config(state='disabled')
        self.no.config(state='disabled')
        self.door_choice.set(None)
        
        # закрывать двери через 4 секунды после открытия
        self.img_file = 'all_closed.png'
        self.parent.after(4000, self.update_image)


# настроить корневое окно и выполнить событийный цикл
root = tk.Tk()
root.title('Эта сидит чешет колоду')
root.geometry('1280x820')  # размерность изображений
game = Game(root)
root.mainloop()
cProfile.run('re.compile("foo|bar")')
