from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re


class SentimentModel():
    def __init__(self, model_path):
        if torch.cuda.is_available():
            self.device = 'cuda'
        else:
            self.device = 'cpu'        
        

        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model = self.model.to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained('oliverguhr/german-sentiment-bert')

        self.clean_chars = re.compile(r'[^A-Za-züöäÖÜÄß ]', re.MULTILINE)
        self.clean_http_urls = re.compile(r'https*\S+', re.MULTILINE)
        self.clean_at_mentions = re.compile(r'@\S+', re.MULTILINE)

    def predict_sentiment_batches(self, texts, output_ids= False, output_probabilities = False):
        texts = [self.clean_text(text) for text in texts]
        

        def chunks(lst, n):
            chunk_counter = 0
            for i in range(0, len(lst), n):
                chunk_counter+=1
                if chunk_counter %10 == 0:
                    print(f"Progress: {(chunk_counter*n)/len(lst):.2f}; Classified {chunk_counter*n} samples. ")
                yield lst[i:i + n]
        
        label_ids =[]
        probabilities = []

        for batch in chunks(texts, 500):
            encoded = self.tokenizer.batch_encode_plus(batch,padding=True, add_special_tokens=True,truncation=True, return_tensors="pt")
            encoded = encoded.to(self.device)
            with torch.no_grad():
                    logits = self.model(**encoded)
            
            curr_label_ids = torch.argmax(logits[0], axis=1)
            label_ids.extend([label_id.item() for label_id in curr_label_ids])

            if output_probabilities:
                predictions = torch.softmax(logits[0], dim=-1).tolist()  
                curr_probabilities = []
                for prediction in predictions:
                    curr_probabilities += [[[self.model.config.id2label[index], item] for index, item in enumerate(prediction)]]
                probabilities.extend(curr_probabilities)

            # Free up GPU-memory      
            del encoded
            del logits
            torch.cuda.empty_cache()

        if output_ids:
            if output_probabilities:
                  label_ids, probabilities
            return label_ids
        else:
            if output_probabilities:
                return [self.model.config.id2label[label_id] for label_id in label_ids], probabilities
            
            return [self.model.config.id2label[label_id] for label_id in label_ids]
    
    def replace_numbers(self,text: str) -> str:
            return text.replace("0"," null").replace("1"," eins").replace("2"," zwei")\
                .replace("3"," drei").replace("4"," vier").replace("5"," fünf") \
                .replace("6"," sechs").replace("7"," sieben").replace("8"," acht") \
                .replace("9"," neun")         

    def clean_text(self,text: str)-> str:    
            text = text.replace("\n", " ")        
            text = self.clean_http_urls.sub('',text)
            text = self.clean_at_mentions.sub('',text)        
            text = self.replace_numbers(text)                
            text = self.clean_chars.sub('', text) # use only text chars                          
            text = ' '.join(text.split()) # substitute multiple whitespace with single whitespace   
            text = text.strip().lower()
            return text