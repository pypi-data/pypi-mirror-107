import typer
import os
import os.path
import twine
import requests


app = typer.Typer()

@app.command()
def publish():

    typer.echo("Eating your files...")
    os.system('python setup.py bdist_wheel sdist')
    os.system('twine upload dist/*')

@app.command()
def create():
    url = "https://raw.githubusercontent.com/ssantoshp/StrategyLibraryQC/main/setup.py"
    response = requests.get(url)

    if os.path.isfile('setup.py'):
        answer = input("Should we replace your actual setup.py file? (y/n)")
        if answer == "y":
            os.remove('setup.py')
        else:
            print("Don't remove actual setup.py file...")
            pass
    else:
        with open('setup.py', 'a') as file:
            print(response.text, file=file)
        print("Just created the setup.py file!")


    url_readme = "https://gist.githubusercontent.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc/raw/d59043abbb123089ad6602aba571121b71d91d7f/README-Template.md"
    response_readme = requests.get(url)

    if os.path.isfile('README.md'):
        answer = input("Should we replace your actual README.md file? (y/n)")
        if answer == "y":
            os.remove('README.md')

        else:
            print("Don't remove actual README.md file...")
            pass
    else:
            with open('README.md', 'a') as file:
                print(response_readme.text, file=file)
            print("Just created the README.md file!")

    os.mkdir("src")



