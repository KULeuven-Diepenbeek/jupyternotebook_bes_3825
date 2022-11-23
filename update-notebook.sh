echo "Updating...";

GITREPO="https://github.com/KULeuven-Diepenbeek/jupyter_BES_3825_exercises.git";
GITHUB_DIR=/home/$USER/github_files;
UPDATEFILE=update_workspace.sh;

mkdir $GITHUB_DIR > /dev/null 2>&1 && git clone $GITREPO ./github_files/. > /dev/null 2>&1 && chmod +x $GITHUB_DIR/$UPDATEFILE > /dev/null 2>&1;
chmod +w -R $GITHUB_DIR > /dev/null && cd $GITHUB_DIR && git reset --hard > /dev/null && git clean -fxd > /dev/null && git pull > /dev/null 2>&1 && chmod +x $GITHUB_DIR/$UPDATEFILE > /dev/null  && chmod -w -R $GITHUB_DIR > /dev/null;
sh $GITHUB_DIR/$UPDATEFILE;
