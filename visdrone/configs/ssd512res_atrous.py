# model settings
input_size = 512
model = dict(
    type='SingleStageDetector',
    pretrained='zoo/resnet101-5d3b4d8f.pth',
    backbone=dict(
        type='SSDResNet',
        depth=101,
        num_stages=2,
        out_from=('layer3', '', '', '', '', '', ''),
        out_channels=(-1, 512, 512, 256, 256, 128, 128),
        use_dilation_conv4=True,
        use_dilation_conv5=True,
        use_resblock_in_extra=False,
        style='pytorch',
        frozen_stages=-1,
        norm_cfg=dict(type='BN', requires_grad=True),
        norm_eval=False),
    neck=None,
    bbox_head=dict(
        type='SSDHead',
        input_size=input_size,
        in_channels=(1024, 512, 512, 256, 256, 128, 128),
        num_classes=11,
        anchor_strides=(8, 16, 32, 64, 128, 256, 512),
        basesize_ratio_range=(0.1, 0.9),
        anchor_ratios=([2, 3], [2, 3], [2, 3], [2, 3], [2, 3], [2], [2]),
        target_means=(.0, .0, .0, .0),
        target_stds=(0.1, 0.1, 0.2, 0.2)))
cudnn_benchmark = True
train_cfg = dict(
    assigner=dict(
        type='MaxIoUAssigner',
        pos_iou_thr=0.5,
        neg_iou_thr=0.5,
        min_pos_iou=0.,
        ignore_iof_thr=-1,
        gt_max_assign_all=False),
    smoothl1_beta=1.,
    allowed_border=-1,
    pos_weight=-1,
    neg_pos_ratio=3,
    debug=False)
test_cfg = dict(
    nms=dict(type='nms', iou_thr=0.45),
    min_bbox_size=0,
    score_thr=0.02,
    max_per_img=500)
# model training and testing settings
# dataset settings
dataset_type = 'VisDroneDataset'
data_root = 'data/VisDrone2019-DET/'
img_norm_cfg = dict(mean=[123.675, 116.28, 103.53], std=[1, 1, 1], to_rgb=True)
data = dict(
    imgs_per_gpu=2,
    workers_per_gpu=3,
    train=dict(
        type='RepeatDataset',
        times=5,
        dataset=dict(
            type=dataset_type,
            ann_file=data_root + 'VisDrone2018-DET-train/annotations_train.json',
            img_prefix=data_root + 'VisDrone2018-DET-train/',
            img_scale=(512, 512),
            img_norm_cfg=img_norm_cfg,
            size_divisor=None,
            flip_ratio=0.5,
            with_mask=False,
            with_crowd=False,
            with_label=True,
            test_mode=False,
            extra_aug=dict(
                photo_metric_distortion=dict(
                    brightness_delta=32,
                    contrast_range=(0.5, 1.5),
                    saturation_range=(0.5, 1.5),
                    hue_delta=18),
                expand=dict(
                    mean=img_norm_cfg['mean'],
                    to_rgb=img_norm_cfg['to_rgb'],
                    ratio_range=(1, 4)),
                random_crop=dict(
                    min_ious=(0.1, 0.3, 0.5, 0.7, 0.9), min_crop_size=0.3)),
            resize_keep_ratio=False)),
    val=dict(
        type=dataset_type,
        ann_file=data_root + 'VisDrone2018-DET-val/annotations_val.json',
        img_prefix=data_root + 'VisDrone2018-DET-val/',
        img_scale=(512, 512),
        img_norm_cfg=img_norm_cfg,
        size_divisor=None,
        flip_ratio=0,
        with_mask=False,
        with_label=False,
        test_mode=True,
        resize_keep_ratio=False),
    test=dict(
        type=dataset_type,
        ann_file=data_root + 'VisDrone2018-DET-val/annotations_val.json',
        img_prefix=data_root + 'VisDrone2018-DET-val/',
        img_scale=(512, 512),
        img_norm_cfg=img_norm_cfg,
        size_divisor=None,
        flip_ratio=0,
        with_mask=False,
        with_label=False,
        test_mode=True,
        resize_keep_ratio=False))
# optimizer
optimizer = dict(type='SGD', lr=0.25e-3, momentum=0.9, weight_decay=5e-4)
optimizer_config = dict()
# learning policy
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=1.0 / 3,
    step=[16, 22])
checkpoint_config = dict(interval=1)
# yapf:disable
log_config = dict(
    interval=1,
    hooks=[
        dict(type='TextLoggerHook'),
        dict(type='TensorboardLoggerHook')
    ])
# yapf:enable
# runtime settings
total_epochs = 48
dist_params = dict(backend='nccl')
log_level = 'INFO'
work_dir = './work_dirs/ssd512res'
load_from = None
resume_from = None
workflow = [('train', 1), ('val', 1)]
