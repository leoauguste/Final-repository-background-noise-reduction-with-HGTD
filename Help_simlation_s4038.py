'''
Français
Vous devez avoir Vim pour suivre ce tutoriel. 
Ce script permet de créer le fichier run_s4038.sh avec autant de sous-fichiers root à traiter que vous le souhaitez. 
Imaginons que vous ayez 10 échantillons BIB au format EVNT stockés dans le même dossier sur la Cernbox. 
Écrivez le chemin d'accès du dossier sur "input_path". 
Écrivez le chemin d'accès du dossier où vous souhaitez le stocker sur "output_path". 
output_name1, num_list, output_name2 servent à la création du nom des sorties. 
Créez un fichier run_s4038.sh sur votre terminal CERN, lancez le code simulation_s4038.py au même endroit que le fichier .sh et cela remplira automatiquement votre fichier .sh.

Anglais
You need to have vim to proceed with this tutorial. 
This script allows you to create the file "run_s4038.sh" with as many sub-files in the root format to process as you want. 
Let's assume you have 10 samples in the BIB format named EVNT stored in the same folder on Cernbox.
Write the path to access the input folder as "input_path". 
Write the path to access the folder where you want to store the output as "output_path". 
"output_name1", "num_list", and "output_name2" are used to create the names of the output files.
To use this, create a file named "run_s4038.sh" on your CERN terminal, then run the "simulation_s4038.py" code in the same location as the ".sh" file. This will automatically populate your ".sh" file with the required content.
'''



import subprocess
import os


input_path = '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/'
output_path = ' /eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/Hit/'
output_name1 = 'BeamHaloB1_20MeV'
output_name2 = '.HIT.root'
filename = 'run_s4038.sh'
num_list = []

def open_file_with_vim(filename):
    subprocess.call(['vim', filename])

def get_files(folder):
    file_list = os.listdir(folder)
    num_list = [item.split('_')[1].split('.')[1] for item in file_list]
    return file_list, num_list

def fill_file_with_text(filename, file_list,num_list ):
    new_text = ""
    for file, num in zip(file_list,num_list):
        new_text += f"Sim_tf.py --CA 'all:True' --conditionsTag 'default:OFLCOND-MC15c-SDR-14-05' --geometryVersion 'default:ATLAS-P2-RUN4-01-01-00' --multithreaded 'True' --postInclude 'default:PyJobTransforms.UseFrontier' --preExec 'ConfigFlags.HGTD.Geometry.useGeoModelXml = True' --preInclude 'EVNTtoHITS:Campaigns.PhaseIISimulation' --simulator 'FullG4MT_QS'  --inputEVNTFile '{input_path}{file}' --outputHITSFile '{output_path}{output_name1}{num}{output_name2}'\n"
    
    with open(filename, 'w') as file:
        file.write(new_text)


if __name__ == '__main__':

    file_list, num_list = get_files(input_path)

    fill_file_with_text(filename, file_list, num_list)



'''
Exemple of result:

Sim_tf.py --CA 'all:True' --conditionsTag 'default:OFLCOND-MC15c-SDR-14-05' --geometryVersion 'default:ATLAS-P2-RUN4-01-01-00' --multithreaded 'True' --postInclude 'default:PyJobTransforms.UseFrontier' --preExec 'ConfigFlags.HGTD.Geometry.useGeoModelXml = True' --preInclude 'EVNTtoHITS:Campaigns.PhaseIISimulation' --simulator 'FullG4MT_QS'  --inputEVNTFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/EVNT.13330069._000021.pool.root.1' --outputHITSFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/1BeamHalo20MeV.HIT.root'
Sim_tf.py --CA 'all:True' --conditionsTag 'default:OFLCOND-MC15c-SDR-14-05' --geometryVersion 'default:ATLAS-P2-RUN4-01-01-00' --multithreaded 'True' --postInclude 'default:PyJobTransforms.UseFrontier' --preExec 'ConfigFlags.HGTD.Geometry.useGeoModelXml = True' --preInclude 'EVNTtoHITS:Campaigns.PhaseIISimulation' --simulator 'FullG4MT_QS'  --inputEVNTFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/EVNT.13330069._000057.pool.root.1' --outputHITSFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/2BeamHalo20MeV.HIT.root'
Sim_tf.py --CA 'all:True' --conditionsTag 'default:OFLCOND-MC15c-SDR-14-05' --geometryVersion 'default:ATLAS-P2-RUN4-01-01-00' --multithreaded 'True' --postInclude 'default:PyJobTransforms.UseFrontier' --preExec 'ConfigFlags.HGTD.Geometry.useGeoModelXml = True' --preInclude 'EVNTtoHITS:Campaigns.PhaseIISimulation' --simulator 'FullG4MT_QS'  --inputEVNTFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/EVNT.13330069._000060.pool.root.1' --outputHITSFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/3BeamHalo20MeV.HIT.root'
Sim_tf.py --CA 'all:True' --conditionsTag 'default:OFLCOND-MC15c-SDR-14-05' --geometryVersion 'default:ATLAS-P2-RUN4-01-01-00' --multithreaded 'True' --postInclude 'default:PyJobTransforms.UseFrontier' --preExec 'ConfigFlags.HGTD.Geometry.useGeoModelXml = True' --preInclude 'EVNTtoHITS:Campaigns.PhaseIISimulation' --simulator 'FullG4MT_QS'  --inputEVNTFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/EVNT.13330069._000062.pool.root.1' --outputHITSFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/4BeamHalo20MeV.HIT.root'
Sim_tf.py --CA 'all:True' --conditionsTag 'default:OFLCOND-MC15c-SDR-14-05' --geometryVersion 'default:ATLAS-P2-RUN4-01-01-00' --multithreaded 'True' --postInclude 'default:PyJobTransforms.UseFrontier' --preExec 'ConfigFlags.HGTD.Geometry.useGeoModelXml = True' --preInclude 'EVNTtoHITS:Campaigns.PhaseIISimulation' --simulator 'FullG4MT_QS'  --inputEVNTFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/EVNT.13330069._000074.pool.root.1' --outputHITSFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/5BeamHalo20MeV.HIT.root'
Sim_tf.py --CA 'all:True' --conditionsTag 'default:OFLCOND-MC15c-SDR-14-05' --geometryVersion 'default:ATLAS-P2-RUN4-01-01-00' --multithreaded 'True' --postInclude 'default:PyJobTransforms.UseFrontier' --preExec 'ConfigFlags.HGTD.Geometry.useGeoModelXml = True' --preInclude 'EVNTtoHITS:Campaigns.PhaseIISimulation' --simulator 'FullG4MT_QS'  --inputEVNTFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/EVNT.13330069._000096.pool.root.1' --outputHITSFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/6BeamHalo20MeV.HIT.root'
Sim_tf.py --CA 'all:True' --conditionsTag 'default:OFLCOND-MC15c-SDR-14-05' --geometryVersion 'default:ATLAS-P2-RUN4-01-01-00' --multithreaded 'True' --postInclude 'default:PyJobTransforms.UseFrontier' --preExec 'ConfigFlags.HGTD.Geometry.useGeoModelXml = True' --preInclude 'EVNTtoHITS:Campaigns.PhaseIISimulation' --simulator 'FullG4MT_QS'  --inputEVNTFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/EVNT.13330069._000100.pool.root.1' --outputHITSFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/7BeamHalo20MeV.HIT.root'
Sim_tf.py --CA 'all:True' --conditionsTag 'default:OFLCOND-MC15c-SDR-14-05' --geometryVersion 'default:ATLAS-P2-RUN4-01-01-00' --multithreaded 'True' --postInclude 'default:PyJobTransforms.UseFrontier' --preExec 'ConfigFlags.HGTD.Geometry.useGeoModelXml = True' --preInclude 'EVNTtoHITS:Campaigns.PhaseIISimulation' --simulator 'FullG4MT_QS'  --inputEVNTFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/EVNT.13330069._000121.pool.root.1' --outputHITSFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/8BeamHalo20MeV.HIT.root'
Sim_tf.py --CA 'all:True' --conditionsTag 'default:OFLCOND-MC15c-SDR-14-05' --geometryVersion 'default:ATLAS-P2-RUN4-01-01-00' --multithreaded 'True' --postInclude 'default:PyJobTransforms.UseFrontier' --preExec 'ConfigFlags.HGTD.Geometry.useGeoModelXml = True' --preInclude 'EVNTtoHITS:Campaigns.PhaseIISimulation' --simulator 'FullG4MT_QS'  --inputEVNTFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/EVNT.13330069._000135.pool.root.1' --outputHITSFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/9BeamHalo20MeV.HIT.root'
Sim_tf.py --CA 'all:True' --conditionsTag 'default:OFLCOND-MC15c-SDR-14-05' --geometryVersion 'default:ATLAS-P2-RUN4-01-01-00' --multithreaded 'True' --postInclude 'default:PyJobTransforms.UseFrontier' --preExec 'ConfigFlags.HGTD.Geometry.useGeoModelXml = True' --preInclude 'EVNTtoHITS:Campaigns.PhaseIISimulation' --simulator 'FullG4MT_QS'  --inputEVNTFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/EVNT.13330069._000152.pool.root.1' --outputHITSFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/10BeamHalo20MeV.HIT.root'
Sim_tf.py --CA 'all:True' --conditionsTag 'default:OFLCOND-MC15c-SDR-14-05' --geometryVersion 'default:ATLAS-P2-RUN4-01-01-00' --multithreaded 'True' --postInclude 'default:PyJobTransforms.UseFrontier' --preExec 'ConfigFlags.HGTD.Geometry.useGeoModelXml = True' --preInclude 'EVNTtoHITS:Campaigns.PhaseIISimulation' --simulator 'FullG4MT_QS'  --inputEVNTFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/EVNT.13330069._000173.pool.root.1' --outputHITSFile '/eos/user/l/lreynaud/BIB_Sample/mc15_13TeV.309681.BeamHaloGenerator_BeamHaloB1_20MeV.evgen.EVNT.e6513/11BeamHalo20MeV.HIT.root'


'''
