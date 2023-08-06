from typing import Callable, List, Optional, Tuple
import pandas as pd
from sklearn.base import TransformerMixin, BaseEstimator
import torch
from typing import Callable, List, Optional, Tuple
import torch
from transformers import TrainingArguments, Trainer
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import EarlyStoppingCallback
from transformers import BertModel, BertTokenizer

import numpy as np
from sklearn.metrics import accuracy_score


def compute_metrics(p):
    pred, labels = p
    pred = np.argmax(pred, axis=1)

    accuracy = accuracy_score(y_true=labels, y_pred=pred)

    return {"accuracy": accuracy}

class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels=None):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        if self.labels:
            item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.encodings["input_ids"])




class Tuning():
    def __init__(
        self,
       
        sentences_train=None,
        labels_train=None,
        sentences_val=None,
        labels_val=None,
        tokenizer_name=None,
        model_name=None,
        labels=None,
        epoch=10,
        save_path='',
        max_length: int = 512,
        
    ):
    
        sentences_train = ["[CLS] " + sentence + " [SEP]" for sentence in sentences_train]
        sentences_val = ["[CLS] " + sentence + " [SEP]" for sentence in sentences_val]
        sentences_train= list(sentences_train)
        labels_train = list(labels_train)
        sentences_val= list(sentences_val)
        labels_val = list(labels_val)

        # Define pretrained tokenizer and model
        #model_name = "/content/drive/MyDrive/bert/bert_acj/checkpoint-10500"
        tokenizer = BertTokenizer.from_pretrained(tokenizer_name)
        model = BertForSequenceClassification.from_pretrained(model_name, num_labels=labels)

        X_train_tokenized = tokenizer(sentences_train, padding=True, truncation=True, max_length=max_length)
        X_val_tokenized = tokenizer(sentences_val, padding=True, truncation=True, max_length=max_length)


        train_dataset = Dataset(X_train_tokenized, labels_train)
        val_dataset = Dataset(X_val_tokenized, labels_val)

        #print(val_dataset)


        # Define Trainer
        args = TrainingArguments(
            output_dir=save_path+"bert",
            evaluation_strategy="steps",
            eval_steps=100,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            num_train_epochs=epoch,
            save_steps=100,
            warmup_steps=1000,
	    weight_decay=0.01,
            save_total_limit=2,
       	    logging_dir=save_path+"bert",
            load_best_model_at_end=True,
        )
        trainer = Trainer(
            model=model,
            args=args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=compute_metrics,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=10)],
        )
        # Train pre-trained model

        print('Fine tuning supervised transformer based LM')
     
        trainer.train()
      
      
        trainer.save_model()
        
        tokenizer.save_pretrained(save_path+"bert")


        print('Tranied !!')
        self.save_path = save_path+"bert"


                
    def output(self):
        tokenizer = BertTokenizer.from_pretrained(self.save_path)

        bert_model = BertModel.from_pretrained(self.save_path)

        return tokenizer, bert_model


class SklTransformer(BaseEstimator, TransformerMixin):
    def __init__(
            self,
            tokenizer_name,
            model_name,
            fine_tuning=False,
            X_train=None,
            y_train=None,
            X_val=None,
            y_val=None,
            labels=None,
            nub_epoch=10,
            save_path='',
            max_length: int = 512,
            embedding_func: Optional[Callable[[torch.tensor], torch.tensor]] = None,
            embedding_func1: Optional[Callable[[torch.tensor], torch.tensor]] = None,
    ):

        if fine_tuning==True:
        
            bert = Tuning(sentences_train=X_train, labels_train=y_train, 
                            sentences_val=X_val, labels_val=y_val, 
                            tokenizer_name =tokenizer_name, model_name= model_name, 
                            labels=labels, epoch=nub_epoch, max_length=max_length, save_path=save_path)
            self.tokenizer, self.model = bert.output()
        else:
            self.tokenizer = BertTokenizer.from_pretrained(tokenizer_name)
            self.model = BertModel.from_pretrained(model_name)




        self.model.eval()
        self.max_length = max_length
        self.embedding_func = embedding_func
        self.embedding_func1 = embedding_func1

        if self.embedding_func is None:
            self.embedding_func = lambda x: x[1][0].squeeze()

        if self.embedding_func1 is None:
            self.embedding_func1 = lambda x: x[0][:, 0, :].squeeze()

    def _tokenize(self, text: str) -> Tuple[torch.tensor, torch.tensor]:
        # Tokenize the text with the provided tokenizer
        tokenized_text = self.tokenizer.encode_plus(text,
                                                    add_special_tokens=True,
                                                    max_length=self.max_length
                                                    )["input_ids"]

        # Create an attention mask telling BERT to use all words
        attention_mask = [1] * len(tokenized_text)

        # bert takes in a batch so we need to unsqueeze the rows
        return (
            torch.tensor(tokenized_text).unsqueeze(0),
            torch.tensor(attention_mask).unsqueeze(0),
        )

    def _tokenize_and_predict(self, text: str) -> torch.tensor:
        tokenized, attention_mask = self._tokenize(text)

        embeddings = self.model(tokenized, attention_mask)
        #return torch.cat((self.embedding_func(embeddings).unsqueeze(0),self.embedding_func1(embeddings).unsqueeze(0)), 1).squeeze()
        return self.embedding_func(embeddings)+self.embedding_func1(embeddings)

    def transform(self, text: List[str]):
        if isinstance(text, pd.Series):
            text = text.tolist()

        with torch.no_grad():
            return torch.stack([self._tokenize_and_predict(string) for string in text])

    def fit(self, X, y=None):
        """No fitting necessary so we just return ourselves"""
        return self