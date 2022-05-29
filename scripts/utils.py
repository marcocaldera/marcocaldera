from bs4 import BeautifulSoup
def update_readme(id, elements):
    
    soup = BeautifulSoup(open("README.md"), "html.parser")
    result = soup.find(id=id)
    
    if type(elements) is str:
        result.string.replace_with(elements)
    else:
        result.replace_with(elements)

    with open("README.md", "wb") as f_output:
        f_output.write(soup.encode(encoding="utf-8", formatter="html5"))