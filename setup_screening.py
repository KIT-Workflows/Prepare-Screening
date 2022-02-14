import os, shutil, glob, yaml 

import ase.io

from rdkit import Chem

def smi2xyz(smi,filename):
    #os.system('obabel -:\"%s\" -O %s --gen3d'%(smi,filename))
    os.system('molconvert -2 mrv:+H \"%s\" | molconvert -3 xyz > %s'%(smi,filename))

def sanitize_multiplicity(multi,n_el):

    multi_new = multi
    multi_min = n_el%2+1

    if multi < 1:
        print('Attention: a multiplicity of %i is not possible.'%(multi))

    elif n_el%2 and multi%2: 
        print('Attention: a multiplicity of %i is not possible for an odd number of electrons.'%(multi))
        multi_new -= 1

    elif not n_el%2 and not multi%2: 
        print('Attention: a multiplicity of %i is not possible for an even number of electrons.'%(multi))
        multi_new -= 1

    if multi_new < multi_min:
        multi_new = multi_min

    if multi != multi_new:
        print('The multiplicity was set to %i by default'%(multi_new))

    return multi_new
    
def write_gaussian_input(xyz_file,gaussian_file,charge = 0,multi = 1):
    
    struct = ase.io.read(xyz_file)
    n_el = sum(struct.numbers-charge)
    
    with open(xyz_file) as infile:
        xyzlines = infile.readlines()

    with open(gaussian_file,'w') as outfile:
        outfile.write('# method/basis\n\ntitle\n\n%i %i\n'%(charge,sanitize_multiplicity(multi,n_el)))

        for line in xyzlines[2:]: outfile.write(line)
        outfile.write(4*'\n')

if __name__ == '__main__':
         
    with open('rendered_wano.yml') as infile:
        mol_input = yaml.full_load(infile)['Molecules input']

    if mol_input['Multiple molecules']:
        multi_mol_dict = mol_input['Screening']
        structures = []

        if multi_mol_dict['Type of input'] == 'List of SMILES':
            with open('mol_file') as infile:
                smiles = infile.readlines()

            for i in range(len(smiles)):
                mol_name = 'mol%i'%i
                xyz = '%s.xyz'%mol_name
                smi2xyz(smiles[i],xyz)
                write_gaussian_input(xyz,'%s.inp'%mol_name,0,1)
                structures.append(mol_name)

        elif multi_mol_dict['Type of input'] == 'List of SMILES with charge/multiplicity':
            with open('mol_file') as infile:
                smiles = infile.readlines()

            for i in range(len(smiles)):
                mol_name = 'mol%i'%i
                xyz = '%s.xyz'%mol_name
                scm = smiles[i].rstrip().split(' ')
                smi2xyz(scm[0],xyz)
                write_gaussian_input(xyz,'%s.inp'%mol_name,int(scm[1]),int(scm[2]))
                structures.append(mol_name)

        else:
            tmp_dir='tmp'
            os.mkdir(tmp_dir)
            os.system('tar -xf mol_file -C %s'%tmp_dir)
            os.chdir(tmp_dir)
            for filename in glob.glob('*'):
                if multi_mol_dict['Type of input'] == 'Archive of xyz files':
                    write_gaussian_input(filename,filename.replace('xyz','inp'),0,1)    

                structures.append(filename)
                os.rename(filename,'../%s'%filename)

            os.chdir('..')
            shutil.rmtree(tmp_dir)

    else:
        single_mol_dict = mol_input['Single molecule']

        if single_mol_dict['Type of input'] != 'Gaussian input file':

            if single_mol_dict['Type of input'] == 'SMILES':
                smi2xyz(single_mol_dict['SMILES'],'structure.xyz')
            
            else:
                os.rename('structure','structure.xyz')

            write_gaussian_input('structure.xyz','structure',single_mol_dict['Charge'],single_mol_dict['Multiplicity'])

        structures = ['structure']

    with open('output_dict.yml','w') as outfile:
        yaml.dump({'structures': structures}, outfile)

