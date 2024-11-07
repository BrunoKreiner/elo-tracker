# Demo

Link: https://youtu.be/2HGcZ9YVitQ

# Authors

Katherine Barbano, Alex Chao, Jenny Huang, Andrew Krier, Amr Tagel-Din, Annie Wang

Final project for Duke Compsci 316, Introduction to Database Systems.

# Description

An elo score is a method for calculating the relative skill levels of players in zero-sum games such as chess. Many popular activities at Duke, including intramural Sports, spikeball, foosball, and e-games, involve tournament-style play that can utilize elo scores. We created an elo system interface to support keeping track of each player’s standings among different activities.

Features include user authentication, a dashboard of elo statistics over time with graph visualization, notifications, leaderboards, and a database with information on activities played, ongoing events, leagues of players, and matches between players.

Skeleton code was provided for this project
by [Rickard Stureborg](http://www.rickard.stureborg.com) and [Yihao Hu](https://www.linkedin.com/in/yihaoh/).

# Setup Instructions

We assume you are in your class VM.
If you have a different setup, your mileage with the following instructions may vary.

## Installing the Current Skeleton

1. Fork this repo by clicking the small 'Fork' button at the very top right [on Gitlab](www.example.com).
   It's important that you fork first, because if you clone the directory directly you won't be able to push changes (save your progress) back to Gitlab.
   Name your forked repo as you prefer.
2. In your newly forked repo, find the blue "Clone" button.
   Copy the "Clone with SSH" text.
   In your terminal on the VM, you can now issue the command `git clone THE_TEXT_YOU_JUST_COPIED`.
   Make sure to replace 'THE_TEXT_YOU_JUST_COPIED' with the "Clone with SSH" text.
3. In your VM, move into the repository directory and then run `install.sh`.
   This will install a bunch of things, set up an important file called `.flashenv`, and creates a simple PostgreSQL database named `amazon`.
4. If you are running a Google VM, to view the app in your browser, you may need to edit the firewall rules.
   The [Google VM instructions](https://sites.duke.edu/compsci316_01_f2021/creating-and-running-vm-on-google-cloud/) on the course page has instructions for how to add rules at the bottom.
   if those for some reason are outdated, here are [instructions provided by Google](https://cloud.google.com/vpc/docs/using-firewalls).
   Create a rule to open up port 5000, which flask will run on.

## Running/Stopping the Website

python3 -m venv env

source env/bin/activate

pip install -r requirements.txt

rename flaskenv to .env and edit

flask run

i had to pip install numpy for it to work


if not work maybe because of psycopg2:
sudo apt-get update
sudo apt-get install libpq-dev

pip uninstall psycopg2
pip install psycopg2

pip uninstall psycopg2
pip install psycopg2-binary

To run your website, in your VM, go into the repository directory and issue the following commands:

```
source env/bin/activate
flask run
```

The first command will activate a specialized Python environment for running Flask.
While the environment is activated, you should see a `(env)` prefix in the command prompt in your VM shell.
You should only run Flask while inside this environment; otherwise it will produce an error.

If you are running a local Vagrant VM, to view the app in your browser, you simply need to visit [http://localhost:5000/](http://localhost:5000/).
If you are running a Google VM, you will need to point your browser to `http://vm_external_ip_addr:5000/`, where `vm_external_ip_addr` is the external IP address of your Google VM.

To stop your website, simply press `<kbd>`Ctrl `</kbd><kbd>`C `</kbd>` in the VM shell where flask is running.
You can then deactivate the environment using

```
deactiviate
```

# Tips for Working on This Project

## Set up VS Code on Google Cloud VM

The following instructions also exist as a recorded video, which you can find [at this link](https://youtu.be/y-l6FLSsCz0).
If you need specific help setting up VSCode, the TAs will be able to help you in office hours.

1. First we need to set up SSH access through your local machine (Mac) to the Google VM.
   1. Create an SSH key-pair on your local machine. If you have a macOS, use: `ssh-keygen -f /Users/YOUR_MAC_USERNAME/.ssh/vm_316`. If you are on Windows, use: `ssh-keygen -f C:\Users\YOUR_WINDOWS_USERNAME\.ssh\vm_316`. Make sure to replace 'YOUR_XXX_USERNAME' with your local machine's username. For the passphrase, just hit enter to opt out.
   2. Now, we need to give the public key (`vm_316.pub`) to the VM instance on Google Cloud. You might have already done this if you followed along with the "SETTING UP AN SSH KEY PAIR TO ACCESS VMS" tutorial on the course website. If so, skip this.
      1. In your internet browser, go to Google Cloud and find the VM instance you want to be able to connect with. Click on its name and then click 'Edit' in the top bar.
      2. Find 'SSH Keys', click 'Show and edit'. The section will expand. Click on the '+ Add Item' button. Now keep this tab open, we are going to paste your key in here.
      3. Back in your local host terminal, run the command `cat /Users/YOUR_MAC_USERNAME/.ssh/vm_316.pub` The output will be your public key. Copy this text (all of it).
      4. Paste the text into the text box you just opened in your browser. Before saving, however, edit the username at the very end of this key. The key will look something like "...OFUNwEsWO/dJNK user@MBP.local". Replace the last bit with your gmail username. That means it would look like this: "...OFUNwEsWO/dJNK gmailusername". Now click save.
2. Download Visual Studio Code (VS Code) from [this link](https://code.visualstudio.com/Download).
3. VS Code has a bunch of useful extensions. To use it with our VM we are going to need to download the 'remote-ssh' extension.
   - Open VS Code and click on the Extensions button in the left-most navigation bar. This button looks like a 3-block tetris piece with a 4th block hovering above it.
   - Search for an extension named 'Remote - SSH'. It will be the one by Microsoft with a description that begins with "Open any folder on a remote machine...". Click it and install the extension.
4. Now you're almost ready to log onto the VM. Open your browser again and find your VM Instances on Google Cloud. The IP Address will be listed under the 'External IP' column. Copy this IP address for the next step.
5. Open a new VS Code window, and click on 'Run a Command' (alternatively, use the shortcut `F1` or `⇧⌘P`). Type in 'Remote-SSH: Connect to Host', scroll down to 'add new host' and hit enter. Here, enter the username and IP address you just looked up like this, along with your local device username as before to specify where the private key is: `ssh -i /Users/YOUR_MAC_USERNAME/.ssh/vm_316 gmailusername@IP_adress`. The `-i` flag specifies to use the given private key instead of the default. If you already set up your SSH keys earlier, you can just issue the command `ssh gmailusername@IP_adress`.
6. You will be asked what type of platform the VM is. Select `Linux`.
7. Now you're connected! In the lower left corner of the window you'll see a green bar that reads "SSH: ...". You can access files and run things through the terminal just as you would be able to locally.
