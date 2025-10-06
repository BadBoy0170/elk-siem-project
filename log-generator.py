#!/usr/bin/env python3
import random
import time
from datetime import datetime
import os

# IP pools
normal_ips = ['192.168.1.10', '192.168.1.20', '10.0.0.5', '172.16.0.10']
attacker_ips = ['45.33.32.156', '185.220.101.45', '198.51.100.23']

# User agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Mozilla/5.0 (X11; Linux x86_64)',
    'python-requests/2.28.0',
    'sqlmap/1.6',
    'Nikto/2.1.6'
]

# Log directories
os.makedirs('logs', exist_ok=True)

def generate_auth_log():
    """Generate SSH authentication logs"""
    timestamp = datetime.now().strftime('%b %d %H:%M:%S')
    hostname = 'ubuntu-server'
    
    # 70% normal, 30% attack
    if random.random() < 0.7:
        ip = random.choice(normal_ips)
        username = random.choice(['admin', 'user', 'devops'])
        log = f"{timestamp} {hostname} sshd[{random.randint(1000,9999)}]: Accepted password for {username} from {ip} port {random.randint(40000,60000)} ssh2\n"
    else:
        ip = random.choice(attacker_ips)
        username = random.choice(['root', 'admin', 'test', 'oracle'])
        log = f"{timestamp} {hostname} sshd[{random.randint(1000,9999)}]: Failed password for {username} from {ip} port {random.randint(40000,60000)} ssh2\n"
    
    return log

def generate_apache_log():
    """Generate Apache access logs with attacks"""
    timestamp = datetime.now().strftime('%d/%b/%Y:%H:%M:%S +0000')
    
    if random.random() < 0.7:
        # Normal traffic
        ip = random.choice(normal_ips)
        method = random.choice(['GET', 'POST'])
        path = random.choice(['/index.html', '/about', '/api/users', '/dashboard'])
        status = random.choice([200, 200, 200, 304])
        bytes_sent = random.randint(1000, 50000)
    else:
        # Attack traffic
        ip = random.choice(attacker_ips)
        attack_type = random.choice(['sqli', 'xss', 'lfi', 'scan'])
        
        if attack_type == 'sqli':
            path = f"/login.php?id=1' OR '1'='1"
            status = random.choice([403, 500, 200])
        elif attack_type == 'xss':
            path = '/search?q=<script>alert(1)</script>'
            status = random.choice([403, 200])
        elif attack_type == 'lfi':
            path = '/page?file=../../../../etc/passwd'
            status = random.choice([403, 404])
        else:  # scan
            path = random.choice(['/.git/config', '/admin', '/.env', '/phpinfo.php'])
            status = 404
        
        bytes_sent = random.randint(200, 5000)
        method = random.choice(['GET', 'POST'])
    
    log = f'{ip} - - [{timestamp}] "{method} {path} HTTP/1.1" {status} {bytes_sent}\n'
    return log

def generate_firewall_log():
    """Generate firewall logs"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if random.random() < 0.8:
        action = 'ALLOW'
        src_ip = random.choice(normal_ips)
        dst_port = random.choice([80, 443, 22, 3306])
    else:
        action = 'BLOCK'
        src_ip = random.choice(attacker_ips)
        dst_port = random.choice([23, 3389, 445, 1433, 27017])
    
    protocol = random.choice(['TCP', 'UDP'])
    dst_ip = '192.168.1.1'
    
    log = f"{timestamp} {action} {src_ip}:{random.randint(40000,60000)} -> {dst_ip}:{dst_port} {protocol}\n"
    return log

def main():
    print("🚀 Starting log generation...")
    print("📊 Generating logs with 30% attack traffic")
    print("⏱️  Generating 10 logs per second")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Generate logs
            with open('logs/auth.log', 'a') as f:
                f.write(generate_auth_log())
            
            with open('logs/access.log', 'a') as f:
                f.write(generate_apache_log())
            
            with open('logs/firewall.log', 'a') as f:
                f.write(generate_firewall_log())
            
            time.sleep(0.1)  # 10 logs per second
            
    except KeyboardInterrupt:
        print("\n✅ Log generation stopped")

if __name__ == "__main__":
    main()
