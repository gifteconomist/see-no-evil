import os
import random
import shutil
import numpy

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

    merger.write("document-output.pdf")
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


def combineAssets(temp_dir):
    temp_pdf_paths = [f for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]
    all_imgs_paths = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))]

    all_imgs_paths = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))]
    all_pdf_paths = ['{temp_dir}/{index}'.format(temp_dir=temp_dir, index=i) for i in [*range(len(temp_pdf_paths))]][:len(all_imgs_paths)]
    scrambled_arr = scrambled([*range(len(all_imgs_paths))])
    
    for i, page in enumerate(all_pdf_paths):
        rand_animal = all_imgs_paths[scrambled_arr[i]]

        page_path = f'{page}.pdf'

        
        pdfToJpg(page_path, save_as=page)
        
        page_img = Image.open(f'{page}.png')
        page_img = page_img.convert('RGBA')
        animal_img = Image.open('{dir}/{animal}'.format(
          dir=img_dir,
          animal=rand_animal))
        animal_img = animal_img.resize((page_img.size[0], page_img.size[1]))
        
        final_path = '{final_dir}/{i}'.format(final_dir=final_dir, i=i)
        rand_1 = random.randint(0, 1000)
        rand_2 = random.randint(0, 1000)
        box = (rand_1, rand_2)
        box = (0, 0)
        page_img.paste(animal_img, box=box, mask=animal_img)

        page_img = page_img.convert('RGB')
        page_img.save(f'{final_path}.pdf')


source_name = 'Adrianne-WHOLETEXT9'
text_docx = f'source/{source_name}.docx'
text_pdf = f'source/{source_name}.pdf'
temp_pdf_dir = 'temp'
img_dir = 'images'
final_dir = 'final'


def __main__():
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
    combineAssets(temp_pdf_dir)
    mergePdf()


__main__()