# simplexfmrartifact

BentoML artifact framework for simpletransformers.

Installation:

    pip install simplexfmrartifact

Usage example (decorate service):

    from simplexfmrartifact.simpletransformers import SimpleTransformersModelArtifact

    @artifacts([SimpleTransformersModelArtifact('tm_train3_roberta_l_weigh')])
    class MyBentoService(BentoService):


Usage example (package model):

    svc = MyBentoService()

    metadata = {
        "classpackage": "simpletransformers.classification", 
        "classname": "ClassificationModel", 
        "opts": {
            "use_cuda": true, 
            "num_labels": 2, 
            "args": {
                "use_multiprocessing": false, 
                "silent": true, 
                "eval_batch_size": 10, 
                "fp16": false
            }
        }
    }
    svc.pack('tm_train3_roberta_l_weigh', model_path, metadata)

Alternatively, during training:

    svc.pack('tm_train3_roberta_l_weigh', {'model': my_trained_model})
