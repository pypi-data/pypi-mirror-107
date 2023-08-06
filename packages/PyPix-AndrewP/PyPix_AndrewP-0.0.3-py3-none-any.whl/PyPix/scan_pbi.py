import glob as gl
import os
import shutil
import zipfile
import json
import argparse


def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)    
    return allFiles

def pointPbixByTable (table_name, pbix_folder):
    print ('Scan in  : ', pbix_folder)
    print ('for table: ', table_name)
    if os.path.exists('temp_pbix_scan'): 
        shutil. rmtree('temp_pbix_scan')
    pbixs = [i for i in getListOfFiles(pbix_folder) if 'pbix' in i]
    os.mkdir('temp_pbix_scan')
    for pbix in pbixs:
        new_zip = 'temp_pbix_scan\\{pbix}'.format(pbix = os.path.basename(pbix).replace('pbix', 'zip'))
        pbix_metadata = 'temp_pbix_scan\\{pbix}'.format(pbix = os.path.basename(pbix).replace('pbix', 'json'))
        shutil.copy(pbix, new_zip)

        with zipfile.ZipFile(new_zip) as zip_file:
            source = zip_file.open(DiagramLayout)
            target = open(pbix_metadata, "wb")
            with source, target:
                shutil.copyfileobj(source, target)
            with open(pbix_metadata, "r", encoding='utf_16_le') as json_file:
                data = json.load(json_file)
                if table_name in data['diagrams'][0]['tables']:
                    print (pbix)
    shutil. rmtree('temp_pbix_scan')

def pointPbixByColumn (column_name, pbix_folder):
    print ('Scan in  : ', pbix_folder)
    print ('for column: ', column_name)
    if os.path.exists('temp_pbix_scan'): 
        shutil.rmtree('temp_pbix_scan')
    pbixs = [i for i in getListOfFiles(pbix_folder) if 'pbix' in i]
    os.mkdir('temp_pbix_scan')
    for pbix in pbixs:
        new_zip = 'temp_pbix_scan\\{pbix}'.format(pbix = os.path.basename(pbix).replace('pbix', 'zip'))
        pbix_metadata = 'temp_pbix_scan\\{pbix}'.format(pbix = os.path.basename(pbix).replace('pbix', 'json'))
        shutil.copy(pbix, new_zip)

        with zipfile.ZipFile(new_zip) as zip_file:
            source = zip_file.open('Report/Layout')
            target = open(pbix_metadata, "wb")
            with source, target:
                shutil.copyfileobj(source, target)
            with open(pbix_metadata, "r", encoding='utf_16_le') as json_file:
                select_queries = [json.loads(d['query'])['Commands'][0]['SemanticQueryDataShapeCommand']['Query']['Select']  for d in json.load(json_file)['sections'][0]['visualContainers'] if 'query' in d]
                for query in select_queries:
                    if column_name in [d['Name'] for d in query if 'Column' in d]:
                        print (pbix)
    shutil. rmtree('temp_pbix_scan')


def pointPbixByMeasure (Measure_name, pbix_folder):
    print ('Scan in  : ', pbix_folder)
    print ('for column: ', Measure_name)
    if os.path.exists('temp_pbix_scan'): 
        shutil.rmtree('temp_pbix_scan')
    pbixs = [i for i in getListOfFiles(pbix_folder) if 'pbix' in i]
    os.mkdir('temp_pbix_scan')
    for pbix in pbixs:
        new_zip = 'temp_pbix_scan\\{pbix}'.format(pbix = os.path.basename(pbix).replace('pbix', 'zip'))
        pbix_metadata = 'temp_pbix_scan\\{pbix}'.format(pbix = os.path.basename(pbix).replace('pbix', 'json'))
        shutil.copy(pbix, new_zip)

        with zipfile.ZipFile(new_zip) as zip_file:
            source = zip_file.open('Report/Layout')
            target = open(pbix_metadata, "wb")
            with source, target:
                shutil.copyfileobj(source, target)
            with open(pbix_metadata, "r", encoding='utf_16_le') as json_file:
                select_queries = [json.loads(d['query'])['Commands'][0]['SemanticQueryDataShapeCommand']['Query']['Select']  for d in json.load(json_file)['sections'][0]['visualContainers'] if 'query' in d]
                for query in select_queries:
                    if Measure_name in [d['Name'] for d in query if 'Measure' in d]:
                        print (pbix)
    shutil. rmtree('temp_pbix_scan')


def pointPbixByRelativeText (relative_text, pbix_folder):
    print ('Scan in  : ', pbix_folder)
    print ('for relative_text: ', relative_text)
    if os.path.exists('temp_pbix_scan'): 
        shutil.rmtree('temp_pbix_scan')
    pbixs = [i for i in getListOfFiles(pbix_folder) if 'pbix' in i]
    os.mkdir('temp_pbix_scan')
    for pbix in pbixs:
        new_zip = 'temp_pbix_scan\\{pbix}'.format(pbix = os.path.basename(pbix).replace('pbix', 'zip'))
        pbix_metadata = 'temp_pbix_scan\\{pbix}'.format(pbix = os.path.basename(pbix).replace('pbix', 'json'))
        shutil.copy(pbix, new_zip)

        with zipfile.ZipFile(new_zip) as zip_file:
            source = zip_file.open('Report/Layout')
            target = open(pbix_metadata, "wb")
            with source, target:
                shutil.copyfileobj(source, target)
            with open(pbix_metadata, "r", encoding='utf_16_le') as json_file:
                if relative_text in json_file.read():
                    print (pbix)
    shutil. rmtree('temp_pbix_scan')



def main():
    parser = argparse.ArgumentParser(description='Parse in repo contain pbix and a table to scan')
    parser.add_argument('--repo', dest='pbix_folder', help='repo contain power bi')
    parser.add_argument('--relative_text', dest='relative_text', help='relative_text to be scanned')
    args = parser.parse_args()
    pointPbixByRelativeText(relative_text = args.pbix_folder, pbix_folder= args.relative_text)
    
    
if __name__ == "__main__":
    main()


