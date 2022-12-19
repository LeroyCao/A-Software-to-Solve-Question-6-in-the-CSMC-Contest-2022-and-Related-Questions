from tkinter import *
from tkinter import messagebox
from itertools import combinations
import numpy as np
import cv2
import tkinter.colorchooser
BallData={}# Sphere information dictionary. The key is the hexadecimal color, and the value is the number of spheres
targetColor=None#Target color ball
buttons = []#Sphere button
root = Tk()#main interface
'''
Select a color button on the main interface, 
and the button will pop up whether to confirm the color ball as the target color ball
'''
def choseTargetColor(color):
    global targetColor
    result = tkinter.messagebox.askokcancel(title='Notice', message='Whether to select the current color as the calculated color?')
    if(result):
        targetColor=color
        root.after(500, update)
'''
The main interface is refreshed. It is called when adding and updating the color and number of spheres
'''
def update():
    global targetColor
    buttonX = 0
    buttonY = 50
    buttonWith = 105
    buttons.clear()
    count=0
    #Draw all sphere information
    for key in BallData.keys():
        loadimage = PhotoImage(file="./" + key + ".png")
        buttons.append(loadimage)
        buttons.append(count)
        if(targetColor!=None and targetColor==key):
            roundedbutton = Button(root, bg='red', image=loadimage,command=lambda key = key: choseTargetColor(key))
        else:
            roundedbutton = Button(root,image=loadimage,command=lambda key = key: choseTargetColor(key))
        roundedbutton.place(x=buttonX,  y=buttonY, anchor='w')
        buttonX += buttonWith
        count+=1
        if (count % 5 == 0):
            buttonX = 0
            buttonY += 110
    #Finally, add a button to add a new sphere
    addfill = PhotoImage(file="./add.png")
    buttons.append(addfill)
    addfillbutton = Button(root, image=addfill,command=callback)
    addfillbutton.pack()
    addfillbutton.place(x=buttonX, y=buttonY,width=102,height=102, anchor='w')
'''
Convert the hex of color to rgb
'''
def hex_to_rgb(value):
    hex = value.lstrip('#')
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)
    return (b,g,r)
'''
Call to generate a picture of a sphere and number after selecting a color
'''
def getButtonPig(color,num):
    # Create a white background picture
    d = 100
    img = np.ones((d, d, 3), np.uint8) * 255

    #Center point
    center_x = 50
    center_y = 50

    #Radius and color
    radius = 50
    cv2.circle(img, (center_x, center_y), radius, hex_to_rgb(color),-1)
    cv2.putText(img, num, (30, 60), 0, 1, (0, 0, 255), 2, cv2.LINE_AA, False)
    # Show Results
    cv2.imwrite('./'+color+'.png', img)
    cv2.waitKey()
    cv2.destroyAllWindows()
'''
New Sphere Button Setting Form
'''
def callback():
    top = Toplevel()
    top.title("Add new ball color and quantity")
    top.geometry("250x130")
    text = Text(top, width=20, height=2)
    text.place(x=100, y=10)
    #Choose a sphere color
    def ChooseColor():
        r = tkinter.colorchooser.askcolor(title='ColorSelector')
        text.delete('1.0', 'end')
        text.insert('end', r[1])
    colorButton = Button(top, text='ColorSelector', anchor='w', command=ChooseColor)
    colorButton.place(width=86, height=35, x=10, y=10)  #
    l = Label(top,text="Numberofballs",width=12,height=1)
    l.place(x=10,y=50)
    textNum = Text(top, width=20, height=2)
    textNum.place(x=100, y=50)
    #Deterministic function
    def setBallColorAndCount():
        color = text.get("1.0", "end-1c")  # 获取文本输入框的内容
        num = textNum.get("1.0", "end-1c")  # 获取文本输入框的内容
        if (color == ''):
            messagebox.showinfo(title='Notice', message='Choose the color of the ball')
            return
        if (num == '' or num.isdigit()==False):
            messagebox.showinfo(title='Notice', message='The number of spheres must not be empty and must be a number')
            return
        getButtonPig(color,num)
        BallData[color]=num
        top.destroy()
        root.after(1000, update)
    #Cancel Function
    def cancel():
        text.delete('1.0', 'end')
        textNum.delete('1.0', 'end')
        top.destroy()

    okButton = Button(top, padx=1, pady=1, text='ok', anchor='w', command=setBallColorAndCount)
    okButton.place(width=80, height=30, x=110, y=90)
    cancelButton = Button(top, padx=1, pady=1, text='cancel', anchor='w', command=cancel)
    cancelButton.place(width=80, height=30, x=10, y=90)
    top.grab_set()  # modal

'''
Main function: create the main interface and display
'''
def mian():
    global BallData
    global targetColor

    root.title("Probability of pumping out first")
    root.geometry("600x400")
    update()#Draw interface information
    textNums = Text(root, width=20, height=2)
    textNums.place(x=260, y=330)
    longtext = '''
        Input the number of colors and define the number of balls in each color.Then choose a 
        color. After that, the software should calculate the answer for the following case:
        Consider balls in different colors are sorted by colors and then put into bags respectively. 
        The balls are chosen randomly and removed one at a time from the bag until all the balls 
        are removed.One color of balls is the first to have 0 remaining in the bag. What is the
        probability that this color is the chosen one?The answer will be displayed in the bottom 
        right corner.'''
    textLabel = Label(root, text=longtext, anchor="w", justify="left")
    textLabel.pack(side=LEFT)
    textLabel.place(x=10, y=160)
    '''
    Main algorithm function, calculate the probability according to the selected sphere
    '''
    def calculations():
        global BallData
        global targetColor
        if(targetColor==None):
            messagebox.showinfo(title='Notice',
                                message='Click the sphere button on the interface. Select Target Sphere')
            return
        length = len(BallData)
        data = []
        tData = int(BallData[targetColor])
        for key in BallData:
            if key != targetColor:
                data.append(int(BallData[key]))
        result = 0
        for i in range(length):
            a = (-1) ** i
            temp = 0
            for c in combinations(data, i + 1):
                temp += sum(c) / (tData + sum(c))
            result += a * temp
        textNums.delete('1.0', 'end')
        textNums.insert('end', round(result, 3))
    #Calculation Function Button
    calculation = Button(root, padx=1, pady=1,bg='grey', text='calculation', anchor='w',command=lambda:calculations())
    calculation.place( x=180, y=330)
    root.mainloop()
mian()