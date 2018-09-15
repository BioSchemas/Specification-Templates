# Bioschemas.org map2model

**map2model** is a Python module that facilitates [Bioschemas Groups](http://bioschemas.org/groups/) in the specification definition process.

**map2model** retrieves properties and Bioschemas fields (Marginality, Cardinality and Controlled Vocabularies) from Bioschemas mapping files (in [GDrive](https://drive.google.com/drive/folders/0Bw_p-HKWUjHoNThZOWNKbGhOODg?usp=sharing)), then classifies properties into two groups:
1. **Extended properties:** Properties that are part of the extended schema.org Type.
1. **New properties:** Properties that are new to the schema.org vocabulary or are completely new to schema.org.

After classifying the properties, **map2model** generates a Markdown file that can be interpreted by Bioschemas.org's web site thereby updating the Bioschemas.org web pages.

Comments on each specification should be done through the *GitHub issues* tool within the [bioschemas repository](https://github.com/BioSchemas/bioschemas). This enables tracking, commenting on and executing of corrections.

![map2model workflow](../master/docs/img/map2model_workflow.jpg)
> If you want to modify the Flow Chart [Click here](https://drive.google.com/file/d/0B9lW_BhBep0TY3NpZ3ZxRnAySkk/view?usp=sharing) and store the result in the *doc > img* folder with the name **map2model_workflow.jpg**.

## Run map2model on your computer

### Requirements

Before starting, please ensure you have the following installed:
1. Git [https://git-scm.com/downloads](https://git-scm.com/downloads)
1. Python 3  [https://www.python.org/downloads/](https://www.python.org/downloads/)
1. Pip [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/)


### Executing map2model

1. Clone the **map2model** repository: ```git clone https://github.com/BioSchemas/map2model.git```
1. Add the [Bioschemas GDrive Folder](https://drive.google.com/open?id=0B8yXU9SkT3ftaWJtTGYyTTJjck0) to your Google Account Drive.
      > In your Google Drive Account go to **Shared with me**, right click the **Bioschemas.org** folder and select **Add to my Drive**)
1. Open the Terminal or Console application of your Operating System and go to the folder where you cloned the **map2model** repository.
1. Modify the *spec2model > configuration.yml* file in your cloned repository (configuration.yml tells map2model which specifications exist and where information on them can be found).
      > If you need help to modify the configuration.yml file, please refer to the *Adding new specifications* section later in this readme.
1. Install Python dependencies using the command ```pip3 install -r requirements.txt```.
1. Run the map2model module by executing the command ```python3 run.py```.
1. After executing the ```run.py``` command a web browser will ask for a Google Account authentication. **Log in using the account you used for step 2.**
1. Once complete, the specifications can be found in a subfolder inside *map2model > spec2model* folder. There should be a folder for each specification listed in ```configuration.yml```.

### Update specifications repository

1. Fork [Bioschemas specification repository](https://github.com/BioSchemas/specifications)
1. Clone your fork to your local computer.
1. If you added a new specification, copy the entire folder from *map2model > spec2model* into the top level of the local copy of **specifications**.
1. If you changed an existing specification copy the *specification.html* file from the specification subfolder in *map2model > spec2model* into the appropriate specification folder in the local **specifications** repo.
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

****
## Advanced user's documentation

### Adding new specifications

If you have created a new specification (or a specification is missing from the 
*[map2model](https://github.com/BioSchemas/map2model) > docs > specification_md_files* folder) 
you will need to extend the *[map2model](https://github.com/BioSchemas/map2model) > spec2model > configuration.yml* file.

If you are unfamiliar with yaml, please read [http://yaml.org/](http://yaml.org/).

1. Open the *[map2model](https://github.com/BioSchemas/map2model) > spec2model > [configuration.yml](https://github.com/BioSchemas/map2model/blob/master/spec2model/configuration.yml)* file.
1. Erase all the file content and start the ```.yml``` file with
```
specifications:
```
1. Add the following yaml structure per each specification:
```
  - name :
    g_folder:
    g_mapping_file:
    status: revision
    spec_type: Profile
    use_cases_url:
    version: 0.0.1
```
      - Please be careful with spacing, as it is important in YAML!
1. Apart from *use_case_url* all fields must have a value:
      - *name* is the name of the specification
      - *g_folder* is the name of the gDocs folder in which the new specification exists. E.g., a *Tool* specification will be found in the **Tool** folder (i.e., *gDrive > BioSchemas.org > Specifications > Tool*).
      - *g_mapping_file* : in the *g_folder* you should have a mapping file based on the [original template](https://docs.google.com/spreadsheets/d/1OMBiB8SXiRe1b3Cl91IuNlHbJ9_UXHg8B-GY0MYRSaY/edit?usp=sharing). Write the name of the mapping file here, e.g., **Tool Mapping**.
      - *use_cases_url* : in the *g_folder* you may have a use case document. If it exists, paste a link to it here.
1. Re-run ```python3 run.py```. Your new markdown files should be in the *bioschemas-map2model > docs > specification_md_files* folder.

### Create your own client_secrets.json

**map2model** can work with the generic client_secrets file, but here you have the process to create your own json. It is unlikely you will ever need to do this, but the instructions remain for completeness.

##### Create a new Google's APIs Project and add Google Drive API Client:
- Go to [Google's APIs Console](https://console.developers.google.com/iam-admin/projects) and create your own project. Call it whatever you want.
- You will need to wait for a few moments while Google creates the project. Refresh the page and you should see your new project listed.
- Click on the **Google APIs** logo (top left of screen). If you have existing projects, select the new one in the dropdown box next to the Google APIs logo.
- Under **G Suite APIs** you will see **Drive API**. Click on it.
- On the next page, click on **Enable**
- You should see a yellow warning at the top of the page informing you of the need for credentials. Do **not** click the create credentials button at the right of this warning. Instead click the **key icon** in the left menu bar.
- In the new dialog box there is a dropdown called **create credentials**... choose **OAuth client ID**.
- A form with radio buttons will appear, but it is greyed out and you cannot select anything. Instead click the blue  **Configure consent screen** button on the right.
- In the new form enter whatever **product name** you wish and click **save**.
- You will be returned to the form with radio buttons; select **Web application**.
- In the text box called 'Authorised Javascript origins' type http://localhost:8080 (notice the lack of a trailing slash)
- In the text box called 'Authorised redirect URIs' type http://localhost:8080/ (notice the trailing slash)
- Click **create** then **OK**.
- You will be on a page called 'Credentials' which has a table with the name of your new app. At the far right you will see a download icon (an arrow pointing down, above a line). Clicking on this allows you to download your credentials.
- The downloaded file will have a very long name, e.g., *client_secret_896441073116-l0karljg25m6uvss45t48ufb9d7u3kku.apps.googleusercontent.com*. Change the name to **client_secrets.json** and move it to the top level of your cloned **bioschemas-map2model** repository.
