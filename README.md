SMART-on-FHIR Genomics API Sandbox deploy tutorial

## Preface

This readme will cover basic process on how to deploy this server from 
a clean-new environment. Although it is tested only in **Ubuntu**, for linux
and Mac OS user, this will be no hard to run this server

**For Windows user, unfortunately, some part in this server, especially 
the pysam package of python, cannot run on Windows environment.**

## How to use it

### Preliminary environment check

1. The quickest way to install python package in this server is using pip:

	```
    # python 2.7
	# this might require previledge (e.g. sudo)
	# or use virtualenv instead (recommended)
	$ pip install -r requirements.txt
	```
	
    However, some part cannot build successfully , in that case , run this command:
    ```
    $ sudo apt-get install python-dev libpq-dev libxml2-dev libxslt1-dev
    ```
    
    
2. Edit `config.py`. Fill in settings for database, host, etc. as you desire. See comments in `config.py` for detailed instructions.

    * postgresql. If you want to use postgresql, check setup_db.py and install posegresql by yourself. You need
to set up PGUSERNAME ,PGPASSWORD , and DBNAME in config.py

    * sqlite (no postgresql). That's the default settings now. Just do not change APP_CONFIG['SQLALCHEMY_DATABASE_URI']

    * Mysql (Not tested)


3. Optional: load your version of FHIR spec.

#### before DSTU2:

run the script `load_spec.py`, which will update `fhir/fhir_spec.py`. Please read comments in `load_spec.py` carefully before using it.
   The specification for Connectathon 11 can be downloaded at: http://www.hl7.org/fhir/2016Jan/downloads.html

#### for STU3:

run the script `load_spec_STU3.py`,  which will update `fhir/fhir_spec.py`. Please read comments in `load_spec_STU3.py` carefully before using it.
  The specification for STU3 Ballot version can be downloaded at: http://www.hl7.org/fhir/2016Sep/downloads.html

4. Load sample data with

	```
	$ python load_example.py
	```

### Usage of this server
5. Now you can use `flask`'s debug instance like this to test your sandbox server

    ```
	$ python server.py run --debug
	```

6. To wipe out the database (for debugging or whatever reason), do

	```
	$ python server.py clear
	```

### How to deploy the server

7. Simply deploy by `gunicorn` , try it with parameter 'run' as follows:

	```
	$ python server.py run
	```

### How to create account and authorize the apps 

To be continued

If you find this useful, please cite the following paper:
Alterovitz G, Warner J, Zhang P, Chen Y, Ullman-Cullere M, Kreda D,
Kohane IS. SMART on FHIR Genomics: facilitating standardized
clinico-genomic apps. Journal of the American Medical Informatics Association:
JAMIA. 2015;22(6):1173-8. doi: 10.1093/jamia/ocv045. PubMed PMID: 26198304.
http://www.ncbi.nlm.nih.gov/pubmed/26198304

For more information (including papers, slides, videos, and tutorials on getting started), please email Gil Alterovitz at ga@alum.mit.edu
