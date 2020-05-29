<p align="center">
<img src="https://github.com/it21208/MeLIR/blob/master/MeLIR-logo.png" width="360">
</p>

# BioBERT

Finetuning the pre-trained [BERT](https://arxiv.org/abs/1810.04805) models for Document Classification tasks.

## Quick start

For fine-tuning the pre-trained BioBERT-base model on Pubmed dataset, just run the following from the project working directory.

```
python -m models.bert --dataset Pubmed --model bert-base-uncased --max-seq-length 256 --batch-size 16 --lr 2e-5 --epochs 30
```

The best model weights will be saved in

```
model/bert/saves/Pubmed/best_model.pt
```

To test the model, you can use the following command.

```
python -m models.bert --dataset Reuters --model bert-base-uncased --max-seq-length 256 --batch-size 16 --lr 2e-5 --epochs 30 --trained-model models/bert/saves/Reuters/best_model.pt
```

## Model Types 

We follow the same types of models as in [huggingface's implementation](https://github.com/huggingface/pytorch-pretrained-BERT.git)
- bert-base-uncased
- bert-large-uncased
- bert-base-cased
- bert-large-cased

## Dataset

We experiment the model on the following PubMed dataset variations:

- Pubmed

## Settings

Finetuning procedure can be found in :
- [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)
- [DocBERT: BERT for Document Classification](https://arxiv.org/abs/1904.08398v1)

## Acknowledgement
- My implementation is inspired from [huggingface's implementation](https://github.com/huggingface/pytorch-pretrained-BERT.git) and (https://github.com/castorini/hedwig)

