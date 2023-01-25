"Parse and clean up log text-files from test.py"
import shutil
import pickle
import argparse
from argparse import Namespace
from pathlib import Path

import yaml

REQUIRED_KEYS = ['epoch', 'mAP IoU=0.50:0.95', 'mAP IoU=0.50']


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


def main(args):
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str)
    parser.add_argument('--dirname', type=str, default='.')
    parser.add_argument('--move', action='store_true', dest='move')
    parser.add_argument('--no-move', action='store_false', dest='move')
    parser.set_defaults(move=True)
    parser.add_argument('--dump-pkl', action='store_true', dest='dump_pickle')
    parser.add_argument('--no-dump-pkl', action='store_false', dest='dump_pickle')
    parser.set_defaults(dump_pickle=True)
    args = parser.parse_args()
    # TODO: IMPROVE. There is a cleaner version of removing the if clause with
    # argparse. But, GithubCopilot suggested the old dirty hack. EOM - Victor.
    if args.filename is None and args.dirname is None:
        raise ValueError(
            f'You must specify either {args.filename=} or {args.dirname=}')
    assert args.move and args.dump_pickle

    main(args)
