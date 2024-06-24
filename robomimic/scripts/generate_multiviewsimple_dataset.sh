# Lift
if [ $1 = "lift" ]; then
python camera_config/generate_camera_config.py \
    --config_path /root/dataset/robomimic/dataset/lift/ph \
    --filename multiview_simple.json \
    --center 0.0 0.0 1.0 --min 1.0 --max 2.0 --num_r 3 --num_theta 4 --num_phi 8
python dataset_states_to_obs.py  \
    --dataset /root/dataset/robomimic/dataset/lift/ph/demo.hdf5 \
    --additional_camera_config=/root/dataset/robomimic/dataset/lift/ph/multiview_simple.json \
    --texture_config=texture_config/simple_arena.json \
    --output_name multiview_simple.hdf5 \
    --camera_names agentview birdview sideview frontview
python playback_dataset.py --use-obs \
    --dataset /root/dataset/robomimic/dataset/lift/ph/multiview_simple.hdf5 \
    --video_path /root/dataset/robomimic/dataset/lift/ph/multiview_simple.mp4 \
    --render_image_names view0 view1 view2 view3 view4 \
    --n 1
# Can
elif [ $1 = "can" ]; then
python camera_config/generate_camera_config.py \
    --config_path /root/dataset/robomimic/dataset/can/ph \
    --filename multiview_simple.json \
    --center 0.0 0.0 1.0 --min 1.0 --max 2.0 --num_r 3 --num_theta 4 --num_phi 8
python dataset_states_to_obs.py  \
    --dataset /root/dataset/robomimic/dataset/can/ph/demo.hdf5 \
    --additional_camera_config=/root/dataset/robomimic/dataset/can/ph/multiview_simple.json \
    --texture_config=texture_config/simple_arena.json \
    --output_name multiview_simple.hdf5 \
    --camera_names agentview birdview frontview
python playback_dataset.py --use-obs \
    --dataset /root/dataset/robomimic/dataset/can/ph/multiview_simple.hdf5 \
    --video_path /root/dataset/robomimic/dataset/can/ph/multiview_simple.mp4 \
    --render_image_names view0 view1 view2 view3 view4 \
    --n 1
fi