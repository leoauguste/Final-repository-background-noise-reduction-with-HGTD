'''
Français
Voici le texte corrigé :

"Il faut avoir Vim pour suivre ce tutoriel.
Ce script permet de réaliser la transformation des coordonnées du système local au système global avec autant de sous-fichiers au format root que vous le souhaitez.
Imaginons que vous ayez 10 échantillons BIB stockés au format Hit dans le même dossier sur la Cernbox.
Écrivez le chemin d'accès dans "input_path".
Indiquez où vous souhaitez stocker le fichier dans "output_path". Vous pouvez changer le nom du fichier que vous stockez en modifiant la dernière instruction print. 
Personnellement, j'ajoute simplement un "Global" au début des noms de fichiers.
Exécutez le code sur votre terminal CERN et cela devrait afficher les lignes de code. Il ne vous restera plus qu'à les copier-coller ensemble lorsque vous effectuerez 
votre transformation du système local au système global.

English
You need to have vim to proceed with this tutorial. 
This script allows you to perform the transformation from Local coordinates to Global coordinates for as many root subfiles as you want to process.
Let's say you have 10 BIB samples in Hit format stored in the same folder on CERNbox. Write the access path to "input_path". 
Write where you want to save it to "output_path". You can change the name of the file you store by modifying the last print statement; I just add "Global" to the beginning of the files.
Run the code on your CERN terminal, and it should print the lines of code. Then you can copy and paste them together when you perform your local-global transformation.
'''



import subprocess
import os


input_path = '/eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Hit/'
output_path = '/eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Global/'



def get_first_10_files(folder):
    file_list = os.listdir(folder)
    return file_list

def print_text(file_list):
    for file in file_list:
        print( f" RunHitAnalysis.py  -i {input_path}{file}")
        print( f" cp SiHitAnalysis.root {output_path}Global_{file}")
    

if __name__ == '__main__':

    file_list = get_first_10_files(input_path)

    print_text(file_list)



'''
Exemple of result: 



-bash-4.2$ python3 SiHitAnalysis.py 
 RunHitAnalysis.py  -i /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Hit/s4038_000003.HIT.root
 cp SiHitAnalysis.root /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Global/Global_s4038_000003.HIT.root
 RunHitAnalysis.py  -i /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Hit/s4038_000014.HIT.root
 cp SiHitAnalysis.root /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Global/Global_s4038_000014.HIT.root
 RunHitAnalysis.py  -i /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Hit/s4038_000023.HIT.root
 cp SiHitAnalysis.root /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Global/Global_s4038_000023.HIT.root
 RunHitAnalysis.py  -i /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Hit/s4038_000054.HIT.root
 cp SiHitAnalysis.root /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Global/Global_s4038_000054.HIT.root
 RunHitAnalysis.py  -i /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Hit/s4038_000055.HIT.root
 cp SiHitAnalysis.root /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Global/Global_s4038_000055.HIT.root
 RunHitAnalysis.py  -i /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Hit/s4038_000062.HIT.root
 cp SiHitAnalysis.root /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Global/Global_s4038_000062.HIT.root
 RunHitAnalysis.py  -i /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Hit/s4038_000067.HIT.root
 cp SiHitAnalysis.root /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Global/Global_s4038_000067.HIT.root
 RunHitAnalysis.py  -i /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Hit/s4038_000085.HIT.root
 cp SiHitAnalysis.root /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Global/Global_s4038_000085.HIT.root
 RunHitAnalysis.py  -i /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Hit/s4038_000090.HIT.root
 cp SiHitAnalysis.root /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Global/Global_s4038_000090.HIT.root
 RunHitAnalysis.py  -i /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Hit/s4038_000092.HIT.root
 cp SiHitAnalysis.root /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Global/Global_s4038_000092.HIT.root
 RunHitAnalysis.py  -i /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Hit/s4038_000095.HIT.root
 cp SiHitAnalysis.root /eos/user/l/lreynaud/BIB_Sample/s4038/309680_BeamGas_20MeV/Global/Global_s4038_000095.HIT.root


'''
