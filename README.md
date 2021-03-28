# filesystem_ops

Description
-----------
Autotests for basic filesystem operations

This package has been tested with Python3.9+ and pytest 6.2.2

How to install
-------------
* Clone the Git repository
  
via HTTPS:
```shell
git clone https://github.com/mnakhaev/filesystem_ops.git
```

via SSH:
```shell
git clone git@github.com:mnakhaev/filesystem_ops.git
```

* Initialize new virtual environment

```shell
cd filesystem_ops
python -m venv venv
source venv/bin/activate
```

* Install requirements
```shell
pip install -r requirements.txt
```

How to run
----------
Set correct PYTHONPATH (assuming that you are in workspace):
```
export PYTHONPATH=$PYTHONPATH:.
```

Run the full tests scope:
```shell
pytest .
```

Run the tests in multiple threads (to be supported):
```shell
pytest . -n <THREADS_NUM>
```

Use custom *.ini config for development/debugging:
```shell
pytest . -c pytest.dev.ini
```