server.py used to deploy the server environment, click to run it.
Input  http://127.0.0.1:5000/# in browser, enter graphic user interface of workflow-based data wrangling tool, shown in GUI.png

# Objectives

This project aims at building a guidance application to facilitate their DW process via data proﬁling methods. This guidance application will be examined in a trafﬁc data use case. It is supposed to have the ability to capture the user knowledge and interests via collecting users’ answers with respect to speciﬁc questions regarding data exploration. During this guidance process, the input of guidance application including data, domain knowledge, user explicit knowledge and history, the output of guidance application including a well transformed data with respect to a speciﬁc goal associated with the users’ interests or a skeleton of a recipe that instructs users to achieve their DW goals.

# Deliverables

In order to achieve the objectives we list for our project, some key deliverable objectives should be marked as indicators. The deliverables are enumerated as follows:

• Review the existing framework for the construction of guidance application mechanisms, analysing the feasibility of each of these frameworks for this project.

• Review the background literature in DW and data proﬁling, evaluate tools and the use of cases in these two ﬁelds that are relevant to this project.

• To carry out an investigation to identify what DW knowledge can be encoded and made available via the existing guidance Frameworks, based on previous research.

• To implement models for representation, storage, retrieval and presentation of the encoded knowledge to be used in the guidance process for guidance users on next movement and parameter prediction, based on existing technologies, models, and frameworks.

• To implement different types of data transformation that enables users to perform DW process.

• To devise and implement an algorithm that could discover suitable columns of each data transform type and predict parameters in each data transform operation.

dependencies:
    - bidict==0.21.2
    - cachelib==0.2.0
    - eventlet==0.31.0
    - flask-session==0.4.0
    - flask-socketio==5.1.0
    - h11==0.12.0
    - iniconfig==1.1.1
    - jsons==1.4.2
    - pluggy==0.13.1
    - py==1.10.0
    - pytest==6.2.4
    - python-engineio==4.2.0
    - python-socketio==5.3.0
    - simple-websocket==0.2.0
    - toml==0.10.2
    - typish==1.9.2
    - wsproto==1.0.0

# Click here to get started
![1632910949108](https://user-images.githubusercontent.com/16412949/135250964-361c913a-af4d-4fa2-b0d4-570f05b8a649.jpg)

# User interface overview
![1632911085552](https://user-images.githubusercontent.com/16412949/135251271-d1e5eb4c-bd0f-4f15-8bfd-0f75edf75345.jpg)



