document.addEventListener("DOMContentLoaded", () => {
  const qrcodeContainer = document.getElementById("qrcode");
  if (qrcodeContainer) {
    new QRCode(qrcodeContainer, {
      text: window.location.href,
      width: 128,
      height: 128,
    });
  }
});