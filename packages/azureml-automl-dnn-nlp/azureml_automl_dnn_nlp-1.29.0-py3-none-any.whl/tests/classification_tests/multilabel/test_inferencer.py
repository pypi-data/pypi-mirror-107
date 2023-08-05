import pytest
import unittest

from azureml.automl.dnn.nlp.classification.inference.multilabel_inferencer import MultilabelInferencer
from azureml.automl.dnn.nlp.classification.io.read.dataloader import get_vectorizer

try:
    import torch
    has_torch = True
except ImportError:
    has_torch = False


class MockExperiment:
    def __init__(self):
        self.workspace = "some_workspace"


class MockRun:
    def __init__(self):
        self.experiment = MockExperiment()


class MockBertClass(torch.nn.Module):
    def __init__(self, num_labels):
        super(MockBertClass, self).__init__()
        self.num_labels = num_labels
        self.l1 = torch.nn.Linear(num_labels, num_labels)
        # number of times forward was called
        self.forward_called = 0
        self.train_called = False
        self.eval_called = False
        return

    def forward(self, ids, attention_mask, token_type_ids):
        self.forward_called = self.forward_called + 1
        return self.l1(torch.randn(ids.shape[0], self.num_labels))

    def train(self, mode=True):
        self.train_called = True
        super().train(mode)

    def eval(self):
        self.eval_called = True
        super().eval()


@pytest.mark.usefixtures('MultilabelDatasetTester')
@pytest.mark.parametrize('multiple_text_column', [False, True])
class TestMultilabelInferencert:
    @unittest.skipIf(not has_torch, "torch not installed")
    def test_obtain_dataloader(self, MultilabelDatasetTester):
        input_df = MultilabelDatasetTester.get_data().copy()
        vectorizer = get_vectorizer(input_df, input_df)
        num_label_cols = len(vectorizer.get_feature_names())
        assert num_label_cols == 6
        run = MockRun()
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        inferencer = MultilabelInferencer(run, device)
        inference_data_loader = inferencer.obtain_dataloader(input_df, vectorizer)
        assert len(inference_data_loader.dataset) == len(input_df)

    @unittest.skipIf(not has_torch, "torch not installed")
    def test_predict(self, MultilabelDatasetTester):
        input_df = MultilabelDatasetTester.get_data().copy()
        vectorizer = get_vectorizer(input_df, input_df)
        num_label_cols = len(vectorizer.get_feature_names())
        assert num_label_cols == 6
        run = MockRun()
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        inferencer = MultilabelInferencer(run, device)
        inference_data_loader = inferencer.obtain_dataloader(input_df, vectorizer)
        assert len(inference_data_loader.dataset) == len(input_df)
        model = MockBertClass(num_label_cols)
        predicted_df = inferencer.predict(model, vectorizer, input_df, inference_data_loader)
        assert len(predicted_df) == len(input_df)
