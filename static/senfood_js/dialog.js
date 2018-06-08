/**
 * Created by root on 22/03/2017.
 */
function handleDialog(e,modal,url,type)
{
        //e.preventDefault();
        //alert(e.attr("id"));
        //.modal("modal");
     $("#dialog_text").hide();
     $("#dialog_img_loader").show();
     $("#dialog_footer").hide();
     $("#dialog_tile").text("Veuillez patienter ...");
     var csrftoken = getCookie('csrftoken');
     /* lancement de la requête ajax pour la suppréssion*/
     var data={};
     //if(url=="/utilisateur/supprimer-utilisateur-post")
     //{
    if(type==1)
    {
       // alert("user");
        data. idUtilisateur=e.attr("id");
    }
    if (type==2)
    {
        //alert("rest");
        data. idRestaurant=e.attr("id");
    }
         //alert(e.attr("id"));
     ///}
     $.ajax({
            //url : "dsdsd",
            url : url,
            type : "POST", // http method
            data: data,
            beforeSend: function(xhr){xhr.setRequestHeader("X-CSRFToken", csrftoken);},
            success :
                function(json)
                {
                    console.log(json); // provide a bit more info about the error to the console
                    $("#flashbag").text(json)
                     modal.modal("toggle");
                     e.parent().parent().fadeOut(2000,function () {
                         $('#flashbag').text(json);
                         $('#flashbag').show();
                          $('#flashbag').fadeOut(4000);
                          $("#dialog_text").show();
                         $("#dialog_img_loader").hide();
                         $("#dialog_footer").show();
                         $("#dialog_tile").text("Avertissement");
                     });

                },
            error :
                function(xhr,errmsg,err)
                {
                    console.log(errmsg); // provide a bit more info about the error to the console
                    console.log(xhr); // provide a bit more info about the error to the console
                     modal.modal("toggle");
                     $('#flashbag').css({backgroundColor:"red",border:"solid red"});
                    $('#flashbag').text("#Erreur");
                    $('#flashbag').show();
                    $('#flashbag').fadeOut(4000);
                    // e.parent().parent().fadeOut(3000);
                },
     });
     /* fin de la requête suppéssion*/

}
 function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
          }
