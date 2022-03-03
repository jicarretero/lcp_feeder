command = "netstat -tunlp"
import subprocess

if __name__ == "__main__":
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    out, err = p.communicate()
    first = True
    j = 0
    for l in out.decode().split('\n'):
        if first:
            first = False
            continue

        info = l.rstrip().split()
        if len(info) > 7:
            continue
        print(len(info), " -- ", l)
