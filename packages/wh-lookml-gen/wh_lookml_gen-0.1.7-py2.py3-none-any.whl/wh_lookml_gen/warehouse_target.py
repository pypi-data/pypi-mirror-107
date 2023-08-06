import os
import yaml


path = os.path.expanduser('~')

profile_pass = os.path.join(path,".lookml_gen/profile.yaml")

with open(profile_pass) as f:
    lookml_config = yaml.load(f, Loader=yaml.FullLoader)

##global vars

project_name =  lookml_config['warehouse']['project_name']
schema_name =  lookml_config['warehouse']['schema_name']

## warehouse schema


warehouse_schema =   """

with source as (

    select * from `{0}.{1}.INFORMATION_SCHEMA.COLUMNS`

    )

    select * from source

""".format(project_name,schema_name)


