import os
import git
import github
import time
import getpass

import dboec
import get_xml


def writeFile(msg, name):
    '''
    (Str, Str) ->  None
    a function just for testing
    create a txt file named name to current working directory
    write msg in it
    '''
    push_file = open(name, "w")
    push_file.write(msg)
    push_file.close()


def configuration():
    '''
    () -> github.Repository
    configure the user and get the repo to be interactive with
    return the target repo
    '''
    # get github information from the user
    username = raw_input("Please enter your github username: ")
    password = getpass.getpass("Please enter your password: ")

    # examining if the security information is correct
    not_login = True
    while (not_login):
        try:
            g = github.Github(username, password)
            git_user = g.get_user(username)
            not_login = False
        except github.GithubException:
            print '\nInvalid username or password, please try again.\n'
            username = raw_input("Please enter your github username: ")
            password = getpass.getpass("Please enter your password: ")

    # target_repo = raw_input("\nPlease enter the github repo that you want to interact with: ")
    # folder_name = (target_repo.split(r'/')[-1].split('.')[0])
    folder_name = "open_exoplanet_catalogue"     # target for this project
    # get the repo that the user wants to interactive with
    no_repo = True
    while (no_repo):
        try:
            repo = git_user.get_repo(folder_name)
            no_repo = False
        except github.GithubException:
            print '\nThere is no repo open_exoplanet_catalogue, please do a fork.\n'
            target_repo = raw_input("Please enter the github repo that you want to interact with: ")
            folder_name = (target_repo.split(r'/')[-1].split('.')[0])
    return repo


def clone_repo(repo):
    '''
    (github.Repository) -> None
    Clone the wanted github repo from remote to local
    for further modification
    '''
    git_url = repo.clone_url
    git_url = git_url[:-4]

    # clone repo if it is first time use
    try:
        git.Git().clone(git_url)
        print 'Clone repo succeed'
    except git.exc.GitCommandError:
        pass

    # checkout master branch
    cloned_repo = git.Repo(repo.name)
    cloned_repo.git.checkout('master')


def pull_repo(repo):
    '''
    (github.Repository) -> None
    Do a git pull on the repo provided
    can be considered as update oec repo
    '''
    git_url = repo.clone_url
    git_url = git_url[:-4]
    # do git pull to make the repo up-to-date
    cloned_repo = git.Repo(repo.name)
    cloned_repo.git.checkout('master')
    cloned_repo.git.pull()


def push_to_git(repo, oec, database):
    '''
    (github.Repository, dboec.Datebase, dboec.Database) -> None
    Takes a github repo, an original oec for line rebasing,
    and a merged database for final result by doing to following.
    Create a branch, and checkout the branch.
    Create xml files with rebased lines based on the original
    database, and do a commit.
    Create xml files with merged database, and do a commit.
    Push the branch to remote.
    Do a pull request.
    '''
    cloned_repo = git.Repo(repo.name)
    # git_ssh = r'git@github.com:{0}/{1}.git'.format(repo.owner.login, repo.name)
    # cloned_repo.git.remote('set-url', 'origin', git_ssh)

    # start with master branch
    cloned_repo.git.checkout('master')

    # create a new branch for merge
    not_branched = True
    while (not_branched):
        try:
            branch_name = raw_input("\nPlease enter the name for your branch: ")
            # create a new branch for merge
            cloned_repo.git.branch(branch_name)
            not_branched = False
        except git.exc.GitCommandError:
            confirm = raw_input("\nThe branch '{0}' already exists, ".format(branch_name) +
                                "do you want to continue and work on this branch (yes/no)? ")
            while ((confirm != 'yes') and (confirm != 'no')):
                confirm = raw_input("\ninvalid input, please type 'yes' or 'no': ")
            if (confirm == 'yes'):
                not_branched = False
            elif (confirm == 'no'):
                pass

    # checkout the branch to be mordified
    cloned_repo.git.checkout(branch_name)

    # change the working directory
    curDir = os.getcwd()
    wantDir = curDir + r'/{0}/systems'.format(repo.name)
    os.chdir(wantDir)

    # write the report file
    i = 0
    for system in oec.system:
        i += 1
        get_xml.toXml(system)
        print i, "..OK"
    cloned_repo.git.add('*')
    commit_msg = "Rebasing for line order"

    try:
        # git commit
        cloned_repo.git.commit(m=commit_msg)
        print("\nRebase succeed.")
    except git.exc.GitCommandError as e:
        print e._cmd
        print e._cmdline
        print e._cause
        print e.stdout
        print e.stderr
        print("\nThere is nothing changed to commit.\n")

    print ('\nWriting updates into files')
    time.sleep(2)

    i = 0
    for system in database.system:
        i += 1
        file_name = get_xml.toXml(system)
        # diff = cloned_repo.git.diff(wantDir + '/' + file_name)
        # print diff
        # cloned_repo.git.add(wantDir + '/' + file_name)
        print i, "..OK"

    # difference
    # diff = cloned_repo.git.diff()
    # print diff

    # git add file
    cloned_repo.git.add('*')

    # require a commit message from the user
    commit_msg = raw_input("\nPlease enter your commit message: ")
    try:
        # git commit
        cloned_repo.git.commit(m=commit_msg)
        print("\nCommit succeed.")
    except git.exc.GitCommandError as e:
        print e._cmd
        print e._cmdline
        print e._cause
        print e.stdout
        print e.stderr
        print("\nThere is nothing changed to commit.\n")
        # change back to master branch, and exit
        cloned_repo.git.checkout('master')
        return

    try:
        cloned_repo.git.push('origin', branch_name)
        print("\nPushed to origin.")
    except git.exc.GitCommandError as e:
        print e._cmd
        print e._cmdline
        print e._cause
        print e.stdout
        print e.stderr
        print("\nPush failed.\n")
        # change back to master branch, and exit
        cloned_repo.git.checkout('master')
        return

    # create pull request and send pull request to the git repo
    print "on", branch_name
    branch_made = False
    i = 0
    while not (branch_made) and i < 5:
        try:
            branch = repo.get_branch(branch_name)
            branch_made = True
        except github.GithubException:
            time.sleep(1)
            i += 1

    pr_title = raw_input("\nPlease enter the title for your pull request: ")
    pr_comment = raw_input("\nPlease enter leave a comment to your pull request: ")
    try:
        pr = repo.create_pull(pr_title, pr_comment, 'master', branch_name)
        print "\nCreating pull request #{0} succeed, please go check the pull request.".format(str(pr.number))
    except github.GithubException:
        print ("There is already a pull request on branch '{0}', ".format(branch_name) +
               "please go check the pull request before making a new one")

    # change back to master branch
    cloned_repo.git.checkout('master')
    # change back to root dir
    os.chdir(curDir)
