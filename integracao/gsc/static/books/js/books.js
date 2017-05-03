$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book").modal("show");
        $("#LoadingImage").show();

      },
      success: function (data) {
        $("#modal-book .modal-content").html(data.html_form);
        $("#LoadingImage").hide();
      },
      error: function(data){
        alert("Não foi possivel executar a ação!");
        $("#modal-book").modal("hide");
        $("#LoadingImage").hide();
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      beforeSend: function () {
        $("#LoadingImage").show();
      },
      success: function (data) {
          $("#modal-book").modal("hide");
          $("#LoadingImage").hide();
          alert("GSC Atualizado com sucesso!");
          // alert("GSC Atualizado com sucesso!");
          document.location.reload();
      },
      error: function(data){
        alert("Não foi possivel executar a ação!");
        $("#modal-book").modal("hide");
        $("#LoadingImage").hide();
      }
    });
    return false;
  };



  var progressForm = function () {
    var btn = $(this);
    $("#LoadingImage").show();
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#LoadingImage").show();
      },
      success: function (data) {
        $("#LoadingImage").hide();
        alert("Banco de Dados Atualizado com sucesso!");
        document.location.reload();
      },
      error: function(data){
        alert("Não foi possivel executar a ação!");
        $("#LoadingImage").hide();
      }
    });
  };




  /* Binding */

  $(".js-create-book").click(loadForm);
  $(".js-database-book").click(progressForm);
  $("#modal-book").on("submit", ".js-book-create-form", saveForm);

});
