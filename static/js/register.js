function validateNumber(num) {
   //var card = document.getElementByID("card").value 
   var card = document.checkout.card.value
   if (card == 'visa') {
      re = '/^4[0-9]{12}(?:[0-9]{3})?$/'
   } else if (card == 'mc') {
      //re = '^5[1-5][0-9]{14}$'
      re = '^5[1-5][0-9]'
   } else if (card == 'amex') {
      re = '^3[47][0-9]{13}$'
   } 
   matches = card.search(re);
   alert("num is " + num + "matches:" + matches);
   if (!card.search(re)) {
      alert("problem with number")
   }
}
