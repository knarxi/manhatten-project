
import pytesseract
import cv2
from PIL import Image, ImageGrab, ImageFilter, ImageEnhance
import numpy as np
import io

from templates import table_dict


CARD_VALUES = "23456789TJQKA"
CARD_SUITES = "CDHS"

#t3 = Image.open('hurz2322222233.jpg')
#t2 = cv2.imread('hurz2322222233.jpg')
#t = cv2.imread('tesseracttest.png')
#s = cv2.imread("spin pp2.png")
s2 = Image.open("spin pp2.png")
filename = 'hurz2322222233.jpg'


def take_screenshot():
    screenshot = ImageGrab.grab()
    return screenshot

def find_template_on_screen(template,cv2_screenshot, threshold):
    """Find tempalte on screen"""
    # 'cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
    # 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    method = eval('cv2.TM_SQDIFF_NORMED')
    # Apply template Matching
    res = cv2.matchTemplate(cv2_screenshot, template, method)
    loc = np.where(res <= threshold)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        bestFit = min_loc
    else:
        bestFit = max_loc

    count = 0
    points = []
    for pt in zip(*loc[::-1]):
        count += 1
        points.append(pt)

    return count, points, bestFit, min_val


def crop_screenshot_with_topleft_corner(screenshot, topleft_corner):
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)
    count, points, bestfit, minimum_value = find_template_on_screen(topleft_corner, img, 0.01)
    cropped_screenshot = screenshot.crop((bestfit[0], bestfit[1], bestfit[0] + 858, bestfit[1] + 629))

    return cropped_screenshot


def binary_pil_to_cv2(img):
    return cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

def pil_to_cv2(img):
    return cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

def cv2_to_pil(img):
    return Image.fromarray(img)



def check_if_image_in_range(template, screenshot, x1, y1, x2, y2):
    cropped_screenshot = screenshot.crop((x1, y1, x2, y2))
    cropped_screenshot = pil_to_cv2(cropped_screenshot)
    #cv2.imwrite(filename, img)
    count, points, bestfit, minimum_value = find_template_on_screen(template, cropped_screenshot, 0.01)
    return count >= 1

def is_template_in_search_area(table_dict, screenshot, image_name, image_area, player=None):
    template_cv2 = table_dict[image_name]
    search_area = table_dict[image_area]
    #cv2.imwrite(filename,template_cv2)
    return check_if_image_in_range(template_cv2, screenshot,
                                   search_area[0], search_area[1], search_area[2], search_area[3])




def get_ocr_str(img,config):
    basewidth = 300
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img_resized = img.convert('L').resize((basewidth, hsize), Image.ANTIALIAS)
    img_min = img_resized.filter(ImageFilter.MinFilter)
    #img_mod = img_resized.filter(ImageFilter.ModeFilter)
    #img_med = img_resized.filter(ImageFilter.MedianFilter)
    #img_sharp = img_resized.filter(ImageFilter.SHARPEN)
    text = pytesseract.image_to_string(img_min,config=config)
    return text

def get_ocr_string(img):
    rgb = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    #gray = cv2.medianBlur(gray, 3)

    text = pytesseract.image_to_string(gray, 'eng',
                                       config='--psm 6 --oem 1 ')
    return text

def ocr(screenshot, image_area, table_dict, player=None):
    """
    get ocr of area of screenshot

    Args:
        screenshot: pil image
        image_area: area name
        table_dict: table dict

    Returns:
        player names or funds
    """
    search_area = table_dict[image_area]
    cropped_screenshot = screenshot.crop((search_area[0], search_area[1], search_area[2], search_area[3]))
    if player:
        config = r'--psm 6 --oem 1'
    else:
        config = r'--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789.'
    return get_ocr_str(cropped_screenshot,config)




b = ocr (s2,"game_number", table_dict)
print(b)







#z=get_ocr_string(img_med)
#z2=get_ocr_float(img_min)
#print(z2)
#print(z)