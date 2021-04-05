// console.log('hello')


function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}

window.onload = function () {
  $(".showModal").click(function (event) {
    $(".modal").show();
    var x = $(event.currentTarget).attr("src");

    $("#modalImg").attr("src", x);
    $(".modal-content").attr("src", x);
    console.log(x);
  });


  $("#overlay").click(function () {
    $(".modal").hide();
  });
};