# Zephyr

Zephyr is a command-line utility that provides project and component scaffolding to build modular pipelines.


## What is Zephyr

Zephyr allows you to quickly bootstrap boilerplate code at the project **and** module level by leveraging  
[cookiecutter](https://github.com/cookiecutter/cookiecutter). Zephyr also provides a way to bootstrap modular pipelines by converting a list of modules into a [Metaflow](https://github.com/Netflix/metaflow) pipeline. 

## Using Zephyr

Getting up and running with Zephyr is easy

### Installing Zephyr

Install zephyr from [pypi]()

```
pip install zephyr_bootstrap 
```

### Bootstrap project

To start simply use zephyr init

```
zephyr init
```

Follow the prompts to create a sample project

```
2021-05-25 21:38:16,467 | INFO : initializing project... 
app_name [my_project]: 
desc [My project Description]: 
Project my_project created
```

The project comes ready with a loaded Makefile, example notebook, and everything to build a library package. 

```
ls my_project/
data  docker-compose.yml  docs  Makefile  my_project  notebooks  pipelines  README.md  requirements.txt  setup.py  tests  VERSION
```

#### Custom template

You can also use custom cookiecutters to bootstrap a project

```
zephyr init --custom https://github.com/drivendata/cookiecutter-data-science
```

### Create Module

Once a project is created, you can create a new module using...

```
zephyr module create
```

Follow the prompts to bootstap a module

```
2021-05-25 21:40:44,452 | INFO : Creating module...
module_name [my_module]: 
desc [My module description]: 
project_name [my_project]: 
Module my_module created
```

The module comes ready with a buildable docker image, example script, and sample proccesing code. 

```
ls my_project/modules/my_module/
build_docker.sh  controller.py  Dockerfile  example.py  __init__.py  linux_packages.txt  README.md  requirements.txt  sample_inputs  sample_outputs  tests

```

#### Custom template

You can also use custom cookiecutters to bootstrap a module

```
zephyr module create --custom https://github.com/audreyfeldroy/cookiecutter-pypackage
```

#### Delete module

Can remove a module using...

```
zephyr module delete
```

Follow promopts to remove module

```
Current modules: ['my_module']
Type module to delete: my_module
Do you want to delete my_module [y/N]: y
2021-05-25 21:43:27,450 | INFO : Deleting module...my_module
Module my_module deleted

```

### Pipeline

Can create a modular pipeline using

```
zephyr pipeline create
```

Select what modules you want, by following the prompts

```
2021-05-25 21:53:59,024 | INFO : Creating pipeline...
Current modules: ['my_module', 'test_mod', 'mod_1', 'mod_2']
Enter comma sepearted modules for pipeline: mod_1,mod_2,my_module
Do you want to continue? with these modules: ['mod_1', 'mod_2', 'my_module'] [Y/n]: 
pipeline_name [my_pipeline]: 
Pipeline created
Test with...
python pipelines/my_pipeline/my_pipeline_pipeline.py run
```

The bootstrapped pipeline is ready to run.

```
Metaflow 2.2.8 executing My_pipelineFlow for user:banjtheman
Validating your flow...
    The graph looks good!
Running pylint...
    Pylint is happy!
2021-05-25 21:54:27.950 Workflow starting (run-id 1621994067931797):
2021-05-25 21:54:27.955 [1621994067931797/start/1 (pid 29700)] Task is starting.
2021-05-25 21:54:28.779 [1621994067931797/start/1 (pid 29700)] 2021-05-25 21:54:28,779 |INFO: Start step
2021-05-25 21:54:28.864 [1621994067931797/start/1 (pid 29700)] Task finished successfully.
2021-05-25 21:54:28.868 [1621994067931797/mod_1_step/2 (pid 29708)] Task is starting.
2021-05-25 21:54:29.519 [1621994067931797/mod_1_step/2 (pid 29708)] 2021-05-25 21:54:29,519 |INFO: Starting module mod_1
2021-05-25 21:54:29.604 [1621994067931797/mod_1_step/2 (pid 29708)] Task finished successfully.
2021-05-25 21:54:29.609 [1621994067931797/mod_2_step/3 (pid 29716)] Task is starting.
2021-05-25 21:54:30.335 [1621994067931797/mod_2_step/3 (pid 29716)] 2021-05-25 21:54:30,334 |INFO: Starting module mod_2
2021-05-25 21:54:30.427 [1621994067931797/mod_2_step/3 (pid 29716)] Task finished successfully.
2021-05-25 21:54:30.432 [1621994067931797/my_module_step/4 (pid 29724)] Task is starting.
2021-05-25 21:54:31.081 [1621994067931797/my_module_step/4 (pid 29724)] 2021-05-25 21:54:31,081 |INFO: Starting module my_module
2021-05-25 21:54:31.178 [1621994067931797/my_module_step/4 (pid 29724)] Task finished successfully.
2021-05-25 21:54:31.183 [1621994067931797/end/5 (pid 29732)] Task is starting.
2021-05-25 21:54:31.863 [1621994067931797/end/5 (pid 29732)] 2021-05-25 21:54:31,862 |INFO: Job's done
2021-05-25 21:54:31.953 [1621994067931797/end/5 (pid 29732)] Task finished successfully.
2021-05-25 21:54:31.953 Done!
```
