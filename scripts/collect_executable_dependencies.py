import os
import os.path
import sys

def cp(from_path, to_path='.'):
    os.system(f'cp {from_path} {to_path}')

def mkdir(folderpath):
    os.system(f'mkdir {folderpath}')

def ldd(executable, ldd_export_path):
    os.system(f'ldd {executable} > {ldd_export_path}')

def batch_cp(filepaths_list, to_path='.'):
    for filepath in filepaths_list:
        if not os.path.exists(filepath):
            print(f'{filepath} doesn\'t exist. Ignorning...')
            continue
        cp(filepath, to_path)

def get_libpaths(ldd_export):
    """
    takes the ldd output file and decomposes it into meaningful lists
    """
    lib_paths = []
    ignored_cases = []
    unknown_cases = []
    with open(ldd_export, 'r') as fin:
        for line in fin.readlines():
            splits = line.split()
            if len(splits) == 2:
                print(splits[0], '- shared object doesn\'t have physical file on disk. Ignored.')
                ignored_cases.append(splits[0])
            elif len(splits) == 4:
                print(splits[0], '- present at', splits[2])
                lib_paths.append([splits[0], splits[2]])
            else:
                print(splits, '- unknown case encountered. Ignore and continue? [Y/n]: ')
                Y_n = input()
                while Y_n not in ['y', 'Y', 'n', 'N']:
                    Y_n = input('Invalid input. Unknown case encountered. Ignore and continue? [Y/n]: ')
                if Y_n in ['n', 'N']:
                    print('Please report the case to nikhilsrajan@gmail.com')
                else:
                    unknown_cases.append(splits)
    return lib_paths, ignored_cases, unknown_cases



if __name__ == '__main__':
    if len(sys.argv) not in [2, 3]:
        if len(sys.argv) > 3:
            print('Too many arguments.')
        elif len(sys.argv) < 2:
            print('Too few arguments.')
        print(f'Usage: {sys.argv[0]} [executable] [to-path, DEFAULT=\'.\']')
        exit(1)
    else:
        executable = sys.argv[1]
        if len(sys.argv) == 3:
            to_path = sys.argv[2]
        else:
            to_path = '.'
            
        ldd_export_path = to_path + '/dependencies.txt'

        ldd(executable, ldd_export_path)
        lib_paths, ignored_cases, unknown_cases = get_libpaths(ldd_export_path)
        batch_cp([x[1] for x in lib_paths], to_path)

        print(f'\nDone.\n\nSuccess: {len(lib_paths)}\nIgnored: {len(ignored_cases)}\nUnknown: {len(unknown_cases)}')