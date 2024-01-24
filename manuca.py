import numpy as np #https://numpy.org/
import chemparse #https://pypi.org/project/chemparse/
from mendeleev import element #https://github.com/lmmentel/mendeleev

version = 0.15
date = "09/2023"

def printHelp():
    '''Print the help dialog'''
    print('================= Manuca Help =================')
    print('Usage: Enter a stoichiometric formula (e.g. H2O) and confirm with ENTER. Type "q" to quit. Enter "multi" to construct a multi-compound sample, see below.')
    print('The input is read with chemparse, which can handle complicated formulas with one level of parentheses, e.g. (Mg0.7Zn0.3)5H2(AsO4)4(H2O)10 (ICSD entry 267). ')
    print('Note: chemparse currently only handles non-nested paretheses. A formula with nested parentheses like "CH3(C2(CH3)2)3CH3" will not work properly. Please use the "multi" option instead to construct such a compound.')
    print('Type "decimals" to adjust the number of decimals for the output (default is 3).')
    print('\nThe program will calculate and output various properties:')
    print('  "Chemical formula" -> The parsed formula read from the user input.')
    print('  "Composition table" -> Composition in atomic % (at.%) and weight % (wt.%).')
    print('  "Mean atomic number" -> Various forms of the mean atomic number as listed in Howell et al, Scanning 20 (1998):')
    print('    "Mueller (1954) -> Mueller, Phys. Rev. 93, 891 (1954), Source:  https://doi.org/10.1002/sca.1998.4950200105')
    print('    "Saldick & Allen (1954) --> Saldick and Allen, J Chem Phys 22 (1954), Source:  https://doi.org/10.1002/sca.1998.4950200105')
    print('    "Joyet (1954) -> Joyet et al, The Dosage of Gamma Radiation at Very High Energies. The Brown Boveri Betatron, (1954), Source:  https://doi.org/10.1002/sca.1998.4950200105')
    print('    "Joyet (1954) -> Hohn and Niedrig: Elektronrenrückstreuung an dünnen Metall-undIsolatorschichten. Optik 35 (1972), Source:  https://doi.org/10.1002/sca.1998.4950200105')
    print('    "Joyet (1954) -> Buechner, Bestimmung der mittleren Ordnungszahl vonLegierungen bei der quantitativen Mikrosondenanalyse, Arch Eisenhüttenwesen 44 (1973), Source: https://doi.org/10.1002/sca.1998.4950200105')
    print('    "Everhart (1960) -> Everhart, Simple theory concerning the reflection of electrons from solids. J Appl Phys 31 (1960), https://doi.org/10.1063/1.1735868')
    print('    "Donovan (2003) -> Donovan, J., Pingitore, N., & Westphal, A. (2003). Compositional Averaging of Backscatter Intensities in Compounds. Microscopy and Microanalysis, 9(3), 202-215. https://doi.org/10.1017/S1431927603030137')
    print('    "Zeff (el, Langmore)" -> Effective atomic number for elastic scattering. Langmore et al. Optik, 38 (1973), pp. 335-350')
    print('    "Zeff (inel, Egerton)" -> Effective atomic number for inelastic scattering. Eq. (5.4) from Egerton, Electron Energy-Loss Spectroscopy in the Electron Microscope, Springer (2011)')
    print('  "Other properties" -> Other compound properties which can be calculated from the stoichiometry.')
    print('    "Aeff (inel, Egerton)" -> Effective atomic mass for inelastic scattering in g/mol.')
    print('    "Tot. at. mass" -> Total atomic/molecular mass in g/mol.')
    print('    "Avg. at. mass" -> Average atomic/molecular mass in g/mol.')
    print('\nUsing "multi" to construct multi-compound samples:')
    print('  (1) Type "multi" to start the dialog.')
    print('  (2) Enter the number of "sub-compounds" you want to mix (e.g. 3).')
    print('  (3) For each sub-compound, specify the stoichiometry and relative concentration. For the latter you can use any relative concentration numbers, as their sum will be used to normalize the concentrations. Example: Mixing 3 compounds with a relative ratio 20%, 30%, and 50% can be done with (2, 3, 5) as well as (20, 30, 50) as well as (40, 60, 100).')
    print('\nManuca is based on the following Python packages. Please cite them if you find use in Manuca.')
    print('  NumPy (https://numpy.org/), chemparse (https://pypi.org/project/chemparse/) , mendeleev (https://github.com/lmmentel/mendeleev)')
    print(f'Manuca version: {version}, {date}, Author: Lukas Gruenewald')
    print(f'Github: https://github.com/lukmuk/manuca')
    print('==============================================')

def multi_compound(n_comp):
    '''Create multi-compound from n_comp compounds'''
    # mc stores compounds
    mc_in = np.zeros(n_comp, dtype=[('comp', 'U500'),('conc', 'f4')])

    # Grab and store sub-compound strings and relative concentrations from user input
    for i in range(n_comp):
            print(f'Compound {i+1} of {n_comp}.')
            comp = input('Enter stoichiometry: ')
            rel_conc = input('Enter relative concentration: ')
            mc_in[i] = (comp, rel_conc)

    # Total concentration for normalization
    mc_in['conc'] /= np.sum(mc_in['conc'])

    #Initialize Complete string
    S = ''

    #Parse each compound, weight with normalized concentration factor, and append to S
    for i, c in enumerate(mc_in['comp']):
        d = chemparse.parse_formula(c)

        # Weight compounds with user input
        d.update((x, np.round(y*mc_in['conc'][i],4)) for x, y in d.items())
        for ele, r in d.items():
            S += ele
            S += str(r)
    return S



print(f'Manuca - Mean Atomic Number calculator (v{version})')
print('Enter "help" to show further information. Enter "q" to quit. Enter "multi" to construct a multi-compound sample. Enter "decimals" to adjust the number of shown decimals.')
print(f'Manuca comes without any warranty for correctness. PLEASE double-check the outputs and if the input stoichiometry is read in correctly.')

decimals = 3 

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
    if(user_input == 'decimals'):
        n_decimals = int(input("Enter number of decimals to print: "))
        decimals = n_decimals

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
    Z = np.array([element.atomic_number for element in m])
    Wtpercents = np.fromiter(d_wtp.values(), dtype='float')
    Atpercents = np.fromiter(d_atp.values(), dtype='float')

    meanZ_Average = np.sum(w/n*Z) #Simple average based on atomic proportions
    meanZ_Mueller = np.sum(Z*Wtpercents) #Mueller 1954
    meanZ_SaldickAllen = np.sum(Atpercents*Z**2)/np.sum(Atpercents*Z) #Saldick and Allen 1954
    meanZ_Joyet = np.sqrt(np.sum(Atpercents*Z**2)) #Joyet 1953, Hohn und Niedrig 1972, Büchner 1973
    meanZ_Everhart = np.sum(Wtpercents*Z**2)/np.sum(Wtpercents*Z) #Everhart 1960, Joy 1995
    meanZ_Donovan_lowZ = np.sum((Atpercents*Z**0.8)/np.sum(Atpercents*Z**0.8)*Z)  #Donovan, 2003, x=0.8, low Z
    meanZ_Donovan_highZ = np.sum((Atpercents*Z**0.7)/np.sum(Atpercents*Z**0.7)*Z) #Donovan, 2003, x=0.7, high Z

    ### Electron fractions in percent, see Donovan, 2003, eq.3, https://doi.org/10.1017/S1431927603030137 
    zi = Atpercents*Z/np.sum(Atpercents*Z)
    
    ### Effective atomic number
    Zeff_Langmore = np.power(np.sum(Atpercents*Z**1.5), 2/3) # effective Z for elastic scattering, Langmore, J.P. and Wall, J. and Isaacson, M.S., Optik 38 1973
    Zeff_Egerton = np.sum(Atpercents*Z**1.3)/np.sum(Atpercents*Z**0.3) #effective Z for inelastic scattering, Egerton for EFTEM
    Aeff_Egerton = np.sum(Atpercents*aw**1.3)/np.sum(Atpercents*aw**0.3) #effective A or inelastic scattering, Egerton for EFTEM

    ### Other properties
    bse_yields = -0.0254 + 0.016*Z- 1.86*1e-4*Z**2 + 8.3*1e-7*Z**3 # Approximation for mean backscatter electron yield at 20 keV (Goldstein et al. Scanning electron microscopy and Xray microanalysis, 2018, p. 17)
    bse_yield = np.sum(bse_yields*Wtpercents)

    ### Atomic mass
    tot_atomic_mass = np.sum(w*aw)
    avg_atomic_mass = np.sum(w/n*aw)

    ### Print results
    print('Chemical formula:')
    print(chemparse.parse_formula(parse))
    print('--------------------------------')
    print('Composition:')
    print('Element\t at.%\t\t','wt.%')
    for key, value in d_atp.items():
        print(key,'\t', np.round(value*100, decimals),'\t',np.round(d_wtp[key]*100, decimals))
    print('--------------------------------')
    print('Electron fractions:')
    print('Element\t Electron fraction in %')
    for i, key in enumerate(d):
        print (key,'\t', np.round(zi[i]*100,decimals))
    print('--------------------------------')
    print('Mean atomic numbers:')
    print('--------------------------------')
    print(f'Atomic-percent average:\t{meanZ_Average:.{decimals}f}')
    print(f'Mueller (1954):\t\t{meanZ_Mueller:.{decimals}f}')
    print(f'Saldick & Allen (1954):\t{meanZ_SaldickAllen:.{decimals}f}')
    print(f'Joyet (1953):\t\t{meanZ_Joyet:.{decimals}f}')
    print(f'Everhart (1960):\t{meanZ_Everhart:.{decimals}f}')
    print(f'Donovan (2003, x=0.8):\t{meanZ_Donovan_lowZ:.{decimals}f}')
    print(f'Donovan (2003, x=0.7):\t{meanZ_Donovan_highZ:.{decimals}f}')
    print('------------------------------')
    print(f'Zeff (el, Langmore):\t{Zeff_Langmore:.{decimals}f}')
    print(f'Zeff (inel, Egerton):\t{Zeff_Egerton:.{decimals}f}')
    print('--------------------------------')
    print('Other properties:')
    print(f'Aeff (inel, Egerton):\t{Aeff_Egerton:.{decimals}f}')
    print(f'Tot. A (g/mol):\t\t{tot_atomic_mass:.{decimals}f}')
    print(f'Avg. A (g/mol):\t\t{avg_atomic_mass:.{decimals}f}')
    print(f'BSE yield @ 20 keV:\t{bse_yield:.{decimals}f}')
    print('================================\n')
