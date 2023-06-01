from bs4 import BeautifulSoup
import yaml


#######################################################################################################################
# read_lncloom HTML
def modules_from_pre_line(preline):
    modules = preline.split()[1:-1]
    o = []
    for module in modules:

        # moduleseq = module.split('-')[-1].split('Depth')[0]
        if '-' in module:
            double_moduleseq = module.split('-')[-1].split('Depth')[0]
        else:
            double_moduleseq = module.split(')')[-1].split('Depth')[0]

        moduleseqindex = int(len(double_moduleseq) / 2)
        moduleseq = double_moduleseq[:moduleseqindex]
        o.append(moduleseq)

    # print(o)
    return o


def depth_of_pre(html):
    pre_depth = []
    headers = html.find_all('h1')
    for header in headers:
        if not 'conserved' in header.text:
            continue
        depth = header.text.split()[-1].replace(')', '')
        pre_depth.append(depth)

    return pre_depth


def modules_from_html(modulehtml):
    with open(modulehtml) as fp:
        soup = BeautifulSoup(fp, features="html.parser")

    all_pre = soup.find_all('pre')
    pre_depths = depth_of_pre(soup)

    if not len(all_pre) == len(pre_depths):
        raise ValueError(f'Number of pre entries does not match number of depths found')

    depth2modules = {}
    for pre in all_pre:
        depth = pre_depths.pop(0)

        first_preline = pre.text.split('>')[1]
        # print(first_preline)
        modules = modules_from_pre_line(first_preline)
        depth2modules[depth] = modules
    return depth2modules


#######################################################################################################################
# YAML
def parse_yaml(path):
    paths = []
    specdict = {}
    with open(path, 'r') as param_handle:
        params = yaml.load_all(param_handle, Loader=yaml.FullLoader)
        for entry in params:
            name = entry.pop('name')
            specdict[name] = entry
            paths.extend([entry['annotation'], entry['genome']])

    return specdict, paths




