### 1. `Percona Monitoring and Management` (`PMM`) Serverni Docker bilan O'rnatish (Docker Filesiz)

**`Docker` volumini yaratish:**

```bash
  sudo docker volume create pmm-data
```

**`PMM Server` konteynerini ishga tushirish:**

```bash
   sudo docker run -d \
     --name pmm-server \
     --restart always \
     -p 80:80 \
     -p 443:443 \
     -v pmm-data:/srv \
     -e ENABLE_DBAAS=1 \
     percona/pmm-server:2
```

**PMM Serverga Kirish**

- `Google Cloud Console`-da `VM instance` uchun tashqi `IP` manzilini aniqlang
- Veb-brauzerda quyidagi manzilga kiring:
    ```ini
    http://<sizning-server-ip-manzilingiz>
    ```
- **Dastlabki kirish ma'lumotlari:**
  - `Login`: admin
  - `Parol`: admin (birinchi marta kirgandan so'ng o'zgartiring)

**Qo'shimcha Sozlamalar**

```bash
sudo docker exec -it pmm-server bash -c 'curl -s https://raw.githubusercontent.com/percona/pmm/main/gethttps.sh | bash'
```
**`PMM` ni yangilash:**
```bash
   sudo docker stop pmm-server
   sudo docker rm pmm-server
   sudo docker pull percona/pmm-server:2
   sudo docker run -d --name pmm-server --restart always -p 80:80 -p 443:443 -v pmm-data:/srv -e ENABLE_DBAAS=1 percona/pmm-server:2
```

**Monitoring qilinadigan serverga `PMM Client` o'rnatish**
Monitoring qilmoqchi bo'lgan har bir serverda:
```bash
   curl -fsSL https://repo.percona.com/apt/percona-release_latest.generic_all.deb -o /tmp/percona-release.deb
   sudo apt-get install -y /tmp/percona-release.deb
   sudo apt-get update
   sudo apt-get install -y pmm2-client
   sudo pmm-admin config --server-url=http://<pmm-server-ip>:80 --server-insecure-tls
   sudo pmm-admin add mysql --username=pmm --password=pass --query-source=slowlog
```
**Muhim Eslatmalar**
- Agar 80-port band bo'lsa, boshqa portga yo'naltirishingiz mumkin:
    ```bash
      sudo docker run -d -p 8080:80 ... # va hokazo
    ```
- `PMM` ma'lumotlarini saqlash uchun Docker volumini muntazam backup qiling
- Ishlab turgan `PMM` konteynerini tekshirish:
    ```bash
    sudo docker ps
    sudo docker logs pmm-server
    ```
> Ushbu usul `Docker` faylsiz, to'g'ridan-to'g'ri `Docker` buyruqlari yordamida `PMM` serverni o'rnatish imkonini beradi. Bu oddiyroq yondashuv bo'lib, tez o'rnatish uchun qulay.


















