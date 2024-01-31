function togglePaymentByType() {
    let checkbox = document.getElementById("togglePaymentButton");
    let net_payment_text = document.querySelectorAll("[id=NetPayment]");
    let gross_payment_text = document.querySelectorAll("[id=GrossPayment");

    for(var number = 0; number < net_payment_text.length; number++) {
      if (checkbox.checked){
        gross_payment_text[number].style.display = "block";
        net_payment_text[number].style.display = "none";

      } else {
        net_payment_text[number].style.display = "block";
        gross_payment_text[number].style.display = "none";
      }
    }
}
