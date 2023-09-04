# TODO: should I rename it into: 'activate_env.template.sh'?
# TODO: venv should not be in ssh connection directly, some apps do not want to use venv
# TODO: if venv-app is not exists, it throws warning when I connect via SSH

# this is direct depedency to the cluster paths
# source /shared/{{APP_DIR}}/venv-app/bin/activate'
if [ -f "/shared/{{APP_DIR}}/venv-app/bin/activate" ]; then
    source "/shared/{{APP_DIR}}/venv-app/bin/activate"
else
    echo "warning: Activate file does not exist"
fi