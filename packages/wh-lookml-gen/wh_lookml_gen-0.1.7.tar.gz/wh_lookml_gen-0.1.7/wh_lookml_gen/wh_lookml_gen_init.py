import os
import yaml

dict_file = {'warehouse': {'warehouse_name': None, 'project_name': None, 'schema_name': None, 'host': None, 'port': None, 'user': None, 'password': None, 'key_file': None}}

path = os.path.expanduser('~')

profile_pass = os.path.join(path,".lookml_gen/profile.yaml")

def main():

    if not os.path.exists(profile_pass):

        with open (profile_pass, 'w') as file:
            
            documents = yaml.dump(dict_file, file)
    
if __name__ == '__main__':
    main()