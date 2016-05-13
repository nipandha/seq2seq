#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
import logging
import argparse

logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

help_msg = """Train a translation model using Moses.
Use `train-lm.py` to train a language model beforehand."""

commands = """\
rm -rf "{output_dir}"
$MOSES_DIR/scripts/training/train-model.perl -root-dir "{output_dir}" \
-corpus {corpus} -f {src_ext} -e {trg_ext} -alignment grow-diag-final-and \
-reordering msd-bidirectional-fe -lm 0:3:{lm_corpus}.blm.{trg_ext}:8 \
-external-bin-dir $GIZA_DIR -mgiza \
-mgiza-cpus {threads} -cores {threads} --parallel\
"""

if __name__ == '__main__':
    if any(var not in os.environ for var in ('GIZA_DIR', 'MOSES_DIR')):
        sys.exit('Environment variable not defined')

    parser = argparse.ArgumentParser(description=help_msg,
            formatter_class=argparse.RawDescriptionHelpFormatter))
    parser.add_argument('output_dir')
    parser.add_argument('corpus')
    parser.add_argument('lm_corpus')
    parser.add_argument('src_ext')
    parser.add_argument('trg_ext')
    parser.add_argument('--threads', type=int, default=16)

    args = parser.parse_args()

    commands = commands.strip().format(**vars(args))

    for cmd in commands.split('\n'):
        logging.info(cmd)
        os.system(cmd)
