import torch.optim as optim

import importlib
import pkgutil

# get a list of all submodules of the current package
package_name = __name__
package_path = __path__
module_names = [name for _, name, _ in pkgutil.walk_packages(package_path)]


def get_optimizer(config, model):
    optimizer_name = config['optimizer_name']
    settings = config['settings']

    if hasattr(optim, optimizer_name):
        # get optimizer from torch.optim package
        optimizer = getattr(optim, optimizer_name)(model.parameters(), **settings)
        return optimizer
    else:
        # get optimizer defined in this package
        for module_name in module_names:
            module = importlib.import_module(f'{package_name}.{module_name}')
            if hasattr(module, optimizer_name):
                optimizer = getattr(module, optimizer_name)(model.parameters(), **settings)
                return optimizer

    raise f"Optimizer with name {optimizer_name} not found"
