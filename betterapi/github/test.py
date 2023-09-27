import re,os,sys
import glob

def use_regex(input_text, type):
    if type == "starlette":
        print("running " + type)
        pattern = re.compile(r"\s+[a-zA-Z]+\(.*/.*\)", re.IGNORECASE)
        print(pattern.findall(input_text))
        return pattern.findall(input_text)
    if type == "flask":
        print("running " + type)
        pattern = re.compile(r"@.*\..*\([^)]*\)", re.IGNORECASE)
        return pattern.findall(input_text)
    if type == "fastapi":
        print("running " + type)
        pattern = re.compile(r'"/.*"', re.IGNORECASE)
        return pattern.findall(input_text)
    else:
        print("running " + type)
        pattern = re.compile(r"@.*\..*\([^)]*\)", re.IGNORECASE)
        return pattern.findall(input_text)
    


app_name = input("app name: ").lower()
# app_github = input("GitHub url: ")
os.system(f"""
mkdir {app_name}_project
""")
os.chdir(f"{app_name}_project")
# os.system(f"git clone {app_github}")
for file in glob.glob("*.py"):
    print(file)
    

file_name = input("select run file: ")
with open(f"{file_name}", "r+") as F:
    data = F.read()
    
    for item in data.split("\n"):
        if "app = " in item:
            item = item.strip()
            platform = item.split("app = ")[1].lower().split("(")[0]
            print("Detected " +platform+ "...")
    obj = use_regex(data, platform)
    for str in obj:
        new_line = re.sub("/", f"/{app_name}/", str, count=1)
        # print(new_line)
        
        data = data.replace(str, new_line)
    
with open(f"run_{file_name}", "w") as X:
    X.write(data)