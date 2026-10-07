# Ảnh thực hành LAB02 – NetRecon

Thư mục này lưu bằng chứng chạy thật trên máy, đối chiếu [Hướng dẫn chụp ảnh](../../HUONG_DAN_CHUP_ANH.md) (mục LAB02, lab-03.pdf trang 16–29).

**Lưu ý bảo mật:** Không commit `.env`, App Password hoặc nội dung mật khẩu lên Git. Nếu ảnh cũ lỡ chụp giá trị `SMTP_PASS`, chỉ dùng nội bộ hoặc chụp lại sau khi che; không đưa mật khẩu vào báo cáo công khai.

## Danh sách ảnh hiện có

| STT | File | Mã gợi ý (HUONG_DAN) | Nội dung chính |
|-----|------|----------------------|----------------|
| 1 | `1791342502329_...jpg` | `03_app_password_da_che.png` | Google Tài khoản → Mật khẩu ứng dụng: đã tạo mục **Netrecom** (chỉ tên, không cần chụp chuỗi 16 ký tự). |
| 2 | `1791342524487_...jpg` | `02_nmap_version.png`, `04_cau_truc.png`, `05_cai_goi.png` | VS Code: cây thư mục LAB02/`netrecon`, file `requirements.txt`; terminal `nmap --version` (Nmap 7.991). |
| 3 | `1791342548610_...jpg` | `06_env_da_che.png` | File `.env` với `SMTP_USER` / `SMTP_PASS` — **nên chụp lại** chỉ hiện tên biến hoặc giá trị đã che trước khi nộp công khai. |
| 4 | `1791342744814_...jpg` | `05_cai_goi.png`, mã nguồn | `pip install -r requirements.txt` (Flask, Click, python-dotenv…); editor mở `cli.py` (các tùy chọn `--target`, `--ports`, `--mode`). |
| 5 | `1791342804514_...jpg` | `04_cau_truc.png`, `05_cai_goi.png` | `.gitignore` loại trừ `.env`, `certs/`; cài dependency tại thư mục LAB02. |
| 6 | `1791343371520_...jpg` | `07_cli.png`, `09_cli_all.png` | `python cli.py` quét `10.12.98.9`: Nmap, cổng 22/80/443 **closed**, banner timeout, bảng ARP/interface. |
| 7 | `1791343459458_...jpg` | `08_cli_scan.png`, `09_cli_all.png` | CLI: bảng CVE mẫu theo cổng; quét `scanme.nmap.org` — `22/tcp`, `80/tcp` **open** (sau khi dùng đúng `--ports`). |
| 8 | `1791343561866_...jpg` | `09_cli_all.png` | `--mode all` với `192.168.1.1` và lệnh quét `scanme.nmap.org`; kết quả Nmap, banner, network map. |
| 9 | `1791343657324_...jpg` | `12_web_result.png` | Trình duyệt `localhost:5000/scan`: Service Detection, Banner Grabbing, Network Map cho target lab. |
| 10 | `1791343676661_...jpg` | `13_email.png` | Gmail: email **Kết quả quét từ NetRecon** (Nmap + banner) gửi sau khi quét web/CLI. |

Thứ tự STT theo timestamp trong tên file (từ cũ → mới).

## Ảnh còn thiếu (nếu báo cáo bám đủ bảng HUONG_DAN)

- `01_nmap_download.png` — trang/cửa sổ cài Nmap Windows  
- `10_flask.png` — terminal chạy `python app.py`, Flask lắng nghe cổng 5000  
- `11_web_form.png` — form Scan trên `localhost:5000` (target, ports, mode, email)  
- `14_git_push.png`, `15_github_lab02.png` — sau khi push repository  

## Lệnh tham chiếu khi chụp bổ sung

```powershell
cd "C:\Users\LOQ\OneDrive\Desktop\BUOI 3\BUOI3\LAB02\netrecon"
nmap --version
python -m pip install -r requirements.txt
python cli.py --target scanme.nmap.org --ports 22,80 --mode scan
python cli.py --target 127.0.0.1 --ports 8000 --mode all
python app.py
```

Mục tiêu quét chỉ dùng IP/domain được phép (máy lab, `127.0.0.1`, `scanme.nmap.org`, v.v.).
