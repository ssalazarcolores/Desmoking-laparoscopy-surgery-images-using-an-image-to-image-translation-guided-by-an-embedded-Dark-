import os,sys,cv2,torch,torchvision.transforms as transforms,numpy as np
from add_dark_channel import add_guide_channel
from models.networks import define_G
from os import scandir, getcwd
from timeit import default_timer as timer
from datetime import datetime

def ls(ruta = getcwd()):
    return [arch.name for arch in scandir(ruta) if arch.is_file()]

class desmoker():
    def __init__(self,model_path):
        self.model = define_G()
        self.transform_list = [transforms.ToTensor(),transforms.Normalize((0.5, 0.5, 0.5,0.5),(0.5, 0.5, 0.5,0.5))]
        self.transform = transforms.Compose(self.transform_list)
        self.model.load_state_dict(torch.load(model_path))
        self.device = torch.device("cuda" if torch.cuda.is_available()else "cpu")
        self.model.eval()

    def tensor2im(self,image_tensor, imtype=np.uint8):
        image_numpy = image_tensor[0].cpu().float().numpy()
        if image_numpy.shape[0] == 1:
            image_numpy = np.tile(image_numpy, (3, 1, 1))
        image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 1) / 2.0 * 255.0
        return image_numpy.astype(imtype)

    def apply(self,img):
        im_tmp=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_ex=add_guide_channel(im_tmp)
        #cv2.imwrite('./img_test/dark/' + url, im_ex[:, :, 3:4])
        im_ex=self.transform(im_ex)
        input = im_ex.unsqueeze(0).to(self.device)
        output = self.model(input)
        return self.tensor2im(output.data)





# ////////////////////////////////////////////////////////////////////////////
# video path
path = './img_test/'
# //////////////////////////////////////////////////////////////////
pathin= path + 'input/'
# output path
pathout = path + 'output/'
# -----------------------------------------------------------------------------
#file list
urls= ls(pathin)

cnt = 0
model_path='./scripts/checkpoints/pix2pix_laparoscopy_ds/best_net_G.pth'
dsmk=desmoker(model_path)


start = datetime.now()

for url in urls:
    img = cv2.imread(pathin + url)
    sys.stdout.write("\r\x1b[K\t   "+'Computing image '+str(cnt)+' from '+str(len(urls))+' images')
    sys.stdout.flush()
    cnt += 1
    img = cv2.resize(img,(256, 256))
    img2 = np.empty_like(img)
    img2 = dsmk.apply(img)
    cv2.imwrite(pathout + url, cv2.cvtColor(img2[:,:,:3], cv2.COLOR_RGB2BGR))
    
now = datetime.now()
time_elapsed=now-start

print("\nTime elapsed =", time_elapsed)

