import cv2
from PIL import Image, ImageEnhance
from matplotlib import pyplot as plt
import numpy as np
import glob
import os

from numpy.core.arrayprint import FloatingFormat

def main():

    dir_name = '0616/3_dimple_suj2_water'
    method_list = ['median', 'max', 'mode']
    method = method_list[2]
    correct_val = 2000

    #make_cool_warm_png(dir_name)
    make_luminance_corrected_png(dir_name, method, correct_val)
    #make_tif_histogram(dir_name, method)
    make_png_histogram(dir_name, method, correct_val)
    make_white_black_gif(dir_name, method, correct_val)
    #make_color_gif(dir_name)


def make_cool_warm_png(dir_name):
    for curdir, dirs, files in os.walk(dir_name):
        for tif_path in sorted(glob.glob(f'{curdir}/*.tif'), key=len):
            tif = cv2.imread(tif_path, -1)

            save_dir_path = 'picture/coolwarm/'+ os.path.split(tif_path)[0]
            save_file_path = save_dir_path +'/' + os.path.splitext(os.path.basename(tif_path))[0] + '.png'
            os.makedirs(save_dir_path, exist_ok=True)

            plt.imshow(tif, cmap='coolwarm')
            plt.colorbar()
            plt.savefig(save_file_path)
            plt.close()

def make_luminance_corrected_png(dir_name, method, correct_val):
    for curdir, dirs, files in os.walk(dir_name):
        for tif_path in sorted(glob.glob(f'{curdir}/*.tif'), key=len):
            tif = cv2.imread(tif_path, -1)

            if method == 'median':
                # median_correction
                # y=ax
                #a*median = 10000
                median_val = np.median(tif)
                a = correct_val / median_val

                tif_corrected = tif*a
                tif_corrected = np.clip(tif_corrected, 0, 2**16-1).astype(np.uint16)

                save_dir_path = 'picture/luminance_corrected_median/'+ os.path.split(tif_path)[0]
                save_file_path = save_dir_path +'/' + os.path.splitext(os.path.basename(tif_path))[0] + '_cval' + str(correct_val) + '.png'

            elif method == 'max':
                # max_correction
                # y=ax
                #a*max = 2**16-1
                max = np.max(tif)
                a = (2**16-1) / max

                tif_corrected = tif*a
                tif_corrected = np.clip(tif_corrected, 0, 2**16-1).astype(np.uint16)

                save_dir_path = 'picture/luminance_corrected_max/'+ os.path.split(tif_path)[0]
                save_file_path = save_dir_path +'/' + os.path.splitext(os.path.basename(tif_path))[0] + '.png'

            elif method == 'mode':
                # mode_correction
                # y=ax
                #a*mode = 10000
                hist, bins = np.histogram(tif)
                mode_val = bins[np.argmax(hist)]

                a = correct_val / mode_val

                tif_corrected = tif*a
                tif_corrected = np.clip(tif_corrected, 0, 2**16-1).astype(np.uint16)

                save_dir_path = 'picture/luminance_corrected_mode/'+ os.path.split(tif_path)[0]
                save_file_path = save_dir_path +'/' + os.path.splitext(os.path.basename(tif_path))[0] + '_cval' + str(correct_val) + '.png'

            os.makedirs(save_dir_path, exist_ok=True)
            cv2.imwrite(save_file_path, tif_corrected)

def make_tif_histogram(dir_name, method):
    for curdir, dirs, files in os.walk(dir_name):
        for tif_path in sorted(glob.glob(f'{curdir}/*.tif'), key=len):
            if not 'histogram' in tif_path:
                tif = cv2.imread(tif_path, -1)

                tif_array = tif.flatten()

                bins_range = range(0,4095,5)

                plt.hist(tif_array, bins=bins_range, label=os.path.basename(tif_path))
                plt.legend(loc='upper right')

        if glob.glob(f'{curdir}/*.tif') != []:
            save_dir_path = f'picture/luminance_corrected_{method}/'+ curdir
            save_file_path = save_dir_path +'/' + 'tif_histogram' + '.png'

            os.makedirs(save_dir_path, exist_ok=True)
            plt.savefig(save_file_path)
            plt.close()

def make_png_histogram(dir_name, method, correct_val):
    for curdir, dirs, files in os.walk(f'picture/luminance_corrected_{method}/' + dir_name):
        for png_path in sorted(glob.glob(f'{curdir}/*{str(correct_val)}.png'), key=len):
            if not 'histogram' in png_path:
                png = cv2.imread(png_path, -1)

                png_array = png.flatten()

                bins_range = range(0,2**16-1,80)

                plt.hist(png_array, bins=bins_range, label=os.path.basename(png_path))
                plt.legend(loc='upper right')

        if glob.glob(f'{curdir}/*.png') != []:
            save_dir_path = curdir
            save_file_path = save_dir_path +'/' + f'{method}_png_histogram' + '_cval' + str(correct_val) + '.png'

            os.makedirs(save_dir_path, exist_ok=True)
            plt.savefig(save_file_path)
            plt.close()

def make_color_gif(dir_name):

    for curdir, dirs, files in os.walk('picture/coolwarm/' + dir_name):
        if 'sliding' in curdir:
            for i in range(len(dirs)):
                png_list = []
                for png_path in sorted(glob.glob(f'{curdir}/{dirs[i]}/*.png'), key=len):
                    png_i = Image.open(png_path)
                    png_list.append(png_i)

                save_dir_path = os.path.split(curdir)[0]
                save_file_path = save_dir_path +'/'+ os.path.split(curdir)[1] +'_'+ dirs[i] +'.gif'

                os.makedirs(save_dir_path, exist_ok=True)
                png_list[0].save(save_file_path, save_all=True, append_images=png_list[1:],
                optimize=False, duration=500, loop=0)

def make_white_black_gif(dir_name, method, correct_val):
    for curdir, dirs, files in os.walk(f'picture/luminance_corrected_{method}/' + dir_name):
        if 'sliding' in curdir:
            for i in range(len(dirs)):
                png_list = []
                for png_path in sorted(glob.glob(f'{curdir}/{dirs[i]}/*{str(correct_val)}.png'), key=len):
                    png_i = Image.open(png_path)

                    png_mat_16bit = np.array(png_i)
                    png_mat_8bit = (png_mat_16bit/(2**8)).astype(np.int)

                    png_i = Image.fromarray(png_mat_8bit, mode='RGBA')
                    png_i = png_i.convert('L').convert('RGBA')
                    png_i = ImageEnhance.Brightness(png_i).enhance(2.0)
                    png_i = ImageEnhance.Contrast(png_i).enhance(2.0)

                    png_list.append(png_i)

                save_dir_path = os.path.split(curdir)[0]
                save_file_path = save_dir_path +'/'+ os.path.split(curdir)[1] +'_'+ dirs[i] + '_cval' + str(correct_val) +'.gif'

                os.makedirs(save_dir_path, exist_ok=True)
                png_list[0].save(save_file_path, save_all=True, append_images=png_list[1:],
                optimize=False, duration=500, loop=0)


if __name__ == '__main__':

    main()
    print('END')