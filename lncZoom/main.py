import logging
import os
import subprocess as sp

from input import modules_from_html, parse_yaml, read_fasta
from processing import load_lncrna2seq
from taxOrder.taxOrder import order_taxa


###############################################################################################
modulehtml = "/home/felixl/applications/LncLOOMv2/cyrano_ordered/Html_Files/Modules.html"
lncloom_input = '/home/felixl/PycharmProjects/lncRNA/data/Cyrano.fas'
tree = '/home/felixl/PycharmProjects/lncRNA/data/test_vertebrate_tree.nwk'
yamlpath = '/home/felixl/PycharmProjects/lncRNA/data/test_input.yaml'
reference = 'Homo_sapiens'

output = '/home/felixl/software/lncZoom/output'
projectname = 'cyrano'

###############################################################################################
lncloom_specs = {
    'Human': 'Homo_sapiens',
    'Rhesus': 'Macaca_mulatta',
    'Mouse': 'Mus_musculus',
    'Rat': 'Rattus_norvegicus',
    'Rabbit': 'Oryctolagus_cuniculus',
    'Dog': 'Canis_lupus_familiaris',
    'Cow': 'Bos_taurus',
    'Opossum': 'Monodelphis_domestica',
    'Chicken': 'Gallus_gallus',
    'Xenopus': 'Xenopus_tropicalis',
    'Zebrafish': 'Danio_rerio',
    'Stickleback': 'Gasterosteus_aculeatus_aculeatus',
    'Fugu': 'Takifugu_rubripes',
    'Medaka': 'Oryzias_latipes',
    'Atlantic_Cod': 'Gadus_morhua',
    'Nile_Tilapia': 'Oreochromis_niloticus',
    'Spotted_Gar': 'Lepisosteus_oculatus',
    'Elepahnt_Shark': 'Callorhinchus_milii',
}
##############################################################################################


def check_files(files):
    for f in files:
        if not os.path.isfile(f):
            raise ValueError(f'File not found at: {f}')


def main():
    logging.basicConfig(level=logging.DEBUG)

    # load lncLoom results
    depth2module = modules_from_html(modulehtml)

    # load lncloom input
    raw_lncloom_seqs = read_fasta(lncloom_input)
    # TEMPORARY
    lncloom_seqs = {lncloom_specs[species]: seq for species, seq in raw_lncloom_seqs.items()}

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

    model = f'{output}/{projectname}.hmm'
    alignment = f'{output}/{projectname}.sto'
    for species in taxorder:
        logging.info(species)
        if species in lncloom_seqs:
            logging.debug('Species in lncloom_seqs')
            lncrnaseq = lncloom_seqs[species]
            # first lncloom seq initializes model
            if not os.path.isfile(model):
                logging.debug('trying to build model')
                cmd = f'hmmbuild --dna -O {alignment} {model} "-"'
                call = sp.Popen(
                    cmd, shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, encoding='utf8'
                )
                res, err = call.communicate(lncrnaseq)
                print(res)
                print(err)



        # lncrna2seq = load_lncrna2seq(tmpout, species, specdict)
        # print(list(lncrna2seq.keys())[:10])
        break








if __name__ == "__main__":
    main()