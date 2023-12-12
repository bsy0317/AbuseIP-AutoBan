from rich import print
from rich.progress import track
import subprocess
import os
import sys
import shutil

repo_url = "https://github.com/borestad/blocklist-abuseipdb.git"
repo_folder = "/tmp/ipban"
file_name = "abuseipdb-s100-7d.ipv4"	# 정확도 100, 7일 이내에 등록된 IP만
except_ip = ["211.105.21.195"]	# 제외할 IP

# 매개변수 reset이 존재하면 iptables 원본 파일로 복원
if len(sys.argv) > 1 and sys.argv[1] == "reset":
	subprocess.run(["sudo", "iptables-restore"], input=open("/etc/iptables/rules.v4.back", "rb").read())
	print("[yellow]Restored original iptables rules[/yellow]")
	sys.exit()
# 매개변수 backup이 존재하면 iptables 원본 파일을 백업
elif len(sys.argv) > 1 and sys.argv[1] == "backup":
	if not os.path.exists("/etc/iptables"):
		os.makedirs("/etc/iptables")
	if not os.path.exists("/etc/iptables/rules.v4.back"):
		open("/etc/iptables/rules.v4.back", "w").close()
	subprocess.run(["sudo", "iptables-save"], stdout=open("/etc/iptables/rules.v4.back", "w"))
	print("[yellow]Backed up original iptables rules[/yellow]")
	sys.exit()

# ipset에 blockip이 존재하지 않으면 생성
if subprocess.run(["sudo", "ipset", "list", "blockip"]).returncode != 0:
	subprocess.run(["sudo", "ipset", "create", "blockip", "hash:ip", "family", "inet", "maxelem", "65536"])
	print("[yellow]Created blockip ipset[/yellow]")

# iptables에 blockip 체인이 존재하지 않으면 생성
if subprocess.run(["sudo", "iptables", "-C", "INPUT", "-m", "set", "--match-set", "blockip", "src", "-j", "DROP"]).returncode != 0:
	subprocess.run(["sudo", "iptables", "-I", "INPUT", "1", "-m", "set", "--match-set", "blockip", "src", "-j", "DROP"])
	subprocess.run(["sudo", "service", "iptables", "save"])
	subprocess.run(["sudo", "service", "iptables", "restart"])
	print("[yellow]Added blockip ipset to iptables[/yellow]")

# ipset blockip을 비움
subprocess.run(["sudo", "ipset", "flush", "blockip"])
subprocess.run(["sudo", "ipset", "save"])
print("[yellow]Flushed blockip ipset[/yellow]")

# 모든 파일 삭제 / git conflict 방지
for file in os.listdir(repo_folder):
    if os.path.isfile(os.path.join(repo_folder, file)):
        os.remove(os.path.join(repo_folder, file))
    elif os.path.isdir(os.path.join(repo_folder, file)):
        shutil.rmtree(os.path.join(repo_folder, file))

# .git 폴더가 없다면 초기화 후 저장소를 가져옴
if not os.path.exists(os.path.join(repo_folder, ".git")):
	subprocess.run(["git", "init"], cwd=repo_folder)

subprocess.run(["git", "fetch", "--all"], cwd=repo_folder)  # 저장소 업데이트
subprocess.run(["git", "pull", repo_url], cwd=repo_folder)  # 저장소 업데이트

file_path = os.path.join(repo_folder, file_name)
with open(file_path, "r") as file:
	ip_addresses = file.read().splitlines()

# ipset에 IP들을 추가
for ip in track(ip_addresses, description="Adding IP addresses..."):
	if ip not in except_ip:
		subprocess.run(["sudo", "ipset", "add", "blockip", ip])

# ipset blockip을 저장
subprocess.run(["sudo", "ipset", "save", "blockip"])

# iptables rules 재시작
subprocess.run(["sudo", "service", "iptables", "restart"])

print("[green]Updated IP list file[/green]")
