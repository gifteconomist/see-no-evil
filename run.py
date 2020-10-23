import os
import random
import shutil
import numpy
import json

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


def makePngTransparent(img, opacity_level = 170):
    datas = img.getdata()

    newData = []
    for item in datas:
        newData.append((0, 0, 0, opacity_level))

    img.putdata(newData)

    return img

def combineAssets(temp_dir, img_dir, opacity):
    temp_pdf_paths = [f for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]
    all_imgs_paths = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))]

    all_imgs_paths = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))]
    all_pdf_paths = ['{temp_dir}/{index}'.format(temp_dir=temp_dir, index=i) for i in [*range(len(temp_pdf_paths))]][:len(all_imgs_paths)]

    arr_img_indexes = [*range(len(all_imgs_paths))]
    if len(temp_pdf_paths) > len(all_imgs_paths):
        arr_img_indexes = arr_img_indexes + ['blank' for x in range(len(temp_pdf_paths) - len(all_imgs_paths))]
    scrambled_arr = scrambled(arr_img_indexes)
    
    for i, page in enumerate(all_pdf_paths):
        animal_index = scrambled_arr[i]

        # convert page to png, open it up, and make rgba
        page_path = f'{page}.pdf'        
        pdfToJpg(page_path, save_as=page)
        page_img = Image.open(f'{page}.png')
        page_img = page_img.convert('RGBA')

        if animal_index != 'blank':
            # get image and paste it onto page img
            rand_animal = all_imgs_paths[animal_index]

            animal_img = Image.open('{dir}/{animal}'.format(
              dir=img_dir,
              animal=rand_animal))
            animal_img = animal_img.resize((page_img.size[0], page_img.size[1]))

            if animal_img.mode != 'RGBA':
                alpha = Image.new('L', animal_img.size, 255)
                animal_img.putalpha(alpha)

            paste_mark = animal_img.split()[3].point(lambda i: i * opacity / 100.)
            box = (0, 0)
            page_img.paste(animal_img, box=box, mask=paste_mark)

        else:
            print('blank', i)
        page_img = page_img.convert('RGB')
        final_path = '{final_dir}/{i}'.format(final_dir=final_dir, i=i)
        page_img.save(f'{final_path}.pdf')


temp_pdf_dir = 'temp'
final_dir = 'final'

def __main__():
    opacity = None
    image_dir = None
    text_pdf = None
    
    with open('parameters.json') as f:
        parameters = json.load(f)
        opacity = parameters.get('opacity')
        image_dir = parameters.get('image_dir')
        text_pdf = parameters.get('text_pdf')

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
      opacity=opacity)
    mergePdf()


__main__()