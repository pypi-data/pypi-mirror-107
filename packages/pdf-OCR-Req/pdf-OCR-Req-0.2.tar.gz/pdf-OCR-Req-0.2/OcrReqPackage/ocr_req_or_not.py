import document_engine as d
import cv2
import numpy as np
import os
import fitz
import random
import shutil
# pip install pdfminer
from pdfminer.pdfpage import PDFPage
from PyPDF2 import PdfFileWriter, PdfFileReader

def find_image_pixel_ratio(path,th,debug=False):
	images = d.get_images(path,50)
	#print(images[0])
	pixel_ratio=[]
	estimated_characters=[]
	flag=[]

	document = fitz.open(path)

	for i in range(len(images)):
		if debug==True:
			cv2.imshow('Gray scale image', images[i])
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		
		for l in range(len(images[i])):
			for m in range(len(images[i][0])):
				if images[i][l][m]>=175:
					images[i][l][m]=255
				else:
					images[i][l][m]=0

		if debug==True:
			cv2.imshow('bw image', images[i])
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		
		n_of_white_pix = np.sum(images[i] == 255)
		n_of_black_pix = np.sum(images[i]==0)
		pr=n_of_black_pix/n_of_white_pix
		ec=pr/0.000048

		estimated_characters.append(ec)
		pixel_ratio.append(pr)

		#print(document[i])
		text= document[i].getText()
		#print(len(text),ec)

		if len(text)>ec:
			flag.append(0)
		elif (len(text)<(th*ec)):
			flag.append(1)
		else:
			flag.append(0)

	for i in range(len(flag)):
		if flag[i]==1:
			return(1)
	return(0)

def create_pdf_data(rootdir,out_dir):
	try:
		os.mkdir(rootdir+"/trash")
	except:
		print("exists")

	for subdir, dirs, files in os.walk(rootdir):
	    for file in files:
	    	path=os.path.join(subdir, file)
	    	if file.endswith(".pdf"):
	        	images = d.get_images(path,50)
	        	document = fitz.open(path)
	        	page = fitz.Document() 
	        	
	        	for i in range(len(images)):
	        		if i % random.randint(1,len(images)-1) == 0:
	        			img_rect = document.loadPage(i).MediaBox
	        			cv2.imwrite(rootdir+"/trash/img.png",images[i])
	        			page.insertPage(pno=i)
	        			page[i].insertImage(img_rect, filename=rootdir+"/trash/img.png")

	        		else:
	        			page.insertPDF(document, from_page = i, to_page = i, start_at = i-1)
	        	page.save(out_dir+"/created_"+file)


def get_pdf_searchable_pages(fname):
    searchable_pages = []
    non_searchable_pages = []
    page_num = 0
    with open(fname, 'rb') as infile:

        for page in PDFPage.get_pages(infile):
            page_num += 1
            if 'Font' in page.resources.keys():
                searchable_pages.append(page_num)
            else:
                non_searchable_pages.append(page_num)
    if page_num > 0:
        if len(searchable_pages) == 0:
        	return(1)
        elif len(non_searchable_pages) == 0:
            return(0)
        else:
            return(1)
    else:
        print(f"Not a valid document")


def dir_ocr_req_or_not(rootdir,create_data=False):
	try:
		os.mkdir(rootdir+"/output")
	except:
		print("../output Directory already exists")

	try:
		os.mkdir(rootdir+"/output/ocr_not_required")
	except:
		print("../output/ocr_not_required Directory already exists")

	try:
		os.mkdir(rootdir+"/output/ocr_required")
	except:
		print("../output/ocr_required Directory already exists")

	output_dir_path = rootdir+"/output"
	output_non_ocr_dir_path = rootdir+"/output/ocr_not_required"
	output_ocr_dir_path = rootdir+"/output/ocr_required" 

	if create_data==True:
		created_data_dir = rootdir+"/created_data"
		try:
			os.mkdir(created_data_dir)
		except:
			print("../created_data_dir Directory already exists")
		create_pdf_data(rootdir,created_data_dir)
	
	for subdir, dirs, files in os.walk(rootdir):
		if "/output" not in subdir:
			print(subdir)
			for file in files:
				if file.endswith(".pdf"):
					path=os.path.join(subdir, file)
					ocr_flag = find_image_pixel_ratio(path,0.5)
					print(path)

					OCR_req_flag = get_pdf_searchable_pages(path)

					if ocr_flag == 1 or OCR_req_flag == 1:
						shutil.copy(path,rootdir+"/output/ocr_required")
						print("file - ocr required")

					else:
						shutil.copy(path,rootdir+"/output/ocr_not_required")
						print("file - ocr not required")

def pdf_ocr_req_or_not(path,create_data=False):
	ocr_flag = find_image_pixel_ratio(path,0.5)
	OCR_req_flag = get_pdf_searchable_pages(path)
	if ocr_flag == 1 or OCR_req_flag == 1:
		return(1)
	else:
		return(0)
		        	
					
		        	




