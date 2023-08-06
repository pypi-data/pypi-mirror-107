import subprocess
from bs4 import BeautifulSoup
import pathlib
from pathlib import Path
from urllib.parse import unquote, quote

class Nextcloud():
    def __init__(self, server , username, password, webdav_token):
        self.server = server
        self.username = username
        self.password = password
        self.webdav_token = webdav_token
        
    def list_dir(self, path):
        xml = subprocess.check_output(
            f'curl -X PROPFIND -H "Depth: 1" -u {self.username}:{self.password} {self.server}{self.webdav_token}/{quote(path)}'.split()
        )
        soup = BeautifulSoup(xml, 'lxml') 
        
        if soup.find('d:error'):
            print(soup.find('s:message').text)
        
        for item in soup.find_all('d:response'):
            print(
                unquote(item.find('d:href').text.split(self.webdav_token)[1]),
                item.find('d:getlastmodified').text)

    def make_dir(self, path):
        xml = subprocess.check_output(
            f'curl -u {self.username}:{self.password} -X MKCOL {self.username}:{self.password} {self.server}{self.webdav_token}/{path}'.split()
        )
        soup = BeautifulSoup(xml, 'lxml')
        if soup.find('d:error'):
            print(soup.find('s:message').text)
            
        
    def download_file(self, path, filename, target_dir):
        binary = self.read_file(path, filename)
            
        p = Path(target_dir)
        p.mkdir(parents=True, exist_ok=True)
        p = p.joinpath(filename)
        with open(p, 'wb') as file:
            file.write(binary)
        
        
    def read_file(self, path, filename):
        p = Path(path).joinpath(filename)
        binary = subprocess.check_output(f'curl -X GET -u {self.username}:{self.password} {self.server}{self.webdav_token}/{quote(str(p))}'.split())
        if r'<s:exception>Sabre\\DAV\\Exception\\NotFound</s:exception>' in str(binary):
            soup = BeautifulSoup(binary, 'lxml')
            print(soup.find('s:message').text)
        return binary
    
    
    def upload_file(self, local_file, path, filename):
        p = Path(path).joinpath(filename)
        xml = subprocess.check_output(f'curl -u {self.username}:{self.password} -T {local_file} {self.server}{self.webdav_token}/{quote(str(p))}'.split())
        soup = BeautifulSoup(xml, 'lxml')
        if soup.find('d:error'):
            print(soup.find('s:message').text)
    
    
    def delete_file(self, path):
        if path is None or path == '' or path ==' ':
            print('Do not delete the root dir!')
            return
        xml = subprocess.check_output(f'curl -u {self.username}:{self.password} -X DELETE {self.server}{self.webdav_token}/{quote(path)}'.split())
        soup = BeautifulSoup(xml, 'lxml')
        if soup.find('d:error'):
            print(soup.find('s:message').text)