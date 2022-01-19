import pandas as pd
import re
import os
# import beutiful soup package
import bs4 as bs


# Read metadatafile of acordos
acordos = pd.read_csv('data/acordos/acordos_metadata.csv')


def formatFilename(n_solic):

    n_solic = n_solic.replace('/', '-')
    dest = 'data/acordos/'+n_solic+'.html'
    
    return dest

def checkIfDownloaded(n_solic):
    if os.path.isfile(formatFilename(n_solic)):
        return True
    else:
        return False

def getClausulas(soup):
    # Create a vector with the text of each element of soup.find_all('label', {'class' : 'tituloClausula'})	
    result = [piece.get_text() for piece in soup.find_all('label', {'class' : 'tituloClausula'} )]
    # Clean extra spaces and /n from the text
    result = [re.sub('\n', '', re.sub('\s+', ' ', piece)) for piece in result]
    # Remove empty strings from the result vector
    result = [piece for piece in result if piece != '']

    return result



def getCNPJS(soup):

    # Find the 'p'tags with attribute 'align' = 'justify' and get the text inside
    html_text = soup.find_all('p', {'align' : 'justify'})[0].get_text()
 

    # Use regular expressions to extract all sequences of numbers similar to 11.416.654/0001-17 and 00.342.957/0001-16
    cnpjs = re.findall('\d{2,3}\.\d{3}\.\d{3}\/\d{4}-\d{2}', html_text)
    return cnpjs


# Function to read the text inside one acordos html file from n_solic
def readAcordoInfo(n_solic):
        
        # Check if file was downloaded
        if checkIfDownloaded(n_solic) == False:
            # Return empty dictionary if file was not downloaded
            return {}
        
        # Read the html file
        with open(formatFilename(n_solic), 'r') as f:
            html = f.read()
        
        # Create a BeautifulSoup object
        soup = bs.BeautifulSoup(html, 'html.parser')
        
        # Get clausulas of soup
        clausulas = getClausulas(soup)

        # Get CNPJs of soup
        cnpjs = getCNPJS(soup)

        # return a dictionary with key n_solic = n_solic, and clausulas = clausulas and cnpjs = cnpjs
        return {'n_solic' : n_solic, 'clausulas' : clausulas, 'cnpjs' : cnpjs}    

        # return pd.DataFrame({'n_solic' : n_solic, 'clausulas' : clausulas, 'cnpjs' : cnpjs})
        



# Create a dataframe with the information of each acordo
acordos_info = pd.DataFrame(columns=['n_solic', 'clausulas', 'cnpjs'])


# Create a dictionary with the information of each acordo with  the key n_solic
acordos_info = {}

# Read the information of each acordo and store in the dictionary acordos_info
for n_solic in acordos['n_solic']:
    acordos_info[n_solic] = readAcordoInfo(n_solic)


# Save the dictionary
with open('data/acordos/acordos_info.json', 'w') as f:
    f.write(str(acordos_info))
    