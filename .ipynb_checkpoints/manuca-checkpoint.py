import numpy as np #https://numpy.org/
import chemparse #https://pypi.org/project/chemparse/
from mendeleev import element #https://github.com/lmmentel/mendeleev

version = 0.12
date = "02/2022"

def printHelp():
    '''Print the help dialog'''
    print('================= Manuca Help =================')
    print('Usage: Enter a stoichiometric formula (e.g. H2O) and confirm with ENTER. Type "q" to quit. Enter "multi" to construct a multi-compound sample, see below.')
    print('The input is read with chemparse, which can handle complicated formulas with one level of parentheses, e.g. (Mg0.7Zn0.3)5H2(AsO4)4(H2O)10 (ICSD entry 267). ')
    print('Note: chemparse currently only handles non-nested paretheses. A formula with nested parentheses like "CH3(C2(CH3)2)3CH3" will not work properly. Please use the "multi" option instead to construct such a compound.')
    print('\nThe program will calculate and output various properties:')
    print('  "Chemical formula" -> The parsed formula read from the user input.')
    print('  "Composition table" -> Composition in atomic % (at.%) and weight % (wt.%).')
    print('  "Mean atomic number" -> Various forms of the mean atomic number as listed in Howell et al, Scanning 20 (1998):')
    print('    "Mueller (1954) -> Mueller, Phys. Rev. 93, 891 (1954).')
    print('    "Saldick & Allen (1954) --> Saldick and Allen, J Chem Phys 22 (1954).')
    print('    "Joyet (1954) -> Joyet et al, The Dosage of Gamma Radiation at Very High Energies. The Brown Boveri Betatron, (1954).')
    print('    "Joyet (1954) -> Hohn and Niedrig: Elektronrenrückstreuung an dünnen Metall-undIsolatorschichten. Optik 35 (1972)')
    print('    "Joyet (1954) -> Buechner, Bestimmung der mittleren Ordnungszahl vonLegierungen bei der quantitativen Mikrosondenanalyse, Arch Eisenhüttenwesen 44 (1973)')
    print('    "Everhart (1960) -> Everhart, Simple theory concerning the reflection of electrons from solids. J Appl Phys 31 (1960)')
    print('  "Other properties" -> Other compound properties which can be calculated from the stoichiometry.')
    print('    "Zeff (Egerton, EFTEM)" -> Eq. (5.4) from Egerton, Electron Energy-Loss Spectroscopy in the Electron Microscope, Springer (2011)')
    print('    "Aeff (Egerton, EFTEM)" -> Effective atomic mass for EFTEM.')
    print('    "Tot. at. mass" -> Total atomic/molecular mass in g/mol.')
    print('    "Avg. at. mass" -> Average atomic/molecular mass in g/mol.')
    print('\nUsing "multi" to construct multi-compound samples:')
    print('  (1) Type "multi" to start the dialog.')
    print('  (2) Enter the number of "sub-compounds" you want to mix (e.g. 3).')
    print('  (3) For each sub-compound, specify the stoichiometry and relative concentration. For the latter you can use any relative concentration numbers, as their sum will be used to normalize the concentrations. Example: Mixing 3 compounds with a relative ratio 20%, 30%, and 50% can be done with (2, 3, 5) as well as (20, 30, 50) as well as (40, 60, 100).')
    print('\nManuca is based on the following Python packages. Please cite them if you find use in Manuca.')
    print('  NumPy (https://numpy.org/), chemparse (https://pypi.org/project/chemparse/) , mendeleev (https://github.com/lmmentel/mendeleev)')
    print(f'Manuca version: {version}, {date}, Author: Lukas Gruenewald')
    print('==============================================')
    
def multi_compound(n_comp):
    '''Create multi-compound from n_comp compounds'''
    #mc stores compounds
    mc_in = np.zeros(n_comp, dtype=[('comp', 'U500'),('conc', 'f4')])
    
    #Grab and store sub-compound strings and relative concentrations from user input
    for i in range(n_comp):
            print(f'Compound {i+1} of {n_comp}.') 
            comp = input('Enter stoichiometry: ')
            rel_conc = input('Enter relative concentration: ')
            mc_in[i] = (comp, rel_conc)
            
    #Total concentration for normalization 
    mc_in['conc'] /= np.sum(mc_in['conc'])
    
    #Initialize Complete string
    S = ''
    
    #Parse each compound, weight with normalized concentration factor, and append to S
    for i, c in enumerate(mc_in['comp']):
        d = chemparse.parse_formula(c)
        
        #Normalize each compound, not useful?
        #d_sum = sum(d.values())
        #d.update((x, np.round(y/d_sum,4)) for x, y in d.items())
        
        #Weight with user input
        d.update((x, np.round(y*mc_in['conc'][i],4)) for x, y in d.items())
        for ele, r in d.items():
            S += ele
            S += str(r)
    return S

print(f'Manuca - Mean Atomic Number calculator (v{version})')
print('Enter "help" to show further information. Enter "q" to quit. Enter "multi" to construct a multi-compound sample.')
print(f'Manuca comes without any warranty for correctness. PLEASE double-check the outputs and if the input stoichiometry is read in correctly.')
while True:
    user_input = input("Enter stoichiometry: ")
    if(user_input == 'q'):
        break
    if(user_input == 'help'):
        printHelp()
        continue
    if(user_input == 'multi'):
        n_comp = int(input("Enter number of compounds: "))
        multicompound = multi_compound(n_comp)
    
    # Dictionary from chemparse with values
    if(user_input == 'multi'):
        parse = multicompound
    else:
        parse = user_input
    
    ### Calculations
    d = chemparse.parse_formula(parse)
    e = list(d.keys()) #elements
    w = np.array(list(d.values())) #weights
    try:
        m = element(e) #Element properties from mendeleev
    except: 
        print('At least one element could not be recognized. Please check stoichiometry and try again.')
        continue

    ### Atomic percentages
    n = np.sum(w)
    d_atp = {k: v / n for k, v in d.items()}

    ### Weight percentages
    aw = np.array([element.atomic_weight for element in m])
    n_weight = np.sum(w/n*aw)
    d_wtp = {k: v/n*aw[i]/n_weight for i, (k, v) in enumerate(d.items())}

    ### Mean atomic numbers
    decimals = 3
    Z = np.array([element.atomic_number for element in m])
    Wtpercents = np.fromiter(d_wtp.values(), dtype='float')
    Atpercents = np.fromiter(d_atp.values(), dtype='float')
    
    meanZ_Average = np.round(np.sum(w/n*Z), decimals) #Simple average based on atomic proportions
    meanZ_Mueller = np.round(np.sum(Z*Wtpercents), decimals) #Mueller 1954
    meanZ_SaldickAllen = np.round(np.sum(Atpercents*Z**2)/np.sum(Atpercents*Z), decimals) #Saldick and Allen 1954
    meanZ_Joyet = np.round(np.sqrt(np.sum(Atpercents*Z**2)), decimals) #Joyet 1953, Hohn und Niedrig 1972, Büchner 1973 
    meanZ_Everhart = np.round(np.sum(Wtpercents*Z**2)/np.sum(Wtpercents*Z), decimals) #Everhart 1960, Joy 1995
    
    ### Effective atomic number
    Zeff_Egerton = np.round(np.sum(Atpercents*Z**1.3)/np.sum(Atpercents*Z**0.3), decimals) #effective Z, Egerton for EFTEM
    Aeff_Egerton = np.round(np.sum(Atpercents*aw**1.3)/np.sum(Atpercents*aw**0.3), decimals) #effective A, Egerton for EFTEM
    
    ### Atomic mass
    tot_atomic_mass = np.round(np.sum(w*aw), decimals)
    avg_atomic_mass = np.round(np.sum(w/n*aw), decimals)
    
    #Print results
    print('Chemical formula:')
    print(chemparse.parse_formula(parse))
    print('------------------------------')
    print('Element\t at.%\t','wt.%')
    for key, value in d_atp.items():
        print(key,'\t', np.round(value*100,2),'\t',np.round(d_wtp[key]*100,2))
    print('------------------------------')
    print('Mean atomic numbers:')
    print('------------------------------')
    print(f'Atomic-percent average:\t{meanZ_Average}')
    print(f'Mueller (1954):\t\t{meanZ_Mueller}')
    print(f'Saldick & Allen (1954):\t{meanZ_SaldickAllen}')
    print(f'Joyet (1953):\t\t{meanZ_Joyet}')
    print(f'Everhart (1960):\t{meanZ_Everhart}')
    print('------------------------------')
    print('Other properties:')
    print('------------------------------')
    print(f'Zeff (Egerton, EFTEM):\t{Zeff_Egerton}')
    print(f'Aeff (EFTEM, g/mol):\t{Aeff_Egerton}')
    print(f'Tot. A (g/mol):\t\t{tot_atomic_mass}')
    print(f'Avg. A (g/mol):\t\t{avg_atomic_mass}')
    print('==============================\n')
    

    
