import os
import json
from pyfaidx import Fasta


#######################################################################################################################
# lncRNA sequences from GFF
def load_json(path):
    with open(path) as fh:
        d = json.load(fh)
    return d


def write_json(d, path):
    with open(path, 'w') as of:
        json.dump(d, of)


def extract_lncRNAs(gff, fnapath):
    """
    returns: {'lncrnaID': 'seq', ...}
    """
    genome = Fasta(fnapath)
    # c = []  # reactivate for writing to disc
    d = {}
    with open(gff) as fh:
        for line in fh:
            if line.startswith('#'):
                continue
            if not 'biotype=lncRNA' in line:
                continue

            ll = line.strip().split('\t')
            chrom = ll[0]
            start, end = map(int, ll[3:5])
            strand = ll[6]
            name = ll[-1].split('ID=')[1].split(';')[0].replace('gene-', '')

            if strand == '-':
                seq = genome[chrom][start:end].reverse.complement.seq
            else:
                seq = genome[chrom][start:end].seq

            # c.append(f'>{name}|{chrom}|{start}|{end}|{strand}\n{seq}\n')
            d[name] = seq
        return d


def load_lncrna2seq(tmpout, species, specdict):
    lncrnafile = f'{tmpout}/{species}_lncrna.json'
    if os.path.isfile(lncrnafile):
        lncrna2seq = load_json(lncrnafile)
    else:
        gffpath = specdict[species]['annotation']
        genome = specdict[species]['genome']
        lncrna2seq = extract_lncRNAs(gffpath, genome)
        write_json(lncrna2seq, lncrnafile)
    return lncrna2seq


#######################################################################################################################