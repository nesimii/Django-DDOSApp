//ekrana uyarı mesajları çıkarmak için
function toastMessage(message, status = "green", timeout = 3000) {
    new SnackBar({
        message: message, status: status, timeout: timeout,
    });
}
