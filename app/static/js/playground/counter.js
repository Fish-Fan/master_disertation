define(function() {
   var value = 0;
   return {
       increment: function() {
           value++;
       },
       decrement: function() {
           value--;
       },
       getValue: function() {
           return value;
       }
   }
});