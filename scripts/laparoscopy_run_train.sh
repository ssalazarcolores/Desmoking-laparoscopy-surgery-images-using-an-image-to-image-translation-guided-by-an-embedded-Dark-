#eval "$(conda shell.bash hook)"
#conda activate keras2# if you have a virtual environment here put its name

cd ../ 

python add_dark_channel.py
cd scripts
python ../prepare_dataset.py


gnome-terminal --title="Training pix2pix net" -x python -i ../train.py --dataroot ../datasets/laparoscopy_dc --name pix2pix_laparoscopy_dc --model pix2pix --which_model_netG unet_256 --which_direction AtoB --lambda_A 100 --dataset_mode aligned --no_lsgan --norm batch --pool_size 0 --niter 50 --niter_decay 5 --loadSize 256 --batchSize 16 




