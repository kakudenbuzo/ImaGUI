import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
import os
from PIL import Image
from PIL import ImageTk
import matplotlib.pyplot as plt
import numpy as np

class Button: 
  
    def __init__(self, root,frame3):
        self.root = root
        self.frame3 = frame3
        self.radio_var = tk.IntVar()
        self.path_selected ='none'
        self.paths = []
        self.radio_handle = []
        self.check_value = []    
          

    def on_click_select_button(self,fname_label):
        print('select button clicked')
        fileType =[('jpg/png file', ('*.jpg','*.png'))]
        self.path_selected=filedialog.askopenfilename(filetypes = fileType)
        fname_label['text'] = os.path.basename(self.path_selected)
        

    def on_click_upload_button(self,path= 'None',image='None'):
        print('upload button clicked')
        
        if path == 'None':
            path = self.path_selected
        else:
          cv2.imwrite(path,image)
            
        
        if path in self.paths:
            messagebox.showerror('Upload Error','"' 
                                + path 
                                + '"' + ' is already uploaded.')
        else:
            self.paths.append(path)
            self.create_radio_button(path)
        
          

    def on_click_show_button(self, method):
        print('showButton clicked')
        image = cv2.imread(self.paths[self.radio_var.get()])
        image = self.image_processing(image,method)
        
        file_name = os.path.basename(self.paths[self.radio_var.get()])
        name, ext = os.path.splitext(file_name)
        path = 'images/' + name + '_' + method + ext
        
        #cv2.imwrite(path, image)
        self.open_image_window(path,image)
    
    def image_processing(self,image,method):
        if method == 'gray':
            image =  cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        elif method == 'binary':
            ret2, image = cv2.threshold(image[:,:,0],0, 255, cv2.THRESH_OTSU)
         
        elif method == 'gblur':
            image = cv2.GaussianBlur(image,(9,9),0)
        
        elif method =='canny':
            image = cv2.Canny(image, 100, 400)

        else:
            print('method is wrong')
         
        return image

    def create_radio_button(self, path):
        
        image = cv2.imread(path)
        #image = cv2.resize(image,(120,120))
        image = self.scale_to_height(image,120)
        image_tk =self.to_tk_image(image)
        
        radio_button = tk.Radiobutton(self.frame3, image=image_tk,
                                    value=len(self.radio_handle),
                                    variable=self.radio_var)
        self.radio_var.set(0)
        self.radio_handle.append(radio_button)
        self.check_value.append(self.radio_var)

        radio_button.grid(row=(len(self.radio_handle)-1)//3,
                            column=(len(self.radio_handle)-1)%3)
        self.root.mainloop()

    def open_image_window(self, path,image):
               
        if image.shape[0]>300:
            image = self.scale_to_height(image,300)
        
        img_win = tk.Toplevel(self.root)
        fname = os.path.basename(path)
        img_win.title(fname)
        img_canvas = tk.Canvas(img_win,width=image.shape[1],
                                 height=image.shape[0]) 
        img_canvas.pack()
        image_tk =self.to_tk_image(image)                         
        img_canvas.create_image(0, 0, image=image_tk, anchor='nw')
        
        uploadButton2 = tk.Button(img_win, text = 'upload',
                   command = lambda : self.on_click_upload_button(path,image))
        uploadButton2.pack()
        
        self.root.mainloop()

    def to_tk_image(self,image_bgr):
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)   
        
        return image_tk
   
    def scale_to_height(self,img, height):
        scale = height / img.shape[0]
        return cv2.resize(img, dsize=None, fx=scale, fy=scale)


if __name__ =='__main__':
   
    os.makedirs('images', exist_ok=True)
    root = tk.Tk()
    #radio_var = tk.IntVar()    
    root.title('ImaGUI')
    root.geometry('1280x960')
    '''
    pw_main = tk.PanedWindow(root, orient='horizontal')
    pw_main.pack(expand=True, fill = tk.BOTH, side="left")

    pw_left = tk.PanedWindow(pw_main, bg="gray", orient='vertical')
    pw_main.add(pw_left)
    pw_right = tk.PanedWindow(pw_main, orient='vertical')
    pw_main.add(pw_right)
    '''
    pw_left = tk.Frame(root, relief = 'ridge',borderwidth = 4)
    #pw_left.grid(row = 0,column = 0)
    pw_left.pack(side = 'left',anchor = 'nw')
    pw_right = tk.Frame(root,relief = 'ridge',borderwidth = 4)
    #pw_right.grid(row = 0,column = 1)
    pw_right.pack(side = 'left',anchor = 'nw')
    
    frame1 = tk.Frame(pw_left, bd = 2, relief = "ridge")
    frame1.pack()
    
    frame2 = tk.LabelFrame(pw_left, bd = 2, relief = "ridge",text = 'options')
    frame2.pack(anchor = 'nw')
    
    frame3 = tk.LabelFrame(pw_right, bd = 2,text = 'Uploaded images')
    frame3.pack(side = 'left',anchor = 'nw')
    
    button = Button(root,frame3)

    # add label
    label = tk.Label(frame1, text = 'File:')
    label.grid(row = 0, column = 0)


    #label to show file name
    file_name_label = tk.Label(frame1, text='-----not selected-----',width = 20,bg = 'white') 
    file_name_label.grid(row = 0, column = 1)

    #file select button
    select_button = tk.Button(frame1, text='select', 
                    command=lambda : button.on_click_select_button(file_name_label))
    select_button.grid(row = 0, column = 2)

    # upload button
    uploadButton = tk.Button(frame1, text = 'Upload',
                   command = lambda : button.on_click_upload_button())
    uploadButton.grid(row = 0, column = 3)
    
    #gray button
    grayscale_label = tk.Label(frame2, text='gray scale')
    grayscale_label.grid(row = 0, column = 0)    
    gray_show = tk.Button(frame2, text = 'show',
                       command = lambda : button.on_click_show_button('gray'))
    gray_show.grid(row = 0, column = 1)

    #binary
    binary_label = tk.Label(frame2, text='binary')
    binary_label.grid(row = 1, column = 0)    
    binary_show = tk.Button(frame2, text = 'show',
                       command = lambda : button.on_click_show_button('binary'))
    binary_show.grid(row = 1, column = 1)
    
    #gaussian blur
    gblur_label = tk.Label(frame2, text='Gaussian blur')
    gblur_label.grid(row = 2, column = 0)    
    gblur_show = tk.Button(frame2, text = 'show',
                       command = lambda : button.on_click_show_button('gblur'))
    gblur_show.grid(row = 2, column = 1)
    
    #canny edge
    canny_label = tk.Label(frame2, text='canny edge')
    canny_label.grid(row = 3, column = 0)    
    canny_show = tk.Button(frame2, text = 'show',
                       command = lambda : button.on_click_show_button('canny'))
    canny_show.grid(row = 3, column = 1)
    
    root.mainloop()





