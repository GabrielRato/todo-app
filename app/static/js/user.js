// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );
    var data = $('#user-posts')
    console.log(data.data());

    populate_task_list();
    $('#new_task').on('keypress', function (e) {
          if(e.which === 13){

             //Disable textbox to prevent multiple submit
             $(this).attr("disabled", "disabled");

             console.log('soajfo');
             //Do Stuff, submit, etc..

             //Enable the textbox again if needed.
             $(this).removeAttr("disabled");
          }
    });
});



function populate_task_list(){
    for(var i = 0; i < _post.length; i++)
    $(".list-group").append('<li class="list-group-item">'+ _post[i] +'</li>')
}
