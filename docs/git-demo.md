# Git demo for the MLOps 2023-24 course
In this demo we will see the main features of [Git](https://git-scm.com/), a version control system.

## Git installation
Git can be installed in different ways depending on the operating system. For example, in Ubuntu you can install it with
the following command:
```bash
sudo apt install git
```

## Git configuration
Once installed, we need to configure Git with our name and email. This is important because every Git commit uses this
information, and it’s immutably baked into the commits you start creating:
```bash
git config --global user.name "John Doe"
git config --global user.email "john.doe@mail.com"
```

## Git initialization
To start using Git, we need to initialize a repository. This can be done with the following command:
```bash
git init
```
This will create a hidden folder called `.git` in the current directory. This folder contains all the information about the repository.
