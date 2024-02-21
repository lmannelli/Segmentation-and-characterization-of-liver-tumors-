import nibabel as nib
import matplotlib.pyplot as plt
import pydicom
from pydicom.data import get_testdata_files
import dicom2nifti
import numpy as np
from skimage.segmentation import active_contour
from skimage import data
from skimage.filters import gaussian
from skimage.segmentation import active_contour
import cv2
import SimpleITK as sitk
from IPython.display import clear_output
import tkinter as tk
from PIL import Image, ImageTk
from scipy import signal
import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox
from skimage.feature import graycomatrix
from scipy.stats import kurtosis, skew
import diplib as dip

# img2=nib.load("C:/Users/lmana/Desktop/volume-10.nii")
# data2 = img2.get_fdata() 
# for i in range(data2.shape[2]):
#     data2[:,:,i]=cv2.rotate(data2[:,:,i],cv2.ROTATE_90_COUNTERCLOCKWISE)

###----APP-----

ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green") 

class tkinterApp(ctk.CTk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        super().__init__(*args, **kwargs)
        width= self.winfo_screenwidth()
        height= self.winfo_screenheight()
        #setting tkinter window size
        self.geometry("%dx%d" % (width, height))
        self.title("AppPIB")
        # creating a container

        container = ctk.CTkFrame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
        self.app_data = {"filename": ctk.StringVar(),
                        }
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Inicio,MainPageApp):  
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(Inicio)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.update()
        frame.event_generate("<<ShowFrame>>")

class Inicio(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        self.controller= controller


        # Calcular la posición x e y para centrar la ventana
        x = int(ancho_pantalla/2 - 400/2)
        y = int(alto_pantalla/2 - 500/2)

        empresa = ctk.CTkLabel(self, text="CMMS \nTechnologies", justify="left",font=ctk.CTkFont(size=25, family="Arial Rounded MT Bold",))
        empresa.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        titulo = ctk.CTkLabel(self, text="Segmentación de\n tumores de hígado", font=ctk.CTkFont(family="Arial Rounded MT Bold",size=60))
        titulo.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # titulo2 = ctk.CTkLabel(self, text="Dispositivo de Evaluación de \n Parkinson por Análisis de la Unidad \n Locomotora", font=ctk.CTkFont(family="Arial Rounded Light",size=25, weight="normal"))
        # titulo2.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        boton_iniciar=ctk.CTkButton(self, corner_radius=40,width=0.2*ancho_pantalla, height=0.1*alto_pantalla, font=ctk.CTkFont(family="Arial Rounded MT Bold",size=25), text="INICIO",command =  lambda : controller.show_frame(MainPageApp))
        boton_iniciar.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def browse_image(self):
        # global uploaded_img, upload_button, punto, cargo_img, imagen, instruc1, photo, img_array
        filename = filedialog.askopenfilename(filetypes=[("Image files", ".nii")])
        if filename:
            # Load the image
            print(filename)
            self.controller.app_data["filename"]=filename
            self.controller.show_frame(MainPageApp)

            # uploaded_img = Image.open(filename)
            # imagen=cv2.imread(filename,0) #con esta trabajamos
            # print('Tamaño:',imagen.shape)
            # img_array = np.array(uploaded_img)  # Convert PIL image to numpy array
            # if img_array is not None:
            #     # Do something with the image array, such as processing or displaying it
            #     messagebox.showinfo("Éxito", "Imagen cargada.")
            # else:
            #     messagebox.showerror("Error", "Failed to load the image.")

class MainPageApp(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller= controller

        width= self.winfo_screenwidth()
        ancho_pantalla=width
        height= self.winfo_screenheight()
        alto_pantalla=height

        boton_mostrar=ctk.CTkButton(self, corner_radius=40, width=0.1*ancho_pantalla, height=0.05*alto_pantalla, font=ctk.CTkFont(family="Arial Rounded MT Bold",size=10), text="CARGAR IMAGEN",command=self.browse_image)
        boton_mostrar.grid(row=1, column=2, padx=0, pady=5)

        # img2=nib.load(self.controller.app_data["filename"])
        # data2 = img2.get_fdata() 
        # for i in range(data2.shape[2]):
        #     data2[:,:,i]=cv2.rotate(data2[:,:,i],cv2.ROTATE_90_COUNTERCLOCKWISE)

        # # self.title("AppPIB")
        # width= self.winfo_screenwidth()
        # ancho_pantalla=width
        # height= self.winfo_screenheight()
        # alto_pantalla=height
        # #setting tkinter window size
        # # self.geometry("%dx%d" % (width, height))
        # #self.grid_columnconfigure(0, weight=1)
        # #self.grid_rowconfigure(0, weight=1)
        # self.imagenFrame1=data2
        # self.imagenFrame2=data2

        # titulo = ctk.CTkLabel(self, text="Detector de tumores de hígado", font=ctk.CTkFont(family="Arial Rounded MT Bold",size=35))
        # titulo.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=5)

        # MinSlice =ctk.CTkLabel(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla,justify="right",corner_radius=40,font=ctk.CTkFont(family="Arial Rounded MT Bold",size=15),text="Valor mínimo de corte")
        # MinSlice.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="e")
        # self.ValorMinSlice = ctk.CTkEntry(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla)
        # self.ValorMinSlice.insert(0, "Valor mínimo")
        # self.ValorMinSlice.bind("<Button-1>", lambda e: self.ValorMinSlice.delete(0, 'end'))
        # self.ValorMinSlice.grid(row=3, column=1, padx=20, pady=(10, 20), sticky="w")

        # MaxSlice =ctk.CTkLabel(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla,justify="right",corner_radius=40,font=ctk.CTkFont(family="Arial Rounded MT Bold",size=15),text="Valor máximo de corte")
        # MaxSlice.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="e")
        # self.ValorMaxSlice = ctk.CTkEntry(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla)
        # self.ValorMaxSlice.insert(0, "Valor máximo")
        # self.ValorMaxSlice.bind("<Button-1>", lambda e: self.ValorMaxSlice.delete(0, 'end'))
        # self.ValorMaxSlice.grid(row=4, column=1, padx=20, pady=(10, 20), sticky="w")

        # self.enviarRecorte = ctk.CTkButton(self,corner_radius=40,width=0.15*ancho_pantalla, height=0.025*alto_pantalla, text="Recortar", font=ctk.CTkFont(family="Arial Rounded MT Bold",size=20), fg_color="green",command=self.botonCortar)
        # self.enviarRecorte.grid(row=5, column=0, padx=0, pady=10, columnspan=2)

        # MinHU =ctk.CTkLabel(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla,justify="right",corner_radius=40,font=ctk.CTkFont(family="Arial Rounded MT Bold",size=15),text="Valor mínimo de HU")
        # MinHU.grid(row=3, column=2, padx=20, pady=(10, 20), sticky="e")
        # self.ValorMinHU = ctk.CTkEntry(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla)
        # self.ValorMinHU.insert(0, "Valor mínimo de HU")
        # self.ValorMinHU.bind("<Button-1>", lambda e: self.ValorMinHU.delete(0, 'end'))
        # self.ValorMinHU.grid(row=3, column=3, padx=20, pady=(10, 20), sticky="w")

        # MaxHU =ctk.CTkLabel(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla,justify="right",corner_radius=40,font=ctk.CTkFont(family="Arial Rounded MT Bold",size=15),text="Valor máximo de HU")
        # MaxHU.grid(row=4, column=2, padx=20, pady=(10, 20), sticky="e")
        # self.ValorMaxHU = ctk.CTkEntry(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla)
        # self.ValorMaxHU.insert(0, "Valor máximo de HU")
        # self.ValorMaxHU.bind("<Button-1>", lambda e: self.ValorMaxHU.delete(0, 'end'))
        # self.ValorMaxHU.grid(row=4, column=3, padx=20, pady=(10, 20), sticky="w")

        # self.enviarHU = ctk.CTkButton(self,corner_radius=40,width=0.15*ancho_pantalla, height=0.025*alto_pantalla, text="Segmentar Hígado", font=ctk.CTkFont(family="Arial Rounded MT Bold",size=20), fg_color="green",command=self.segmentarHigado)
        # self.enviarHU.grid(row=5, column=2, padx=0, pady=10)

        # self.enviarTumor = ctk.CTkButton(self,corner_radius=40,width=0.15*ancho_pantalla, height=0.025*alto_pantalla, text="Segmentar Tumor", font=ctk.CTkFont(family="Arial Rounded MT Bold",size=20), fg_color="green",command=self.extraerTumores)
        # self.enviarTumor.grid(row=5, column=3, padx=10, pady=10, sticky="nsew")

        # sliceTumor =ctk.CTkLabel(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla,justify="right",corner_radius=40,font=ctk.CTkFont(family="Arial Rounded MT Bold",size=15),text="Elegir slice del tumor:")
        # sliceTumor.grid(row=2, column=4, padx=20, pady=(10, 20), sticky="s")
        # self.ValorsliceTumor = ctk.CTkEntry(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla)
        # self.ValorsliceTumor.insert(0, "Slice del tumor")
        # self.ValorsliceTumor.bind("<Button-1>", lambda e: self.ValorsliceTumor.delete(0, 'end'))
        # self.ValorsliceTumor.grid(row=3, column=4, padx=20, pady=(10, 20), sticky="n")

        # self.caractTumor = ctk.CTkButton(self,corner_radius=40,width=0.15*ancho_pantalla, height=0.025*alto_pantalla, text="Características Tumor", font=ctk.CTkFont(family="Arial Rounded MT Bold",size=20), fg_color="blue",command=self.segmentarHigado)
        # self.caractTumor.grid(row=4, column=4, padx=10, pady=10, sticky="nsew")

        # self.botonReiniciar = ctk.CTkButton(self,corner_radius=40,width=0.15*ancho_pantalla, height=0.025*alto_pantalla, text="Reiniciar procesamiento", font=ctk.CTkFont(family="Arial Rounded MT Bold",size=20), fg_color="red",command=self.reiniciarProcesamiento)
        # self.botonReiniciar.grid(row=5, column=4, padx=10, pady=10, sticky="nsew")

        # self.Image1 =tk.Label(self)
        # self.Image1.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="nsew",columnspan=2)

        # self.Image2 = tk.Label(self)
        # self.Image2.grid(row=1, column=2, padx=10, pady=(10, 10), sticky="nsew",columnspan=2)

 
        # self.slider = tk.Scale(self, from_=1, to=data2.shape[2], orient=tk.HORIZONTAL,command=self.update_image1)
        # self.slider.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew",columnspan=2)
        # self.slider.set(1)
        # self.update_image1(1)

        # self.slider2 = tk.Scale(self, from_=1, to=self.imagenFrame2.shape[2], orient=tk.HORIZONTAL,command=self.update_image2)
        # self.slider2.grid(row=2, column=2, padx=(20, 10), pady=(10, 10), sticky="ew",columnspan=2)
        # self.slider2.set(1)
        # self.update_image2(1)

    def browse_image(self):
        # global uploaded_img, upload_button, punto, cargo_img, imagen, instruc1, photo, img_array
        filename = filedialog.askopenfilename(filetypes=[("Image files", ".nii")])
        if filename:
            # Load the image
            print(filename)
            img2=nib.load(filename)
            data2 = img2.get_fdata() 
            for i in range(data2.shape[2]):
                data2[:,:,i]=cv2.rotate(data2[:,:,i],cv2.ROTATE_90_COUNTERCLOCKWISE)

            # self.title("AppPIB")
            width= self.winfo_screenwidth()
            ancho_pantalla=width
            height= self.winfo_screenheight()
            alto_pantalla=height
            #setting tkinter window size
            # self.geometry("%dx%d" % (width, height))
            #self.grid_columnconfigure(0, weight=1)
            #self.grid_rowconfigure(0, weight=1)

            boton_mostrar=ctk.CTkButton(self, corner_radius=40, width=0.1*ancho_pantalla, height=0.05*alto_pantalla, font=ctk.CTkFont(family="Arial Rounded MT Bold",size=10), text="CARGAR IMAGEN",command=self.browse_image)
            boton_mostrar.grid(row=1, column=2, padx=0, pady=5)

            self.imagenFrame1=data2
            self.imagenFrame2=data2

            titulo = ctk.CTkLabel(self, text="Detector de tumores de hígado", font=ctk.CTkFont(family="Arial Rounded MT Bold",size=35))
            titulo.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=5)

            MinSlice =ctk.CTkLabel(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla,justify="right",corner_radius=40,font=ctk.CTkFont(family="Arial Rounded MT Bold",size=15),text="Valor mínimo de corte")
            MinSlice.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="e")
            self.ValorMinSlice = ctk.CTkEntry(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla)
            self.ValorMinSlice.insert(0, "Valor mínimo")
            self.ValorMinSlice.bind("<Button-1>", lambda e: self.ValorMinSlice.delete(0, 'end'))
            self.ValorMinSlice.grid(row=3, column=1, padx=20, pady=(10, 20), sticky="w")

            MaxSlice =ctk.CTkLabel(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla,justify="right",corner_radius=40,font=ctk.CTkFont(family="Arial Rounded MT Bold",size=15),text="Valor máximo de corte")
            MaxSlice.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="e")
            self.ValorMaxSlice = ctk.CTkEntry(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla)
            self.ValorMaxSlice.insert(0, "Valor máximo")
            self.ValorMaxSlice.bind("<Button-1>", lambda e: self.ValorMaxSlice.delete(0, 'end'))
            self.ValorMaxSlice.grid(row=4, column=1, padx=20, pady=(10, 20), sticky="w")

            self.enviarRecorte = ctk.CTkButton(self,corner_radius=40,width=0.15*ancho_pantalla, height=0.025*alto_pantalla, text="Recortar", font=ctk.CTkFont(family="Arial Rounded MT Bold",size=20), fg_color="green",command=self.botonCortar)
            self.enviarRecorte.grid(row=5, column=0, padx=0, pady=10, columnspan=2)

            MinHU =ctk.CTkLabel(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla,justify="right",corner_radius=40,font=ctk.CTkFont(family="Arial Rounded MT Bold",size=15),text="Valor mínimo de HU")
            MinHU.grid(row=3, column=2, padx=20, pady=(10, 20), sticky="e")
            self.ValorMinHU = ctk.CTkEntry(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla)
            self.ValorMinHU.insert(0, "Valor mínimo de HU")
            self.ValorMinHU.bind("<Button-1>", lambda e: self.ValorMinHU.delete(0, 'end'))
            self.ValorMinHU.grid(row=3, column=3, padx=20, pady=(10, 20), sticky="w")

            MaxHU =ctk.CTkLabel(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla,justify="right",corner_radius=40,font=ctk.CTkFont(family="Arial Rounded MT Bold",size=15),text="Valor máximo de HU")
            MaxHU.grid(row=4, column=2, padx=20, pady=(10, 20), sticky="e")
            self.ValorMaxHU = ctk.CTkEntry(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla)
            self.ValorMaxHU.insert(0, "Valor máximo de HU")
            self.ValorMaxHU.bind("<Button-1>", lambda e: self.ValorMaxHU.delete(0, 'end'))
            self.ValorMaxHU.grid(row=4, column=3, padx=20, pady=(10, 20), sticky="w")

            self.enviarHU = ctk.CTkButton(self,corner_radius=40,width=0.15*ancho_pantalla, height=0.025*alto_pantalla, text="Segmentar Hígado", font=ctk.CTkFont(family="Arial Rounded MT Bold",size=20), fg_color="green",state="disabled",command=self.segmentarHigado)
            self.enviarHU.grid(row=5, column=2, padx=0, pady=10)

            self.enviarTumor = ctk.CTkButton(self,corner_radius=40,width=0.15*ancho_pantalla, height=0.025*alto_pantalla, text="Segmentar Tumor", font=ctk.CTkFont(family="Arial Rounded MT Bold",size=20), fg_color="green",state="disabled",command=self.extraerTumores)
            self.enviarTumor.grid(row=5, column=3, padx=10, pady=10, sticky="nsew")

            sliceTumor =ctk.CTkLabel(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla,justify="right",corner_radius=40,font=ctk.CTkFont(family="Arial Rounded MT Bold",size=15),text="Elegir slice del tumor:")
            sliceTumor.grid(row=2, column=4, padx=20, pady=(10, 20), sticky="s")
            self.ValorsliceTumor = ctk.CTkEntry(self,width=0.15*ancho_pantalla, height=0.025*alto_pantalla)
            self.ValorsliceTumor.insert(0, "Slice del tumor")
            self.ValorsliceTumor.bind("<Button-1>", lambda e: self.ValorsliceTumor.delete(0, 'end'))
            self.ValorsliceTumor.grid(row=3, column=4, padx=20, pady=(10, 20), sticky="n")

            self.caractTumor = ctk.CTkButton(self,corner_radius=40,width=0.15*ancho_pantalla, height=0.025*alto_pantalla, text="Características Tumor", font=ctk.CTkFont(family="Arial Rounded MT Bold",size=20), fg_color="blue",state="disabled",command=self.caractTumores)
            self.caractTumor.grid(row=4, column=4, padx=10, pady=10, sticky="nsew")

            self.botonReiniciar = ctk.CTkButton(self,corner_radius=40,width=0.15*ancho_pantalla, height=0.025*alto_pantalla, text="Reiniciar procesamiento", font=ctk.CTkFont(family="Arial Rounded MT Bold",size=20), fg_color="red",command=self.reiniciarProcesamiento)
            self.botonReiniciar.grid(row=5, column=4, padx=10, pady=10, sticky="nsew")

            self.Image1 =tk.Label(self)
            self.Image1.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="nsew",columnspan=2)

            self.Image2 = tk.Label(self)
            self.Image2.grid(row=1, column=2, padx=10, pady=(10, 10), sticky="nsew",columnspan=2)

    
            self.slider = tk.Scale(self, from_=1, to=data2.shape[2], orient=tk.HORIZONTAL,command=self.update_image1)
            self.slider.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew",columnspan=2)
            self.slider.set(1)
            self.update_image1(1)

            self.slider2 = tk.Scale(self, from_=1, to=self.imagenFrame2.shape[2], orient=tk.HORIZONTAL,command=self.update_image2)
            self.slider2.grid(row=2, column=2, padx=(20, 10), pady=(10, 10), sticky="ew",columnspan=2)
            self.slider2.set(1)
            self.update_image2(1)            


    def caractTumores(self):
        valorSlice=int(ctk.CTkEntry.get(self.ValorsliceTumor))-1
        print("ValorSLice:",valorSlice)
        tumorPruebaBB = self.imagenFrame2[:,:,valorSlice].astype("uint8")

        cnts = cv2.findContours(tumorPruebaBB, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        imagen2 = tumorPruebaBB.copy()
        original = imagen2.copy()

        bounding_boxes = []
        max_area = -1
        max_box = None
        for c in cnts:
            xbox,ybox,wbox,hbox = cv2.boundingRect(c)
            bounding_boxes.append((xbox, ybox, wbox, hbox))
            box=xbox,ybox,wbox,hbox
            cv2.rectangle(imagen2, (xbox, ybox), (xbox + wbox, ybox + hbox), (36,255,12), 2) # parámetros, img, punto inicial, punto final, color, espesor
            ROITumor = original[ybox:ybox+hbox, xbox:xbox+wbox]
            area = wbox * hbox
            if area > max_area:
                max_area = area
                max_box = box
        print("Max box:",max_box)
        xbox,ybox,wbox,hbox=max_box
        ROITumor=original[ybox:ybox+hbox, xbox:xbox+wbox]
        glcm0 = graycomatrix(ROITumor, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
        glcm45 = graycomatrix(ROITumor, distances=[1], angles=[45], levels=256, symmetric=True, normed=True)
        glcm90 = graycomatrix(ROITumor, distances=[1], angles=[90], levels=256, symmetric=True, normed=True)
        glcm135 = graycomatrix(ROITumor, distances=[1], angles=[135], levels=256, symmetric=True, normed=True)
        entropy0 = round(-np.sum(glcm0 * np.log2(glcm0 + (glcm0 == 0))),4)
        entropy45 = round(-np.sum(glcm45 * np.log2(glcm45 + (glcm45 == 0))),4)
        entropy90 = round(-np.sum(glcm90 * np.log2(glcm90 + (glcm90 == 0))),4)
        entropy135 = round(-np.sum(glcm135 * np.log2(glcm135 + (glcm135 == 0))),4)
        energia0 =round( np.sum(glcm0 ** 2),4)
        energia45 = round(np.sum(glcm45 ** 2),4)
        energia90 = round(np.sum(glcm90 ** 2),4)
        energia135 = round(np.sum(glcm135 ** 2),4)

        labels = dip.Label(ROITumor > 0)

        msr = dip.MeasurementTool.Measure(labels, features=["Perimeter", "Size", "Roundness", "Circularity"])
        Circularity = round(msr[1]["Roundness"][0],4)
        solidArea=round(msr[1]["SolidArea"][0],4)

        KurtosisROI=round(kurtosis(ROITumor, axis=None),4)

        skewROI=round(skew(ROITumor, axis=None),4)

        messagebox.showinfo("Características", "Características extraídas:\nÁrea(px^2): "+str(solidArea)+"\nEntropía (0°): "+str(entropy0)+"\nEntropía (45°): "+str(entropy45)+"\nEntropía (90°): "+str(entropy90)+"\nEntropía (135°): "+str(entropy135)+"\nEnergía (0°): "+str(energia0)+"\nEnergía (45°): "+str(energia45)+"\nEnergía (90°): "+str(energia90)+"\nEnergía (135°): "+str(energia135)+"\nCircularity: "+str(Circularity)+"\nKurtosis: "+str(KurtosisROI)+"\nSkewness: "+str(skewROI))


    def reiniciarProcesamiento(self):
        self.imagenFrame2=self.imagenFrame1
        for widget in self.slider2.winfo_children():
            widget.destroy()
        self.slider2 = tk.Scale(self, from_=1, to=self.imagenFrame2.shape[2], orient=tk.HORIZONTAL,command=self.update_image2)
        self.slider2.grid(row=2, column=2, padx=(20, 10), pady=(10, 10), sticky="ew",columnspan=2)
        self.slider2.set(1)
        self.update_image2(1)
        self.caractTumor.configure(state="disabled")
        self.enviarTumor.configure(state="disabled")
        self.enviarHU.configure(state="disabled")
        self.enviarRecorte.configure(state="normal")

    def update_image1(self,val):
        #print(type(val))
        val=int(val)
        #global img_tk
        # Load the image from file
        #img = Image.open(data2[:,:,val-1])
        img = self.imagenFrame1[:,:,val-1]
        #g,h=Ecualizacion_H(data2[:,:,val-1],256)
        # Resize the image to fit in the label
        #img = img.resize((400, 400))

        # Convert the image to Tkinter format

        img_tk = ImageTk.PhotoImage(Image.fromarray(img))

        # Update the label with the new image
        self.Image1.config(image=img_tk)
        self.Image1.image = img_tk

    def update_image2(self,val):
        #print(type(val))
        val=int(val)
        #global img_tk
        # Load the image from file
        #img = Image.open(data2[:,:,val-1])
        img = self.imagenFrame2[:,:,val-1]
        #g,h=Ecualizacion_H(data2[:,:,val-1],256)
        # Resize the image to fit in the label
        #img = img.resize((400, 400))

        # Convert the image to Tkinter format

        img_tk = ImageTk.PhotoImage(Image.fromarray(img))

        # Update the label with the new image
        self.Image2.config(image=img_tk)
        self.Image2.image = img_tk

    def botonCortar(self):
        imagenRecorte=self.imagenFrame1.copy()
        sliceMin= int(ctk.CTkEntry.get(self.ValorMinSlice))
        sliceMax=int(ctk.CTkEntry.get(self.ValorMaxSlice))
        imagenRecorte = imagenRecorte[:,:,sliceMin:sliceMax]

        cantInfY=int(0.1*imagenRecorte.shape[0])
        cantSupY=int(0.8*imagenRecorte.shape[0])
        cantXSup=int(0.05*imagenRecorte.shape[1])
        cantXInf=int(0.6*imagenRecorte.shape[1])
        dataRecortada=imagenRecorte[cantInfY:cantSupY,cantXSup:cantXInf,:]
        for i in range(dataRecortada.shape[2]):
            dataRecortada[:,:,i] =signal.medfilt2d(dataRecortada[:,:,i],kernel_size=5) 

        x=dataRecortada.shape[0]
        y=dataRecortada.shape[1]
        z=dataRecortada.shape[2]
        img8bits=dataRecortada.astype(np.uint8)

        self.imagenFrame2=dataRecortada
        for widget in self.slider2.winfo_children():
            widget.destroy()
        self.slider2 = tk.Scale(self, from_=1, to=self.imagenFrame2.shape[2], orient=tk.HORIZONTAL,command=self.update_image2)
        self.slider2.grid(row=2, column=2, padx=(20, 10), pady=(10, 10), sticky="ew",columnspan=2)
        self.slider2.set(1)
        self.update_image2(1)
        self.enviarRecorte.configure(state="disabled")
        self.enviarHU.configure(state="normal")

    def segmentarHigado(self):
        imagenHigado=self.imagenFrame2.copy()
        x=imagenHigado.shape[0]
        y=imagenHigado.shape[1]
        z=imagenHigado.shape[2]
        segmHigado=np.zeros((x,y,z))
        HUMin= int(ctk.CTkEntry.get(self.ValorMinHU))
        HUMax=int(ctk.CTkEntry.get(self.ValorMaxHU))
        for i in range(z):
            for j in range(x):
                for k in range(y):
                    if(imagenHigado[j][k][i]>HUMin and imagenHigado[j][k][i]<HUMax):
                        segmHigado[j][k][i]=1

        kernel13= np.ones((13,13), 'uint8')
        kernel11= np.ones((11,11), 'uint8')
        kernel9= np.ones((9,9), 'uint8')
        kernel7= np.ones((7,7), 'uint8')
        kernel5 = np.ones((5,5), 'uint8')
        kernel3 = np.ones((3,3), 'uint8')
        imagenCierreHig=segmHigado.copy()

        # for i in range(5):

        #Primero hago cierre para definir estructuras
        imagenCierreHig=cv2.dilate(imagenCierreHig,kernel5, iterations=1)
        imagenCierreHig=cv2.erode(imagenCierreHig,kernel5, iterations=1)

        #Despues hago apertura para filtrar
        imagenCierreHig=cv2.erode(imagenCierreHig,kernel5, iterations=1)   
        imagenCierreHig=cv2.dilate(imagenCierreHig,kernel5, iterations=1)


        imagenCierreHig8bits=imagenCierreHig.astype(np.uint8)
        # print(imagenCierreHig28bits)

        pruebaLlenar=imagenCierreHig8bits.copy()
        for i in range(z):
            pruebaLlenar[:,:,i]=cv2.floodFill(np.float32(imagenCierreHig8bits[:,:,i]), None, (0, 0), 1)[1]

        imagenRellenada=np.zeros((x,y,z))

        for i in range(x):
            for j in range(y):
                for k in range(z):
                    if(int(pruebaLlenar[i][j][k])==1):
                        pruebaLlenar[i][j][k]=0
                    elif(int(pruebaLlenar[i][j][k])==0):
                        pruebaLlenar[i][j][k]=1

        for i in range(x):
            for j in range(y): 
                for k in range(z):
                    imagenRellenada[i][j][k]=int(imagenCierreHig8bits[i][j][k]+pruebaLlenar[i][j][k])

        binariaConBBHigado=np.zeros((x,y,z))
        for k in range(z):
            imagenPrueba = imagenRellenada[:,:,k].astype("uint8")

            cnts = cv2.findContours(imagenPrueba, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            imagen2 = self.imagenFrame2[:,:,k].copy()
            original = imagen2.copy()

            bounding_boxes = []
            max_area = -1
            max_box = None
            for c in cnts:
                xbox,ybox,wbox,hbox = cv2.boundingRect(c)
                bounding_boxes.append((xbox, ybox, wbox, hbox))
                box=xbox,ybox,wbox,hbox
                cv2.rectangle(imagen2, (xbox, ybox), (xbox + wbox, ybox + hbox), (36,255,12), 2) # parámetros, img, punto inicial, punto final, color, espesor
                ROI = original[ybox:ybox+hbox, xbox:xbox+wbox]
                area = wbox * hbox
                if area > max_area:
                    max_area = area
                    max_box = box
            xbox,ybox,wbox,hbox=max_box
            for i in range(x):
                for j in range(y):
                    if (j>=xbox and j<(xbox+wbox) and i>=ybox and i<(ybox+hbox)):
                        binariaConBBHigado[i,j,k]=imagenRellenada[i,j,k]

        primeraSegHigado=np.zeros((x,y,z))

        for i in range(z):
            for j in range(x):
                for k in range(y):
                    primeraSegHigado[j,k,i]=binariaConBBHigado[j,k,i]*self.imagenFrame2[j,k,i]
        
        self.imagenFrame2=primeraSegHigado

        for widget in self.slider2.winfo_children():
            widget.destroy()
        self.slider2 = tk.Scale(self, from_=1, to=self.imagenFrame2.shape[2], orient=tk.HORIZONTAL,command=self.update_image2)
        self.slider2.grid(row=2, column=2, padx=(20, 10), pady=(10, 10), sticky="ew",columnspan=2)
        self.slider2.set(1)
        self.update_image2(1)
        self.enviarHU.configure(state="disabled")
        self.enviarTumor.configure(state="normal")        

    def extraerTumores(self):
        segHigado=self.imagenFrame2.copy()
        segHigado8bits=segHigado.astype(np.uint8)
        kernel_FP = 1/25 * np.array(([1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1])) #kernel promedio
        # kernel_FP = 1/9 * np.array(([1,1,1],[1,1,1],[1,1,1])) #kernel promedio
        x=segHigado.shape[0]
        y=segHigado.shape[1]
        z=segHigado.shape[2]
        imagen_Gauss_Filtrada_FP=np.zeros((x,y,z))
        for i in range(z):
            imagen_Gauss_Filtrada_FP[:,:,i] =cv2.filter2D(segHigado8bits[:,:,i],-1,kernel_FP)        
        umbralizadaLucas=np.zeros((x,y,z))

        HUMin= int(ctk.CTkEntry.get(self.ValorMinHU))

        for i in range(z):
            for j in range(x):
                for k in range(y):
                    if(imagen_Gauss_Filtrada_FP[j][k][i]>HUMin):
                        umbralizadaLucas[j][k][i]=255
        kernel5 = np.ones((5,5), 'uint8')
        binTumorSegmLucas=cv2.dilate(umbralizadaLucas,kernel5, iterations=1)
        binTumorSegmLucas=cv2.erode(binTumorSegmLucas,kernel5, iterations=1)

        binariaConBB=np.zeros((x,y,z))

        for k in range(z):
            imagenPrueba = binTumorSegmLucas[:,:,k].astype("uint8")

            cnts = cv2.findContours(imagenPrueba, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            imagen2 = self.imagenFrame2[:,:,k].copy()
            original = imagen2.copy()

            bounding_boxes = []
            max_area = -1
            max_box = None
            for c in cnts:
                xbox,ybox,wbox,hbox = cv2.boundingRect(c)
                bounding_boxes.append((xbox, ybox, wbox, hbox))
                box=xbox,ybox,wbox,hbox
                cv2.rectangle(imagen2, (xbox, ybox), (xbox + wbox, ybox + hbox), (36,255,12), 2) # parámetros, img, punto inicial, punto final, color, espesor
                ROI = original[ybox:ybox+hbox, xbox:xbox+wbox]
                area = wbox * hbox
                if area > max_area:
                    max_area = area
                    max_box = box
            xbox,ybox,wbox,hbox=max_box
            for i in range(x):
                for j in range(y):
                    if (j>=xbox and j<(xbox+wbox) and i>=ybox and i<(ybox+hbox)):
                        binariaConBB[i,j,k]=binTumorSegmLucas[i,j,k]

        pruebaTumor=np.zeros((x,y,z))
        for i in range(z):
            pruebaTumor[:,:,i]=cv2.floodFill(np.float32(binariaConBB[:,:,i]), None, (0, 0), 255)[1]  
             
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    if(int(pruebaTumor[i][j][k])==255):
                        pruebaTumor[i][j][k]=0
                    elif(int(pruebaTumor[i][j][k])==0):
                        pruebaTumor[i][j][k]=1
        tumorSegmentado=np.zeros((x,y,z))
        for i in range(z):
            for j in range(x):
                for k in range(y):
                    tumorSegmentado[j,k,i]=int(int(pruebaTumor[j,k,i])*segHigado[j,k,i]) 

        self.imagenFrame2=tumorSegmentado
        for widget in self.slider2.winfo_children():
            widget.destroy()
        self.slider2 = tk.Scale(self, from_=1, to=self.imagenFrame2.shape[2], orient=tk.HORIZONTAL,command=self.update_image2)
        self.slider2.grid(row=2, column=2, padx=(20, 10), pady=(10, 10), sticky="ew",columnspan=2)
        self.slider2.set(1)
        self.update_image2(1)
        self.enviarTumor.configure(state="disabled")
        self.caractTumor.configure(state="normal")

app = tkinterApp()
app.mainloop()