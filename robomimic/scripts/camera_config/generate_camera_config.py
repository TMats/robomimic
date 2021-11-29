import argparse
import json
import numpy as np
from sklearn.utils.extmath import cartesian
from scipy.spatial.transform import Rotation as R
from pyquaternion import Quaternion


def polar2cartesian(position):
    x = position[0] * np.sin(position[1]) * np.cos(position[2])
    y = position[0] * np.sin(position[1]) * np.sin(position[2])
    z = position[0] * np.cos(position[1])
    return np.array([x,y,z])

def generate_pose_in_hemisphere(args):
    r_endpoint = args.min_r > np.finfo(float).eps  # avoid singular at origin
    rs = np.linspace(args.max_r, args.min_r, num=args.num_r, endpoint=r_endpoint)
    thetas = np.linspace(np.pi/2, 0.0, num=args.num_theta, endpoint=False)
    phis = np.linspace(0.0, 2*np.pi, num=args.num_phi, endpoint=False)
    # make combination
    polar_positions = cartesian((rs,thetas,phis))
    cartesian_positions = np.apply_along_axis(polar2cartesian, 1, polar_positions)
    # drop duplicated pose along with z-axis
    cartesian_positions, indecies = np.unique(cartesian_positions, axis=0, return_index=True)
    # polar_positions = polar_positions[indecies] #unused

    # calcuate camera coordinates
    # Note: mujoco has different coordinate system than usual
    # X: right, Y: UP, -Z: camera direction
    # https://github.com/yusukeurakami/mujoco_2d_projection 
    camZ_direction = cartesian_positions
    camZ_direction = camZ_direction / np.linalg.norm(camZ_direction, axis=1, keepdims=True)
    camX_direction = np.cross(np.array([0.0, 0.0, 1.0]), camZ_direction)
    camX_direction = camX_direction / np.linalg.norm(camX_direction, axis=1, keepdims=True)
    camY_direction = np.cross(camZ_direction, camX_direction)
    camY_direction = camY_direction / np.linalg.norm(camY_direction, axis=1, keepdims=True)
    rotation_mat = np.zeros((camZ_direction.shape[0], 3, 3))
    rotation_mat[:, :, 0] = camX_direction
    rotation_mat[:, :, 1] = camY_direction
    rotation_mat[:, :, 2] = camZ_direction
    quats = R.from_matrix(rotation_mat).as_quat()    

    # xyzw -> wxyz
    quats = quats[:,[3,0,1,2]]

    cartesian_positions += np.array(args.center)
    poses = np.concatenate((cartesian_positions, quats), axis=1)
    return poses

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--center",
        type=float,
        nargs=3,
        default=[0., 0., 0.],
        help="center of hemisphere",
    )
    parser.add_argument(
        "--min_r",
        type=float,
        default=0.,
        help="minimum of radius",
    )
    parser.add_argument(
        "--max_r",
        type=float,
        default=1.,
        help="maximum of radius",
    )
    parser.add_argument(
        "--num_r",
        type=int,
        default=2,
        help="number of split along with radius",
    )
    parser.add_argument(
        "--num_theta",
        type=int,
        default=2,
        help="number of split in theta angle",
    )
    parser.add_argument(
        "--num_phi",
        type=int,
        default=4,
        help="number of split in phi angle",
    )
    args = parser.parse_args()
    # TODO: reflect argparse
    poses = generate_pose_in_hemisphere(args)
    pose_list = []
    for idx, pose in enumerate(poses):
        pose_list.append(
            {
                "camera_name": "view{}".format(idx),
                "pos": list(pose[:3]),
                "quat": list(pose[3:]),
                "camera_attribs": {}
            }
        )
    with open("testview.json", "w") as f:
        json.dump(pose_list, f, indent=2) 
    



