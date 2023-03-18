"""
Generated with the following prompt to GPT-4

I have a directory tree

```
├── Alien-0-just-nightingale-20211202
│   └── peers
│       └── learnfair0258:3408982:frisky-nuthatch
│           ├── experiment.log
│           ├── logs.tsv
│           └── meta.json
├── Alien-1-just-nightingale-20211202
│   └── peers
│       └── learnfair0319:266410:ruddy-tapir
│           ├── experiment.log
│           ├── logs.tsv
│           └── meta.json
├── Alien-2-just-nightingale-20211202
│   └── peers
│       └── learnfair0319:266799:rustling-cockle
│           ├── experiment.log
│           ├── logs.tsv
│           └── meta.json
├── Amidar-0-just-nightingale-20211202
│   └── peers
│       └── learnfair0319:267292:real-skunk
│           ├── experiment.log
│           ├── logs.tsv
│           └── meta.json
```

The `experiment.log`s have the following content

```
....
[INFO:learnfair0258:3408982:frisky-nuthatch experiment:208 2021-12-02 15:31:33,301] calculate_sps 33920 steps in 10.0119
[INFO:learnfair0258:3408982:frisky-nuthatch experiment:208 2021-12-02 15:31:33,301] calculate_sps 32000 steps in 10.0119
[INFO:learnfair0258:3408982:frisky-nuthatch experiment:177 2021-12-02 15:31:33,301] {'local/mean_episode_return': 8542.777777777777, 'local/mean_episode_step': 2845.722222222222, 'local/SPS': 3387.965350120707, 'local/env_act_steps': 49992320, 'local/env_train_steps': 49989760, 'local/optimizer_steps': 78108, 'local/running_reward': 4496.1273193359375, 'local/running_step': 1499.1755065917969, 'local/steps_done': 49992320, 'local/episodes_done': 37443, 'local/unclipped_grad_norm': 4.061947072927769, 'local/model_version': 78108, 'local/virtual_batch_size': 32.0, 'local/num_gradients': 1.0}
[INFO:learnfair0258:3408982:frisky-nuthatch experiment:177 2021-12-02 15:31:33,302] {'global/mean_episode_return': 8531.363636363636, 'global/mean_episode_step': 2769.409090909091, 'global/SPS': 3196.193726528969, 'global/env_act_steps': 49990784, 'global/env_train_steps': 49986560, 'global/optimizer_steps': 78104, 'global/running_reward': 4493.264571629214, 'global/running_step': 1499.5152153558051, 'global/steps_done': 49990784, 'global/episodes_done': 37443, 'global/unclipped_grad_norm': 3.9800223626342475, 'global/model_version': 78104, 'global/virtual_batch_size': 32.0, 'global/num_gradients': 1.0}
[INFO:learnfair0258:3408982:frisky-nuthatch experiment:369 2021-12-02 15:31:38,789] Stopping training after 50001920 steps
```

Write me a python script that extracts the last 100 `global/mean_episode_return` for each folder, and put them in a pandas dataframe

---------

Revision prompt 1: The `0` in `SpaceInvaders-0-just-nightingale-20211202` means the random seed. Could you put that into a column of the dataframe?

Revision prompt 2: Could you make the first column to be the environment, such as `Alien` and remove the the folder column?
"""


import os
import re
import numpy as np
import pandas as pd

# Recursively find all experiment.log files
root_dir = '.'  # Replace with the root directory of your tree
log_files = []
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file == 'experiment.log':
            log_files.append(os.path.join(root, file))

# Extract the last 100 global/mean_episode_return values for each file
data = []
for log_file in log_files:
    with open(log_file, 'r') as f:
        content = f.read()
    mean_episode_returns = re.findall(r"'global/mean_episode_return': (\d+\.\d+)", content)[-100:]
    mean_episode_returns = [float(value) for value in mean_episode_returns]
    mean_episode_return = np.average(mean_episode_returns)
    
    # Extract environment ID and random seed from the folder name
    folder_name = os.path.dirname(log_file)
    # env_id, random_seed = re.match(r'(.+)-(\d+)-just-nightingale-\d+', os.path.basename(folder_name)).groups()
    env_id, random_seed = folder_name[7:].split('-')[:2]
    # data.extend([(env_id, int(random_seed), float(value)) for value in mean_episode_returns])
    data.extend([(env_id, int(random_seed), mean_episode_return)])

# Create a pandas DataFrame
df = pd.DataFrame(data, columns=['EnvironmentID', 'RandomSeed', 'GlobalMeanEpisodeReturn'])

print(df.groupby("EnvironmentID").mean())
