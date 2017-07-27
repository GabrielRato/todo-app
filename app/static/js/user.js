// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );
    var data = $('#user-posts')
    console.log(data.data());

    populate_task_list();

});



function populate_task_list(){
    for(var i = 0; i < _post.length; i++)
    $(".list-group").append('<li class="list-group-item">'+ _post[i] +'</li>')
}
