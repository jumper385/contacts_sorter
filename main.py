import argparse

def csv_parser(filename):
    """outputs a csv as a multidimensional array"""
    raw = [row.strip().split(',') for row in open(filename)] # clean, split by commas and append to a list
    return raw # return the list

def csv_to_dict(filename):
    """outputs a dictionary from a csv and merges duplicates to account for repetition in csv"""
    csv_array = csv_parser(filename) # parses csv to list of rows (type list)
    heading, data= csv_array[0], csv_array[1:] # splits the data into headings and contacts 
    newDict = {} # open a new dictionary please!
    
    for row in data: # Now we're gonna iterate through each row list
        firstname, lastname, mobile, email1, email2 = row # we assume each row has the following structure so we breakdown as such
        fullname = "~||sep||~".join([firstname, lastname]) # grabs the first and last name and joins them with a seperator symbol which we can use later to break down the name into first and last name again
        emailArray = [x for x in [*[email1.strip()], *[email2.strip()]] if x] # grabs the emails, cleans theme and puts them into an array which we'll place into the dictionary later
        
        newDict.setdefault(fullname,{"mobile":[] if mobile else [],"emails":[]}) # if entry with key=fullname doesn't exist we start it up as such
        newDict[fullname]['mobile'] = [*set( filter(lambda x: x != '', [*newDict[fullname]['mobile'], mobile]) )] # append and only keep the unique mobile numbers
        newDict[fullname]['emails'] = [*set( filter(lambda x: x != '', [*newDict[fullname]['emails'], *emailArray]))] # append and only keep the unique emails
    
    return newDict # finally return the data thanks

def dict_to_csv(target_dict, filename):
    """translates dictionary into csv file - repetiotions are enumerated as columns"""
    root_keys = [*target_dict.keys()] # holds the fullnames
    subkeys = [*target_dict[root_keys[0]].keys()] # holds the email and mobile keys
    max_key_len = {} # new dictionary we use to help define if we'll need email1, email2 ect...
    
    new_file = open(filename,'w') # open the output and write to it
    
    for root_key in root_keys: # looks through the full names
        for subkey in subkeys: # looks through each entry
            entries = target_dict[root_key][subkey] # grabs the entries for each fullname's email and mobile
            
            max_key_len.setdefault(subkey,int()) # if entry in max key length doesn't exist, we'll set it up as such
            max_key_len[subkey] = len(entries) if len(entries) > max_key_len[subkey] else max_key_len[subkey] # if the current length we see is longer than the previous length, we change it else we leave it as is 
    
    headings = ['firstname','lastname'] # we need these headings in the final csv
    for name in sorted([*max_key_len.keys()]): # grabs the mobile and email keys  
        headings = [*headings, *[f'{name}{x}' for x in range(max_key_len[name])]] # makes the headings based on the max key len
    
    new_file.write(f'{",".join(headings)}\n') # write headings to the file as a csv
    
    for root_key in root_keys:
        row_entry = [*root_key.split('~||sep||~')] # split so that we have the full names 
        for subkey in sorted(subkeys): # for each subkey, we need to format them into an array
            raw_entries = target_dict[root_key][subkey]
            padded_entries = raw_entries + ['' for x in range(0,max_key_len[subkey] - len(raw_entries))] # any empty entries are made into ''
            row_entry = [*row_entry,*padded_entries]
        new_file.write(','.join(row_entry)+'\n') # write each row as csv
    
    new_file.close() # close and we're golden

def merge_dict(dict1, dict2):
    """merges dictionaries together - concatenates arrays of matching fields and returns set of unique concatenations"""
    matching = [key for key in dict1.keys() if key in dict2.keys() ] # finds fullname matches from dict 1 in dict 2
    mismatch = [key for key in dict1.keys() if key not in dict2.keys() ] # finds fullname mismatches from dict1 in dict 2
    
    for key in matching: # if they match, we just append
        data_keys = [*dict1[key].keys()] # base keys (mobile and emails) from dict 1
        for subfield in data_keys: 
            dict1[key][subfield] = [*set([*dict1[key][subfield], *dict2[key][subfield]])] # for each field (mobile and email) merge from the two dictionaries and get the unique values and chuck them in an array
            
    for key in mismatch: # just update the dicitonary with new dictionary fields of the fullnames
        dict1.update(dict2)
    
    return dict1

def main(filename1, filename2, outputname):
    """main function to do all the operations"""
    
    csv1 = csv_to_dict(filename1) 
    csv2 = csv_to_dict(filename2)
    
    merged_contacts = merge_dict(csv1, csv2)
    
    dict_to_csv(merged_contacts, outputname)

def parse_conf(conffile):
    """parses a preformatted configuration file"""
    configs = [tuple(x.split(':')) for x in open(conffile).read().split('|')]
    return dict(configs)

if __name__ == "__main__":
    """documentation is on the argparse docs - much better than me explaining everything"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    
    parser.add_argument('--f1', metavar='F1', help='adds one CSV of contacts')

    parser.add_argument('--f2', metavar='F2', help='adds another CSV of contacts')

    parser.add_argument('--out', metavar='OUTFILE', help='name of the output file')

    parser.add_argument('--conf', metavar='CONFIG', help='use a config file instead with a set string filename1:[STRING]|filename2:[STRING]|outname:[STRING]')

    args = parser.parse_args()

    if args.conf: # if there's a configuration file, we use that (and forget the rest)
        conf_args = parse_conf(args.conf)
        merger(conf_args['filename1'], conf_args['filename2'], conf_args['outname'])
    elif args.f1 and args.f2 and args.out: # if there isnt a config file we require f1, f2 and out
        merger(args.f1, args.f2, args.out)
    else:
        print('Error! you need to provide either a configuration file OR all the relevant filenames. run --h for help!')