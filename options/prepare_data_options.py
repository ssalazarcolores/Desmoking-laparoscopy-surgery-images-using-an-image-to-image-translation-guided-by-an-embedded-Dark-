from .base_options import BaseOptions


class PrepareDataOptions(BaseOptions):
    def initialize(self):
        BaseOptions.initialize(self)
        name='smog/'
        path_root='../datasets/'+name
        self.parser.add_argument('--path_root', type=str, default='../datasets/smog/')
        self.parser.add_argument('--path_imgs_A', type=str, default=path_root+'output/')
        self.parser.add_argument('--path_imgs_B', type=str, default=path_root+'input/')
        self.parser.add_argument('--path_result', type=str, default=path_root+'merged/')
        self.parser.add_argument('--merge', type=bool, default=True)
                              