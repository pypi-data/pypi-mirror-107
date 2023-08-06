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
"""COLORSPACE
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
#!< COLORSPACE TRANSFORM
#!<----------------------------------------------------------------------------


def _rgb_to_yuv_bt709_videorange_np(image: np.array, is_bgr=False):

  if is_bgr:
    B, G, R = np.split(image, 3, axis=2)
  else:
    R, G, B = np.split(image, 3, axis=2)

  Y = 0.1826 * R + 0.6142 * G + 0.0620 * B + 16  # [16, 235]
  U = -0.1007 * R - 0.3385 * G + 0.4392 * B + 128  # [16, 240]
  V = 0.4392 * R - 0.3990 * G - 0.0402 * B + 128  # [16, 240]

  yuv_image = np.concatenate([Y, U, V], axis=2)
  return yuv_image


def _rgb_to_yuv_bt709_videorange_tensor(image: torch.Tensor, is_bgr=False):

  if is_bgr:
    B, G, R = torch.split(image, 1, dim=-3)
  else:
    R, G, B = torch.split(image, 1, dim=-3)

  Y = 0.1826 * R + 0.6142 * G + 0.0620 * B + 16  # [16, 235]
  U = -0.1007 * R - 0.3385 * G + 0.4392 * B + 128  # [16, 240]
  V = 0.4392 * R - 0.3990 * G - 0.0402 * B + 128  # [16, 240]

  yuv_image = torch.cat([Y, U, V], dim=-3)
  return yuv_image


def _rgb_to_yuv_bt709_fullrange_np(image: np.array, is_bgr=False):

  if is_bgr:
    B, G, R = np.split(image, 3, axis=2)
  else:
    R, G, B = np.split(image, 3, axis=2)

  Y = 0.2126 * R + 0.7152 * G + 0.0722 * B  # [0, 255]
  U = -0.1146 * R - 0.3854 * G + 0.5000 * B + 128  # [0, 255]
  V = 0.5000 * R - 0.4542 * G - 0.0468 * B + 128  # [0, 255]

  yuv_image = np.concatenate([Y, U, V], axis=2)
  return yuv_image


def _rgb_to_yuv_bt709_fullrange_tensor(image: torch.Tensor, is_bgr=False):

  if is_bgr:
    B, G, R = torch.split(image, 1, dim=-3)
  else:
    R, G, B = torch.split(image, 1, dim=-3)

  Y = 0.2126 * R + 0.7152 * G + 0.0722 * B  # [0, 255]
  U = -0.1146 * R - 0.3854 * G + 0.5000 * B + 128  # [0, 255]
  V = 0.5000 * R - 0.4542 * G - 0.0468 * B + 128  # [0, 255]

  yuv_image = torch.cat([Y, U, V], dim=-3)
  return yuv_image


def _yuv_bt709_videorange_to_rgb_np(image: np.array, is_bgr=False):

  Y, U, V = np.split(image, 3, axis=2)

  Y = Y - 16
  U = U - 128
  V = V - 128

  R = 1.1644 * Y + 1.7927 * V
  G = 1.1644 * Y - 0.2132 * U - 0.5329 * V
  B = 1.1644 * Y + 2.1124 * U

  if is_bgr:
    return np.concatenate([B, G, R], axis=2)
  else:
    return np.concatenate([R, G, B], axis=2)


def _yuv_bt709_videorange_to_rgb_tensor(image: torch.Tensor, is_bgr=False):

  Y, U, V = torch.split(image, 1, dim=-3)

  Y = Y - 16
  U = U - 128
  V = V - 128

  R = 1.1644 * Y + 1.7927 * V
  G = 1.1644 * Y - 0.2132 * U - 0.5329 * V
  B = 1.1644 * Y + 2.1124 * U

  if is_bgr:
    return torch.cat([B, G, R], dim=-3)
  else:
    return torch.cat([R, G, B], dim=-3)


def _yuv_bt709_fullrange_to_rgb_np(image: np.array, is_bgr=False):

  Y, U, V = np.split(image, 3, axis=2)

  Y = Y
  U = U - 128
  V = V - 128

  R = 1.000 * Y + 1.570 * V
  G = 1.000 * Y - 0.187 * U - 0.467 * V
  B = 1.000 * Y + 1.856 * U

  if is_bgr:
    return np.concatenate([B, G, R], axis=2)
  else:
    return np.concatenate([R, G, B], axis=2)


def _yuv_bt709_fullrange_to_rgb_tensor(image: torch.Tensor, is_bgr=False):

  Y, U, V = torch.split(image, 1, dim=-3)

  Y = Y
  U = U - 128
  V = V - 128

  R = 1.000 * Y + 1.570 * V
  G = 1.000 * Y - 0.187 * U - 0.467 * V
  B = 1.000 * Y + 1.856 * U

  if is_bgr:
    return torch.cat([B, G, R], dim=-3)
  else:
    return torch.cat([R, G, B], dim=-3)


def _change_colorspace_np(image: np.array, src: T.COLORSPACE, dst: T.COLORSPACE):

  assert isinstance(src, T.COLORSPACE)
  assert isinstance(dst, T.COLORSPACE)

  code = T.COLORSPACE_MAPPING[(src, dst)]

  if code == 'RGB_TO_YUV_BT709_FULLRANGE':
    return _rgb_to_yuv_bt709_fullrange_np(image, is_bgr=False)
  elif code == 'BGR_TO_YUV_BT709_FULLRANGE':
    return _rgb_to_yuv_bt709_fullrange_np(image, is_bgr=True)
  elif code == 'RGB_TO_YUV_BT709_VIDEORANGE':
    return _rgb_to_yuv_bt709_videorange_np(image, is_bgr=False)
  elif code == 'BGR_TO_YUV_BT709_VIDEORANGE':
    return _rgb_to_yuv_bt709_videorange_np(image, is_bgr=True)
  elif code == 'YUV_BT709_FULLRANGE_TO_RGB':
    return _yuv_bt709_fullrange_to_rgb_np(image, is_bgr=False)
  elif code == 'YUV_BT709_FULLRANGE_TO_BGR':
    return _yuv_bt709_fullrange_to_rgb_np(image, is_bgr=True)
  elif code == 'YUV_BT709_VIDEORANGE_TO_RGB':
    return _yuv_bt709_videorange_to_rgb_np(image, is_bgr=False)
  elif code == 'YUV_BT709_VIDEORANGE_TO_BGR':
    return _yuv_bt709_videorange_to_rgb_np(image, is_bgr=True)
  return cv2.cvtColor(image, code)


def _change_colorspace_tensor(image: np.array, src: T.COLORSPACE, dst: T.COLORSPACE):

  assert isinstance(src, T.COLORSPACE)
  assert isinstance(dst, T.COLORSPACE)

  code = T.COLORSPACE_MAPPING[(src, dst)]

  if code == 'RGB_TO_YUV_BT709_FULLRANGE':
    return _rgb_to_yuv_bt709_fullrange_tensor(image, is_bgr=False)
  elif code == 'BGR_TO_YUV_BT709_FULLRANGE':
    return _rgb_to_yuv_bt709_fullrange_tensor(image, is_bgr=True)
  elif code == 'RGB_TO_YUV_BT709_VIDEORANGE':
    return _rgb_to_yuv_bt709_videorange_tensor(image, is_bgr=False)
  elif code == 'BGR_TO_YUV_BT709_VIDEORANGE':
    return _rgb_to_yuv_bt709_videorange_tensor(image, is_bgr=True)
  elif code == 'YUV_BT709_FULLRANGE_TO_RGB':
    return _yuv_bt709_fullrange_to_rgb_tensor(image, is_bgr=False)
  elif code == 'YUV_BT709_FULLRANGE_TO_BGR':
    return _yuv_bt709_fullrange_to_rgb_tensor(image, is_bgr=True)
  elif code == 'YUV_BT709_VIDEORANGE_TO_RGB':
    return _yuv_bt709_videorange_to_rgb_tensor(image, is_bgr=False)
  elif code == 'YUV_BT709_VIDEORANGE_TO_BGR':
    return _yuv_bt709_videorange_to_rgb_tensor(image, is_bgr=True)
  elif code == cv2.COLOR_BGR2RGB:
    b, g, r = torch.split(image, 1, dim=-3)
    return torch.cat([r, g, b], dim=-3)
  elif code == cv2.COLOR_RGB2BGR:
    r, g, b = torch.split(image, 1, dim=-3)
    return torch.cat([b, g, r], dim=-3)
  else:
    raise NotADirectoryError(code)


@T.MetaWrapper(support=[T.ImageMeta, T.VideoMeta, T.BoxListMeta, T.KpsListMeta])
def _change_colorspace_meta(metas: Sequence[T.MetaBase], src: T.COLORSPACE, dst: T.COLORSPACE, **kwargs):

  for meta in metas:

    if meta.source in [T.COLORSPACE.HEATMAP]:
      continue

    if isinstance(meta, T.ImageMeta):
      meta.bin = _change_colorspace_np(meta.bin, src, dst)
      meta.source = dst

    if isinstance(meta, T.VideoMeta):
      for i in range(meta.n):
        meta.bin[i] = _change_colorspace_np(meta.bin[i], src, dst)

  return metas


def change_colorspace(inputs, src: T.COLORSPACE, dst: T.COLORSPACE, **kwargs):
  """inputs will be aspect sized by short side to min_size.

  Args:
      inputs ([type]): [description]
      min_size (int): image will aspect resize according to short side size.
      interpolation ([type], optional): [description]. Defaults to cv2.INTER_LINEAR.

  Returns:
      [type]: [description]
  """
  if T.IsNumpy(inputs):
    return _change_colorspace_np(inputs, src, dst)
  elif T.IsMeta(inputs):
    return _change_colorspace_meta(inputs, src, dst, **kwargs)
  elif T.IsTensor(inputs):
    return _change_colorspace_tensor(inputs, src, dst)
  elif T.IsPilImage(inputs):
    raise NotImplementedError
