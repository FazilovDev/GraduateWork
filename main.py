from Algorithms.Winnowing import get_fingerprints, get_text_from_file
from tkinter import *
from tkinter import filedialog as fd
import locale

k = 15
q = 259#259
w = 4

class PlagiarismDetect(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")

        self.parent = parent
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()

        self.parent.title("DetectPlagiarismMoss")
        self.pack(fill=BOTH, expand=True)

        self.file1 = 'file1'
        self.file2 = 'file2'

        self.create_main_menu()

    def choice_f1(self):
        self.file1 = fd.askopenfilename(defaultextension='.cpp', filetypes=[('CPP', '.cpp'),('TXT', '.txt'), ('Py', '.py')])
        self.text_info_menu['text'] = "Загрузите\n {}\n {}:".format(self.file1, self.file2)
        
    def choice_f2(self):
        self.file2 = fd.askopenfilename(defaultextension='.cpp', filetypes=[('CPP', '.cpp'),('TXT', '.txt'),('Py', '.py')])   
        self.text_info_menu['text'] = "Загрузите\n {}\n {}:".format(self.file1, self.file2)
    
    def print_file1(self,text, points, side):
        newCode = text[: points[0][0]]
        if side == 0:
            textfield = self.text1
        else:
            textfield = self.text2
        textfield.insert('end', newCode)
        plagCount = 0
        for i in range(len(points)):
            if points[i][1] > points[i][0]:
                plagCount += points[i][1] - points[i][0]
                newCode = newCode  + text[points[i][0] : points[i][1]]
                textfield.insert('end', text[points[i][0] : points[i][1]], 'warning')
                if i < len(points) - 1:
                    newCode = newCode + text[points[i][1] : points[i+1][0]]
                    textfield.insert('end', text[points[i][1] : points[i+1][0]])
                else:
                    newCode = newCode + text[points[i][1] :]
                    textfield.insert('end', text[points[i][1] :])
        return plagCount / len(text)

    def analyze(self):
        self.text1.tag_config('warning', background="orange",)
        self.text2.tag_config('warning', background="orange")
        text1 = get_text_from_file(self.file1)
        text2 = get_text_from_file(self.file2)

        mergedPoints = get_fingerprints(self.file1, self.file2, k, q, w)
        res = self.print_file1(text1, mergedPoints[0], 0)
        res1 = self.print_file1(text2, mergedPoints[1], 1)
        self.text_plagiarism['text'] = "Уникальность файла: {} : {}%\nУникальность файла: {} : {}%".format(self.file1.split('/')[-1::][0], int((1-res)*100), self.file2.split('/')[-1::][0], int((1-res1)*100))



    def create_main_menu(self):
        frame1 = Frame(self)
        frame1.pack(fill=X)
        frame1.config(bg="white")
        self.text_info_menu = Label(frame1, text="Загрузите \n{} \n{}:".format(self.file1, self.file2), font=("Arial Bold", 20))
        self.text_info_menu.config(bg="white")
        self.text_info_menu.pack()

        self.text_plagiarism = Label(frame1, text="Уникальность файла: {} : {}%\nУникальность файла: {} : {}%".format("",0, "", 0), font=("Arial Bold", 20))
        self.text_plagiarism.config(bg="white")
        self.text_plagiarism.pack()
        choice_file2 = Button(frame1, text="Файл №2", command=self.choice_f2)
        choice_file2.pack(side=RIGHT, expand=True)
        choice_file1 = Button(frame1, text="Файл №1", command=self.choice_f1)
        choice_file1.pack(side=RIGHT, expand=True)
        
        frame2 = Frame(self)
        frame2.pack(fill=X)
        frame2.config(bg="white")
        analyze = Button(frame2, text="Обработать", command=self.analyze)
        analyze.pack()

        frame3 = Frame(self)
        frame3.pack(fill=X)
        frame3.config(bg="white")
        self.text1 = Text(frame3, width=int(100), height=int(100))
        self.text1.pack(side=LEFT)
        self.text2 = Text(frame3, width=int(100), height=int(100))
        self.text2.pack(side=LEFT)



        
def main():
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF8')
    root = Tk()
    root.geometry("{}x{}".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    app = PlagiarismDetect(root)
    root.mainloop()

if __name__ == '__main__':
    main()