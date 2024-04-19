import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv2.imread("text.png")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

thresh1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 11, 2)

rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

im2 = img.copy()

file = open("recognized.txt", "w+")
file.write("")
file.close()

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
	
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 6)
	
    cropped = im2[y:y + h, x:x + w]
	
    file = open("recognized.txt", "a")
	
    try:
        text = pytesseract.image_to_string(cropped, lang='eng', config='--psm 6')
    except Exception as e:
        print(f"Error during OCR: {e}")
        text = ""
        
    file.write(text)
    file.write("\n")
    file.close
