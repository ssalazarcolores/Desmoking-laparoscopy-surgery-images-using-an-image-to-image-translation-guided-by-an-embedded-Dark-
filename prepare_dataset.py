# -*- coding: utf-8 -*-

import cv2,os, numpy as np, sys
from glob import glob
import shutil
# from options.prepare_data_options import PrepareDataOptions
from natsort import natsorted

def prepare_data(path_root,path_imgs_A,path_imgs_B,path_result,make_dataset=False):
    print('Preparing data to train...')
    print('   Creating directory merged and merging images...')
    names=os.listdir(path_imgs_A)
    names=natsorted(names)
    create_directory('',path_result)

    print('\tDataset size: '+str(len(names)))    
    if len(names)!=len([os.path.basename(f) for f in glob(path_result+"*")]) or make_dataset==True:

        num=1
        for img in names:
            img_A =cv2.imread(path_imgs_A+img,-1)#.astype(np.float)
            img_B = cv2.imread(path_imgs_B+img,-1)#.astype(np.float)
            im_res = cv2.hconcat([img_A, img_B])
            cv2.imwrite(path_result+img,im_res)
            sys.stdout.write("\r\x1b[K\t   "+'Merging '+str(num)+' from '+str(len(names))+' images')
            sys.stdout.flush()
            num+=1
    else:
        sys.stdout.write("\r\x1b[K\t   "+'Merging skipped....')
        
    print('...............................ok!')
        
def create_directory(path_root,name):
    try:
        path=path_root+name
        os.mkdir(path)
    except OSError:
        print ("\tDirectory %s already exists!" % path)
    else:
        print ("\tSuccessfully created the directory %s " % path)
    
    
def separate_data(path_root,path_result,rate):    
    names=os.listdir(path_result)
    names=natsorted(names)
    length_data=len(names)
    train_data=int(len(names)*rate[0]*0.01)
    validation_data=int(len(names)*rate[1]*0.01)
    test_data=length_data-train_data-validation_data

    print('   Creating directories and splitting dataset in train, validation and test with '+str(rate[0])+'%, '+str(rate[1])+'%, '+'and '+str(rate[2])+'% from the total of images, respectively...')
    create_directory(path_root,'train')
    create_directory(path_root,'validation')
    create_directory(path_root,'test')
    print('\n\tTrain dataset will have '+str(train_data)+' images from '+str(length_data))
    print('\tValidation dataset will have '+str(validation_data)+' images from '+str(length_data))   
    print('\tTest dataset will have '+str(test_data)+' images from '+str(length_data)+'\n')
    
    
    cnt=0
    for img in names:
        if cnt<train_data:
            shutil.copy(path_result+img,path_root+'train/')
            sys.stdout.write("\r\x1b[K\t   "+'Moving to train folder: '+str(cnt+1)+' from '+str(train_data))
            if cnt==train_data-1:
                print('...ok!')      
        elif cnt>=train_data and cnt<train_data+validation_data:   
            shutil.copy(path_result+img,path_root+'validation/')
            sys.stdout.write("\r\x1b[K\t   "+'Moving to validation folder: '+str(cnt-train_data+1)+' from '+str(validation_data))
            if cnt==train_data+validation_data-1:
                print('...ok!')  
        elif cnt>=train_data+validation_data:
            shutil.copy(path_result+img,path_root+'test/')
            sys.stdout.write("\r\x1b[K\t   "+'Moving to test folder: '+str(cnt-validation_data-train_data+1)+' from '+str(test_data))
            if cnt==length_data-1:
                print('...ok!')          
        cnt+=1
    
    
    
if  __name__=='__main__':
    path_root='../datasets/laparoscopy_dc/'
    path_imgs_B=path_root+'output/'
    path_imgs_A=path_root+'input/'
    path_result=path_root+'merged/'    
    
    # opt = PrepareDataOptions().parse()
    
    # print(opt)
    
    # path_root=opt.path_root
    # path_imgs_A=opt.path_imgs_A
    # path_imgs_B=opt.path_imgs_B
    # path_result=opt.path_result
    # merge=opt.merge        
    
    
    prepare_data(path_root,path_imgs_A,path_imgs_B,path_result,True)
    separate_data(path_root,path_result,[80, 10, 10])
    print('Beggining training...')
