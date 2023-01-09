import os
os.system("rm -rf cloudflare")

os.system("clear")

os.system("apt install wget php -y") 

os.system("pkg install proot -y")
os.system("pkg install proot resolv-conf -y")
os.system("mkdir cloudflare")

sysInfo = os.popen("uname -m")
sysData = sysInfo.read().replace("\n","")

if sysData=="aarch64" or sysData =="Android":
     os.system("cd cloudflare && wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm")
elif sysData=="arm64":
     os.system("cd cloudflare && wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64")
elif sysData =="x86_64":
     os.system("cd cloudflare && wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64")
else :
     os.system("cd cloudflare && wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386")

os.system("cd cloudflare && chmod +x *")

getFileby = os.popen("ls cloudflare")
getFilename = getFileby.read().replace("\n","")
os.system(f"cd cloudflare && mv {getFilename} cldf")
os.system("cd cloudflare && cp cldf $PREFIX/bin/")
os.system("chmod +X $PREFIX/bin/cldf")
os.system("rm -rf cloudflare")

os.system("clear")
print (" [*] Setup Done :)")
print (" Run :: cldf --help ")
