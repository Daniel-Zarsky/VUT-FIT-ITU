console.log("Hello world")
$(document).on('submit', '#create_new' ,function (e) {
    $.ajax({
        type: "POST",
        url: '{% url "create" %}',
        data :{
            name: $("#name-66b3").val(),
            csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val(),
            action : "post"
        },
        success:function (json){
            console.log(json)
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
})