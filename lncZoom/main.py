import logging
import os

from input import modules_from_html, parse_yaml
from processing import load_lncrna2seq
from taxOrder.taxOrder import order_taxa


###############################################################################################
modulehtml = "/home/felixl/applications/LncLOOMv2/cyrano_ordered/Html_Files/Modules.html"
tree = '/home/felixl/PycharmProjects/lncRNA/data/test_vertebrate_tree.nwk'
yamlpath = '/home/felixl/PycharmProjects/lncRNA/data/test_input.yaml'
reference = 'Homo_sapiens'

output = '/home/felixl/software/lncZoom/output'


##############################################################################################


def check_files(files):
    for f in files:
        if not os.path.isfile(f):
            raise ValueError(f'File not found at: {f}')


def main():
    logging.basicConfig(level=logging.DEBUG)

    # load lncLoom results
    # depth2module = modules_from_html(modulehtml)

    # load yaml
    specdict, paths = parse_yaml(yamlpath)

    # check input
    paths.append(tree)
    check_files(paths)

    # load species tree and linearize
    taxorder = order_taxa(tree, 'Homo_sapiens')

    # create temporary output directory if necessary
    tmpout = f'{output}/tmp'
    if not os.path.isdir(tmpout):
        os.makedirs(tmpout)

    for species in taxorder:
        logging.info(species)
        lncrna2seq = load_lncrna2seq(tmpout, species, specdict)
        print(list(lncrna2seq.keys())[:10])
        break








if __name__ == "__main__":
    main()