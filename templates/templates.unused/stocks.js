(function () {
    'use strict'
  
    feather.replace()
  
    // Graphs
    var ctx = document.getElementById('myChart')
    // eslint-disable-next-line no-unused-vars
    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [
          'Sunday',
          'Monday',
          'Tuesday',
          'Wednesday',
          'Thursday',
          'Friday',
          'Saturday'
        ],
        datasets: [{
          data: [
            15339,
            21345,
            18483,
            24003,
            23489,
            24092,
            12034
          ],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#007bff',
          borderWidth: 4,
          pointBackgroundColor: '#007bff'
        }]
      },
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: false
            }
          }]
        },
        legend: {
          display: false
        }
      }
    })
  })()


//STOCKS==========
"use strict";

// A function to get stock info from AA API using stock symbol stored in the database 
function get_stock_info(evt){
    evt.preventDefault();

    let symbol = $("#stock_symbol").val();

    $.get('/api/stock?symbol='+ symbol, updateInfo);

    $("#all_items").show();

    displayPrices();


};
// ************************************************************************************************************************************************************
// when page is loaded page renders all stock info from get_stock_info, price function's

function load_page(){

    let symbol = getUrlParameter('symbol');

    if (symbol != false) {
        $.get('/api/stock?symbol='+ symbol, updateInfo);
        $("#all_items").show();
        get_price();
        displayPrices();
    } else {
        console.log("Please select");
    }
    

}
// ************************************************************************************************************************************************************
// gets current price from AA API, updates every 1 minute 

function get_price(){

    let symbol = getUrlParameter('symbol');
    console.log($("#StockID").text())
    
    if (symbol != false) {

        $.get('/api/price?symbol='+ symbol, (price) => {
        var last_price = (price["Time Series (1min)"][Object.keys(price["Time Series (1min)"])[0]][ "1. open"]);
        $("#price").html((last_price));
    }

        );
    };

 }
// ************************************************************************************************************************************************************

// toggles between the full heart and empty heart when user likes and unlikes stock
jQuery(function($) {
    $('#swapHeart').on('click', function() {
      var $el = $(this),
        textNode = this.lastChild;
      $el.find('span').toggleClass('glyphicon-heart glyphicon-heart-empty');
      
      $el.toggleClass('swap');
       
      var stock_id = $('#StockID').text();

      $.post(`/api/favorite/${stock_id}`, {"stock_id": stock_id}, favorite_table);
  
    });
  });

// ************************************************************************************************************************************************************
// adds favortie to database and favorite table 
function favorite(evt){
    evt.preventDefault();
    
    $("#unHeart").hide();
    $("#swapHeart").show();

    var stock_id = $('#StockID').text();



    $.post('/api/favorite', {"stock_id": stock_id}, favorite_table);

};
// ************************************************************************************************************************************************************
// delete favorite from database and favorite table 
 function delete_favorite(evt){
    evt.preventDefault();
    console.log("Hello");

    $("#swapHeart").hide();
    $("#unheart").show();

    var stock_id = $('#StockID').text();

    $.post('/api/delete_favorite', {"stock_id": stock_id}, favorite_table);
 };
// ************************************************************************************************************************************************************
// Show user favorites in user favorite table, updated when user likes a stock 
 function favorite_table(){
   
     $.get('/api/userfavorite', (favs) => {
        var favs_length = favs.length;
        $("#user_favorites").html("");
        for (var i = 0; i < favs_length; i++) {
            // console.log(favs[i]);
            $("#user_favorites").append("<span><a href ='/stocks?symbol="+favs[i][2]+"'>"+favs[i][1]+"</a></span>");
    
        };
        
    });
    
};
// get all stock info from AA api 

let StockID = null

function updateInfo(results){
    $(".company_info").show();
    $("#StockID").html(results.StockID);
    $('#Name').html(results.Name);    
    $('#Symbol_ticker').html(results.Symbol);
    $('#Description').html(results.Description);      
    $('#Address').html(results.Address);
    $('#FullTimeEmployees').html(results.FullTimeEmployees);
    $('#RevenueTTM').html(results.RevenueTTM);
    $('#FiscalYearEnd').html(results.FiscalYearEnd);
    $('#AssetType').html(results.AssetType);
    $('#GrossProfitTTM').html(results.GrossProfitTTM);
    $('#DividendPerShare').html(results.DividendPerShare);
    $('#DividendYield').html(results.DividendYield);
    $('#DividendPerShare').html(results.DividendPerShare);
    $('#PEGRatio').html(results.PEGRatio);
    $('#PERatio').html(results.PERatio);
    $('#EPS').html(results.EPS);
    $('#WomenLead').html(results.WomenLead ? 'Yes': 'No');
    $('#52WeekHigh').html(results["52WeekHigh"]);
    $('#52WeekLow').html(results["52WeekLow"]);
    $('#EPS').html(results.EPS);
    StockID = results.StockID
    if (results["UserFaved"] == true) {
        $("#not_favorite").hide();
        $("#favorited").show();

    } 

};

  
// ************************************************************************************************************************************************************
var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return typeof sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
    return false;
};

// ************************************************************************************************************************************************************
// Get the modal
function new_user(){
    var modal = document.getElementById('id01');

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
    };
// ************************************************************************************************************************************************************
// call's all functions from above  
    $("#stock_select").on('submit', get_stock_info);
    $("#unHeart").on('click', favorite);
    $("#swapHeart").on('click', delete_favorite);
    $("#modal").on('click',new_user);
    $(document).ready(favorite_table);
    $(document).ready(load_page);
    

// ************************************************************************************************************************************************************
// CHART.JS 
function displayPrices(){

let duration = $("#duration").val();

if (duration == null) {
duration = 12

};


let symbol = getUrlParameter('symbol');

var xmlhttp = new XMLHttpRequest(),
    url = `/api/monthly?symbol=${symbol}`;

xmlhttp.open('GET', url, true);
xmlhttp.onload = function() {
if (this.readyState == 4 && this.status == 200) {
    let json=JSON.parse(this.responseText);
    let keys = Object.keys(json['Monthly Time Series']);
    let keys_length = keys.length
    var dates = [];
    var pricesClose = [];
    const months = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ];

    for (let i=duration; i>= 0; i--) {
    let key = keys[keys_length-i-1];
    pricesClose.push(json['Monthly Time Series'][key]['4. close']);
    dates.push(months[Number(key.slice(5, 7) - 1)] + key.slice(2, 4));
 
   
    }

    displayChart(symbol, dates, pricesClose)
}
};
xmlhttp.send();
}

function displayChart(symbol, dates, pricesClose) {
let labels = dates;
let data = pricesClose;

let ctx = document.getElementById('stock-chart').getContext('2d');
let chart = new Chart(ctx, {
    
    type: 'line',

    
    data: {
        labels: labels,
        datasets: [{
            label: symbol,
            borderColor: 'rgb(255, 99, 132)',
            data: data,
            lineTension: 0,
        }]
    },

    
    options: {
        responsive: true,
        maintainAspectRatio: false,
    }
});
}


  