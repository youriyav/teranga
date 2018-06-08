/**
 * Created by root on 15/04/2017.
 */

        var selectedProduct;
        var selectedProductPrize=0;
        var selectedProductId=0;
        var currentQte=0;
        var selected_item_title;
        var selected_item_prix;
        var selectedMenu;
        var trToRemove;
        var mysecret="";
             $(function()
             {

             });

             function addInBasket(produit) {
                 currentQte=1;
                 $("#nbr_qte").text(currentQte);
                 //$("#preview_prize").text(selectedProductPrize+" Fcfa");
                 $("#block_quantite").modal('toggle');
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



