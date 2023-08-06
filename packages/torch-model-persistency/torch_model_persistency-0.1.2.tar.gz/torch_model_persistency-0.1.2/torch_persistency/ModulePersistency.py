import torch
import os
from shutil import rmtree

class ModulePersistency:

    def __init__(self,checkpoint_dir,version = None):

        if not version:
            try:
                with open("torch_persistency.env","r+") as fp:

                    version = int(fp.read())
                    # Delete all content in file.
                    
            except FileNotFoundError:
                version = 0
            
            except ValueError:
                version = 0
                
            
            finally:
                with open("torch_persistency.env","w") as fp:
                    fp.write(f"{version+1}")

        self.checkpoint_dir = checkpoint_dir
        self.version = version
        self.save_dir = os.path.join(self.checkpoint_dir,str(self.version))
        self._prepare()



    def _prepare(self):
        if os.path.exists(self.save_dir):
            rmtree(self.save_dir)

        os.mkdir(self.save_dir)

    def save(self,module,epoch : int,name = None):
        
        if not name:
            name = type(module).__name__

        torch.save(module,os.path.join(self.save_dir,f"{name}_{epoch}.pt"))
