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
"""PAD
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
#!< PAD VALUE
#!<----------------------------------------------------------------------------

def _pad_np(inputs, left, top, right, bottom, fill_value=0):

  if inputs.ndim == 3:
    h, w, c = inputs.shape
  else:
    h, w = inputs.shape

  new_w = left + w + right
  new_h = top + h + bottom

  if inputs.ndim == 3:
    img = np.ones(shape=[new_h, new_w, c], dtype=inputs.dtype) * fill_value
    img[top:top+h, left:left+w, :] = inputs
  else:
    img = np.ones(shape=[new_h, new_w], dtype=inputs.dtype) * fill_value
    img[top:top+h, left:left+w] = inputs

  return img


@T.MetaWrapper(support=[T.ImageMeta, T.BoxListMeta, T.KpsListMeta])
def _pad_meta(metas: Sequence[T.MetaBase], left, top, right, bottom, fill_value=0):
  r"""pad space around sample.
  """
  for meta in metas:

    if isinstance(meta, T.ImageMeta):
      h, w, c = meta.bin.shape
      new_w = left + w + right
      new_h = top + h + bottom
      img = np.ones(shape=[new_h, new_w, c], dtype=meta.bin.dtype) * fill_value
      img[top:top+h, left:left+w, :] = meta.bin
      meta.bin = img

    if isinstance(meta, T.BoxListMeta):
      assert meta.is_affine_size
      meta.bboxes += [left, top, left, top]
      width = meta.max_x + left + right
      height = meta.max_y + top + bottom
      meta.set_affine_size(height, width)
      meta.clip_with_affine_size()

    if isinstance(meta, T.KpsListMeta):
      assert meta.is_affine_size
      meta.keypoints += [left, top]
      width = meta.max_x + left + right
      height = meta.max_y + top + bottom
      meta.set_affine_size(height, width)
      meta.clip_with_affine_size()

  return metas


def pad(inputs, left, top, right, bottom, fill_value=0):
  if T.IsNumpy(inputs):
    raise _pad_np(inputs, left, top, right, bottom, fill_value=fill_value)
  elif T.IsMeta(inputs):
    return _pad_meta(inputs, left, top, right, bottom, fill_value=fill_value)
  elif T.IsTensor(inputs):
    raise NotImplementedError
  elif T.IsPilImage(inputs):
    return tvt.Pad((left, top, right, bottom), fill=fill_value)(inputs)


#!<----------------------------------------------------------------------------
#!< PAD TO SIZE DIVISIBLE
#!<----------------------------------------------------------------------------

def _pad_to_size_divisible_np(image_list: Sequence[np.array], size_divisible=32):
  max_size = list(max(s) for s in zip(*[img.shape for img in image_list]))
  max_size[1] = int(math.ceil(max_size[1] / size_divisible) * size_divisible)
  max_size[2] = int(math.ceil(max_size[2] / size_divisible) * size_divisible)
  max_size = tuple(max_size)
  batch_shape = (len(image_list),) + max_size
  batched_imgs = image_list[0].new(*batch_shape).zero_()
  for img, pad_img in zip(image_list, batched_imgs):
    pad_img[: img.shape[0], : img.shape[1], : img.shape[2]].copy_(img)
  return batched_imgs


def pad_to_size_divisible(input_list, size_divisible=32, **kwargs):
  """padding images in a batch to be divisible

  Args:
      image_list list[nd.array]:
      size_divisible: padding to divisible image list

  Returns:
      [np.array]: image_list nd.array[N, C, H, W]
  """
  assert isinstance(input_list, (list, tuple))
  if isinstance(input_list[0], np.array):
    return _pad_to_size_divisible_np(input_list, size_divisible=size_divisible)
  else:
    raise NotImplementedError
