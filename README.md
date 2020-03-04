# Desmoking laparoscopy surgery images using an image-to-image translation guided by an embedded Dark channel


## Abstract

In laparoscopic surgery, image quality can be severely degraded by smoke caused by the use of dissection tools and $CO_2$ reducing the visibility of the observed organs and tissues. This lack of visibility increases the possibility of mistakes and surger=100x20y time with negative consequences on the patient's health. In this paper, a novel computational approach to remove the smoke effects is introduced. The proposed method is based on an Image-to-Image conditional generative adversarial network in which the dark channel is used as an embedded guide mask. Obtained experimental results are evaluated and compared quantitatively with other desmoking and dehazing state-of-art methods using the metrics of the Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity (SSIM) index. Based on these metrics, it is found that the proposed algorithm has improved performance compared to the state-of-the-art.
Moreover, the time processing required by the proposed method of 92 fps showed that it can be applied to real-time medical systems, and even in an embedded device.


## Sample animation result

[![Demo sample result](lap.gif)](https://youtu.be/Gw8OZNDdicE)


## Neural network

<img src="GAN3-1.png" alt="Neural network" width="500"/>

## How to test

* Place the input laparoscopic images

> - path='./img_test/input/'

* The results will be saved in

> - path='./img_test/output/'





and Run
main_run.py

The result will be saved in
pred_dir='./Desmoked'
