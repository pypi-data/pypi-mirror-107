# Copyright 2018 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""CROP
"""
from typing import Sequence
import math
import random
import cv2
import numpy as np
import torch
import torchvision.transforms.functional as tvf
import torchvision.transforms as tvt
import kornia
import PIL

from tw import transform as T
from tw import logger

#!<----------------------------------------------------------------------------
#!< CROP
#!<----------------------------------------------------------------------------


def _get_crop_coords(img_h, img_w, crop_h, crop_w, rh, rw):
  y1 = int((img_h - crop_h) * rh)
  y2 = y1 + crop_h
  x1 = int((img_w - crop_w) * rw)
  x2 = x1 + crop_w
  return x1, y1, x2, y2


def _random_crop_np(inputs: np.array, height, width):
  rh = random.random()
  rw = random.random()

  h, w = inputs.shape[:2]
  new_width = int(w * width) if width < 1 else width
  new_height = int(h * height) if height < 1 else height
  x1, y1, x2, y2 = _get_crop_coords(h, w, new_height, new_width, rh, rw)
  return inputs[y1:y2, x1:x2]


@T.MetaWrapper(support=[T.ImageMeta, T.BoxListMeta, T.VideoMeta, T.KpsListMeta])
def _random_crop_meta(metas: Sequence[T.MetaBase], height, width):
  rh = random.random()
  rw = random.random()

  for meta in metas:

    if isinstance(meta, T.ImageMeta):
      h, w = meta.bin.shape[:2]
      new_width = int(w * width) if width < 1 else width
      new_height = int(h * height) if height < 1 else height
      x1, y1, x2, y2 = _get_crop_coords(h, w, new_height, new_width, rh, rw)
      meta.bin = meta.bin[y1:y2, x1:x2]

    if isinstance(meta, T.VideoMeta):
      h, w = meta.bin.shape[1:3]
      new_width = int(w * width) if width < 1 else width
      new_height = int(h * height) if height < 1 else height
      x1, y1, x2, y2 = _get_crop_coords(h, w, new_height, new_width, rh, rw)
      meta.bin = meta.bin[:, y1:y2, x1:x2]

    if isinstance(meta, T.BoxListMeta):
      assert meta.is_affine_size
      new_width = int(meta.max_x * width) if width < 1 else width
      new_height = int(meta.max_y * height) if height < 1 else height
      x1, y1, x2, y2 = _get_crop_coords(meta.max_y, meta.max_x, new_height, new_width, rh, rw)
      meta.bboxes -= [x1, y1, x1, y1]
      meta.set_affine_size(new_height, new_width)
      meta.clip_with_affine_size()

    if isinstance(meta, T.KpsListMeta):
      assert meta.is_affine_size
      new_width = int(meta.max_x * width) if width < 1 else width
      new_height = int(meta.max_y * height) if height < 1 else height
      x1, y1, x2, y2 = _get_crop_coords(meta.max_y, meta.max_x, new_width, new_height, rh, rw)
      meta.keypoints -= [x1, y1]
      meta.set_affine_size(y2, x2)
      meta.clip_with_affine_size()

  return metas


def random_crop(inputs, height, width):
  """random crop, require width and height less than image

  Args:
      inputs ([type]): [description]
      width (int or float): output width, or keep ratio (0 ~ 1)
      height (int or float): output height, or keep ratio (0 ~ 1)

  Returns:
      [type]: [description]
  """
  if T.IsNumpy(inputs):
    return _random_crop_np(inputs, height, width)
  elif T.IsMeta(inputs):
    return _random_crop_meta(inputs, height, width)
  elif T.IsTensor(inputs):
    return kornia.augmentation.RandomCrop(size=(height, width))(inputs)
  elif T.IsPilImage(inputs):
    return tvt.RandomCrop(size=(height, width))(inputs)


#!<----------------------------------------------------------------------------
#!< CENTER CROP
#!<----------------------------------------------------------------------------

def _get_center_crop_coords(height, width, crop_height, crop_width):
  y1 = (height - crop_height) // 2
  y2 = y1 + crop_height
  x1 = (width - crop_width) // 2
  x2 = x1 + crop_width
  return x1, y1, x2, y2


def _center_crop_np(inputs: np.array, height, width):
  h, w = inputs.shape[:2]
  x1, y1, x2, y2 = _get_center_crop_coords(h, w, height, width)
  return inputs[y1:y2, x1:x2]


@T.MetaWrapper(support=[T.ImageMeta, T.BoxListMeta, T.VideoMeta, T.KpsListMeta])
def _center_crop_meta(metas: Sequence[T.MetaBase], height, width):

  for meta in metas:

    if isinstance(meta, T.ImageMeta):
      h, w = meta.bin.shape[:2]
      x1, y1, x2, y2 = _get_center_crop_coords(h, w, height, width)
      meta.bin = meta.bin[y1:y2, x1:x2]

    if isinstance(meta, T.VideoMeta):
      h, w = meta.bin.shape[1:3]
      x1, y1, x2, y2 = _get_center_crop_coords(h, w, height, width)
      meta.bin = meta.bin[:, y1:y2, x1:x2]

    if isinstance(meta, T.BoxListMeta):
      assert meta.is_affine_size
      x1, y1, x2, y2 = _get_center_crop_coords(meta.max_y, meta.max_x, height, width)
      meta.bboxes -= [x1, y1, x1, y1]
      meta.set_affine_size(height, width)
      meta.clip_with_affine_size()

    if isinstance(meta, T.KpsListMeta):
      assert meta.is_affine_size
      x1, y1, x2, y2 = _get_center_crop_coords(meta.max_y, meta.max_x, height, width)
      meta.keypoints -= [x1, y1]
      meta.set_affine_size(y2, x2)
      meta.clip_with_affine_size()

  return metas


def center_crop(inputs, height, width):
  """crop inputs to target height and width.

  Args:
      inputs ([type]): [description]
      height ([type]): [description]
      width ([type]): [description]

  Returns:
      [type]: [description]
  """
  if T.IsNumpy(inputs):
    return _center_crop_np(inputs, height, width)
  elif T.IsMeta(inputs):
    return _center_crop_meta(inputs, height, width)
  elif T.IsTensor(inputs):
    return kornia.augmentation.CenterCrop(size=(height, width))(inputs)
  elif T.IsPilImage(inputs):
    return tvt.CenterCrop(size=(height, width))(inputs)
