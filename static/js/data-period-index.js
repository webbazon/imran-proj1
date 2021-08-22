$(document).ready(function(){
    $('#dataperiodform').change(function(){
         localStorage.setItem('dataperiod', $(this).val());
         $('#dataperiodform').value(localStorage.getItem('dataperiod'));
    });
});