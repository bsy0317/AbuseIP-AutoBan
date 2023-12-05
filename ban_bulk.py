from rich import print
from rich.progress import track
import subprocess
import os
import sys
import shutil

repo_url = "https://github.com/borestad/blocklist-abuseipdb.git"
repo_folder = "/tmp/ipban"
file_name = "db/abuseipdb-s100-latest.ipv4"
old_file_path = os.path.join(repo_folder, "abuseipdb.old")
iptables_rules_file = os.path.join(repo_folder, "iptables_rules.txt")

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

# old_file_path 을 제외하고 모든 파일 삭제 / git conflict 방지
for file in os.listdir(repo_folder):
    if os.path.isfile(os.path.join(repo_folder, file)) and file != "abuseipdb.old":
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

# abuseipdb.old 파일 존재 여부 확인
if os.path.exists(old_file_path):
	with open(old_file_path, "r") as old_file:
		old_ip_addresses = old_file.read().splitlines()

	# 기존 IP들을 파일에 추가하여 iptables_bulk_rules.txt 파일 생성
	with open(iptables_rules_file, "wb") as rules_file:
		rules_file.write(b"*filter\n")
		for ip in old_ip_addresses:
			rules_file.write(f"-D INPUT -p tcp --dport 443 -s {ip} -j DROP\n".encode('utf-8'))
		rules_file.write(b"COMMIT\n")

	# iptables_bulk_rules.txt를 사용하여 기존 IP 삭제
	subprocess.run(["sudo", "iptables-restore", "--noflush"], input=open(iptables_rules_file, "rb").read())
	print("[yellow]Removed old IP rules[/yellow]")

	os.remove(old_file_path)  # abuseipdb.old 파일 삭제
	print("[yellow]Removed old IP list file[/yellow]")

# 새로운 IP들을 파일에 추가하여 iptables_bulk_rules.txt 파일 생성
with open(iptables_rules_file, "wb") as rules_file:
	rules_file.write(b"*filter\n")
	for ip in ip_addresses:
		rules_file.write(f"-I INPUT 1 -p tcp --dport 443 -s {ip} -j DROP\n".encode('utf-8'))
	rules_file.write(b"COMMIT\n")

# iptables_bulk_rules.txt를 사용하여 새로운 IP 추가
subprocess.run(["sudo", "iptables-restore", "--noflush"], input=open(iptables_rules_file, "rb").read())
print("[green]Added new IP rules[/green]")

# iptables rules 저장
subprocess.run(["sudo", "service", "iptables", "save"])

# abuseipdb.old 파일 업데이트
with open(old_file_path, "w") as old_file:
	for ip in ip_addresses:
		old_file.write(ip + '\n')
print("[green]Updated IP list file[/green]")
