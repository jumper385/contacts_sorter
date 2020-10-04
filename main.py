import argparse

def csv_parser(filename):
    """outputs a csv as a multidimensional array"""
    raw = [row.strip().split(',') for row in open(filename)]
    return raw

def csv_to_dict(filename):
    """outputs a dictionary from a csv and merges duplicates to account for repetition in csv"""
    csv_array = csv_parser(filename)
    heading = csv_array[0]
    data = csv_array[1:]
    newDict = {}
    
    for row in data:
        firstname, lastname, mobile, email1, email2 = row
        fullname = "~||sep||~".join([firstname, lastname])
        emailArray = [x for x in [*[email1.strip()], *[email2.strip()]] if x]
        
        if fullname not in newDict.keys():
            newDict[fullname] = {
                "mobile": [mobile] if mobile else [],
                "emails": emailArray
            }
        else:
            newDict[fullname]['mobile'] = [*newDict[fullname]['mobile'], mobile]
            newDict[fullname]['emails'] = [*newDict[fullname]['emails'], *emailArray]
    
    return newDict

def dict_to_csv(target_dict, filename):
    """translates dictionary into csv file - repetiotions are enumerated as columns"""
    root_keys = [*target_dict.keys()]
    subkeys = [*target_dict[root_keys[0]].keys()]
    max_key_len = {}
    
    new_file = open(filename,'w')
    
    for root_key in root_keys:
        for subkey in subkeys:
            entries = target_dict[root_key][subkey]
            
            if subkey not in max_key_len.keys():
                max_key_len[subkey] = len(entries)
            else:
                max_key_len[subkey] = len(entries) if len(entries) > max_key_len[subkey] else max_key_len[subkey]
    
    headings = ['firstname','lastname']
    for name in sorted([*max_key_len.keys()]):
        headings = [*headings, *[f'{name}{x}' for x in range(max_key_len[name])]]
    
    new_file.write(f'{",".join(headings)}\n')
    
    for root_key in root_keys:
        row_entry = [*root_key.split('~||sep||~')]
        for subkey in sorted(subkeys):
            raw_entries = target_dict[root_key][subkey]
            padded_entries = raw_entries + ['' for x in range(0,max_key_len[subkey] - len(raw_entries))]
            row_entry = [*row_entry,*padded_entries]
        new_file.write(','.join(row_entry)+'\n')
    
    new_file.close()

def merge_dict(dict1, dict2):
    """merges dictionaries together - concatenates arrays of matching fields and returns set of unique concatenations"""
    matching = [key for key in dict1.keys() if key in dict2.keys() ]
    mismatch = [key for key in dict1.keys() if key not in dict2.keys() ]
    
    for key in matching:
        data_keys = [*dict1[key].keys()]
        for subfield in data_keys:
            dict1[key][subfield] = [*set([*dict1[key][subfield], *dict2[key][subfield]])]
            
    for key in mismatch:
        dict1.update(dict2)
    
    return dict1

def merger(filename1, filename2, outputname):
    """main function to do all the operations"""
    print('hello world')
    
    csv1 = csv_to_dict(filename1)
    csv2 = csv_to_dict(filename2)
    
    merged_contacts = merge_dict(csv1, csv2)
    
    dict_to_csv(merged_contacts, outputname)

def parse_conf(conffile):
    configs = [tuple(x.split(':')) for x in open(conffile).read().split('|')]
    return dict(configs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    
    parser.add_argument('--f1', metavar='F1', help='adds one CSV of contacts')

    parser.add_argument('--f2', metavar='F2', help='adds another CSV of contacts')

    parser.add_argument('--out', metavar='OUTFILE', help='name of the output file')

    parser.add_argument('--conf', metavar='CONFIG', help='use a config file instead with a set string filename1:[STRING]|filename2:[STRING]|outname:[STRING]')

    args = parser.parse_args()

    if args.conf:
        conf_args = parse_conf(args.conf)
        merger(conf_args['filename1'], conf_args['filename2'], conf_args['outname'])
    elif args.f1 and args.f2 and args.out:
        merger(args.f1, args.f2, args.out)
    else:
        print('Error! you need to provide either a configuration file OR all the relevant filenames. run --h for help!')