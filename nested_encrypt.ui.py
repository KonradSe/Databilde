from tkinter import *
from PIL import Image,ImageTk
import math
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import tkinter.scrolledtext as st

tegn=[]
for a in range(155):
    if a<94:tegn.append(chr(a+33))
    else:tegn.append(chr(a+99))
tegn.append(' ')
tegn.append('\n')

root = Tk()
root.title='ape'
root.geometry('500x650')
bg_color="#bcaa99"
txt_color="#552222"
title_font=('times', 24)
title_font2=('times', 20)
font2=('times', 15)
font3=('times', 13)
root.config(bg=bg_color)
title=Label(root,text='Tekst til Bilde encrypter', font=title_font,bg=bg_color,fg=txt_color)
#title.grid(row=0,column=0, columnspan=3,padx=5,pady=5)
title.place(x=50,y=20,width=400)
canvas_de = Canvas(root, width=250, height=275,bg=bg_color)
canvas_de.place(x=0,y=75,width=250, height=275)
canvas_en = Canvas(root, width=250, height=275,bg=bg_color)
canvas_en.place(x=250,y=75,width=250, height=275)
canvas_b = Canvas(root, width=510, height=500,bg=bg_color)
canvas_b.place(x=0,y=345,width=510, height=800)
imagemade=False
image2made=False
img = Image.new('RGB', (10,10))
tk_image = ImageTk.PhotoImage(img)
label = Label(canvas_en, image=tk_image)
tk_image1 = ImageTk.PhotoImage(img)
label1 = Label(canvas_de, image=tk_image1)
img2=""
filename=""


text_area = st.ScrolledText(canvas_b,width = 480, height = 16, font = font3,bg=bg_color)
text_area.place(x=10,y=0,width=480)
text_area.insert(INSERT,"")
text_area.configure(state ='disabled')


def les_bilde():
    global filename
    global text_area
    img = Image.open(filename)

    pixels = img.load()
    tekst="Melding: "
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]

            if r>200:ind_r=int(r-100)
            else:ind_r=int(r/2)
            if g>200:ind_g=int(g-100)
            else:ind_g=int(g/2)
            if b>200:ind_b=int(b-100)
            else:ind_b=int(b/2)
            tekst+=tegn[ind_r]+tegn[ind_g]+tegn[ind_b]
    #translation.config(text=tekst)
    text_area.configure(state='normal')
    text_area.delete('1.0', END) 
    text_area.insert(INSERT,tekst)
    text_area.configure(state='disabled')

def skriv_bilde(tekst,name="bilde"):   
    global imagemade
    while len(tekst)%3!=0:
        tekst+=' '
    pixels=(len(tekst)/3)
    dimen=[(x, pixels//x) for x in range(1, 1+int(math.sqrt(pixels))) if pixels % x == 0]
    dim= dimen[-1]
    
    pixels2=(len(tekst)/3)+1
    dimen2=[(x, pixels2//x) for x in range(1, 1+int(math.sqrt(pixels2))) if pixels2 % x == 0]
    dim2= dimen2[-1]
    if dim[1]-dim[0]>dim2[1]-dim[0]:
        tekst+=' '*3
        pixels=(len(tekst)/3)
        dimen=[(x, pixels//x) for x in range(1, 1+int(math.sqrt(pixels))) if pixels % x == 0]
        dim= dimen[-1]

    # Lag et tomt bilde
    img = Image.new('RGB', (int(dim[0]), int(dim[1])))

    # Lag et tomt pikselrutenett
    pixels = img.load()

    # Fyll pikselrutenettet med farger
    for i in range(img.width):
        for j in range(img.height):
            index=(i*img.height+j)*3
            ind=tegn.index(tekst[index])
            if ind>100:ind_r=ind+100
            else:ind_r=ind*2
            ind=tegn.index(tekst[index+1])
            if ind>100:ind_g=ind+100
            else:ind_g=ind*2
            ind=tegn.index(tekst[index+2])
            if ind>100:ind_b=ind+100
            else:ind_b=ind*2

            pixels[i, j] = (ind_r,ind_g,ind_b)
    navn=name+'.png'
    #img.save(navn)
    height=10*int(dim[1])
    width=10*int(dim[0])

    if height>100:
        height=100
    if width>100:
        width=100
    global img2
    img2=img
    newimg=img.resize((width,height),resample=Image.Resampling.NEAREST)
    tk_image = ImageTk.PhotoImage(newimg)
    # Create a label to display the image
    label.image = tk_image
    label.config(image=tk_image)
    if imagemade ==False:
        #label = Label(root, image=tk_image)
        label.grid(row=4, column=1,padx=1,pady=1)
        Label(canvas_en, text="Image created!").grid(row=5, column=1,padx=1,pady=1)
        imagemade=True
        button = Button(canvas_en, text="Save Image", command=download_file)
        button.grid(row=6, column=1,padx=1,pady=1)

def lag_bilde():
    # Get the text from the entry field
    text = entry.get()
    # Call the skriv_bilde function to create the image from the text
    skriv_bilde(text, "bilder/melding4")
    # Show a message to the user indicating that the image was created

def upload_file():
    global img
    global image2made
    global filename
    f_types = [('PNG Files', '*.png')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = Image.open(filename)

    newimg=img.resize((100,100),resample=Image.Resampling.NEAREST)
    tk_image = ImageTk.PhotoImage(newimg)
    label1.image = tk_image
    label1.config(image=tk_image)
    if image2made ==False:
        label1.grid(row=3,column=0)
        button = Button(canvas_de, text="Translate Image", command=les_bilde)
        button.grid(row=5, column=0,padx=5,pady=5)
    
def download_file():
    global img2
    image=img2

    path = filedialog.asksaveasfilename(defaultextension=".png")
    image.save(path)


encrypt_title=Label(canvas_en,text='Encrypt',font=title_font2,bg=bg_color,fg=txt_color)
encrypt_title.grid(row=1,column=1,padx=80,pady=5)
entry = Entry(canvas_en)
entry.grid(row=2, column=1,padx=5,pady=5)
button = Button(canvas_en, text="Create Image", command=lag_bilde)
button.grid(row=3, column=1,padx=5,pady=5)


b1 = Button(canvas_de, text='Upload File', 
   width=20,command = lambda:upload_file())
b1.grid(row=2,column=0) 
decrypt_title=Label(canvas_de,text='Decrypt',font=title_font2,bg=bg_color,fg=txt_color)
decrypt_title.grid(row=1,column=0,padx=80,pady=5)

root.mainloop()