from paddleocr import PaddleOCR,draw_ocr


def text_extractor(file_path):
    """
    Process the file and return extracted text using pytesseract.
    """
    extracted_text = ""
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
     
    result = ocr.ocr(file_path, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        try:
            for line in res:
                extracted_text += line[-1][0] + " \n\n"
        except:
            pass
    
    return extracted_text

