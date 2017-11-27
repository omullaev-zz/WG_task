# WG_task

## Requirements

```
python 2.7.10
 ```
 
## Tutorial MacOS

```bash
# Download sqlite artefact
wget https://www.sqlite.org/snapshot/sqlite-${VERSION}.tar.gz

# Extract artefact
tar -xzf sqlite-${VERSION}.tar.gz && cd sqlite-${VERSION}

# Local deploy 
./configure; make

# Install pip
easy_install pip

# Use a virtual python environment
# You may want to add 'source ~/wg_env/bin/activate' 
# to the bottom of your .bash_profile to always run in this environment.
pip install virtualenv
virtualenv ~/wg_env
source ~/wg_env/bin/activate

# Install required modules
pip install -r requirements.txt

# run tests
nosetests test.py --with-html --html-report=report.html

# view report
open report.html in browser
```