import json
import os
from ..client import Boto3Client


class S3Client(Boto3Client):
    """
    """
    
    def __init__(self):
        """
        """
        super().__init__('s3')
        
    def upload_model(self,
                     bucket: str,
                     project_name: str,
                     version_id: int,
                     model_name: str,
                     filepath: str):
        """
        """
        file_path = f"{project_name}/versions/{version_id}/models/{model_name}/model.pb"
        self.upload_file(filepath, Bucket=bucket, Key=file_path)
        
    def download_model(self,
                       bucket: str,
                       project_name: str,
                       version_id: int,
                       model_name: str,
                       filepath: str = 'model.pb') -> str:
        """
        """
        file_path = f"{project_name}/versions/{version_id}/models/{model_name}/model.pb"
        self.download_file(bucket, file_path, filepath)
        return filepath
    
    def upload_model_parameters(self,
                                bucket: str,
                                project_name: str,
                                version_id: int,
                                model_name: str,
                                parameters: dict = {}):
        """
        """
        file_path = f"{project_name}/versions/{version_id}/models/{model_name}/parameters.json"
        self.put_object(Body=json.dumps(parameters).encode(), Bucket=bucket, Key=file_path)
        
    def get_model_parameters(self,
                             bucket: str,
                             project_name: str,
                             version_id: int,
                             model_name: str) -> dict:
        """
        """
        file_path = f"{project_name}/versions/{version_id}/models/{model_name}/parameters.json"
        self.download_file(bucket, file_path, 'tmp.json')
        parameters = json.load(open('tmp.json', 'r'))
        os.remove('tmp.json')
        return parameters
        
    def get_vocab(self,
                  bucket: str,
                  project_name: str) -> dict:
        """
        """
        vocab = self.get_object(Bucket=bucket, Key=f"{project_name}/config/vocab.json")
        return json.loads(vocab['Body'].read())
    
    def upload_vocab(self,
                     bucket: str,
                     project_name: str,
                     vocab: dict):
        """
        """
        self.put_object(Body=json.dumps(vocab).encode(), Bucket=bucket, Key=f"{project_name}/config/vocab.json")
            
    def get_word2idx(self,
                     bucket: str,
                     project_name: str) -> dict:
        """
        """
        vocab = self.get_object(Bucket=bucket, Key=f"{project_name}/config/word2idx.json")
        return json.loads(vocab['Body'].read())
    
    def upload_word2idx(self,
                        bucket: str,
                        project_name: str,
                        word2idx: dict):
        """
        """
        self.put_object(Body=json.dumps(word2idx).encode(), Bucket=bucket, Key=f"{project_name}/config/word2idx.json")
    
    def upload_model(self,
                     bucket: str,
                     project_name: str,
                     version_id: int,
                     model_name: int,
                     model_path: str):
        """
        """
        extension = model_path.split('.')[-1]
        self.upload_file(model_path, bucket, f"{project_name}/versions/{version_id}/models/{model_name}/model.{extension}")

    def get_project_classes(self,
                            bucket: str,
                            project_name: str) -> dict:
        """
        """
        classes = self.get_object(Bucket=bucket, Key=f"{project_name}/config/classes.json")
        return json.loads(classes['Body'].read())
