import numpy as np
from dival.data import TestData
from dival.datasets.dataset import Dataset
from dival.evaluation import TaskTable
from dival.measure import L2
from odl.discr import uniform_discr
from dival.reconstructors.regression_reconstructors import LinRegReconstructor

# %% data
observation_space = uniform_discr(-0.5, 6.5, 7)
reco_space = uniform_discr(-0.5, 11.5, 12)

np.random.seed(0)


class LinearDataset(Dataset):
    def __init__(self, observation_space, reco_space, train_len=10000,
                 test_len=1000):
        self.train_len = train_len
        self.test_len = test_len
        self.observation_space = observation_space
        self.reco_space = reco_space
        self.shape = (self.observation_space.shape, self.reco_space.shape)
        self.forward_matrix = np.random.rand(self.shape[0][0],
                                             self.shape[1][0])

    def generator(self, test=False):
        rs = np.random.RandomState(1 if test else 42)
        for _ in range(self.test_len if test else self.train_len):
            x = rs.rand(self.shape[1][0])
            y = (np.dot(self.forward_matrix, x) +
                 0.4 * rs.normal(scale=.1, size=self.shape[0]))
            yield (self.observation_space.element(y),
                   self.reco_space.element(x))


dataset = LinearDataset(observation_space, reco_space)
test_generator = dataset.get_test_generator()
observation, ground_truth = next(test_generator)
test_data = TestData(observation, ground_truth)

# %% task table and reconstructors
eval_tt = TaskTable()

reconstructor = LinRegReconstructor(observation_space=observation_space,
                                    reco_space=reco_space)

rs = np.random.RandomState(0)
eval_tt.append(
    reconstructor=reconstructor, test_data=test_data, dataset=dataset,
    options={'hyper_param_search': {
                'measure': L2,
                'hyperopt_max_evals_retrain': 10,
                'hyperopt_rstate': rs}})

# %% run task table
results = eval_tt.run()
print(results.to_string(formatters={'reconstructor': lambda r: r.name}))

# %% plot reconstructions
fig = results.plot_all_reconstructions(fig_size=(9, 4), vrange='individual')
