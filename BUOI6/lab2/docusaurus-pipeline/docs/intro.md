---
sidebar_position: 1
---

# BUOI6 - DevSecOps

Đây là trang tài liệu của pipeline Docusaurus trong Bài 6. Nội dung trang được build thành static files bởi job `build-job`, lưu trong artifact `build/` và được job `pages` chuyển sang `public/` để triển khai GitLab Pages.

## Luồng pipeline

```text
build-job (stage build) -> pages (stage deploy)
```

### 1. build-job

Job dùng image Node.js để chạy:

```text
npm install
npm run build
```

Sau khi hoàn tất, Docusaurus tạo thư mục `build/`. Thư mục này được lưu thành artifact để job sau sử dụng.

### 2. pages

Job `pages` nhận artifact của bước build, chạy:

```text
mv build/ public/
```

GitLab Pages tìm nội dung website trong `public/`, vì vậy bước chuyển thư mục này là phần triển khai của pipeline.

## Đối chiếu giáo trình

| Thành phần | Vai trò | Trang PDF |
|---|---|---|
| `image: node` | Môi trường chạy npm và build Docusaurus | 12 |
| `build/` | Artifact sinh ra sau build | 12-13 |
| `pages` | Job deploy sau stage build | 13-14 |
| `public/` | Thư mục GitLab Pages phục vụ website | 14-15 |

Pipeline tương ứng với mục 6.2.2 của giáo trình Bài 6.
