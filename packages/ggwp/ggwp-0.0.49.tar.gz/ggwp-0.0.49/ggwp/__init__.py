# import everything of this pagages
# from folder.file import class

from ggwp.EzDataModel.BasketEvolving import *
from ggwp.EzDataModel.Cohort import *
from ggwp.EzDataModel.CustomerMovement import *
from ggwp.EzDataModel.DataModel import *
from ggwp.EzDataModel.RFMT import *

from ggwp.EzModeling.BenchMark import *
from ggwp.EzModeling.Check import *
from ggwp.EzModeling.Evaluation import *
from ggwp.EzModeling.Log import *

from ggwp.EzPipeline.ConvertVariables import *
from ggwp.EzPipeline.GroupImputer import *

from ggwp.EzUtils import *

from ggwp.config.config import *

# params go below here
# example: ggwp.__version__

__version__ = EzConfig().get_config(section='default',key='version')