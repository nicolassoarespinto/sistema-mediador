import pandas as pd
import os
import urllib.request
import time

### PARAMETERS ####
replace = False 
verbose = False

###################

# Function to create URL to download the html file
def GetURLmediador(n_solic):
    url = 'http://www3.mte.gov.br/sistemas/mediador/Resumo/ResumoVisualizar?NrSolicitacao='+ n_solic
    return url


def formatFilename(n_solic):

    n_solic = n_solic.replace('/', '-')
    dest = 'data/acordos/'+n_solic+'.html'
    
    return dest

# Function to check if file is already downloaded
def checkIfDownloaded(n_solic):
    if os.path.isfile(formatFilename(n_solic)):
        return True
    else:
        return False


###################


if __name__ == '__main__':

    # Create a folder to save the html files with acordos information
    os.makedirs('data/acordos', exist_ok=True)

    # Clear the content of '/data/acordos'
    if(replace == True):
        os.system('rm -rf data/acordos/*.html')

    # Import the html file
    wb = pd.read_html("InstrumentoColetivoFiliacao.xls")


    # Convert acordos into DataFrame
    acordos = pd.DataFrame(wb[1])

    # Rename columns of acordos to ['n_registro, n_processo, n_solic, 'tipo', 'vigencia', 'trabalhador', empregador']
    acordos.columns = ['n_registro', 'n_processo', 'n_solic', 'tipo', 'vigencia', 'trabalhador', 'empregador']

    # Save db with cleaned acordos metadata into acordos_metadata.csv
    acordos.to_csv('data/acordos/acordos_metadata.csv', index=False)

    print('Number of acordos: ', len(acordos))
    print("Acordos metadata saved in 'data/acordos/acordos_metadata.csv'")


    #Add a column to acordos with an indication if the file was already downloaded
    acordos['downloaded'] = acordos['n_solic'].apply(checkIfDownloaded)

    # Count how many files were already downloaded
    n_downloaded = acordos[acordos['downloaded'] == True].shape[0]


    # Print number of acordos that will be downloaded 
    print('Number of acordos already downloaded:', n_downloaded)


    # Print message with number of acordos left to be downloaded
    print('Number of acordos to be downloaded:', len(acordos)-n_downloaded)

    # Message that the program will start downloading the files
    print('Starting download of acordos...')

    # Loop through the acordos DataFrame and create a URL to download the html file
    for index, row in acordos.iterrows():

        if(verbose == True):
            print(row['n_solic'],":", row['downloaded'])

        if(row['downloaded'] == False):

            url = GetURLmediador(row['n_solic'])

            # Format the filename to save the html file
            dest = formatFilename(row['n_solic'])

            try:
                # Download the html file into data/acordos folder
                urllib.request.urlretrieve(url, dest)
            except:
                pass
            
            # Sleep for 10 seconds
            time.sleep(10)


    # Print message that the program finished downloading the files
    print('Finished downloading acordos.')




