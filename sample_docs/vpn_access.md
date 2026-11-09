---
title: Hướng dẫn kết nối VPN doanh nghiệp
category: Network & Remote Access
id: IT-KB-002
audience: Nhân viên, IT Helpdesk
tags: [vpn, remote, ket-noi, mfa, mang-noi-bo]
version: '1.0'
status: Tài liệu mẫu cho dự án AI Knowledge Assistant
---

# Hướng dẫn kết nối VPN

## 1. VPN dùng để làm gì?
VPN (Virtual Private Network) cung cấp kênh kết nối được bảo vệ để nhân viên truy cập **những tài nguyên nội bộ được cấp quyền** khi làm việc từ xa. VPN không tự cấp quyền vào mọi hệ thống. Việc sử dụng phải tuân theo chính sách của doanh nghiệp.

## 2. Điều kiện trước khi kết nối
- Được quản lý hoặc IT phê duyệt quyền truy cập từ xa.
- Đang sử dụng thiết bị được doanh nghiệp cho phép, đã cập nhật hệ điều hành và phần mềm bảo vệ.
- Đã cài **ứng dụng VPN chính thức** từ kho phần mềm/cổng nội bộ do IT công bố.
- Có tài khoản công ty hợp lệ và phương thức MFA đang hoạt động nếu hệ thống yêu cầu.
- Có Internet ổn định; tránh sử dụng thiết bị hoặc điểm truy cập không đáng tin cậy.

## 3. Quy trình kết nối VPN
1. Kết nối thiết bị với Internet và xác nhận có thể mở một trang web bình thường.
2. Mở ứng dụng VPN đã được IT cung cấp.
3. Chọn cấu hình doanh nghiệp đã được cấp sẵn; **không tự nhập máy chủ từ nguồn không xác minh**.
4. Chọn **Connect / Kết nối**.
5. Đăng nhập bằng tài khoản công ty qua trang xác thực chính thức, nếu được yêu cầu.
6. Hoàn thành bước MFA trên thiết bị của mình. Chỉ phê duyệt yêu cầu MFA do chính bạn vừa khởi tạo.
7. Chờ trạng thái **Connected** và mở ứng dụng nội bộ được cấp quyền để kiểm tra.

**Kết quả thành công:** Ứng dụng VPN hiển thị đã kết nối và người dùng truy cập được đúng hệ thống nội bộ đã được cấp quyền.

## 4. Ngắt kết nối an toàn
1. Lưu công việc đang mở trên hệ thống nội bộ.
2. Trong ứng dụng VPN, chọn **Disconnect / Ngắt kết nối**.
3. Xác nhận trạng thái chuyển về **Disconnected**.
4. Khóa màn hình khi rời thiết bị; không cho người khác dùng phiên làm việc còn đăng nhập.

## 5. Các lỗi thường gặp
| Hiện tượng | Cách kiểm tra an toàn |
|---|---|
| Không có Internet | Kiểm tra Wi-Fi/cáp mạng; thử truy cập trang web công khai |
| Sai thông tin đăng nhập | Đăng nhập lại qua trang chính thức; tham khảo `password_reset.md` nếu quên mật khẩu |
| Không nhận được MFA | Kiểm tra ứng dụng xác thực, kết nối thiết bị; liên hệ IT nếu mất thiết bị MFA |
| VPN kết nối nhưng không mở được ứng dụng nội bộ | Ghi lại tên ứng dụng, thời điểm và thông báo lỗi; có thể thiếu quyền truy cập |
| VPN tự ngắt | Kiểm tra độ ổn định Internet, cập nhật ứng dụng qua kênh chính thức và thử kết nối lại |
| Thiết bị không đạt yêu cầu bảo mật | Liên hệ IT để kiểm tra chính sách thiết bị; **không tắt antivirus hoặc firewall để vượt kiểm tra** |

## 6. Gửi yêu cầu hỗ trợ IT
Tạo ticket tại **[Cổng IT Helpdesk nội bộ]** với các thông tin: mã nhân viên, thiết bị sử dụng, phiên bản hệ điều hành, tên ứng dụng VPN, thời điểm lỗi, thông báo lỗi và tài nguyên cần truy cập. Không gửi mật khẩu, mã MFA, khóa riêng, tệp cấu hình bí mật hoặc mã khôi phục.

IT Helpdesk kiểm tra trạng thái dịch vụ, tài khoản, quyền truy cập và mức độ tuân thủ thiết bị; chuyển nhóm Network/Security khi cần. Ghi lại kết quả xử lý trong ticket.

## 7. Quy tắc bảo mật khi dùng VPN
- Chỉ dùng VPN do doanh nghiệp phê duyệt; không tự cài công cụ kết nối không rõ nguồn gốc.
- Không chia sẻ tài khoản VPN hay phê duyệt MFA thay người khác.
- Không thay đổi cấu hình bảo mật, DNS, chứng chỉ hoặc firewall để cố kết nối.
- Báo IT ngay nếu thấy yêu cầu MFA bất thường, mất thiết bị hoặc có nghi ngờ truy cập trái phép.

## 8. Câu hỏi thường gặp
**Hỏi: Kết nối VPN rồi mà vẫn không vào được hệ thống kế toán?**  
Đáp: VPN chỉ tạo kết nối; bạn còn phải được cấp quyền vào hệ thống kế toán. Gửi ticket để IT kiểm tra quyền.

**Hỏi: Tôi có thể dùng máy tính cá nhân để kết nối không?**  
Đáp: Chỉ khi chính sách doanh nghiệp cho phép và thiết bị đáp ứng yêu cầu bảo mật.

## 9. Tài liệu liên quan
- [Quy trình đặt lại mật khẩu](password_reset.md)
- [Quy định bảo mật thông tin](security_policy.md)
- [Cài đặt thiết bị cho nhân viên mới](device_setup.md)
