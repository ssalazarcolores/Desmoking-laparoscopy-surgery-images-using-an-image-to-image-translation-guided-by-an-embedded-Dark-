from matplotlib import pyplot as plt
import os,sys,cv2,numpy as np;
from matplotlib import pyplot as plt
import glob


def compute_dc(im,sz):
    b,g,r = cv2.split(im)
    min_dc = cv2.min(cv2.min(r,g),b);
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(sz,sz))
    dark = cv2.erode(min_dc,kernel)
    return dark, min_dc

def apply_guided_filter(im,p,r,eps):
    mean_I = cv2.boxFilter(im,cv2.CV_64F,(r,r));
    mean_p = cv2.boxFilter(p, cv2.CV_64F,(r,r));
    mean_Ip = cv2.boxFilter(im*p,cv2.CV_64F,(r,r));
    cov_Ip = mean_Ip - mean_I*mean_p;

    mean_II = cv2.boxFilter(im*im,cv2.CV_64F,(r,r));
    var_I   = mean_II - mean_I*mean_I;

    a = cov_Ip/(var_I + eps);
    b = mean_p - a*mean_I;

    mean_a = cv2.boxFilter(a,cv2.CV_64F,(r,r));
    mean_b = cv2.boxFilter(b,cv2.CV_64F,(r,r));

    q = mean_a*im + mean_b;
    return q;

def refine_dc(im,dc,min_dc):
    r = 15;
    eps = 0.0001;
    dc_rfd = apply_guided_filter(min_dc,dc,r,eps);
    return min_dc;


def get_refined_dc(path_image):
    input_img = cv2.imread(path_image);
    dc,min_dc=compute_dc(input_img.astype('float64')/255,15)
    dc=refine_dc(input_img,dc,min_dc)*255
    dc[dc<0]=0
    dc[dc>255]=255
    return np.uint8(dc), input_img

def add_guide_channel(input_img):
    dc,min_dc=compute_dc(input_img.astype('float64')/255,15)
    dc_rfd=refine_dc(input_img,dc,min_dc)*255
    dc_rfd[dc_rfd<0]=0
    dc_rfd[dc_rfd>255]=255
    dark = np.expand_dims(np.uint8((dc_rfd)), axis=2)
    RGBD=np.concatenate((input_img,dark),axis=2)
    return RGBD

def createRGBD (img,path_input,path_result):
    cad=img.replace('jpg', 'png')
    dark1,img1=get_refined_dc(path_input+'/input/'+img)
    dark2,img2=get_refined_dc(path_input+'/output/'+img)
    dark1 = np.expand_dims(dark1, axis=2)
    RGBD1=np.concatenate((img1,dark1),axis=2)
    RGBD2=np.concatenate((img2,dark1),axis=2)
    cv2.imwrite(path_result+'/input/'+cad,RGBD1)
    cv2.imwrite(path_result+'/output/'+cad,RGBD2)

def add_DC_as_aplha(path_input,path_result):
    try:
        os.makedirs(path_result+'/input/');
        os.makedirs(path_result+'/output/');
    except OSError:
        pass

    num=1
    images = glob.glob(path_input+'/input/*.jpg')
    print(len(images))

    for img in images:
        createRGBD(os.path.basename(img),path_input,path_result)

        sys.stdout.write("\r\x1b[K\t   "+'Computing and adding dark channel to alpha channel '+str(num)+' from '+str(len(images))+' images')
        sys.stdout.flush()
        num+=1

if __name__ == '__main__':
    path_input='./datasets/laparoscopy/'
    path_result='./datasets/laparoscopy_dc/'
    add_DC_as_aplha(path_input,path_result)
