# -*- coding: UTF-8 -*-
################################################################################
#
#   Copyright (c) 2020  Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
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
#################################################################################
import sys
import os
import datetime
import logging
import math
import pickle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import LAC
import numpy as np
from paddle import fluid
from paddle.fluid import dygraph
from paddle.fluid import layers

from DuDepParser.parser import model as md
from DuDepParser.parser.config import ArgConfig
from DuDepParser.parser.config import Environment
from DuDepParser.parser.utils import corpus
from DuDepParser.parser.utils import data
from DuDepParser.parser.utils import field
from DuDepParser.parser.utils import utils
from DuDepParser.parser.utils.metric import Metric
"""
程序入口，定义了训练，评估，预测等函数
"""


def train(env):
    """训练函数"""
    args = env.args

    logging.info("loading data.")
    train = corpus.Corpus.load(args.train_data_path, env.fields)
    dev = corpus.Corpus.load(args.valid_data_path, env.fields)
    test = corpus.Corpus.load(args.test_data_path, env.fields)
    logging.info("init dataset.")
    train = data.TextDataset(train, env.fields, args.buckets)
    dev = data.TextDataset(dev, env.fields, args.buckets)
    test = data.TextDataset(test, env.fields, args.buckets)
    logging.info("set the data loaders.")
    train.loader = data.batchify(train, args.batch_size,
                                 args.use_data_parallel, True)
    dev.loader = data.batchify(dev, args.batch_size)
    test.loader = data.batchify(test, args.batch_size)

    logging.info(f"{'train:':6} {len(train):5} sentences, "
                 f"{len(train.loader):3} batches, "
                 f"{len(train.buckets)} buckets")
    logging.info(f"{'dev:':6} {len(dev):5} sentences, "
                 f"{len(dev.loader):3} batches, "
                 f"{len(train.buckets)} buckets")
    logging.info(f"{'test:':6} {len(test):5} sentences, "
                 f"{len(test.loader):3} batches, "
                 f"{len(train.buckets)} buckets")

    logging.info("Create the model")
    model = md.Model(args, env.WORD.embed)

    # init parallel strategy
    if args.use_data_parallel:
        strategy = dygraph.parallel.prepare_context()
        model = dygraph.parallel.DataParallel(model, strategy)

    if args.use_cuda:
        grad_clip = fluid.clip.GradientClipByNorm(clip_norm=args.clip)
    else:
        grad_clip = fluid.clip.GradientClipByGlobalNorm(clip_norm=args.clip)
    decay = dygraph.ExponentialDecay(learning_rate=args.lr,
                                     decay_steps=args.decay_steps,
                                     decay_rate=args.decay)
    optimizer = fluid.optimizer.AdamOptimizer(
        learning_rate=decay,
        beta1=args.mu,
        beta2=args.nu,
        epsilon=args.epsilon,
        parameter_list=model.parameters(),
        grad_clip=grad_clip)

    total_time = datetime.timedelta()
    best_e, best_metric = 1, Metric()

    puncts = dygraph.to_variable(env.puncts)
    logging.info("start training.")
    for epoch in range(1, args.epochs + 1):
        start = datetime.datetime.now()
        # train one epoch and update the parameter
        logging.info(f"Epoch {epoch} / {args.epochs}:")
        md.epoch_train(args, model, optimizer, train.loader, epoch)
        if args.local_rank == 0:
            loss, dev_metric = md.epoch_evaluate(args, model, dev.loader,
                                                 puncts)
            logging.info(f"{'dev:':6} Loss: {loss:.4f} {dev_metric}")
            loss, test_metric = md.epoch_evaluate(args, model, test.loader,
                                                  puncts)
            logging.info(f"{'test:':6} Loss: {loss:.4f} {test_metric}")

            t = datetime.datetime.now() - start
            # save the model if it is the best so far
            if dev_metric > best_metric and epoch > args.patience // 10:
                best_e, best_metric = epoch, dev_metric
                md.save(args.model_path, args, model, optimizer)
                logging.info(f"{t}s elapsed (saved)\n")
            else:
                logging.info(f"{t}s elapsed\n")
            total_time += t
            if epoch - best_e >= args.patience:
                break
    if args.local_rank == 0:
        model = md.load(args.model_path)
        loss, metric = md.epoch_evaluate(args, model, test.loader, puncts)
        logging.info(
            f"max score of dev is {best_metric.score:.2%} at epoch {best_e}")
        logging.info(
            f"the score of test at epoch {best_e} is {metric.score:.2%}")
        logging.info(f"average time of each epoch is {total_time / epoch}s")
        logging.info(f"{total_time}s elapsed")


def evaluate(env):
    """评估函数"""
    args = env.args
    puncts = dygraph.to_variable(env.puncts)

    logging.info("Load the dataset")
    evaluates = corpus.Corpus.load(args.test_data_path, env.fields)
    dataset = data.TextDataset(evaluates, env.fields, args.buckets)
    # set the data loader
    dataset.loader = data.batchify(dataset, args.batch_size)

    logging.info(f"{len(dataset)} sentences, "
                 f"{len(dataset.loader)} batches, "
                 f"{len(dataset.buckets)} buckets")
    logging.info("Load the model")
    model = md.load(args.model_path)

    logging.info("Evaluate the dataset")
    start = datetime.datetime.now()
    loss, metric = md.epoch_evaluate(args, model, dataset.loader, puncts)
    total_time = datetime.datetime.now() - start
    logging.info(f"Loss: {loss:.4f} {metric}")
    logging.info(f"{total_time}s elapsed, "
                 f"{len(dataset) / total_time.total_seconds():.2f} Sents/s")


def predict(env):
    """预测函数"""
    args = env.args

    logging.info("Load the dataset")
    if args.prob:
        env.fields = env.fields._replace(PHEAD=field.Field('probs'))
    predicts = corpus.Corpus.load(args.infer_data_path, env.fields)
    dataset = data.TextDataset(predicts, [env.WORD, env.FEAT], args.buckets)
    # set the data loader
    dataset.loader = data.batchify(dataset, args.batch_size)
    logging.info(f"{len(dataset)} sentences, "
                 f"{len(dataset.loader)} batches")

    logging.info("Load the model")
    model = md.load(args.model_path)
    model.args = args

    logging.info("Make predictions on the dataset")
    start = datetime.datetime.now()
    pred_arcs, pred_rels, pred_probs = md.epoch_predict(
        env, args, model, dataset.loader)
    total_time = datetime.datetime.now() - start
    # restore the order of sentences in the buckets
    indices = np.argsort(
        np.array([i for bucket in dataset.buckets.values() for i in bucket]))
    predicts.head = [pred_arcs[i] for i in indices]
    predicts.deprel = [pred_rels[i] for i in indices]
    if args.prob:
        predicts.probs = [pred_probs[i] for i in indices]
    logging.info(f"Save the predicted result to {args.infer_result_path}")
    predicts.save(args.infer_result_path)
    logging.info(f"{total_time}s elapsed, "
                 f"{len(dataset) / total_time.total_seconds():.2f} Sents/s")


def predict_query(env):
    """预测单条数据"""
    args = env.args
    logging.info("Load the model")
    model = md.load(args.model_path)
    lac_mode = "seg" if args.feat != "pos" else "lac"
    lac = LAC.LAC(mode=lac_mode)
    if args.prob:
        env.fields = env.fields._replace(PHEAD=field.Field('probs'))

    while True:
        query = input()
        if not query:
            logging.info("quit!")
            return
        if len(query) > 500:
            logging.info("The length of the query should be less than 500！")
            continue
        start = datetime.datetime.now()
        lac_results = lac.run([query])
        predicts = corpus.Corpus.load_lac_results(lac_results, env.fields)
        dataset = data.TextDataset(predicts, [env.WORD, env.FEAT])
        # set the data loader
        dataset.loader = data.batchify(dataset,
                                       args.batch_size,
                                       use_multiprocess=False,
                                       sequential_sampler=True)
        pred_arcs, pred_rels, pred_probs = md.epoch_predict(
            env, args, model, dataset.loader)
        predicts.head = pred_arcs
        predicts.deprel = pred_rels
        if args.prob:
            predicts.probs = pred_probs
        predicts.print()
        total_time = datetime.datetime.now() - start
        logging.info(
            f"{total_time}s elapsed, "
            f"{len(dataset) / total_time.total_seconds():.2f} Sents/s, {total_time.total_seconds() / len(dataset) * 1000:.2f} ms/Sents"
        )


class DuDepParser(object):
    def __init__(self,
                 use_cuda=False,
                 tree=True,
                 prob=False,
                 use_pos=False,
                 model_files_path=None):
        if model_files_path is None:
            model_files_path = self._get_abs_path('./model_files/baidu')
            if not os.path.exists(model_files_path):
                try:
                    utils.download_model_from_url(model_files_path)
                except Exception as e:
                    logging.warning(
                        "Failed to download model, please try again")
                    return

        args = [
            f"--model_files={model_files_path}",
            f"--config_path={self._get_abs_path('config.ini')}"
        ]

        if use_cuda:
            args.append("--use_cuda")
        if tree:
            args.append("--tree")
        if prob:
            args.append("--prob")

        args = ArgConfig(args)
        # 不实例化log handler
        args.log_path = None
        self.env = Environment(args)
        self.args = self.env.args
        fluid.enable_imperative(self.env.place)
        self.model = md.load(self.args.model_path)
        self.lac = None
        self.use_pos = use_pos
        if args.prob:
            self.env.fields = self.env.fields._replace(
                PHEAD=field.Field('probs'))

    def parse(self, inputs):
        if not self.lac: 
            self.lac = LAC.LAC(mode='lac' if self.use_pos else "seg")
        if isinstance(inputs, str):
            inputs = [inputs]
        if all([isinstance(i, str) for i in inputs]):
            lac_results = self.lac.run(inputs)
            predicts = corpus.Corpus.load_lac_results(lac_results,
                                                      self.env.fields)
        else:
            logging.warning("please check the foramt of your inputs.")
            return
        dataset = data.TextDataset(predicts, [self.env.WORD, self.env.FEAT])
        # set the data loader
        dataset.loader = data.batchify(dataset,
                                       self.args.batch_size,
                                       use_multiprocess=False,
                                       sequential_sampler=True)
        pred_arcs, pred_rels, pred_probs = md.epoch_predict(
            self.env, self.args, self.model, dataset.loader)
        predicts.head = pred_arcs
        predicts.deprel = pred_rels
        if self.args.prob:
            predicts.probs = pred_probs
        return predicts.json()

    def parse_seg(self, inputs):
        if all([isinstance(i, list) for i in inputs]):
            predicts = corpus.Corpus.load_word_segments(
                inputs, self.env.fields)
        else:
            logging.warning("please check the foramt of your inputs.")
            return
        dataset = data.TextDataset(predicts, [self.env.WORD, self.env.FEAT])
        # set the data loader
        dataset.loader = data.batchify(dataset,
                                       self.args.batch_size,
                                       use_multiprocess=False,
                                       sequential_sampler=True)
        pred_arcs, pred_rels, pred_probs = md.epoch_predict(
            self.env, self.args, self.model, dataset.loader)
        predicts.head = pred_arcs
        predicts.deprel = pred_rels
        if self.args.prob:
            predicts.probs = pred_probs
        return predicts.json()

    def _get_abs_path(self, path):
        return os.path.normpath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), path))


if __name__ == '__main__':
    logging.info("init argsments.")
    args = ArgConfig()
    logging.info("init environment.")
    env = Environment(args)
    logging.info(f"Override the default configs\n{env.args}")
    logging.info(f"{env.WORD}\n{env.FEAT}\n{env.ARC}\n{env.REL}")
    logging.info(f"Set the max num of threads to {env.args.threads}")
    logging.info(
        f"Set the seed for generating random numbers to {env.args.seed}")
    logging.info(f"Run the subcommand in mode {env.args.mode}")

    fluid.enable_imperative(env.place)
    mode = env.args.mode
    if mode == "train":
        train(env)
    elif mode == "evaluate":
        evaluate(env)
    elif mode == "predict":
        predict(env)
    elif mode == "predict_q":
        predict_query(env)
    else:
        logging.error(f"Unknown task mode: {mode}.")
