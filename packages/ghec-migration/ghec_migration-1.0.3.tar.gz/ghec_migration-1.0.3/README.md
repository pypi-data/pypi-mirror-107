# Github Enterprise cloud migration tool

This tool helps you do the below tasks

## Github Migration

Migrates provided github repos from source org to target organization

#### Generate Github Personal Access Token 

- Follow the steps [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) to generate personal access token. Copy the token.
- For github enterprise cloud, the token should be enabled with SAML SSO
- Follow the steps [here](https://docs.github.com/en/github/authenticating-to-github/authenticating-with-saml-single-sign-on/authorizing-a-personal-access-token-for-use-with-saml-single-sign-on)

#### Running the tool

- Install python3 ```brew install python3```
- Store the token in an variable ```export token=<github personal access token>```
Run the below command to install the github migration tool

```pip3 install ghec-migration```

Invoke the tool by running ```ghec-migration```

Output of the tool

```shell script

➜  ~ ghec-migration
Github Migration
? What do you want to do?  Github Migration
? Source github org  nike-platform-fulfillment
? Target github org  nike-internal
? Target Team Slug  fulfillment-squad-artemis
? Team Prefix  fulfillment
? Github Username  test@nike.com
? Github access token  $token
? How do you want to get the repos?  Search by Topic
? Topic Name  artemis

```


### Jenkins Migration

We can change the github url in the bmx job using this tool

Generate a jenkins following the steps [here](https://support.cloudbees.com/hc/en-us/articles/115003090592-How-to-re-generate-my-Jenkins-user-token)

```shell script
Github Migration
? What do you want to do?  Jenkins BMX Migration
? Update Jenkins Job with new repo  Yes
? BMX Jenkins URL  https://mpartemis.jenkins.bmx.nikecloud.com/
? Jenkins Token  <jenkins token>
? Jenkins Username  <nike email id>
? New Github Url  https://github.com/nike-internal
? old Github Url  https://github.nike.com/mp-commerce-fulfillment
? Team Prefix  fulfillment
? Check the job artemis-wafflecone-cf-poc in jenkins. Is it ok to proceed?  (Use arrow keys)
 ❯ yes
   no
   don't ask me again!

```
