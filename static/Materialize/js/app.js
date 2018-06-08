function getSolde(){
    var ctx = document.getElementById("solde");
    var myChart = new Chart(ctx, {
        type: 'line',
          data: {
            labels: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin","Juillet",'Août',"Septembre","Octobre","Novembre","Décembre"],
            datasets: [{
                label: 'solde sur 12 mois',
                data: [120, 190, 30, 50, 20, 30,40,60,85,35,45,100],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',

                ],
                borderColor: [
                    'rgba(255,99,132,1)',

                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            },
            responsive:true,
          }
    });
}

function getConso(){
    var ctx = document.getElementById("conso");
    var myChart = new Chart(ctx, {
        type: 'line',
          data: {
            labels: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet","Août","Septembre"],
            datasets: [{
                label: 'consommation du mois',
                data: [650, 590, 800, 810, 560, 550, 400,250,450],
                backgroundColor: [
                                'rgba(255, 99, 132, 0.2)',

                            ],
                borderColor: [
                    'rgba(255,99,132,1)',

                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            },
            responsive:true,
          }
    });
}
function getDebit(){
    var ctx = document.getElementById("debit");
    var myDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: [
                "Red",
                "Blue",
                "Yellow"
            ],
            datasets: [
                {
                    data: [300, 50, 100],
                    backgroundColor: [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56"
                    ],
                    hoverBackgroundColor: [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56"
                    ]
                }]
        },
     });
}

jQuery(document).ready(function($) {

	"use strict"

	//preloader
	$(window).on("load",function () {
        $('#preloader').delay(2000).fadeOut('slow', function () {
           $(this).remove();
        });
	 });

	//sidenav collapse
    $('.button-collapse').sideNav({
        menuWidth: 240,
        edge: 'left',
        closeOnClick: true
    });
    $('.right-sidebar-button').sideNav({
        menuWidth: 240,
        edge: 'right',
        closeOnClick: false
    });

    //date picker
    $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 15, // Creates a dropdown of 15 years to control year,
        monthsFull: ['janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
        weekdaysFull: ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Dimanche'],
        today: false,
        clear: 'Effacer',
        close: 'Fermer',
        format:'yyyy/mm/dd',
        weekdaysShort: ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],
        //selectYears:80

      });
    //select
    $('select').material_select();
    // dupliquer champ
    var max_fields      = 5; //maximum input boxes allowed
    var wrapper         = $(".input_fields_wrap"); //Fields wrapper
    var add_button      = $(".add_field_button"); //Add button ID
    var x=1;
    $("#add_field_button").click(function(e){
        e.preventDefault();
        if (x<max_fields) {
            x++;
            $(wrapper).append('<div><p class="input-field col s4">'+
                                                     '<input id="alias" type="text">'+
                                                    '<label for="alias" class="">Alias</label>'+
                                                 '</p>'+
                                                 '<p class="input-field col s4">'+
                                                     '<input id="tel" type="text">'+
                                                     '<label for="tel" class="">Téléphone</label>'+
                                                 '</p>'+
                                                 '<p class="input-field col s3">'+
                                                    '<input type="text" name="montant">'+
                                                     '<label for="montant">Montant</label>'+
                                                  '</p>'+' <a href="#" class="col s1 remove_field "><i class="material-icons">delete</i></a> </p>');
        }
      });
    $(wrapper).on('click',".remove_field",function(e){
        e.preventDefault();
        $(this).parent('div').remove();x--;
    });

    //modal
    $('.modal').modal();

    //getSolde();

    //getConso();

    //getDebit();

});