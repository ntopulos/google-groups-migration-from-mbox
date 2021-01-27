# Google Groups Migration from Mbox

This Python tool allows you to import the messages contained in an mbox file to an existing Google Group on Workspace for Business.


## Prerequisites

1. Enable the _Groups for Business_ in your _Google Workspace_.
2. Enable the _Groups Migration API_ in your _Google Cloud Platform_.
3. Create credentials of the _Service account_ type with _owner_ role and enable their "G Suite Domain-wide Delegation".
4. Create a JSON access key for the service account.
5. Add a Domain-wide Delegation for your service account (https://admin.google.com/ac/owl/domainwidedelegation) with the scope: `https://www.googleapis.com/auth/apps.groups.migration`


## Usage

1. Put the JSON access key in the script directory and rename it `access-ggroups.json`.

1. Put the mbox file in the script directory.

2. Install the dependencies:

       pip install

3. Run the script and follow the instructions:

       python ggroups-mbox-import.py
