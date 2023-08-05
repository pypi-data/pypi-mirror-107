import os
from glob import glob
from dataclasses import dataclass, field


@dataclass
class QATrainArguments:

    pretrained_model_name: str = field(
        default="beomi/kcbert-base",
        metadata={"help": "pretrained model name"}
    )
    downstream_corpus_name: str = field(
        default=None,
        metadata={"help": "The name of the downstream data."}
    )
    downstream_corpus_root_dir: str = field(
        default="/root/Korpora",
        metadata={"help": "The root directory of the downstream data."}
    )
    downstream_model_dir: str = field(
        default=None,
        metadata={"help": "The output model dir."}
    )
    max_seq_length: int = field(
        default=384,
        metadata={
            "help": "The maximum total input sequence length after tokenization. Sequences longer "
                    "than this will be truncated, sequences shorter will be padded."
        }
    )
    doc_stride: int = field(
        default=128,
        metadata={
            "help": "When splitting up a long document into chunks, how much stride to take between chunks."
        }
    )
    max_query_length: int = field(
        default=64,
        metadata={
            "help": "The maximum number of tokens for the question. Questions longer than this will "
                    "be truncated to this length."
        }
    )
    threads: int = field(
        default=4,
        metadata={
            "help": "the number of threads, using for preprocessing"
        }
    )
    cpu_workers: int = field(
        default=os.cpu_count(),
        metadata={"help": "number of CPU workers"}
    )
    save_top_k: int = field(
        default=1,
        metadata={"help": "save top k model checkpoints."}
    )
    monitor: str = field(
        default="min val_loss",
        metadata={"help": "monitor condition (save top k)"}
    )
    seed: int = field(
        default=7,
        metadata={"help": "random seed."}
    )
    overwrite_cache: bool = field(
        default=False,
        metadata={"help": "Overwrite the cached training and evaluation sets"}
    )
    force_download: bool = field(
        default=False,
        metadata={"help": "force to download downstream data and pretrained models."}
    )
    test_mode: bool = field(
        default=False,
        metadata={"help": "Test Mode enables `fast_dev_run`"}
    )
    learning_rate: float = field(
        default=5e-5,
        metadata={"help": "learning rate"}
    )
    optimizer: str = field(
        default="AdamW",
        metadata={"help": "optimizer"}
    )
    lr_scheduler: str = field(
        default="exp",
        metadata={"help": "ExponentialLR or CosineAnnealingWarmRestarts"}
    )
    epochs: int = field(
        default=20,
        metadata={"help": "max epochs"}
    )
    batch_size: int = field(
        default=0,
        metadata={"help": "batch size. if 0, Let PyTorch Lightening find the best batch size"}
    )
    fp16: bool = field(
        default=False,
        metadata={"help": "Enable train on FP16"}
    )
    tpu_cores: int = field(
        default=0,
        metadata={"help": "Enable TPU with 1 core or 8 cores"}
    )
    tqdm_enabled: bool = field(
        default=True,
        metadata={"help": "do tqdn enabled or not"}
    )


@dataclass
class QADeployArguments:

    def __init__(
            self,
            pretrained_model_name=None,
            downstream_model_dir=None,
            downstream_model_checkpoint_fpath=None,
            max_seq_length=128,
            max_query_length=32,
    ):
        self.pretrained_model_name = pretrained_model_name
        self.max_seq_length = max_seq_length
        self.max_query_length = max_query_length
        if downstream_model_checkpoint_fpath is not None:
            self.downstream_model_checkpoint_fpath = downstream_model_checkpoint_fpath
        elif downstream_model_dir is not None:
            ckpt_file_names = glob(os.path.join(downstream_model_dir, "*.ckpt"))
            ckpt_file_names = [el for el in ckpt_file_names if "temp" not in el and "tmp" not in el]
            if len(ckpt_file_names) == 0:
                raise Exception(f"downstream_model_dir \"{downstream_model_dir}\" is not valid")
            selected_fname = ckpt_file_names[-1]
            min_val_loss = os.path.split(selected_fname)[-1].replace(".ckpt", "").split("=")[-1]
            try:
                for ckpt_file_name in ckpt_file_names:
                    val_loss = os.path.split(ckpt_file_name)[-1].replace(".ckpt", "").split("=")[-1]
                    if float(val_loss) < float(min_val_loss):
                        selected_fname = ckpt_file_name
                        min_val_loss = val_loss
            except:
                raise Exception(f"the ckpt file name of downstream_model_directory \"{downstream_model_dir}\" is not valid")
            self.downstream_model_checkpoint_fpath = selected_fname
        else:
            raise Exception("Either downstream_model_dir or downstream_model_checkpoint_fpath must be entered.")
        print(f"downstream_model_checkpoint_fpath: {self.downstream_model_checkpoint_fpath}")
