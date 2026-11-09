---
title: Quy định bảo mật thông tin (bản mẫu)
category: Information Security
id: IT-KB-005
audience: Toàn bộ nhân viên, Nhà thầu được cấp quyền, IT, Security
tags: [security, bao-mat, phishing, data, mfa, incident]
version: '1.0'
status: BẢN MẪU MINH HỌA — không phải chính sách được ban hành
---

# Quy định bảo mật thông tin

> **Lưu ý:** Đây là **chính sách giả lập** phục vụ dự án Enterprise AI Knowledge Assistant. Doanh nghiệp thực tế phải rà soát, phê duyệt, công bố kênh liên hệ và điều chỉnh yêu cầu trước khi áp dụng.

## 1. Mục đích và đối tượng áp dụng
Bảo vệ tài khoản, thiết bị, dữ liệu khách hàng và thông tin nội bộ trước rủi ro mất mát, truy cập trái phép và lộ lọt dữ liệu. Quy định mẫu áp dụng cho nhân viên và đối tác được cấp quyền truy cập tài nguyên doanh nghiệp.

## 2. Phân loại thông tin
| Mức độ | Ví dụ | Nguyên tắc xử lý |
|---|---|---|
| Công khai (Public) | Thông tin đã được doanh nghiệp công bố | Được chia sẻ theo hướng dẫn truyền thông |
| Nội bộ (Internal) | Tài liệu hướng dẫn nội bộ, thông báo vận hành | Chỉ chia sẻ trong phạm vi công việc |
| Bảo mật (Confidential) | Hợp đồng, dữ liệu khách hàng, kế hoạch kinh doanh | Chỉ người có quyền được truy cập; dùng công cụ lưu trữ/chia sẻ được duyệt |
| Hạn chế (Restricted) | Khóa riêng, bí mật hệ thống, dữ liệu đặc biệt nhạy cảm | Kiểm soát chặt, cấp quyền tối thiểu, không đưa vào công cụ không được phê duyệt |

Nếu không chắc thông tin thuộc mức nào, hãy tạm xử lý như **Bảo mật** và hỏi chủ sở hữu dữ liệu/nhóm Security.

## 3. Tài khoản và xác thực
1. Mỗi nhân viên sử dụng tài khoản riêng; không chia sẻ tài khoản hoặc mật khẩu.
2. Dùng mật khẩu dài, duy nhất; sử dụng trình quản lý mật khẩu đã được phê duyệt khi có thể.
3. Bật MFA trên các dịch vụ yêu cầu; **không phê duyệt yêu cầu MFA không do mình khởi tạo**.
4. Không gửi mật khẩu, mã OTP, recovery code hoặc token qua chat/email.
5. Khi nghi tài khoản bị lộ, lập tức báo IT/Security và làm theo hướng dẫn bảo vệ tài khoản.
6. Quyền truy cập được cấp theo nhu cầu công việc và được thu hồi khi thay đổi vai trò hoặc nghỉ việc.

## 4. Thiết bị và phần mềm
- Chỉ sử dụng thiết bị, ứng dụng và dịch vụ lưu trữ được doanh nghiệp phê duyệt để xử lý thông tin công việc.
- Bật khóa màn hình, mã hóa ổ đĩa, cập nhật hệ điều hành và phần mềm bảo vệ theo cấu hình IT.
- Không tắt firewall, phần mềm bảo vệ, MFA hay tính năng giám sát để khắc phục lỗi.
- Không cài phần mềm lậu, tiện ích không rõ nguồn gốc hoặc sử dụng USB lạ.
- Báo ngay khi thiết bị bị mất, bị đánh cắp hoặc có dấu hiệu xâm nhập.

## 5. Email, Internet và làm việc từ xa
- Kiểm tra người gửi và đường dẫn trước khi tương tác với email; báo cáo thư nghi phishing.
- Không gửi tài liệu Confidential/Restricted đến email cá nhân hoặc nền tảng không được duyệt.
- Sử dụng VPN doanh nghiệp khi cần truy cập tài nguyên nội bộ từ xa theo quy định.
- Không để người khác nhìn thấy dữ liệu nội bộ trên màn hình; khóa máy khi rời chỗ.
- Không đưa dữ liệu bảo mật vào công cụ AI công cộng nếu chưa được doanh nghiệp cho phép.

## 6. Lưu trữ và chia sẻ dữ liệu
1. Lưu dữ liệu công việc tại vị trí được doanh nghiệp quản lý và sao lưu theo quy định.
2. Chỉ cấp quyền cho người cần biết; kiểm tra người nhận trước khi chia sẻ.
3. Không tạo liên kết “ai có link đều xem được” cho dữ liệu mật nếu chưa được cho phép.
4. Không chụp màn hình, sao chép hay tải xuống dữ liệu nhạy cảm vào thiết bị cá nhân khi chưa được phê duyệt.
5. Khi dữ liệu không còn cần thiết, làm theo chính sách lưu giữ và xóa dữ liệu đã được doanh nghiệp ban hành; không tự ý xóa dữ liệu phục vụ điều tra sự cố.

## 7. Báo cáo sự cố bảo mật
**Ví dụ sự cố:** Mất laptop, nhấp vào link phishing, phát hiện đăng nhập lạ, gửi nhầm dữ liệu cho người khác, rò rỉ thông tin khách hàng.

### Quy trình nhân viên
1. Ngừng thao tác có nguy cơ làm tình hình nghiêm trọng hơn. Nếu nghi thiết bị bị xâm nhập, ưu tiên liên hệ IT/Security để nhận chỉ dẫn.
2. **Báo ngay** qua **[Kênh báo cáo sự cố bảo mật chính thức]** hoặc **[Cổng IT Helpdesk nội bộ]**.
3. Cung cấp sự việc đã quan sát, thời gian, tài khoản/thiết bị liên quan và ảnh chụp đã che thông tin nhạy cảm nếu có.
4. Không tự xóa email, nhật ký hoặc tệp có thể là bằng chứng; không tự điều tra ngoài phạm vi được giao.
5. Hợp tác với IT/Security và thực hiện các bước khôi phục do nhóm có thẩm quyền hướng dẫn.

### Quy trình IT/Security (tổng quan)
1. Tiếp nhận, ghi nhận sự cố và đánh giá mức độ ảnh hưởng.
2. Thực hiện biện pháp ngăn chặn phù hợp theo quyền được cấp (ví dụ: thu hồi phiên đăng nhập, cô lập thiết bị bằng công cụ quản trị được phê duyệt).
3. Điều tra và khắc phục nguyên nhân trong phạm vi thẩm quyền.
4. Khôi phục dịch vụ và thông báo kết quả theo quy trình quản lý sự cố.
5. Rút kinh nghiệm, cập nhật biện pháp phòng ngừa và hồ sơ sự cố.

## 8. Trách nhiệm và ngoại lệ
- **Nhân viên:** Bảo vệ tài khoản, tuân thủ quy định và báo cáo sự cố kịp thời.
- **Quản lý:** Phê duyệt nhu cầu truy cập phù hợp vị trí công việc.
- **IT:** Cấu hình, vận hành và hỗ trợ hệ thống theo quyền được giao.
- **Security:** Hướng dẫn kiểm soát rủi ro và xử lý sự cố bảo mật.
- **Ngoại lệ:** Chỉ được áp dụng khi có phê duyệt của chủ sở hữu quy định và nhóm Security, được ghi nhận bằng văn bản và có thời hạn rõ ràng.

## 9. Câu hỏi thường gặp
**Hỏi: Tôi có thể đưa tài liệu nội bộ vào chatbot AI công khai để tóm tắt không?**  
Đáp: Không nếu chưa được doanh nghiệp cho phép. Chỉ sử dụng công cụ AI được phê duyệt và tuân thủ phân loại dữ liệu.

**Hỏi: IT nhắn tin hỏi mã OTP để hỗ trợ đăng nhập thì sao?**  
Đáp: Không cung cấp mã. Xác minh yêu cầu qua kênh Helpdesk chính thức và báo cáo hành vi đáng ngờ.

**Hỏi: Gửi nhầm file cho người ngoài thì có nên xóa email rồi bỏ qua không?**  
Đáp: Không. Báo ngay Security/IT để đánh giá và xử lý theo quy trình.

## 10. Tài liệu liên quan
- [Quy trình đặt lại mật khẩu](password_reset.md)
- [Hướng dẫn kết nối VPN](vpn_access.md)
- [Xử lý lỗi email công ty](email_support.md)
- [Cài đặt thiết bị cho nhân viên mới](device_setup.md)
