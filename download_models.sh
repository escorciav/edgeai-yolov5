# Download pretrained YOLOv5-pose models
# Usage: bash download_models.sh
#
# WIP: refactor version. ChatGPT play mambo jambo and didn't help me to come
# out with a nice for loop in bash. EOM - Victor


# models = (
#     "yolov5s6_pose_640 http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/other/best_models/yolov5s6_640_60p7_85p3_kpts_head_6x_dwconv_3x3_lr_0p01/weights/last.pt"
#     "pyolov5s6_pose_960 http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/other/person_detector/yolov5s6_960_71p6_93p1/weights/last.pt"
#     "yolov5m6_pose_960 http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/other/best_models/yolov5m6_960_67p8_89p3_kpts_head_6x_dwconv_3x3_lr_0p01/weights/last.pt"
#     "yolov5l6_pose_960 http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/other/person_detector/yolov5l6_960_74p7_94p0/weights/last.pt"
#     "yolov5s6_pose_640_ti_lite http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/yolov5s6_640_ti_lite_54p9_82p2/weights/last.pt"
#     "yolov5s6_pose_960_ti_lite http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/yolov5s6_960_ti_lite_59p7_85p6/weights/last.pt"
#     "yolov5s6_pose_1280_ti_lite http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/yolov5s6_1280_ti_lite_60p9_85p9/weights/last.pt"
#     "yolov5m6_pose_640_ti_lite http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/yolov5m6_640_ti_lite_60p5_86p8/weights/best.pt"
#     "yolov5m6_pose_960_ti_lite http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/yolov5m6_960_ti_lite_65p9_88p6/weights/last.pt"
# )

# for tuple in "${models[@]}"; do
#   first_string="${tuple%% *}"
#   second_string="${tuple#* }"
#   echo $first_string
#   echo wget $second_string
#   break
# done

model_dir=pretrained_models
dirname=$model_dir/yolov5s6_pose_640; wget http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/other/best_models/yolov5s6_640_60p7_85p3_kpts_head_6x_dwconv_3x3_lr_0p01/weights/last.pt && mkdir -p $dirname && mv last.pt $dirname
dirname=$model_dir/pyolov5s6_pose_960; wget http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/other/person_detector/yolov5s6_960_71p6_93p1/weights/last.pt && mkdir -p $dirname && mv last.pt $dirname
dirname=$model_dir/yolov5m6_pose_960; wget http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/other/best_models/yolov5m6_960_67p8_89p3_kpts_head_6x_dwconv_3x3_lr_0p01/weights/last.pt && mkdir -p $dirname && mv last.pt $dirname
dirname=$model_dir/yolov5l6_pose_960; wget http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/other/person_detector/yolov5l6_960_74p7_94p0/weights/last.pt && mkdir -p $dirname && mv last.pt $dirname
dirname=$model_dir/yolov5s6_pose_640_ti_lite; wget http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/yolov5s6_640_ti_lite_54p9_82p2/weights/last.pt && mkdir -p $dirname && mv last.pt $dirname
dirname=$model_dir/yolov5s6_pose_960_ti_lite; wget http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/yolov5s6_960_ti_lite_59p7_85p6/weights/last.pt && mkdir -p $dirname && mv last.pt $dirname
dirname=$model_dir/yolov5s6_pose_1280_ti_lite; wget http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/yolov5s6_1280_ti_lite_60p9_85p9/weights/last.pt && mkdir -p $dirname && mv last.pt $dirname
dirname=$model_dir/yolov5m6_pose_640_ti_lite; wget http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/yolov5m6_640_ti_lite_60p5_86p8/weights/best.pt && mkdir -p $dirname && mv last.pt $dirname
dirname=$model_dir/yolov5m6_pose_960_ti_lite; wget http://software-dl.ti.com/jacinto7/esd/modelzoo/gplv3/08_02_00_11/edgeai-yolov5/pretrained_models/checkpoints/keypoint/coco/edgeai-yolov5/yolov5m6_960_ti_lite_65p9_88p6/weights/last.pt && mkdir -p $dirname && mv last.pt $dirname
