from tools import get_platiarism, get_text_from_file
k = 15  # Размер k-грамм
q = 259
w = 4

from tkinter import *
from tkinter import filedialog as fd

class VideoSystem(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")

        self.parent = parent
        self.width = self.winfo_screenwidth()  # Ширина экрана
        self.height = self.winfo_screenheight()  # Высота экрана

        self.parent.title("DetectPlagiarismMoss")
        self.pack(fill=BOTH, expand=True)

        self.file1 = 'file1'
        self.file2 = 'file2'

        self.create_main_menu()  # Создаем главное меню

    def choice_f1(self):
        self.file1 = fd.askopenfilename(defaultextension='.cpp', filetypes=[('CPP', '.cpp'),('TXT', '.txt'), ('Py', '.py')])
        self.text_info_menu['text'] = "Загрузите\n {}\n {}:".format(self.file1, self.file2)
        
    def choice_f2(self):
        self.file2 = fd.askopenfilename(defaultextension='.cpp', filetypes=[('CPP', '.cpp'),('TXT', '.txt'),('Py', '.py')])   
        self.text_info_menu['text'] = "Загрузите\n {}\n {}:".format(self.file1, self.file2)

    def analyze(self):
        self.text.tag_config('warning', background="green",)
        text1 = get_text_from_file(self.file1)
        mergedPoints = get_platiarism(self.file1, self.file2, k, q, w)
        newCode = text1[: mergedPoints[0][0]]
        self.text.insert('end', newCode)
        plagCount = 0
        for i in range(len(mergedPoints)):
            if mergedPoints[i][1] > mergedPoints[i][0]:
                plagCount += mergedPoints[i][1] - mergedPoints[i][0]
                newCode = newCode + '|||\x1b[6;30;42m' + text1[mergedPoints[i][0] : mergedPoints[i][1]] + '\x1b[0m|||'
                self.text.insert('end', text1[mergedPoints[i][0] : mergedPoints[i][1]], 'warning')
                if i < len(mergedPoints) - 1:
                    newCode = newCode + text1[mergedPoints[i][1] : mergedPoints[i+1][0]]
                    self.text.insert('end', text1[mergedPoints[i][1] : mergedPoints[i+1][0]])
                else:
                    newCode = newCode + text1[mergedPoints[i][1] :]
                    self.text.insert('end', text1[mergedPoints[i][1] :])
        print(newCode)
        self.text_plagiarism['text'] = "Плагиат в файле {} : {}%".format(self.file1, int(100 * plagCount/len(text1)))
        #self.text.insert(1.0, newCode)


    def create_main_menu(self):
        frame1 = Frame(self)
        frame1.pack(fill=X)
        frame1.config(bg="white")
        self.text_info_menu = Label(frame1, text="Загрузите {} {}:".format(self.file1, self.file2), font=("Arial Bold", 20))
        self.text_info_menu.config(bg="white")
        self.text_info_menu.pack()

        choice_file2 = Button(frame1, text="Файл №2", command=self.choice_f2)
        choice_file2.pack(side=RIGHT, expand=True)
        choice_file1 = Button(frame1, text="Файл №1", command=self.choice_f1)
        choice_file1.pack(side=RIGHT, expand=True)
        self.text_plagiarism = Label(frame1, text="Плагиат в файле {} : {}".format("",0), font=("Arial Bold", 20))
        self.text_plagiarism.config(bg="white")
        self.text_plagiarism.pack()
        
        frame2 = Frame(self)
        frame2.pack(fill=X)
        frame2.config(bg="white")
        analyze = Button(frame2, text="Обработать", command=self.analyze)
        analyze.pack(expand=True)

        self.text = Text(frame2, width=int(self.width * 0.75), height=int(self.height*0.5))
        self.text.pack()
 



        
def main():
    root = Tk()
    root.geometry("{}x{}".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    app = VideoSystem(root)
    root.mainloop()

if __name__ == '__main__':
    main()