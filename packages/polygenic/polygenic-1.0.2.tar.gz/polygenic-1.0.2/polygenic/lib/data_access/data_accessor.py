import logging
import pathlib
from typing import Dict
from typing import List
from typing import Union
from polygenic.lib import mobigen_utils
from polygenic.lib.data_access.dto import SnpData
from polygenic.lib.data_access.dto import SnpDataManySamples

# rsidx
import os
from gzip import open as gzopen
import rsidx
import sqlite3

logger = logging.getLogger('description_language.' + __name__)

class VcfAccessor(object):
    def __init__(self, vcf_path:str):
        super().__init__()
        self.path = vcf_path
        if os.path.exists(self.path + '.idx.db'):
            os.remove(self.path + '.idx.db')
        with sqlite3.connect(self.path + '.idx.db') as dbconn, gzopen(self.path, 'rt') as vcffh:
            rsidx.index.index(dbconn, vcffh)
        self.sample_names = mobigen_utils.get_sample_names([vcf_path])
        self.__data: Dict[str, Dict[str:SnpData]] = {}  # dictionary rsid:{sample_name:ModelSnpData}

    def __get_data_for_given_rsid(self, rsid) -> Dict[str, SnpData]:
        line = self.get_vcf_line_for_rsid(rsid)
        if not line:
            logger.debug(f'No line for rsid {rsid} found')
            raise DataNotPresentError
        data = mobigen_utils.get_genotypes(line, self.sample_names)
        self.__data[rsid] = {sample_name: SnpData(data.ref, data.alts, genotype) for sample_name, genotype in data.genotypes.items()}
        return self.__data[rsid]

    def get_data_for_sample(self, sample_name:str, rsid:str) -> SnpData:
        try:
            return self.__data[rsid][sample_name]
        except KeyError:
            try:
                return self.__get_data_for_given_rsid(rsid)[sample_name]
            except DataNotPresentError:
                return None

    def get_vcf_line_for_rsid(self, rsid:str) -> Union[None, str]:
        try:
            with sqlite3.connect(self.path + '.idx.db') as dbconn:
                for line in rsidx.search.search([rsid], dbconn, self.path):
                    return line
        except KeyError:
            raise DataNotPresentError
        #id_ = rs_id[2:]
        #line = mobigen_utils.extract_line_containing_rs_id(f_path, rsid_end, id_)
        #return line if not line.startswith('#') else None
        raise DataNotPresentError

class DataNotPresentError(RuntimeError):
    pass





def path_to_fname_stem(path:str) -> str:
    return pathlib.PurePath(path).name.split('.')[0]