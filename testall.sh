for i in `seq 1 18`
do
    python changecpt.py $i
    CUDA_VISIBLE_DEVICES=$1 python setup.py build develop
    CUDA_VISIBLE_DEVICES=$1 python tools/test_net.py --config-file configs/e2e_mask_rcnn_R_50_FPN_1x.yaml
done
