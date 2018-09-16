# Bioschemas.org map2model

**map2model** is a Python module that facilitates [Bioschemas Groups](http://bioschemas.org/groups/) in the specification definition process.

**map2model** retrieves properties and Bioschemas fields (Marginality, Cardinality and Controlled Vocabularies) from Bioschemas mapping files (in the [specifications](specifications)) folder, then classifies properties into two groups:
1. **Extended properties:** Properties that are part of the extended schema.org Type.
1. **New properties:** Properties that are new to the schema.org vocabulary or are completely new to schema.org.

After classifying the properties, **map2model** generates a Markdown file that can be interpreted by Bioschemas.org's web site thereby updating the Bioschemas.org web pages.

Comments on each specification should be done through the *GitHub issues* tool within the [bioschemas repository](https://github.com/BioSchemas/bioschemas). This enables tracking, commenting on and executing of corrections.

![map2model workflow](docs/img/map2model_workflow.png)
> If you want to modify the Flow Chart open the [xml file](docs/img/map2model_workflow.xml) and name it `map2model_workflow.png` in the *doc > img*.

## Run map2model on your computer

### Requirements

Before starting, please ensure you have the following installed:
1. Git [https://git-scm.com/downloads](https://git-scm.com/downloads)
1. Python 3  [https://www.python.org/downloads/](https://www.python.org/downloads/)
1. Pip [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/)


### Executing map2model

Clone the **map2model** repository: ```git clone https://github.com/BioSchemas/map2model.git```

```bash
git clone https://github.com/BioSchemas/map2model.git
cd map2model
```

Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

If you want to add a specification, add an entry to [spec2model/configuration.yml]. This file tells map2model which specifications exist. To create a new specification, the section that you need to add includes:

```
- name: NameOfMySpec
  status: revision
  spec_type: Profile
  use_cases_url:
  version: 0.2.0
```

And importantly, the following expectations will be tested:
  1. you have created a `_NameOfMySpec` folder under [specifications](specifications)
  2. you have copied the mapping template [specifications/_templates_/Template_mapping.xlsx](specifications/_templates_/mapping.xlsx) into your `NameOfMySpec` folder and named it `NameOfMySpec_Mapping.xlsx`.
  3. You are using a correct version string (e.g., 0.2.0 and not 0.2 or v0.2, etc.)

While your specification is a draft, the name of the folder will start with an underscore (`_NameOfMySpec`). When you are done, remove the underscore (`NameOfMySpec`).

When you are finished with your spec, run the script to generate files in *map2model > docs > spec_files*. Check that your folder is present! Next, you will want to open a pull request (PR) to update the repository.

### Update specifications repository

1. Fork [Bioschemas specification repository](https://github.com/BioSchemas/specifications)
1. Clone your fork to your local computer.
1. If you added a new specification, copy the entire folder from *map2model > docs > spec_files* into the top level of the local copy of **specifications**.
1. If you changed an existing specification copy the *specification.html* file from the specification subfolder in *map2model > docs > spec_files* into the appropriate specification folder in the local **specifications** repo.
1. Check everything is OK. If it is, commit your changes. Then push to the GitHub hosted version of your fork.
1. Make a **Pull Request** of your specifications repository fork:
      - Go to the GitHub webpage and choose your fork of the main **specifications** repository.
      - Click the button called *Create new pull request*
      - Click the green button titled *Create pull request*
      - Write a simple summary of your changes in the *Write* window.
      - Click the *Create pull request* button
1. Your changes will now be manually checked to ensure they do not conflict with existing content.
1. Wait until your **Pull Request** is merged into [Bioschemas Web](https://github.com/BioSchemas/bioschemas.github.io)
      > To preserve [Bioschemas Web Page](http://bioschemas.org), changes to [bioschemas.github.io repository](https://github.com/BioSchemas/bioschemas.github.io) will be issued by Bioschemas Web Master.
1. Check your changes at [Specifications Bioschemas Web section](htt://bioschemas.org/bsc_specs)
