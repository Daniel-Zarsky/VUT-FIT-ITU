console.log("Hello from tasks jquerry")
$(document).on('submit', '#addTask' ,function (e) {
    $.ajax({
        type: "POST",
        url: '{% url "submit" %}',
        data :{
            name: $("#name-af1b").val(),
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