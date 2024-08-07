# Git demo<!-- omit in toc -->
In this demo we will see the main features of [Git](https://git-scm.com/), a version control system.

## Table of contents <!-- omit in toc -->
- [Git installation](#git-installation)
- [Git configuration](#git-configuration)
- [Create a repository](#create-a-repository)
- [Tracking files](#tracking-files)
- [Configuring a remote repository](#configuring-a-remote-repository)
- [Update your local repository](#update-your-local-repository)
- [Branching](#branching)


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

## Create a repository
Once we have Git installed and configured, we can create a repository. A repository is a place where we can store our
code and track its history. Now, let’s create a new directory and initialize a Git repository in it:
```bash
mkdir git-demo && cd git-demo
git init
```

This will create a hidden folder called `.git` in the current directory. This folder contains all the information about the repository.

Alternatively, you can clone an existing repository with the following command:
```bash
git clone url-to-repository
```
This will create a new directory with the name of the repository and initialize a Git repository in it.

## Tracking files
Now that we have our repository, we can start tracking files. To do this, we first need to create a file in the repository:
```bash
echo "Hello world" > hello.txt
```

Now, we can check the status of the repository with the following command:
```bash
git status
```

This will show us that the file `hello.txt` is not tracked by Git. To start tracking the file, we can use the following command:
```bash
git add hello.txt
```

If we check the status of the repository again, we will see that the file `hello.txt` is now tracked by Git. However, if
we modify the file, the status of the repository will change again. To see the changes in the file, we can use the
following command:
```bash
git diff
```

To commit the changes, we can use the following command:
```bash
git commit -m "Create hello.txt"
```

The `-m` flag is used to specify the commit message. If we do not use this flag, Git will open a text editor to write the
commit message.

## Configuring a remote repository
Now that we have our local repository, we can configure a remote repository to store our commits. This can be done with
the following command:
```bash
git remote add origin url-to-remote-repository
```

> **Note:** Remote repositories require authentication. If you are using GitHub, you can create an SSH key and add it to
> your GitHub account. Then, you can use the SSH URL of the repository to avoid entering your credentials every time you
> push your commits. See [Connecting to GitHub with SSH](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) for more information.

Once the remote is added, we need to tell Git that our local `main` branch is related to the remote `main` branch.
This can be done with the following commands:
```bash
git push -u origin main
```

This will push our commit to the remote repository.

The `-u` flag is used to set the upstream branch. This means that in the future we can use the following command to push
our commits to the remote:
```bash
git push
```

## Update your local repository
If someone else has pushed commits to the remote repository, your local repository will be out of date.
To update your local repository with the changes from the remote, you can use the following commands:
```bash
git fetch
git pull
```

## Branching
Branching is a core concept in GitHub Flow. Branches are cheap to create and easy to delete. We can use branches to
experiment and make edits before committing them to `main`.

Let’s create a new branch to add a new file to our repository:
```bash
git checkout -b feature/add-file
```

This will create a new branch called `feature/add-file` and switch to it. Now, we can create a new file in the repository:
```bash
echo "This is a new file" > new-file.txt
```

Now, we can add the file to the staging area, commit it and push it to the remote repository:
```bash
git add new-file.txt
git commit -m "Add new-file.txt"
git push -u origin feature/add-file
```
