Write-Host "Started script to create virtual enviroment"
# Add-Content -Path .gitignore* -Value "Yo"
python -m venv env
Write-Host "Enviroment Created!"
touch .gitignore
Add-Content -Path .gitignore -Value "env/"
Add-Content -Path .gitignore -Value "__pycache__"
Write-Host 'Installing packges'
env/Scripts/activate
pip install flask 