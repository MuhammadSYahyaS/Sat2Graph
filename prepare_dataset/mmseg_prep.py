import glob
import os
import shutil
import sys

import cv2
import numpy as np
from tqdm import tqdm


def main():
    assert len(sys.argv) == 2, "Usage: python3 mmseg_prep.py <input dir>"
    input_dir = sys.argv[1]
    if "omani_cities" in input_dir:
        rs = np.random.RandomState(np.random.MT19937(
            np.random.SeedSequence(987654321)))
        indices = set(range(180))
        exclude_no_roads = set([27, 28, 34, 75, 76])
        exclude_too_few_roads = set(
            [29, 30, 31, 35, 39, 41, 42, 49, 111, 126, 127, 168, 177, 178])
        # include_no_roads = set([33, 38, 72, 110, 118])
        indices = list(indices.difference(
            exclude_no_roads.union(exclude_too_few_roads)))
        rs.shuffle(indices)
        i_t = int(len(indices) * 0.7)
        i_v = i_t + int(len(indices) * 0.1)
        indrange_train = indices[:i_t]
        indrange_validation = indices[i_t:i_v]
        indrange_test = indices[i_v:]
        out_dir = "omani_cities_mmseg"
        os.makedirs(os.path.join(out_dir, "img_dir", "train"), exist_ok=True)
        os.makedirs(os.path.join(out_dir, "img_dir", "val"), exist_ok=True)
        os.makedirs(os.path.join(out_dir, "img_dir", "test"), exist_ok=True)
        os.makedirs(os.path.join(out_dir, "ann_dir", "train"), exist_ok=True)
        os.makedirs(os.path.join(out_dir, "ann_dir", "val"), exist_ok=True)
        os.makedirs(os.path.join(out_dir, "ann_dir", "test"), exist_ok=True)

        for subset, indrange_subset in {"train": indrange_train, "val": indrange_validation, "test": indrange_test}.items():
            for i in tqdm(indrange_subset):
                shutil.copy2(os.path.join(input_dir, "region_%d_sat.png" % i), os.path.join(out_dir, "img_dir", subset, "region_%d_sat.png" % i))
                ann_img = cv2.imread(os.path.join(input_dir, "region_%d_gt.png" % i), cv2.IMREAD_GRAYSCALE)
                ann_img = np.divide(ann_img, 255).astype(np.uint8)
                cv2.imwrite(os.path.join(out_dir, "ann_dir", subset, "region_%d_gt.png" % i), ann_img)
    else:
        raise NotImplementedError("the dataset is not yet supported")


if __name__ == "__main__":
    main()
