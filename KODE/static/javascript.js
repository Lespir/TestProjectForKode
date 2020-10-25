// Функция для ищменения яркости изображения

$(document).ready(function(){
    $('.count').prop('disabled', true);
    $(document).on('click','.plus',function(){
        $('.count').val(parseInt($('.count').val()) + 1 );
    });
    $(document).on('click','.minus',function(){
        $('.count').val(parseInt($('.count').val()) - 1 );
            if ($('.count').val() == 0) {
                $('.count').val(1);
            }
        });
});


var range=document.querySelectorAll('#playground-value-input');
function changeHandler(event){
  var px=(this.value==0)?'':'%';
  document.getElementById('playground-property').style.filter='brightness('+this.value+'%)';
  document.getElementById('playground-code-value').innerText=this.value+px;
}
Array.prototype.forEach.call(range,function(range){
  range.addEventListener('input',changeHandler);
});

function sizePic() {
    size = document.getElementById("size").value;
    img = document.getElementById("pic");
    img.width = 60 + 20*size;
}

function copy_text(el) {
    var $tmp = $("<input>");
    $("body").append($tmp);
    $tmp.val($(el).text()).select();
    document.execCommand("copy");
    $tmp.remove();
}
