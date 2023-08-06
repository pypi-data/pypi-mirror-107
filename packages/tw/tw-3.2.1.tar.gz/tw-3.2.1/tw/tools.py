# Copyright 2020 The KaiJIN Authors. All Rights Reserved.
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
r"""TensorWrapper Tools
"""
import os  # nopep8
import warnings  # nopep8
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # nopep8
warnings.simplefilter("ignore", UserWarning)  # nopep8
warnings.simplefilter("ignore", FutureWarning)  # nopep8

import re
import argparse
import sys
import glob
import shutil
import pickle
import subprocess
import psutil
import xml.etree.ElementTree as ET
import time

import torch
import torchvision
import tw

from tensorboard.backend.event_processing import event_accumulator

import matplotlib.pyplot as plt
import matplotlib.pylab as plb

#!<----------------------------------------------------------------------------
#!< busy
#!<----------------------------------------------------------------------------


class BusyTasker():

  def __init__(self, config):
    self.config = config
    self.device = 'cuda:{}'.format(config.dist_rank)
    print(self.config, self.device)

  def __call__(self):
    model = torchvision.models.resnet152()
    model.to(self.device)

    count = 0
    while True:
      t1 = time.time()
      with torch.no_grad():
        inputs = torch.rand(128, 3, 224, 224).float().to(self.device)
        model(inputs)
      t2 = time.time()
      time.sleep(1.0)
      count += 1
      print('[Elapsed] {}: {}'.format(count, (t2 - t1) * 1000.0))


def busy(parser):
  tw.runner.launch(parser, BusyTasker)


#!<----------------------------------------------------------------------------
#!< monitor
#!<----------------------------------------------------------------------------


def monitor_kill(process_name):
  for proc in psutil.process_iter():
    try:
      pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cmdline'])
    except psutil.NoSuchProcess:
      pass
    else:
      for cmd in pinfo['cmdline']:
        if process_name in cmd and 'tw.tools' not in cmd:
          print(pinfo)
          os.system('kill -9 %d' % pinfo['pid'])
          break


def monitor_usage(proc_name):
  r"""monitor cpu and gpu activity status.

    e.g.
      python -m tw.tools monitor --task usage --src name

  """
  # find corresponding name
  pid = None

  try:
    pid = int(proc_name)

  except Exception as e:
    for proc in psutil.process_iter():
      pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cmdline'])
      if pinfo['name'] == proc_name:
        pid = pinfo['pid']
        break

      # for cmd in pinfo['cmdline']:
      #   if proc_name in cmd:
      #     if pinfo['pid'] == os.getpid():
      #       continue
      #     pid = pinfo['pid']
      #     print(pinfo)
      # if pid is not None:
      #   break

  if pid is None:
    raise ValueError(f'Failed to find {proc_name}')

  # create proc
  proc = psutil.Process(pid=pid)

  # initialize
  logger = tw.utils.logger.Logger()
  logger.init('monitor.{}.{}.log'.format(proc_name, int(time.time())), './')
  logger.info('=> {}'.format(proc))

  while True:
    memory_rss = proc.memory_info().rss / 1024.0 / 1024.0
    memory_vms = proc.memory_info().vms / 1024.0 / 1024.0
    memory_shared = proc.memory_info().shared / 1024.0 / 1024.0
    memory_text = proc.memory_info().text / 1024.0 / 1024.0
    cpu_usage = proc.cpu_percent(interval=0.1)
    num_thread = proc.num_threads()
    tick = int(time.time() * 10**3)  # precision to ms
    logger.info('{}, cpu, {}, {}, {}, {}, {}, {}, {}'.format(
        tick, num_thread, memory_rss, memory_vms,
        memory_shared, memory_text, cpu_usage, num_thread))

    try:
      res = subprocess.check_output('nvidia-smi -q -x', shell=True)
      s = 'gpu'
      if res is not None:
        res = ET.fromstring(res)
        for g in res.findall('gpu'):
          s += ', ' + g.find('fb_memory_usage').find('used').text.split(' MiB')[0]
      tick = int(time.time() * 10**3)  # precision to ms
      logger.info('{}, {}'.format(tick, s))

    except:
      pass


def monitor_hook(process_name):
  while(1):
    try:
      monitor_usage(process_name)
    except Exception as e:
      print('[WARN] Sleep for 5 seconds to scan again.')
      time.sleep(5)


def monitor_plot(src, dst=None, legend=None):
  r"""visualize monitor result and compare such logs

   e.g.
    python -m tw.tools monitor \
      --task plot \
      --src monitor.203482.1608025215.log,monitor.265693.1608025607.log,monitor.112314.1608026529.log \
      --legend vanilla,vsr-v2,vsr-v1

  """
  print('=> tw.tools.monitor: visualize monitor result.')

  inputs = src.split(',')

  if legend:
    legends = legend.split(',')
  else:
    legends = [i for i in inputs]

  if dst is None:
    dst = 'monitor.png'

  sources = []
  for idx, src in enumerate(inputs):
    info = {
        'memory_rss': [],
        'memory_gpu': [],
        'usage_cpu': [],
        'tick_cpu': [],
        'tick_cpu_init': 0,
        'count_cpu': 0,
        'tick_gpu': [],
        'tick_gpu_init': 0,
        'count_gpu': 0,
    }

    assert os.path.exists(src), "File not found."
    with open(src) as fp:
      for line in fp:
        line = line.replace('\n', '')
        if 'cpu,' in line:
          res = line.split(',')
          tick = float(res[0].split(' [INF] ')[1]) / 1000.0
          if info['count_cpu'] == 0:
            info['tick_cpu_init'] = tick
          info['tick_cpu'].append(tick - info['tick_cpu_init'])

          info['memory_rss'].append(float(res[3]))
          info['usage_cpu'].append(float(res[7]))
          info['count_cpu'] += 1

        if 'gpu,' in line:
          res = line.split(',')
          tick = float(res[0].split(' [INF] ')[1]) / 1000.0
          if info['count_gpu'] == 0:
            info['tick_gpu_init'] = tick
          info['tick_gpu'].append(tick - info['tick_gpu_init'])

          info['memory_gpu'].append(int(res[2]))  # default to use gpu-0
          info['count_gpu'] += 1

    sources.append(info)
    plt.figure(figsize=(16, 16))

    plt.subplot(3, 1, 1)
    plt.title('CPU Memory Resource (MB)')
    for i, s in enumerate(sources):
      plt.plot(s['tick_cpu'], s['memory_rss'], label=legends[i])
    plt.grid()
    plt.xlabel('time')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.title('GPU Memory Resource (MB)')
    for i, s in enumerate(sources):
      plt.plot(s['tick_gpu'], s['memory_gpu'], label=legends[i])
    plt.grid()
    plt.xlabel('time')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.title('CPU Usage (interval: 1s) %')
    for i, s in enumerate(sources):
      plt.plot(s['tick_cpu'], s['usage_cpu'], label=legends[i])
    plt.grid()
    plt.xlabel('time')
    plt.legend()

    plt.savefig(dst)

  print(f'=> Successfully output to {dst}.')


#!<----------------------------------------------------------------------------
#!< media
#!<----------------------------------------------------------------------------

#!<----------------------------------------------------------------------------
#!< tensor event
#!<----------------------------------------------------------------------------


class TFEventAccumulator():
  def __init__(self, root):
    # root
    if not os.path.exists(root):
      raise FileExistsError(root)
    self._root = root

    # store all info
    self._kv = {
        'images': [],
        'audio': [],
        'histograms': [],
        'scalars': {},
        'distributions': [],
        'tensors': [],
        'graph': False,
        'meta_graph': False,
        'run_metadata': []
    }

  def dump(self):
    with open('%s.pkl' % self._root, 'wb') as fw:
      pickle.dump(self._kv, fw)

  def load_scalars(self):
    # parse all info at root dir
    files = glob.glob('%s/*/events.out.tfevents.*' % self._root)
    for path in files:
      tag = path.split('/')[-2]
      ea = event_accumulator.EventAccumulator(path)
      ea.Reload()
      for key in ea.Tags()['scalars']:
        vals = [(int(scalar.step), scalar.value) for scalar in ea.Scalars(key)]
        self._kv['scalars'][tag + '/' + key] = [v for v in zip(*vals)]

  @property
  def epoch(self):
    models = glob.glob('%s/model.epoch-*' % self._root)
    epoches = [int(re.findall('model.epoch-(.*?).step', model)[0]) for model in models]
    return max(epoches) if len(epoches) else 0

  @property
  def kv(self):
    return self._kv

  @property
  def root(self):
    return self._root


def event_count(root):
  training_dirs = glob.glob('%s/*' % root)
  training_dirs.sort()
  for folder in training_dirs:
    if os.path.isdir(folder):
      event = TFEventAccumulator(folder)
      print('MODEL:', event.root, 'EPOCH:', event.epoch)


def event_clear(root):
  training_dirs = glob.glob('%s/*' % root)
  training_dirs.sort()
  for folder in training_dirs:
    if os.path.isdir(folder):
      event = TFEventAccumulator(folder)
      if event.epoch == 0:
        shutil.rmtree(event.root)
        print('REMOVE EMPTY FOLDER:', event.root)


def event_dump(root):
  training_dirs = glob.glob('%s/*' % root)
  for folder in training_dirs:
    if os.path.isdir(folder):
      event = TFEventAccumulator(folder)
      if event.epoch != 0:
        print('MODEL:', event.root, 'EPOCH:', event.epoch)
        event.load_scalars()
        event.dump()

#!<----------------------------------------------------------------------------
#!< checkpoint
#!<----------------------------------------------------------------------------


if __name__ == "__main__":
  # domain first
  domain = sys.argv[1]
  assert domain in ['monitor', 'media', 'event', 'checkpoint', 'busy']

  # parser
  parser = argparse.ArgumentParser()

  if domain == 'monitor':
    parser.add_argument('--task', type=str, choices=['usage', 'plot', 'kill', 'hook', 'busy'])
    parser.add_argument('--src', type=str, help='pid name or process name.')
    parser.add_argument('--dst', type=str, help='output folder for plot.')
    parser.add_argument('--legend', type=str)
    args, _ = parser.parse_known_args()

    if args.task == 'kill':
      monitor_kill(args.src)

    elif args.task == 'usage':
      monitor_usage(args.src)

    elif args.task == 'hook':
      monitor_hook(args.src)

    elif args.task == 'plot':
      monitor_plot(args.src, dst=args.dst, legend=args.legend)

  elif domain == 'busy':
    busy(parser)

  elif domain == 'media':
    parser.add_argument('--task', type=str, choices=['vid2img', 'img2vid', 'concat_image'])
    parser.add_argument('--src', type=str, help='image folder, video path, image paths.')
    parser.add_argument('--dst', type=str, help='output folder.')
    args, _ = parser.parse_known_args()

  elif domain == 'event':
    parser.add_argument('--task', type=str, choices=['plot', 'count', 'clear', 'dump', 'compare'])
    parser.add_argument('--src', type=str, default=None)
    parser.add_argument('--dst', type=str, default=None)
    args, _ = parser.parse_known_args()

    if args.task == 'count':
      event_count(args.src)

    elif args.task == 'clear':
      event_clear(args.src)

    elif args.task == 'dump':
      event_dump(args.src)

    elif args.task == 'plot':
      pass

    elif args.task == 'compare':
      pass

  elif domain == 'checkpoint':
    parser.add_argument('--task', type=str, choices=['replace_prefix'])
    parser.add_argument('--src', type=str, default=None)
    parser.add_argument('--dst', type=str, default=None)
    args, _ = parser.parse_known_args()

  else:
    raise NotImplementedError(domain)
