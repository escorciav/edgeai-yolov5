"""Clean up log text-files from test.py, OR monitoring

Usage:

  1. [cleaning up] python monitor_test.py

  2. [monitoring] python monitor_test.py --task monitor --dirname runs/exp4

Hangover/Alzheimer pills 💊

Victor usually launches the validation along with training, with something
along these lines:

```bash
sleep 3780
for i in {1..19}; do
    echo $(date)
    python test.py --data coco_kpts.yaml --epoch-suffix --img 640 --kpt-label \
    --conf 0.001 --iou 0.65 --weights runs/train/exp/weights/last.pt | tee \
    log_$(date +"%y-%m-%d-%H:%M:%S")".txt";
    echo iter: $i, $(date);
    sleep 6300;
done
```
"""
import shutil
import pickle
import argparse
from argparse import Namespace
from pathlib import Path

import yaml
import matplotlib.pyplot as plt

TASKS = ['monitor', 'cleanup']
REQUIRED_KEYS = ['epoch', 'mAP IoU=0.50:0.95', 'mAP IoU=0.50']
EXTRA_INFO = 'boxes = All'
COLORS = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4']
LINE_WIDTH, MARKER_SIZE = 3, 5


def parse_log(filename):
    "Grab relevant values of the logfile"
    data = {}
    field_tokens = [
        ('mAP IoU=0.50:0.95', 'Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all'),
        ('mAP IoU=0.50', 'Average Precision  (AP) @[ IoU=0.50      | area=   all'),
        ('dirname','Results saved to ')
    ]
    with open(filename, 'r') as fid:
        for line in fid:
            line = line.strip()
            if line.startswith('Namespace'):
                # eval while use Namespace ;)
                args = eval(line)
                data['args'] = args
                assert len(args.weights) == 1, "Unsupported parsing of ensembles"
                ckpt_file = Path(args.weights[0])
                train_dir = ckpt_file.parent.parent
                data['train_dir'] = train_dir
            else:
                for key, token in field_tokens:
                    if key != 'dirname':
                        token = token + ' | maxDets= 20 ] =  '

                    if line.startswith(token):
                        value = line.split(token)[-1]
                        if key != 'dirname':
                            value = float(value)
                        else:
                            value = Path(value)
                        data[key] = value

    corrupted = True
    log_msg = 'Parsing fail. Review it manually ☺️'
    if len(data) > 0:
        log_msg = ''
        corrupted = False
        epoch = int(data['dirname'].stem.split('epoch-')[-1])

        if epoch < 0:
            opt_yaml = data['train_dir'] / 'opt.yaml'
            if opt_yaml.exists():
                with open(opt_yaml, 'r') as fid:
                    opt = yaml.safe_load(fid)
                epoch = opt['epochs']
                log_msg = 'Success!'
            else:
                corrupted = True
                log_msg = f'NO {opt_yaml=}'
        else:
            log_msg = 'Success!'

        data['epoch'] = epoch

    data['potentially_corrupted'] = corrupted
    data['log'] = log_msg
    return data


def clean_up(args):
    if args.dirname is not None:
        log_files = list(Path(args.dirname).glob('log*.txt'))
    else:
        log_files = [args.filename]

    for log_file in log_files:
        data = parse_log(log_file)

        skip_file = (
            data['potentially_corrupted'] or
            not all([i in data for i in REQUIRED_KEYS])
        )
        if skip_file:
            print(f'Skipping {log_file=}. Maybe corrupted ☺️')
            continue

        # Cleaning up dirname ☺️
        if args.move:
            dest_file = data['train_dir'] / f'log_test_epoch-{data["epoch"]}.txt'
            shutil.move(log_file, dest_file)

        if args.dump_pickle:
            pkl_file = data['train_dir'] / f'test_epoch-{data["epoch"]}.pkl'
            with open(pkl_file, 'wb') as fid:
                pickle.dump(data, fid)


def monitor(args):
    "Grab all the pkl and plot the performance along the course of the training"
    pkl_files = list(args.dirname.glob(f'{args.wildcard}.pkl'))
    if len(pkl_files) == 0:
        print('No pickle files associated with results found\nEARLY EXIT!')

    results = []
    for filename in pkl_files:
        with open(filename, 'rb') as fid:
            data = pickle.load(fid)
        results.append(data)
    results = sorted(results, key=lambda x: x['epoch'])
    data = [
        (i['epoch'], i['mAP IoU=0.50:0.95'], i['mAP IoU=0.50'])
        for i in results
    ]
    epoch, *kpis = zip(*data)
    for i, kpi_i in enumerate(kpis):
        plt.plot(
            epoch, kpis[i], color=COLORS[i], label=REQUIRED_KEYS[i + 1],
            linewidth=LINE_WIDTH, marker='o', markersize=MARKER_SIZE)
    plt.ylabel('mAP / AP')
    # plt.xticks(epoch)
    plt.xlim([0, max(epoch) + 1])
    plt.xlabel('Epoch')
    plt.grid(True)
    plt.title(f'{args.dirname.stem}, {EXTRA_INFO}')
    plt.legend(loc='best')
    plt.savefig(args.dirname / 'test_results.jpg', bbox_inches='tight')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', choices=TASKS, default='cleanup')
    parser.add_argument('--filename', type=Path)
    parser.add_argument('--dirname', type=Path, default='.')
    parser.add_argument('--move', action='store_true', dest='move')
    parser.add_argument('--no-move', action='store_false', dest='move')
    parser.set_defaults(move=True)
    parser.add_argument('--dump-pkl', action='store_true', dest='dump_pickle')
    parser.add_argument('--no-dump-pkl', action='store_false', dest='dump_pickle')
    parser.set_defaults(dump_pickle=True)
    parser.add_argument('--wildcard', default='test_epoch*',
        help='wildcard to find pkl files with results')
    args = parser.parse_args()
    # TODO: IMPROVE. There is a cleaner version of removing the if clause with
    # argparse. But, GithubCopilot suggested the old dirty hack. EOM - Victor.
    if args.filename is None and args.dirname is None:
        raise ValueError(
            f'You must specify either {args.filename=} or {args.dirname=}')
    assert args.move and args.dump_pickle

    if args.task == 'cleanup':
        clean_up(args)
    elif args.task == 'monitor':
        monitor(args)
