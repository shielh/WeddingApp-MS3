var select = '';
for (i=1;i<=10;i++){
    select += '<option val=' + i + '>' + i + '</option>';
}
$('#number_of_party').html(select);