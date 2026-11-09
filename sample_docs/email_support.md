---
title: Hướng dẫn xử lý lỗi email công ty
category: Email & Collaboration
id: IT-KB-003
audience: Nhân viên, IT Helpdesk
tags: [email, outlook, mail, sync, spam, phishing]
version: '1.0'
status: Tài liệu mẫu cho dự án AI Knowledge Assistant
---

# Xử lý lỗi email công ty

## 1. Phạm vi
Hướng dẫn các bước cơ bản khi nhân viên không đăng nhập được email, không gửi/nhận thư, lỗi đồng bộ hoặc nhận thư đáng ngờ. Dịch vụ email có thể là Microsoft 365, Google Workspace hoặc hệ thống khác; **sử dụng cổng và ứng dụng chính thức của doanh nghiệp**.

## 2. Phân loại vấn đề trước khi xử lý
1. **Không đăng nhập:** Báo sai mật khẩu, MFA, tài khoản khóa hoặc không mở được trang đăng nhập.
2. **Không nhận thư:** Người gửi nói đã gửi nhưng hộp thư chưa xuất hiện thư.
3. **Không gửi được thư:** Thư ở Outbox/Drafts hoặc có thông báo gửi thất bại.
4. **Không đồng bộ:** Email trên trình duyệt có nhưng ứng dụng máy tính/điện thoại không cập nhật.
5. **Thư nghi lừa đảo:** Thư yêu cầu nhập mật khẩu, tải tệp lạ hoặc phê duyệt MFA.

## 3. Quy trình kiểm tra ban đầu
1. Kiểm tra kết nối Internet và xem có thông báo gián đoạn dịch vụ từ IT không.
2. Đăng nhập **webmail chính thức** qua trang do doanh nghiệp công bố để so sánh với ứng dụng email.
3. Ghi lại thông báo lỗi, thời gian xảy ra, thiết bị, tên ứng dụng email và ảnh chụp màn hình **đã che thông tin nhạy cảm**.
4. Xác định lỗi ảnh hưởng một tài khoản, một thiết bị hay nhiều người trong bộ phận.
5. Áp dụng hướng dẫn tương ứng phía dưới; nếu chưa giải quyết được, tạo ticket.

## 4. Cách xử lý theo tình huống
### A. Không đăng nhập được
- Kiểm tra tên tài khoản và bàn phím nhập liệu.
- Dùng quy trình đặt lại mật khẩu tại `password_reset.md` nếu quên mật khẩu.
- Nếu MFA không hoạt động, liên hệ IT để khôi phục đúng quy trình; không tìm cách bỏ qua MFA.

### B. Không nhận được email
- Kiểm tra **Junk/Spam**, bộ lọc, thư mục khác và dung lượng hộp thư nếu dịch vụ có giới hạn.
- Kiểm tra trong webmail để xác định thư chỉ bị thiếu trên ứng dụng hay thiếu trên cả máy chủ.
- Nhờ người gửi kiểm tra có nhận được thông báo trả lại thư (bounce) không; chuyển nguyên văn **mã lỗi không nhạy cảm** cho IT.
- Không tự thay đổi chính sách lọc thư hoặc cho phép toàn bộ thư lạ.

### C. Không gửi được email
- Kiểm tra địa chỉ người nhận, kết nối Internet và tình trạng tệp đính kèm.
- Xem thông báo lỗi về giới hạn dung lượng, quyền gửi hoặc chính sách chống spam.
- Nếu email chứa dữ liệu nhạy cảm, sử dụng phương thức chia sẻ được công ty phê duyệt thay vì gửi qua email cá nhân.

### D. Ứng dụng email không đồng bộ
- So sánh hộp thư trên webmail và ứng dụng.
- Đóng/mở lại ứng dụng, kiểm tra cập nhật và đăng nhập lại qua quy trình chính thức nếu được yêu cầu.
- Nếu lỗi chỉ xuất hiện trên một thiết bị, gửi thông tin phiên bản ứng dụng và hệ điều hành cho IT.

### E. Nhận email nghi lừa đảo (phishing)
- **Không nhấp liên kết, không mở tệp đính kèm, không trả lời và không cung cấp mã MFA.**
- Dùng nút **Report phishing** hoặc chuyển qua kênh báo cáo bảo mật đã được doanh nghiệp chỉ định.
- Nếu đã bấm liên kết hoặc nhập thông tin, báo ngay IT/Security để được hỗ trợ bảo vệ tài khoản và thiết bị.

## 5. Quy trình xử lý ticket của IT Helpdesk
1. Xác nhận danh tính người yêu cầu và mức độ ảnh hưởng.
2. Kiểm tra trạng thái dịch vụ, lỗi đăng nhập, giới hạn hộp thư và nhật ký quản trị trong phạm vi được phân quyền.
3. Kiểm tra quyền, cấu hình ứng dụng và chính sách thư mà **không yêu cầu người dùng cung cấp mật khẩu**.
4. Chuyển nhóm Email Admin khi có lỗi hệ thống hoặc quyền; chuyển Security khi có dấu hiệu phishing hoặc chiếm quyền tài khoản.
5. Yêu cầu người dùng xác nhận gửi/nhận thư thành công, ghi lại cách xử lý và đóng ticket.

## 6. Khi nào cần báo khẩn?
- Nhiều nhân viên đồng thời không gửi/nhận được email.
- Có thư nghi lừa đảo gửi tới nhiều người.
- Phát hiện thư gửi đi bất thường từ tài khoản của mình.
- Có khả năng gửi nhầm dữ liệu nhạy cảm cho người không có quyền.

## 7. Câu hỏi thường gặp
**Hỏi: Tôi nhận được email yêu cầu xác thực lại mật khẩu trong 10 phút, nên làm gì?**  
Đáp: Không làm theo liên kết trong email. Kiểm tra thông báo qua cổng nội bộ hoặc liên hệ IT chính thức và báo cáo thư đáng ngờ.

**Hỏi: Webmail hoạt động nhưng Outlook không nhận thư?**  
Đáp: Khả năng cao vấn đề nằm ở ứng dụng, phiên đăng nhập hoặc đồng bộ trên thiết bị. Ghi nhận lỗi rồi thử cập nhật/đăng nhập lại theo hướng dẫn IT.

## 8. Tài liệu liên quan
- [Quy trình đặt lại mật khẩu](password_reset.md)
- [Quy định bảo mật thông tin](security_policy.md)
