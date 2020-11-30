import os
import random
import shutil
import numpy
import json
import sys

from IPython import embed
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from PIL import Image
from wand.image import Image as wImage
from docx2pdf import convert


def mergePdf():
    filenames = [f for f in os.listdir(final_dir) if os.path.isfile(os.path.join(final_dir, f))]

    merger = PdfFileMerger()

    for i, filename in enumerate(filenames):
        merge_path = '{directory}/{index}.pdf'.format(
            directory=final_dir,
            index=i)
        merger.append(merge_path)

    final_doc_name = 'see-no-evil'
    final_doc_path = '{final_dir}/{name}.pdf'.format(
      final_dir=final_dir,
      name=final_doc_name)
    merger.write(final_doc_path)
    merger.close()


def scrambled(orig):
    dest = orig[:]
    random.shuffle(dest)
    return dest


def splitPDF(file_name, output_dir=None):
    inputpdf = PdfFileReader(open(file_name, "rb"))
    

    numPages = inputpdf.numPages
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))

        # prev_path = os.path.basename(file_name.replace('.pdf', ''))
        
        output_name = f"{i}.pdf"
        if output_dir is not None:
            output_name = os.path.join(output_dir, output_name)

        with open(output_name, "wb") as outputStream:
            output.write(outputStream)

def pdfToJpg(pdf_file, save_as):
    with(wImage(filename=pdf_file, resolution=450)) as img: 
        with img.convert('png') as converted:
            converted.save(filename=f'{save_as}.png')


def PngImageClasstoImageClass(image):
    minv = numpy.amin(image)
    maxv = numpy.amax(image)
    image = image - minv
    image = image / (maxv - minv)
    image = image * 255
    img = Image.fromarray(image.astype(numpy.uint8))
    return img


def defineHandedness(start_hand):
    if start_hand == 'right' or start_hand == 'r' or start_hand == 'R':
        start_index = 1
    elif start_hand == 'left' or start_hand == 'l' or start_hand == 'L':
        start_index = 0
    else:
        print('Start handedness not specified.')

    return start_index

def makePngTransparent(img, opacity_level = 170):
    datas = img.getdata()

    newData = []
    for item in datas:
        newData.append((0, 0, 0, opacity_level))

    img.putdata(newData)

    return img

  
def sortImgArrByHand(arr, start_index):
    '''
    If start_index is 0 (or even number), assume 0 index is lefthand side.
    If start_index is 1 (or odd number), assume 0 index is righthand side, 
    '''
    print('start index', start_index)
    def is_even(num):
      return (num % 2) == 0

    def on_left_side(index):
        return is_even(index) if is_even(start_index) else not is_even(index)

    def swap_arr_element(array, index):
        array[index], array[index + 1] = array[index + 1], array[index]

    for i, a in enumerate(arr):
        if a[1].startswith('l-') or a[1].startswith('L-') and not on_left_side(i):
            swap_arr_element(arr, i)
            # print('Swap', a[1], i, i+1)
        if a[1].startswith('r-') or a[1].startswith('R-') and on_left_side(i):
            swap_arr_element(arr, i)
            # print('Swap', a[1], i, i+1)
            
    return arr

def combineAssets(temp_dir, img_dir, opacity, page_width, page_height, dpi, start_index):
    temp_pdf_paths = [f for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]
    all_imgs_paths = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f)) and '.png' in f]

    all_pdf_paths = ['{temp_dir}/{index}'.format(temp_dir=temp_dir, index=i) for i in [*range(len(temp_pdf_paths))]]
    # [:len(all_imgs_paths)]
    arr_img_indexes = [(i, all_imgs_paths[i]) for i in [*range(len(all_imgs_paths))]]

    if len(temp_pdf_paths) > len(all_imgs_paths):
        arr_img_indexes = arr_img_indexes + [(i + len(arr_img_indexes), 'blank') for i, x in enumerate(range(len(temp_pdf_paths) - len(all_imgs_paths)))]
    
    scrambled_arr = scrambled(arr_img_indexes)
    scrambled_arr = sortImgArrByHand(scrambled_arr, start_index=start_index)
    for i, page in enumerate(all_pdf_paths):
        animal_index = scrambled_arr[i][0]

        # convert page to png, open it up, and make rgba
        page_path = f'{page}.pdf'        
        pdfToJpg(page_path, save_as=page)
        page_img = Image.open(f'{page}.png')
        page_img = page_img.convert('RGBA')

        if arr_img_indexes[animal_index][1] != 'blank':
            
            # get image and paste it onto page img
            rand_animal = arr_img_indexes[animal_index][1]

            animal_img = Image.open('{dir}/{animal}'.format(
              dir=img_dir,
              animal=rand_animal))
            animal_img = animal_img.resize((page_img.size[0], page_img.size[1]), resample=Image.LANCZOS)

            if animal_img.mode != 'RGBA':
                alpha = Image.new('L', animal_img.size, 255)
                animal_img.putalpha(alpha)

            paste_mark = animal_img.split()[3].point(lambda i: i * opacity / 100.)
            box = (0, 0)
            page_img.paste(animal_img, box=box, mask=paste_mark)

        else:
            print('blank', i)
        page_img = page_img.convert('RGB')
        page_img = page_img.resize((page_width, page_height), resample=Image.LANCZOS)
        final_path = '{final_dir}/{i}'.format(final_dir=final_dir, i=i)
        page_img.save(f'{final_path}.pdf', resolution=dpi, optimize=True)


temp_pdf_dir = 'temp'
final_dir = 'final'

def __main__():
    opacity = None
    image_dir = None
    text_pdf = None
    page_width = 8.75
    page_height = 11.25
    dpi = 300
    start_hand = "right"
    
    # get parameters from json
    with open('parameters.json') as f:
        parameters = json.load(f)
        opacity = parameters.get('opacity')
        image_dir = parameters.get('image_dir')
        text_pdf = parameters.get('text_pdf')
        page_width = parameters.get('page_width')
        page_height = parameters.get('page_height')
        dpi = parameters.get('dpi')
        start_hand = parameters.get('start_hand')

    # px / dpi = inches
    page_pixel_w = int(page_width * dpi)
    page_pixel_h = int(page_height * dpi)
    
    start_index = defineHandedness(start_hand)

    # see if opacity was passed via cmd line
    passed_args = sys.argv
    if (len(passed_args) > 1):
        try:
            opacity = int(passed_args[len(passed_args) - 1])
        except Exception as e:
            print('Exception:', e)

    print(f'An opacity of {opacity} has been set.')
    get_temp_dir = None

    if os.path.exists(temp_pdf_dir):
        shutil.rmtree(temp_pdf_dir)
        os.mkdir(temp_pdf_dir)
    else:
        os.mkdir(temp_pdf_dir)

    if os.path.exists(final_dir):
        shutil.rmtree(final_dir)
        os.mkdir(final_dir)
    else:
        os.mkdir(final_dir)

    splitPDF(text_pdf, temp_pdf_dir)
    combineAssets(
      temp_dir=temp_pdf_dir,
      img_dir=image_dir,
      opacity=opacity,
      page_width=page_pixel_w,
      page_height=page_pixel_h,
      dpi=dpi,
      start_index=start_index)
    mergePdf()


__main__()