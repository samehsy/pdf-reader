from flask import request, send_file
import flask
import numpy as np
import cv2
from pdf2image import convert_from_path
from os import listdir
from fpdf import FPDF
import shutil

import os


class Core:
    """A simple example class"""
    PATH = os.getcwd() + '/'
    TEMP_IMAGES_FOLDER = 'images/'
    PDF_FILE = 'pdf_to_proccess.pdf'
    RGBA = [0, 0, 0]
    PREV_TEXT = [0, 0, 0]
    PREV_BACK = [255, 255, 255]
    BLUE_PERCENT = 0
    HIGHLIGHT_CORS = {}
    

# to  recive  the  file  from  FE and  save  it  as PDF_FILE
    def set_file(self):
        uploaded_file = request.files['pdf']
        print(uploaded_file.filename)

        if uploaded_file.filename != '':
            if os.path.exists(self.PDF_FILE):
                print(self.PDF_FILE)
                os.remove(self.PATH + self.PDF_FILE)
            uploaded_file.save(self.PDF_FILE)
        return True

    def set_prev_text(self, rgb):
        self.PREV_TEXT[0] = rgb.get('r')
        self.PREV_TEXT[1] = rgb.get('g')
        self.PREV_TEXT[2] = rgb.get('b')

    def rgb_2_json(self, rgba):
        return {'r': rgba[0], 'g': rgba[1], 'b': rgba[2]}

    def json_2_rgb(self, json):
        return [json.get('r'), json.get('g'), json.get('b')]

    def set_prev_back(self, rgb):
        self.PREV_BACK[0] = rgb.get('r')
        self.PREV_BACK[1] = rgb.get('g')
        self.PREV_BACK[2] = rgb.get('b')

    def send_pdf(self, output):
        if(output):
            return send_file(self.PATH + 'output/' + self.PDF_FILE)
        else:
            return send_file(self.PATH + self.PDF_FILE)

    # for single image
    def proccess_text_color(self, image):
        # image = cv2.cvtColor(image,  cv2.COLOR_BGR2RGB)
        lower_color = np.array([0, 0, 0])
        upper_color = np.array([50, 50, 50])
        mask = cv2.inRange(image, lower_color, upper_color)
        # Change image to red where we found brown
        image[mask <= 0] = (self.PREV_BACK[0],
                            self.PREV_BACK[1], self.PREV_BACK[2])
        print(self.RGBA)
        image[mask > 0] = (self.RGBA[0], self.RGBA[1], self.RGBA[2])
        return image

    # for single image background
    def proccess_background_color(self, image):
        # image = cv2.cvtColor(image,  cv2.COLOR_BGR2RGB)
        lower_color = np.array([230, 230, 230])
        upper_color = np.array([255, 255, 255])
        mask = cv2.inRange(image, lower_color, upper_color)
        # Change image to red where we found brown
        image[mask <= 0] = (self.PREV_TEXT[0],
                            self.PREV_TEXT[1], self.PREV_TEXT[2],)
        image[mask > 0] = (self.RGBA[0], self.RGBA[1], self.RGBA[2],)
        return image

    def proccess_eye_comfort(self, image):
        convert = lambda x: x-self.BLUE_PERCENT
        image[:, :, 2] = convert(image[:, :, 2])
        return image

    def proccess_highlight(self, image):
        image = cv2.resize(image, (1006,1422))
        for i in range( image.shape[0]) :
            for  j in  range(image.shape[1]):
                if( ( self.HIGHLIGHT_CORS.get('last_mousex')  < j <self.HIGHLIGHT_CORS.get('final_x') )  & ( self.HIGHLIGHT_CORS.get('last_mousey') < i < self.HIGHLIGHT_CORS.get('final_y'))):
                    lower_color = np.array([0, 0, 0])
                    upper_color = np.array([200, 200, 200])
                    is_low =lower_color < image[i][j]
                    is_up =upper_color < image[i][j]
                    if  (np.all(is_low  == True) & np.all(is_up  == True)):
                        image[i][j]  = [255,255,0]
        return image

    def store_pdf_result(self, proccess_type):
        if os.path.exists(self.PATH + self.TEMP_IMAGES_FOLDER):
            shutil.rmtree(self.PATH + self.TEMP_IMAGES_FOLDER)
            os.mkdir(self.PATH + self.TEMP_IMAGES_FOLDER)

        # Store Pdf with convert_from_path function
        images = convert_from_path(self.PATH + self.PDF_FILE)
        for i in range(len(images)):
            print(i)
            image = np.copy(images[i])
            if(proccess_type == 'change_text_color'):
                image = self.proccess_text_color(image)
            if (proccess_type == 'change_background_color'):
                image = self.proccess_background_color(image)
            if (proccess_type == 'change_eye_comfort'):
                image = self.proccess_eye_comfort(image)
            if ((proccess_type == 'proccess_highlight') & (i+1 ==  self.HIGHLIGHT_CORS.get('page')) ):
                print('here')
                image = self.proccess_highlight(image)    
            # Save pages as images in the pdf
            image = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
            cv2.imwrite(self.PATH + self.TEMP_IMAGES_FOLDER +
                        'temp_image' + str(i)+'.jpg', image)

    def convert_images_to_pdf(self):
        # get list of all images
       
        imagelist =  sorted( filter( lambda x: os.path.isfile(os.path.join(self.TEMP_IMAGES_FOLDER, x)),
                        os.listdir(self.TEMP_IMAGES_FOLDER) ) )
        # listdir(self.PATH + self.TEMP_IMAGES_FOLDER)
        pdf = FPDF('P', 'mm', 'A4')  # create an A4-size pdf document
        x, y, w, h = 0, 0, 200, 300
        for image in imagelist:
            pdf.add_page()
            pdf.image(self.PATH + self.TEMP_IMAGES_FOLDER+image, x, y, w, h)

        if os.path.exists(self.PATH + 'output/' + self.PDF_FILE):
            os.remove(self.PATH + 'output/'+self.PDF_FILE)

        pdf.output(self.PATH + 'output/' + self.PDF_FILE, "F")

    def change_background_color(self, rgba):
        self.set_prev_back(rgba)
        self.RGBA = self.json_2_rgb(rgba)
        self.store_pdf_result('change_background_color')
        self.convert_images_to_pdf()
        return self.send_pdf(True)

    def change_text_color(self, rgba):
        print(rgba)
        self.set_prev_text(rgba)
        self.RGBA = self.json_2_rgb(rgba)
        self.store_pdf_result('change_text_color')
        self.convert_images_to_pdf()
        return self.send_pdf(True)

    def change_eye_comfort(self, rgba):
        # print(rgba)
        self.BLUE_PERCENT = rgba.get('b')
        # self.RGBA = self.json_2_rgb(rgba)
        self.store_pdf_result('change_eye_comfort')
        self.convert_images_to_pdf()
        return self.send_pdf(True)

    def dark_mode(self, active):
        back = [15, 23, 42]
        text = [226, 232, 240]
        if(not active):
            text = [0, 0, 0]
            back = [255, 255, 255]
        # self.set_prev_back(self.rgb_2_json(back))
        self.change_text_color(self.rgb_2_json(text))
        self.change_background_color(self.rgb_2_json(back))
        self.convert_images_to_pdf()
        return self.send_pdf(True)


    def set_highlight(self , options): 
        self.HIGHLIGHT_CORS = options
        print(self.HIGHLIGHT_CORS.get('page'))
        self.store_pdf_result('proccess_highlight') 
        self.convert_images_to_pdf()
        return self.send_pdf(True)
